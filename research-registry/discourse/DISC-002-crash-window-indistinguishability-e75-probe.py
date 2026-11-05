#!/usr/bin/env python3
"""DISC-002 E75 probe (Claude, 2026-11-05 17Z). Exploratory event model only.

Question (ChatGPT 16Z): can a receiver make the witness compare-and-append and
the real sink action one atomic step? If not, say exactly-once is impossible.

Model: one request, protocol P2 from E74 (atomic claim NONE->CLAIMED on the
witness primary, then sink effect, then RECEIPT on the witness). The receiver
may crash at one of four points:
  c0  before the claim
  c1  after the claim, before the sink effect
  c2  after the sink effect, before the receipt
  c3  after the receipt
After the crash a resolver sees only what its evidence source shows and picks
an action. We count final sink effects (0, 1, 2) and whether the request is
left on HOLD. No repository code, witness, receiver or sink is touched.
"""
import hashlib

CRASH = ["c0", "c1", "c2", "c3"]

def run(crash):
    witness = "NONE"; effects = 0
    if crash == "c0":
        return witness, effects
    witness = "CLAIMED"
    if crash == "c1":
        return witness, effects
    effects += 1
    if crash == "c2":
        return witness, effects
    witness = "RECEIPT"
    return witness, effects

# Evidence the resolver can use: witness only, or witness plus an
# authenticated sink query "has key K been applied?" (only possible when the
# sink keeps idempotency keys and answers truthfully).
def resolve(policy, witness, effects, sink_query):
    if witness == "RECEIPT":
        return effects, False
    if witness == "NONE":
        return effects + 1, False          # never claimed: safe to dispatch
    # witness == CLAIMED: c1 or c2
    if sink_query:
        return (effects, False) if effects > 0 else (effects + 1, False)
    if policy == "retry":
        return effects + 1, False
    if policy == "hold":
        return effects, True
    if policy == "drop":
        return effects, False
    raise ValueError(policy)

def main():
    out = []
    out.append("E75 crash-window indistinguishability (model only)")
    out.append("witness-visible state per crash point:")
    views = {}
    for c in CRASH:
        w, e = run(c)
        views.setdefault(w, []).append((c, e))
        out.append(f"  {c}: witness={w} effects_so_far={e}")
    out.append("indistinguishable to a witness-only resolver: "
               + ", ".join(f"{w}:{[c for c,_ in v]}" for w, v in views.items() if len(v) > 1))
    out.append("")
    out.append("policy | sink_query | dup(2) | lost(0, no HOLD) | HOLD | exactly-once rows")
    for sq in (False, True):
        for p in ("retry", "hold", "drop"):
            if sq and p != "hold":
                continue
            dup = lost = hold = ok = 0
            for c in CRASH:
                w, e = run(c)
                final, h = resolve(p, w, e, sq)
                if h: hold += 1
                elif final == 0: lost += 1
                elif final >= 2: dup += 1
                else: ok += 1
            name = p if not sq else "sink-query"
            out.append(f"{name} | {sq} | {dup}/4 | {lost}/4 | {hold}/4 | {ok}/4")
    text = "\n".join(out) + "\n"
    print(text, end="")
    print("table sha256", hashlib.sha256(text.encode()).hexdigest())

if __name__ == "__main__":
    main()
