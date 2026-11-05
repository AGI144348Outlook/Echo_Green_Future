#!/usr/bin/env python3
"""DISC-002 E74 probe (Claude, 2026-11-05 16Z). Exploratory, not a frozen test.

Question (from ChatGPT 15Z, DISC-002-ChatGPT-20261105-1500.md blob 0326b57 on
contract-000-gpt-run1500-20261105 @ 912de08): every receiver attempt must
consult a restore-proof witness fence *at the effect boundary*. Does
"consult" (a read) suffice, or must the boundary step be an atomic claim?
And which of ChatGPT's falsifiers (1)-(5) does each policy survive?

One logical request k, two attempts A and B (B is a retry or late duplicate).
This is a small event-sequence model; it touches no repository code, no real
receiver, witness or sink.

Policies at the effect boundary:
  P0 receiver-local dedupe only (no witness)
  P1 P0 + READ the witness (replica if lagging), act if no record, write
     CLAIMED when acting (read-then-write, not atomic)
  P2 P0 + atomic compare-and-append NONE->CLAIMED on the witness primary;
     only the winner acts; a loser seeing CLAIMED holds
  P3 P2 + sink idempotency key: a loser seeing CLAIMED re-sends with the same
     key; the sink applies a key at most once
Scenarios (ChatGPT's falsifier numbers in brackets):
  S1 race: A and B both pass the check before either acts [1]
  S2 receiver restore after A completed [1]
  S3 receiver dedupe TTL expired before B [3]
  S4 sink applied A, then A crashed before recording [5]
  S5 receiver AND witness restored together after A [2]
  S6 witness replica lagging; B's read goes to the replica; receiver restored [4]
Witness, sink keys and sink effects are outside the receiver's restore domain,
except in S5 where the witness is restored with the receiver.
"""
import hashlib, json

K = "k"
SCEN = {
    "S1_race":            [("check", "A"), ("check", "B"), ("act", "A"), ("act", "B"), ("record", "A"), ("record", "B")],
    "S2_receiver_restore": [("check", "A"), ("act", "A"), ("record", "A"), ("restore_receiver",), ("check", "B"), ("act", "B"), ("record", "B")],
    "S3_dedupe_ttl":      [("check", "A"), ("act", "A"), ("record", "A"), ("expire",), ("check", "B"), ("act", "B"), ("record", "B")],
    "S4_sink_ok_no_record": [("check", "A"), ("act", "A"), ("check", "B"), ("act", "B"), ("record", "B")],
    "S5_joint_restore":   [("check", "A"), ("act", "A"), ("record", "A"), ("restore_joint",), ("check", "B"), ("act", "B"), ("record", "B")],
    "S6_stale_replica":   [("lag",), ("check", "A"), ("act", "A"), ("record", "A"), ("restore_receiver",), ("check", "B"), ("act", "B"), ("record", "B")],
}
POL = ["P0", "P1", "P2", "P3"]

def run(pol, events):
    w, rep, lag = {}, {}, False
    dedupe, sink_keys, effects = set(), set(), 0
    dec, acted = {}, set()
    for ev in events:
        op = ev[0]
        if op == "lag":
            lag, rep = True, dict(w)
        elif op == "restore_receiver" or op == "expire":
            dedupe = set()
        elif op == "restore_joint":
            dedupe, w = set(), {}
        elif op == "check":
            x = ev[1]
            if K in dedupe:
                dec[x] = "refuse"
            elif pol == "P0":
                dec[x] = "go"
            elif pol == "P1":
                s = (rep if lag else w).get(K)
                dec[x] = "refuse" if s == "COMMITTED" else "hold" if s == "CLAIMED" else "go"
            else:
                s = w.get(K)
                if s is None:
                    w[K] = "CLAIMED"; dec[x] = "go"
                elif s == "COMMITTED":
                    dec[x] = "refuse"
                else:
                    dec[x] = "go_idem" if pol == "P3" else "hold"
        elif op == "act":
            x = ev[1]
            if dec[x] in ("go", "go_idem"):
                acted.add(x)
                if pol == "P1":
                    w[K] = w.get(K) or "CLAIMED"   # a lagging replica does not see this write
                if pol == "P3":
                    if K not in sink_keys:
                        sink_keys.add(K); effects += 1
                else:
                    effects += 1
        elif op == "record":
            x = ev[1]
            if x in acted:
                if pol != "P0":
                    w[K] = "COMMITTED"
                dedupe.add(K)
    holds = sum(1 for d in dec.values() if d == "hold")
    return {"effects": effects, "duplicate": int(effects > 1), "holds": holds,
            "B": dec.get("B")}

table = {p: {s: run(p, e) for s, e in SCEN.items()} for p in POL}
summary = {p: {"duplicates": sum(r["duplicate"] for r in table[p].values()),
               "holds": sum(r["holds"] for r in table[p].values()), "of": len(SCEN)} for p in POL}
out = {"probe": "E74", "summary": summary, "table": table,
       "table_sha256": hashlib.sha256(json.dumps(table, sort_keys=True).encode()).hexdigest()}
print(json.dumps(out, indent=1, sort_keys=True))
