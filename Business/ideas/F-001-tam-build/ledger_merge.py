#!/usr/bin/env python3
"""F-001 records step (§48/§49/§53, PROPOSED): merge ledger_map.py output into a running ledger.

§48/§49 found that appending each month's ledger_map.py output double-counts sales
(all-time exports) or loses late refunds (month-only exports). The rule: export ALL-TIME
each month, map it with ledger_map.py, then merge here, keyed on `source_ref`:

  - every row of the existing ledger is kept as is (never edited, never dropped);
  - a new row whose source_ref is already in the ledger is skipped and counted;
  - a new row with a new source_ref is appended (a late refund arrives as `<id>:refund`);
  - a new row with an EMPTY source_ref is not merged: it is listed for a person to look at
    (ledger_map.py lists the same line as "missing sale_id");
  - a skipped row whose figures differ from the kept row is listed as a conflict
    (the ledger keeps the first figures; a correction is a new reversing row, by hand).

It writes a NEW file and refuses to overwrite one, refuses output inside a git repository
(ledger rows are private), never reads the network, and contacts nothing.

Usage: python3 -I ledger_merge.py <ledger.csv | -> <new-rows.csv> <out.csv>
       ("-" = no ledger yet). Prints a JSON report; exit 1 if any row needs a person.
"""
import csv, json, sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

FIELDS = ["date", "fiscal_contract", "kind", "category", "gross", "fees", "net",
          "asset_or_liability", "share", "source", "source_ref", "receipt_ref",
          "evidence", "entered_by"]
COMPARE = ("date", "category", "gross", "fees", "net")


def read(path):
    if path == "-":
        return []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if r.fieldnames != FIELDS:
            sys.exit(f"{path}: header {r.fieldnames} is not the ledger_map.py header")
        return list(r)


def dec(t):
    try:
        return Decimal(t) if t else None
    except InvalidOperation:
        return None


def main(ledger, new, out):
    o = Path(out)
    if o.exists():
        sys.exit(f"refusing: {out} exists (write a new file; the old ledger is kept)")
    if any((p / ".git").exists() for p in o.resolve().parent.parents) or (o.resolve().parent / ".git").exists():
        sys.exit("refusing: output is inside a git repository (ledger rows are private)")
    kept, incoming = read(ledger), read(new)
    by_ref = {r["source_ref"]: r for r in kept if r["source_ref"]}
    rep = {"ledger_rows": len(kept), "new_rows": len(incoming), "appended": 0,
           "skipped_same": 0, "conflicts": [], "unkeyed_not_merged": []}
    rows = list(kept)
    for n, r in enumerate(incoming, start=2):
        ref = r["source_ref"].strip()
        if not ref:
            rep["unkeyed_not_merged"].append(f"{new} line {n}")
        elif ref in by_ref:
            old = by_ref[ref]
            diff = [k for k in COMPARE if old[k] != r[k]]
            if diff:
                rep["conflicts"].append({"source_ref": ref, "fields": diff, "line": n})
            else:
                rep["skipped_same"] += 1
        else:
            by_ref[ref] = r; rows.append(r); rep["appended"] += 1
    month = defaultdict(lambda: Decimal(0)); open_net = []
    for i, r in enumerate(rows, start=2):
        v = dec(r["net"])
        if v is None: open_net.append(f"{out} line {i}: net")
        else: month[r["date"][:7] or "unknown-month"] += v
    rep["net_by_month"] = {k: str(v) for k, v in sorted(month.items())}
    rep["net_total"] = str(sum(month.values(), Decimal(0)))
    rep["net_missing"] = open_net
    o.parent.mkdir(parents=True, exist_ok=True)
    with open(o, "x", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print(json.dumps(rep, indent=2))
    return 1 if (rep["conflicts"] or rep["unkeyed_not_merged"]) else 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
