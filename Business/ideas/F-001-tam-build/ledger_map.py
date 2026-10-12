#!/usr/bin/env python3
"""F-001 records step (§6 / §15.4, PROPOSED): map a platform sales export to ledger rows.

Reads ONE sales CSV that Timothy exports privately from the sales platform and writes,
OUTSIDE any repository, rows in the shape of Business/ledger/SCHEMA.md plus a
monthly summary:
  ledger-rows.csv     one row per sale; one extra reversing row per refund (never an edit)
  ledger-month.json   per month: sales count, refunds count, gross, fees, net, missing figures

Rules carried from SCHEMA.md:
  - amounts are never estimated: an empty or unreadable fee or amount stays empty
    and is listed under "missing" in the summary;
  - a refund is a new negative row (category "refunds issued"), the sale row is kept;
  - evidence is SOURCE-OBSERVED only for figures read from the export.

The column names of the real export are NOT known (UNVERIFIED): edit COLUMNS to match
the header of the file actually exported. The script stops with a clear message if a
required column is missing, rather than guessing.

It never reads the network, never sells, uploads or contacts anything, and must not be
pointed at a path inside a public repository for its output.

Usage: python3 -I ledger_map.py <export.csv> <out-dir> <run-id>
"""
import csv, json, sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

# Map: ledger meaning -> header in the platform export (PROPOSED; UNVERIFIED).
COLUMNS = {
    "date": "Purchase Date",        # YYYY-MM-DD or YYYY-MM-DD HH:MM:SS
    "sale_id": "Sale ID",
    "gross": "Price",               # amount paid by the buyer, before fees
    "fees": "Fees",                 # platform + processing fees, if the export has them
    "refunded": "Refunded",         # "true"/"yes"/"1" when refunded
    "refund_date": "Refund Date",   # optional; falls back to the sale date if absent
}
REQUIRED = ("date", "sale_id", "gross")
SOURCE = "sales platform (name set by Timothy)"
OUT_FIELDS = ["date", "fiscal_contract", "kind", "category", "gross", "fees", "net",
              "asset_or_liability", "share", "source", "source_ref", "receipt_ref",
              "evidence", "entered_by"]


def amount(text):
    """Decimal from the export, or None if empty/unreadable (never guessed)."""
    t = (text or "").strip().replace("$", "").replace(",", "")
    if not t:
        return None
    try:
        return Decimal(t)
    except InvalidOperation:
        return None


def day(text):
    t = (text or "").strip()[:10]
    return t if len(t) == 10 and t[4] == "-" and t[7] == "-" else None


def main(src, out_dir, run_id):
    out = Path(out_dir)
    if (out / ".git").exists() or any((p / ".git").exists() for p in out.resolve().parents):
        sys.exit("refusing: output directory is inside a git repository (ledger rows are private)")
    out.mkdir(parents=True, exist_ok=True)
    with open(src, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        missing_cols = [k for k in REQUIRED if COLUMNS[k] not in header]
        if missing_cols:
            sys.exit(f"export lacks required columns {[COLUMNS[k] for k in missing_cols]}; "
                     f"header is {header}; edit COLUMNS")
        has = {k: COLUMNS[k] in header for k in COLUMNS}
        rows, month = [], defaultdict(lambda: {"sales": 0, "refunds": 0, "gross": Decimal(0),
                                               "fees": Decimal(0), "net": Decimal(0),
                                               "missing": []})
        for n, r in enumerate(reader, start=2):
            d, sid = day(r[COLUMNS["date"]]), r[COLUMNS["sale_id"]].strip()
            g = amount(r[COLUMNS["gross"]])
            fee = amount(r[COLUMNS["fees"]]) if has["fees"] else None
            key = d[:7] if d else "unknown-month"
            m = month[key]
            if d is None: m["missing"].append(f"line {n}: date")
            if g is None: m["missing"].append(f"line {n}: gross")
            if fee is None: m["missing"].append(f"line {n}: fees")
            net = (g - fee) if (g is not None and fee is not None) else None
            base = {"fiscal_contract": "F-001", "asset_or_liability": "asset",
                    "share": "business", "source": SOURCE, "receipt_ref": "",
                    "evidence": "SOURCE-OBSERVED", "entered_by": f"ledger_map.py {run_id}"}
            rows.append({**base, "date": d or "", "kind": "income", "category": "product sales",
                         "gross": g if g is not None else "", "fees": fee if fee is not None else "",
                         "net": net if net is not None else "", "source_ref": sid})
            m["sales"] += 1
            for k, v in (("gross", g), ("fees", fee), ("net", net)):
                if v is not None: m[k] += v
            refunded = has["refunded"] and r[COLUMNS["refunded"]].strip().lower() in ("true", "yes", "1")
            if refunded:
                rd = day(r[COLUMNS["refund_date"]]) if has["refund_date"] else None
                rkey = (rd or d or "unknown-month")[:7] if (rd or d) else "unknown-month"
                rm = month[rkey]
                # Fees on refunds are platform-specific (UNVERIFIED): the reversing row
                # reverses gross only; any fee refund must come from the export, not a guess.
                rows.append({**base, "date": rd or d or "", "kind": "income",
                             "category": "refunds issued",
                             "gross": -g if g is not None else "", "fees": "",
                             "net": -g if g is not None else "", "source_ref": f"{sid}:refund"})
                rm["refunds"] += 1
                rm["missing"].append(f"line {n}: refund fee treatment (not in export mapping)")
                if g is not None:
                    rm["gross"] -= g; rm["net"] -= g
    with open(out / "ledger-rows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS); w.writeheader(); w.writerows(rows)
    summary = {k: {**v, "gross": str(v["gross"]), "fees": str(v["fees"]), "net": str(v["net"])}
               for k, v in sorted(month.items())}
    (out / "ledger-month.json").write_text(json.dumps({"source_file": Path(src).name,
                                                       "columns_used": {k: COLUMNS[k] for k in COLUMNS if has[k]},
                                                       "months": summary}, indent=2))
    print(f"{len(rows)} ledger rows; months: {', '.join(summary)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
