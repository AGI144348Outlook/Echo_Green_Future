#!/usr/bin/env python3
"""F-001 records step, year end (§58, PROPOSED draft; not yet adopted).

Reads one or more ledger-rows.csv files written by ledger_map.py (or the merged file
written by ledger_merge.py) and prints, per calendar year, the totals a filing packet
needs, plus the gaps that would make those totals wrong:

  sales_count, sales_gross   "product sales" rows only, before refunds (the figure a
                             platform's Form 1099-K, if one is issued, would be compared
                             with; what a 1099-K reports is UNVERIFIED here)
  refunds_count, refunds_gross   "refunds issued" rows (negative), dated when refunded
  fees, net                  sums of the non-empty cells
  rows_missing_figures       rows whose gross, fees or net cell is empty (never guessed)
  months_with_rows / months_without_rows   calendar months with no row at all are listed,
                             because a month with no sales and a month whose export was
                             never merged look the same in the ledger
  duplicate_source_refs      the same source_ref twice (the §48 double-export case)

Options:
  --year=YYYY            only that year
  --form-gross=AMOUNT    a gross figure read by Timothy from a platform tax form for
                         --year; the difference from sales_gross is printed. Exit 1 when it
                         is not zero, so the year is not closed silently. Requires --year.

Exit 0 when nothing is flagged; exit 1 when any row lacks a figure or a date, any
source_ref repeats, or --form-gross differs. It reads local files only, writes nothing,
never reads the network, and must be run on private ledger files outside any repository.
Not tax advice: which figure goes where on a return is for Timothy or his preparer.

Usage: python3 -I year_close.py <ledger-rows.csv> [more.csv ...] [--year=YYYY] [--form-gross=AMOUNT]
"""
import csv, sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation


def amount(text):
    t = (text or "").strip().replace("$", "").replace(",", "")
    if not t:
        return None
    try:
        return Decimal(t)
    except InvalidOperation:
        return None


def main(argv):
    files, year, form_gross = [], None, None
    for a in argv:
        if a.startswith("--year="):
            year = a.split("=", 1)[1]
            if not (len(year) == 4 and year.isdigit()):
                sys.exit("--year must be YYYY")
        elif a.startswith("--form-gross="):
            form_gross = amount(a.split("=", 1)[1])
            if form_gross is None:
                sys.exit("--form-gross must be an amount, e.g. 1234.56")
        elif a.startswith("--"):
            sys.exit(f"unknown option {a!r}")
        else:
            files.append(a)
    if not files:
        sys.exit(__doc__)
    if form_gross is not None and year is None:
        sys.exit("--form-gross needs --year")

    years = defaultdict(lambda: {"sales_count": 0, "sales_gross": Decimal(0), "refunds_count": 0,
                                 "refunds_gross": Decimal(0), "fees": Decimal(0), "net": Decimal(0),
                                 "rows_missing_figures": 0, "months": set()})
    refs, undated, flagged = Counter(), 0, False
    for path in files:
        with open(path, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                d = (r.get("date") or "").strip()
                if len(d) < 7 or d[4] != "-":
                    undated += 1
                    continue
                y = years[d[:4]]
                y["months"].add(d[:7])
                refs[(r.get("source_ref") or "").strip()] += 1
                g, fee, net = amount(r.get("gross")), amount(r.get("fees")), amount(r.get("net"))
                cat = (r.get("category") or "").strip()
                if cat == "refunds issued":
                    y["refunds_count"] += 1
                    if g is not None: y["refunds_gross"] += g
                    if g is None: y["rows_missing_figures"] += 1  # refund fee cell is empty by design
                else:
                    y["sales_count"] += 1
                    if g is not None: y["sales_gross"] += g
                    if None in (g, fee, net): y["rows_missing_figures"] += 1
                if fee is not None: y["fees"] += fee
                if net is not None: y["net"] += net

    dups = sorted(k for k, n in refs.items() if n > 1 and k)
    for k in sorted(years):
        if year and k != year:
            continue
        v = years[k]
        present = sorted(v["months"])
        lo, hi = int(present[0][5:]), int(present[-1][5:])
        absent = [f"{k}-{m:02d}" for m in range(lo, hi + 1) if f"{k}-{m:02d}" not in v["months"]]
        print(f"{k}: sales {v['sales_count']} gross {v['sales_gross']}; refunds {v['refunds_count']} "
              f"gross {v['refunds_gross']}; fees {v['fees']}; net {v['net']}")
        print(f"  months with rows {present[0]}..{present[-1]} ({len(present)}); "
              f"gaps inside that span: {absent or 'none'}")
        if v["rows_missing_figures"]:
            print(f"  FLAG rows missing a figure: {v['rows_missing_figures']}"); flagged = True
        if absent:
            print("  NOTE a gap may be a month with no sales or an export never merged; check which")
        if form_gross is not None and k == year:
            diff = form_gross - v["sales_gross"]
            print(f"  form gross {form_gross} - ledger sales gross {v['sales_gross']} = {diff}")
            if diff != 0:
                print("  FLAG form and ledger differ; find the cause before the year is closed")
                flagged = True
    if year and year not in years:
        print(f"{year}: no dated rows"); flagged = flagged or form_gross is not None
    if undated:
        print(f"FLAG rows without a usable date: {undated}"); flagged = True
    if dups:
        print(f"FLAG source_ref repeated: {dups}"); flagged = True
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
