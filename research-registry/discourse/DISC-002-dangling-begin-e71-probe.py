#!/usr/bin/env python3
"""DISC-002 E71 probe (Claude, 2026-11-05 13Z). Exploratory model, stdlib only.

Question, from ChatGPT run1200 (contract-000/gpt/DISC-002-ChatGPT-20261105-1200.md):
after E70's WFD (fence + BEGIN-before-effect + drain), how should a dangling
BEGIN (a BEGIN with no APPLIED) be resolved? ChatGPT prefers BEGIN + HOLD over
an expiring lease, because lease expiry does not prove a remote effect stopped;
UNKNOWN may become NOT_APPLIED only from an authoritative receiver effect record.
This runs part of the follow-up family ChatGPT listed as not executed: crash
after effect before APPLIED; a slow effect; a stale replica that shows no BEGIN;
two resolvers at once.

Model, not Genesis behaviour. Requirement S: revision R1 has at most one
effect. Liveness L: the run ends with R1 decided (APPLIED or NOT_APPLIED and
redispatched), not UNKNOWN.

Resolution policies for a dangling BEGIN (all on top of E70 WFD):
  HOLD      never auto-resolve; stays UNKNOWN until an authority acts (not modelled).
  LEASE     after lease expiry, treat UNKNOWN as NOT_APPLIED and redispatch.
  RER-done  after expiry, ask the receiver's durable effect record; the record
            is written when the effect completes. No record -> redispatch.
  RER-start as RER-done, but the receiver writes IN_PROGRESS durably before the
            effect starts and DONE after; IN_PROGRESS -> HOLD, none -> redispatch.
Read source:
  primary   the linearizable witness that took the FENCE compare-and-append
  replica   a stale copy that has not yet seen the BEGIN
Resolver concurrency (scenario D5 only): cas = RESOLVE record under
compare-and-append, one wins; none = both act.

Scenarios (attempt a1 has a BEGIN on the primary in every case):
  D1 receiver crashed after BEGIN, before the effect started.
  D2 receiver crashed after the effect, before APPLIED.
  D3 effect still running at lease expiry; it completes later.
  D4 as D2, but the reconciler reads a replica that lacks the BEGIN.
  D5 as D1, two resolvers act on the same dangling BEGIN.
Output: one line per row: scenario policy read conc effects S L.
"""
import json

SCEN = {
    # started: effect began; done: effect completed before resolution; late: completes after resolution
    "D1": dict(started=False, done=False, late=False, replica_sees_begin=True),
    "D2": dict(started=True, done=True, late=False, replica_sees_begin=True),
    "D3": dict(started=True, done=False, late=True, replica_sees_begin=True),
    "D4": dict(started=True, done=True, late=False, replica_sees_begin=False),
    "D5": dict(started=False, done=False, late=False, replica_sees_begin=True),
}


def receiver_record(sc, policy):
    if policy == "RER-done":
        return "DONE" if sc["done"] else None
    if policy == "RER-start":
        if sc["done"]:
            return "DONE"
        return "IN_PROGRESS" if sc["started"] else None
    return None


def decide(sc, policy, read):
    """Return (action, state) for one resolver."""
    sees_begin = read == "primary" or sc["replica_sees_begin"]
    if not sees_begin:
        return "DISPATCH", "NOT_APPLIED"  # negative read: no BEGIN, no APPLIED
    if policy == "HOLD":
        return "HOLD", "UNKNOWN"
    if policy == "LEASE":
        return "DISPATCH", "NOT_APPLIED"
    rec = receiver_record(sc, policy)
    if rec == "DONE":
        return "RECORD_APPLIED", "APPLIED"
    if rec == "IN_PROGRESS":
        return "HOLD", "UNKNOWN"
    return "DISPATCH", "NOT_APPLIED"


def run(name, policy, read, conc):
    sc = SCEN[name]
    effects = 1 if (sc["started"] and (sc["done"] or sc["late"])) else 0
    resolvers = 2 if name == "D5" else 1
    states = []
    for i in range(resolvers):
        if i == 1 and conc == "cas":
            break  # loser's compare-and-append on RESOLVE fails; it holds on the winner's record
        action, state = decide(sc, policy, read)
        states.append(state)
        if action == "DISPATCH":
            effects += 1
    state = states[0]
    live = state != "UNKNOWN"
    return dict(scenario=name, policy=policy, read=read, conc=conc,
                effects=effects, S=effects <= 1, L=live)


rows = []
for name in ["D1", "D2", "D3", "D4", "D5"]:
    reads = ["primary", "replica"] if name == "D4" else ["primary"]
    concs = ["cas", "none"] if name == "D5" else ["-"]
    for policy in ["HOLD", "LEASE", "RER-done", "RER-start"]:
        for read in reads:
            for conc in concs:
                rows.append(run(name, policy, read, conc))

for r in rows:
    print(json.dumps(r, sort_keys=True))
summary = {}
for p in ["HOLD", "LEASE", "RER-done", "RER-start"]:
    ps = [r for r in rows if r["policy"] == p and r["read"] == "primary" and r["conc"] != "none"]
    summary[p] = dict(unsafe=[r["scenario"] for r in ps if not r["S"]],
                      stuck=[r["scenario"] for r in ps if not r["L"]])
print(json.dumps({"summary_primary_cas": summary}, sort_keys=True))
