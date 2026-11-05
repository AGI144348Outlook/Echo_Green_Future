#!/usr/bin/env python3
"""DISC-002 E76 probe (Claude, 2026-11-05 18Z). Exploratory, synthetic, deterministic.

Part A (falsifier 5, sink key expiry): one request, crash after the sink effect (E75 c2),
resolver asks the sink "was key K applied?" after a delay d. The sink keeps K for TTL ticks.
If d > TTL the sink answers "unknown/not applied" and the resolver re-sends: duplicate.
Policies compared: sink query only; sink query + HOLD when the key may have expired
(resolver knows TTL and the claim time); retry-only (E75 baseline).

Part B (falsifier 6, EXECUTE separation): callers checked by three gates.
 G0 = name 'A-000' and status ACTIVE (the shape observed in Genesis blob 63eb982 lines 9381-9435,
      modelled here, not imported);
 G1 = pinned digest only; G2 = pinned digest AND an EXECUTE grant.
No repository code is imported or changed.
"""
PINNED = "sha256:aaaa"
TTLS = [2, 4, 8]
DELAYS = [1, 3, 5, 9]

def part_a():
    rows = []
    for policy in ("retry_only", "sink_query", "sink_query_hold_if_expired"):
        dup = held = once = 0
        for ttl in TTLS:
            for d in DELAYS:
                applied = 1  # c2: effect happened before the crash
                key_known = d <= ttl
                if policy == "retry_only":
                    applied += 1
                elif policy == "sink_query":
                    if not key_known:
                        applied += 1
                else:
                    if not key_known:
                        held += 1
                        continue
                if applied == 1:
                    once += 1
                else:
                    dup += 1
        rows.append((policy, dup, held, once, len(TTLS) * len(DELAYS)))
    return rows

CALLERS = [
    ("C1 valid digest, EXECUTE", "A-000", "ACTIVE", PINNED, {"EXECUTE"}, True),
    ("C2 valid digest, READ only", "A-000", "ACTIVE", PINNED, {"READ"}, False),
    ("C3 impostor name, no digest", "A-000", "ACTIVE", "sha256:ffff", {"EXECUTE"}, False),
    ("C4 valid digest, no grant", "A-000", "ACTIVE", PINNED, set(), False),
    ("C5 valid digest, EXECUTE, INACTIVE", "A-000", "INACTIVE", PINNED, {"EXECUTE"}, False),
]

def g0(c): return c[1] == "A-000" and c[2] == "ACTIVE"
def g1(c): return c[3] == PINNED
def g2(c): return c[3] == PINNED and "EXECUTE" in c[4] and c[2] == "ACTIVE"

def part_b():
    out = []
    for c in CALLERS:
        out.append((c[0], c[5], g0(c), g1(c), g2(c)))
    return out

if __name__ == "__main__":
    print("E76 part A: crash after effect, resolver queries sink after delay d; TTL in", TTLS, "delays", DELAYS)
    print("policy | duplicate | HOLD | exactly-once | cases")
    for r in part_a():
        print(" | ".join(str(x) for x in r))
    print()
    print("E76 part B: deploy decision per gate (True = deploys); expected = should deploy")
    print("caller | expected | G0 name+ACTIVE | G1 digest | G2 digest+EXECUTE+ACTIVE")
    wrong = {"G0": 0, "G1": 0, "G2": 0}
    for name, exp, a, b, c in part_b():
        print(f"{name} | {exp} | {a} | {b} | {c}")
        for k, v in (("G0", a), ("G1", b), ("G2", c)):
            wrong[k] += (v != exp)
    print("wrong decisions /5:", wrong)
