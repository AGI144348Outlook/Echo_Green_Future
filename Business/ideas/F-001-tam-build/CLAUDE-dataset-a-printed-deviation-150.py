#!/usr/bin/env python3
"""F-001 §150 (Claude, 2026-10-29T19Z; records only). Dataset A printed deviations vs direct arithmetic,
and the exact 6/5 relation between the two fraction menus (ChatGPT run 449, Issue #129).
Reads no file. Values copied from The-TAM-protocol d46456a, Dataset A blob b62c970a."""
from fractions import Fraction as F
rows = [("Ingot Slice (Heavy)", "136.98", F(10), "-0.01"), ("Coiled Wire (Large)", "68.52", F(5), "+0.03"),
        ("Hacksilber Scraps (x3)", "13.71", F(1), "+0.07"), ("Flattened Foil", "6.86", F(1, 2), "+0.14"),
        ("Silver Droplet", "3.42", F(1, 4), "-0.03"), ("Small Scrap", "1.71", F(1, 8), "<0.01")]
base = F("13.7")
bad = 0
for name, m, k, printed in rows:
    t = base * k; d = 100 * (F(m) - t) / t
    p = None if printed.startswith("<") else float(printed)
    ok = (abs(float(d)) < 0.01) if p is None else abs(float(d) - p) < 0.01
    bad += not ok
    print(f"{name:24s} {m:>7s} target {float(t):8.4f}  direct {float(d):+.4f}%  printed {printed:>6s}  {'ok' if ok else 'MISMATCH'}")
print("printed deviations that do not match direct arithmetic:", bad)
alt = [F(12), F(6), F(6, 5), F(3, 5), F(3, 10), F(3, 20)]
print("alt/orig ratios:", sorted({a / k for a, (_, _, k, _) in zip(alt, rows)}), " effective base:", float(F("11.4") * F(6, 5)))
