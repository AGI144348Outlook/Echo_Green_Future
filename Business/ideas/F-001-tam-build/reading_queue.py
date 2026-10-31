#!/usr/bin/env python3
"""F-001 §182: human reading queue for the 69 rights units (no quoted text).

Reads only DECISION-UNITS-175.tsv and QUOTED-SPANS-TRIAGE-174.tsv in this
directory and prints a TSV queue. Order: read_order ascending; inside each
read order, units whose longest span is >= 300 characters and that have no
cue come first (the §181 proposal), then by longest span descending, then
unit id. The queue is a reading hint only: it classifies nothing.
Usage: python3 -I reading_queue.py > READING-QUEUE-182.tsv
Exit 1 if a unit references a row missing from the triage file.
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def read(name):
    with open(os.path.join(HERE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def main():
    spans = {r["row"]: r for r in read("QUOTED-SPANS-TRIAGE-174.tsv")}
    units = read("DECISION-UNITS-175.tsv")
    out, errors = [], 0
    for u in units:
        rows = u["rows"].split(",")
        missing = [r for r in rows if r not in spans]
        if missing:
            print("unit %s: missing rows %s" % (u["unit"], missing), file=sys.stderr)
            errors += 1
            continue
        longest = max(int(spans[r]["chars"]) for r in rows)
        total = sum(int(spans[r]["chars"]) for r in rows)
        long_uncued = longest >= 300 and u["cued"] != "yes"
        out.append((int(u["read_order"]), 0 if long_uncued else 1, -longest,
                    u["unit"], u, longest, total, long_uncued))
    if errors:
        return 1
    out.sort(key=lambda t: t[:4])
    w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    w.writerow(["queue", "unit", "read_order", "cued", "long_uncued",
                "longest_chars", "total_chars", "n_rows", "rows", "files", "classification"])
    for i, t in enumerate(out, 1):
        u = t[4]
        w.writerow([i, u["unit"], u["read_order"], u["cued"], "yes" if t[7] else "no",
                    t[5], t[6], u["n_rows"], u["rows"], u["files"], ""])
    return 0

if __name__ == "__main__":
    sys.exit(main())
