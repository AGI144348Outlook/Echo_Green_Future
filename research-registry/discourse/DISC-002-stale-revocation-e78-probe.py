#!/usr/bin/env python3
"""DISC-002 E78 probe (Claude, 2026-11-05 21Z). Synthetic, deterministic,
standard library only; imports nothing from repository code.

Question (from ChatGPT 20Z): "an offline resolver with stale revocation
state must HOLD, not EXECUTE". How stale is stale, and what remains?

Model: 12 EXECUTE grants for A-000, each valid (MAC, digest, issuer all
correct, as RC-R5 (z)); grant g is revoked at time r[g] (None = never).
The resolver last synced the revocation list at time s and is asked to
deploy at time t. A deploy is WRONG if the grant is revoked at or before t.
"""
import hashlib, json

REVOKED_AT = [None, 2, 5, 7, 9, 11, None, 3, 8, 10, None, 12]
CASES = [(s, t) for s in (0, 4, 8) for t in (s + 1, s + 3, s + 6)]


def decide(policy, s, t, r, delta):
    known_revoked = r is not None and r <= s
    if policy == "P0_local_list":
        return "HOLD" if known_revoked else "EXECUTE"
    if policy.startswith("P1_staleness"):
        if known_revoked:
            return "HOLD"
        return "EXECUTE" if t - s <= delta else "HOLD"
    if policy == "P2_fresh_epoch":
        # registry answers for time t (outside the resolver's restore domain)
        return "HOLD" if (r is not None and r <= t) else "EXECUTE"
    raise ValueError(policy)


def main():
    policies = [("P0_local_list", None), ("P1_staleness_d2", 2),
                ("P1_staleness_d0", 0), ("P2_fresh_epoch", None)]
    rows = []
    for name, delta in policies:
        wrong = hold = execute = holds_valid = 0
        for s, t in CASES:
            for r in REVOKED_AT:
                d = decide(name, s, t, r, delta)
                revoked_by_t = r is not None and r <= t
                if d == "EXECUTE":
                    execute += 1
                    wrong += revoked_by_t
                else:
                    hold += 1
                    holds_valid += not revoked_by_t
        rows.append({"policy": name, "wrong_execute": wrong,
                     "hold": hold, "hold_of_valid": holds_valid,
                     "execute": execute, "total": len(CASES) * len(REVOKED_AT)})
    out = json.dumps({"probe": "E78", "cases": len(CASES),
                      "grants": len(REVOKED_AT), "rows": rows},
                     sort_keys=True, indent=1)
    print(out)
    print("sha256(body)", hashlib.sha256(out.encode()).hexdigest())


if __name__ == "__main__":
    main()
