#!/usr/bin/env python3
"""F-001 §148 (Claude, 2026-10-29T17Z; records only). Article 1 ("Hacksilber") arithmetic.
Reads no file. The six Dataset A masses are copied from The-TAM-protocol d46456a, Dataset A blob b62c970a.
Question: do the masses fit the 13.7 g unit better than the 11.4 g shekel the article says they fail?"""
masses = [("Ingot Slice (Heavy)", 136.98), ("Coiled Wire (Large)", 68.52), ("Hacksilber Scraps (x3)", 13.71),
          ("Flattened Foil", 6.86), ("Silver Droplet", 3.42), ("Small Scrap", 1.71)]
def nearest(r, steps):  # nearest allowed multiple and its % deviation
    best = min(steps, key=lambda s: abs(r - s)); return best, 100 * (r - best) / best
indus = [10, 5, 1, 0.5, 0.25, 0.125]                  # the article's own fractions of 13.7 g
local = [12, 6, 1.2, 0.6, 0.3, 0.15, 1, 0.5, 0.25]    # simple multiples of 11.4 g (tenths and halves)
print("13.7/11.4 =", round(13.7 / 11.4, 4), "(about 6/5)")
worst = {"13.7": 0, "11.4": 0}
for name, m in masses:
    a, da = nearest(m / 13.7, indus); b, db = nearest(m / 11.4, local)
    worst["13.7"] = max(worst["13.7"], abs(da)); worst["11.4"] = max(worst["11.4"], abs(db))
    print(f"{name:24s} {m:7.2f} g  13.7 g x {a:<6} {da:+.3f}%   11.4 g x {b:<5} {db:+.3f}%")
print("largest deviation: 13.7 g unit %.3f%%, 11.4 g shekel %.3f%%" % (worst["13.7"], worst["11.4"]))
print("13.7/2 =", 13.7 / 2, " 13.7/4 =", 13.7 / 4, "(the text prints 3.42)")
# Same rows counted in gerah, taking the gerah as 1/20 of an 11.4 g shekel (0.57 g; the 1/20 ratio is
# the biblical one, Exodus 30:13 -- general knowledge, not checked against an archaeological source here).
g = 11.4 / 20
for name, m in masses:
    n = round(m / g); print(f"{name:24s} {m:7.2f} g = {n:3d} gerah of {g:.2f} g  {100*(m/g-n)/n:+.3f}%")
