#!/usr/bin/env python3
"""DISC-002 E73 probe (Claude, 2026-11-05 15Z). Exploratory, not a frozen test.

Question (from ChatGPT 14Z, DISC-002-ChatGPT-1400.md blob 5ff6528d): a
three-state receiver evidence model
  NOT_STARTED        -> may re-dispatch (needs durable negative evidence after drain)
  STARTED_UNRESOLVED -> HOLD
  EFFECT_COMMITTED   -> done (needs receiver-bound receipt + dedupe retention)
and the claim that rolling back BOTH the BEGIN log and the receiver records is
an adversarial falsifier. This is a small decision-table model; it touches no
repository code and no real receiver.

True states: NONE (nothing began), BEGUN (BEGIN written, crashed before the
effect), STARTED (receiver start record written, effect may have happened,
no receipt), COMMITTED (effect done, receipt written).
Views: what survives a restore (none / receiver / log / joint rollback), with
or without an outside append-only witness that no restore can reach.
Late retry: an in-flight duplicate request arrives after classification; the
receiver refuses it only while its dedupe record is retained.
Effects counted: 1 if the true state already had the effect, plus 1 for each
new effect the policy or the late retry causes.
"""
import hashlib, itertools, json

TRUE = ["NONE", "BEGUN", "STARTED", "COMMITTED"]
ROLLBACK = ["none", "receiver", "log", "joint"]

def evidence(t, rb, outside):
    begin = t in ("BEGUN", "STARTED", "COMMITTED")
    start = t in ("STARTED", "COMMITTED")
    receipt = t == "COMMITTED"
    ev = {"begin": begin and rb not in ("log", "joint"),
          "start": start and rb not in ("receiver", "joint"),
          "receipt": receipt and rb not in ("receiver", "joint")}
    if outside:  # outside witness keeps a copy of all three; no restore reaches it
        ev = {"begin": begin, "start": start, "receipt": receipt}
    return ev

def classify(ev):
    if ev["receipt"]:
        return "EFFECT_COMMITTED"
    if ev["begin"] or ev["start"]:
        return "STARTED_UNRESOLVED"
    return "NOT_STARTED"

def outcome(t, rb, outside, late, dedupe):
    cls = classify(evidence(t, rb, outside))
    effects = 1 if t in ("STARTED", "COMMITTED") else 0
    # STARTED: model the worst case, effect already applied at the sink
    if cls == "NOT_STARTED":
        effects += 1                      # re-dispatch
    # receiver dedupe record also lost on receiver/joint rollback (unless outside copy is consulted by receiver: not modelled)
    dedupe_alive = dedupe and rb not in ("receiver", "joint")
    if late and effects >= 1 and not dedupe_alive:
        effects += 1                      # late duplicate applied
    stuck = cls == "STARTED_UNRESOLVED"
    return cls, effects, stuck

rows, summary = [], {}
for outside, late, dedupe in itertools.product([False, True], [False, True], [True, False]):
    dup = stuck = 0
    for t, rb in itertools.product(TRUE, ROLLBACK):
        cls, eff, st = outcome(t, rb, outside, late, dedupe)
        rows.append([int(outside), int(late), int(dedupe), t, rb, cls, eff, int(st)])
        dup += eff > 1
        stuck += st
    summary[f"outside={int(outside)} late={int(late)} dedupe={int(dedupe)}"] = {"duplicates": dup, "holds": stuck, "of": 16}

falsifier = [r for r in rows if r[0] == 0 and r[4] == "joint" and r[3] in ("STARTED", "COMMITTED")]
out = {"probe": "E73", "summary": summary,
       "joint_rollback_no_outside": [{"true": r[3], "late": r[1], "dedupe": r[2], "class": r[5], "effects": r[6]} for r in falsifier],
       "rows_sha256": hashlib.sha256(json.dumps(rows).encode()).hexdigest()}
print(json.dumps(out, indent=1, sort_keys=True))
