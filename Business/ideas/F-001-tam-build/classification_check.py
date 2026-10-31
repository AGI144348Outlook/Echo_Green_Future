#!/usr/bin/env python3
"""F-001 gate-H rights check (Claude, 2026-10-31 10Z, §184). DRAFT: the value list is Timothy's to set.

Reads a reading-queue TSV (READING-QUEUE-182.tsv shape) and refuses unless every row's `classification`
is non-empty and in the list given with --allowed. There is no default list on purpose. Prints counts only,
never unit text. Exit 0 = all rows classified with allowed values; 1 = refused; 2 = unusable input.
A pass here is evidence for one part of gate H, never a release decision.
"""
import argparse, csv, sys
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("queue"); ap.add_argument("--allowed", required=True, help="comma-separated value list")
a = ap.parse_args()
allowed = [v.strip() for v in a.allowed.split(",") if v.strip()]
if not allowed: print("unusable: empty --allowed"); sys.exit(2)
try:
    with open(a.queue, newline="", encoding="utf-8") as f: rows = list(csv.DictReader(f, delimiter="\t"))
except OSError as e: print(f"unusable: {e.__class__.__name__}"); sys.exit(2)
if not rows or "classification" not in rows[0] or "unit" not in rows[0]: print("unusable: no rows or missing column"); sys.exit(2)
units = [r["unit"] for r in rows]
dups = len(units) - len(set(units))
c = Counter("EMPTY" if not (r["classification"] or "").strip() else
            (r["classification"].strip() if r["classification"].strip() in allowed else "OUTSIDE-LIST") for r in rows)
print("allowed\t" + ",".join(sorted(set(allowed))))  # §185: record which list the verdict used
print(f"rows\t{len(rows)}\nduplicate_units\t{dups}")
for k in sorted(c): print(f"{k}\t{c[k]}")
ok = dups == 0 and c["EMPTY"] == 0 and c["OUTSIDE-LIST"] == 0
print("result\t" + ("PASS (one H item only; not a release)" if ok else "REFUSED")); sys.exit(0 if ok else 1)
