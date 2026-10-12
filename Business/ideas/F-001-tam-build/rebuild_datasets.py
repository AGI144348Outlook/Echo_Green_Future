#!/usr/bin/env python3
"""F-001 candidate A, TAM shape: rebuild Dataset A and B as CSV (PROPOSED; §17).

The two dataset files in AGI144348Outlook/The-TAM-protocol lost their column
separators when copied from NotebookLM (F-001 §16.2). This script rebuilds the
columns with fixed, documented patterns (one per table), refuses any row that
does not match, and re-checks every number against the 13.7 g base.

Reads a local clone (read-only) and writes, into an output directory OUTSIDE any
repository: dataset-a.csv, dataset-b.csv, dataset-check.json. It never edits the
source and never corrects a value: stated values are copied as stated, and the
recomputed values sit in separate columns so Timothy can decide (§16.2).

Usage: python3 -I rebuild_datasets.py <tam-clone-dir> <out-dir>
"""
import csv, hashlib, json, re, sys
from pathlib import Path

BASE = 13.7  # grams per Unit (U), as stated by the source
A_FILE = "Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)"
B_FILE = "Dataset_B_Binary_Matrix.md"

# Dataset A: <object> <mass>g <units> Unit(s) (<sign>) <deviation>\% <term>
A_ROW = re.compile(r"^(?P<object>.+?) (?P<mass>\d+\.\d+)g (?P<units>\d+(?:\.\d+)?) Units? \((?P<sign>[^)]*)\) "
                   r"(?P<dev>[<+\-]?\d+\.\d+)\\?% (?P<term>.+)$")
# Dataset B: <ratio> <mass>g <sign> <unit_label> Unit(s) <relation>
B_ROW = re.compile(r"^(?P<ratio>\d+) (?P<mass>\d+\.\d+)g (?P<sign>.+?) (?P<units>\d+(?:/\d+)?(?:\.\d+)?) Units? "
                   r"(?P<relation>.+)$")


def units_value(s):
    if "/" in s:
        n, d = s.split("/")
        return int(n) / int(d)
    return float(s)


def pct(measured, expected):
    return round((measured - expected) / expected * 100, 3)


def parse(text, pattern, header_prefix):
    rows, rejected = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(header_prefix) or line.startswith("Source:") or line.startswith("This table"):
            continue
        m = pattern.match(line)
        (rows if m else rejected).append(m.groupdict() if m else line)
    return rows, rejected


def main(src, out):
    src, out = Path(src).resolve(), Path(out).resolve()
    if out == src or src in out.parents:
        sys.exit("refusing to write inside the source clone")
    out.mkdir(parents=True, exist_ok=True)
    report = {"base_g_per_unit": BASE, "files": {}}

    a_text = (src / A_FILE).read_text(encoding="utf-8")
    a_rows, a_rej = parse(a_text, A_ROW, "Object Description")
    with open(out / "dataset-a.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["object", "measured_g", "units", "registry_sign", "stated_deviation_pct", "term",
                    "expected_g", "recomputed_deviation_pct", "stated_matches_recomputed"])
        for r in a_rows:
            u = float(r["units"]); exp = BASE * u; rec = pct(float(r["mass"]), exp)
            stated = r["dev"]
            ok = (abs(rec) < 0.01) if stated.startswith("<") else abs(float(stated) - rec) <= 0.01
            w.writerow([r["object"], r["mass"], r["units"], r["sign"], stated, r["term"], round(exp, 4), rec, ok])
    report["files"]["A"] = {"sha256": hashlib.sha256(a_text.encode()).hexdigest(),
                            "rows": len(a_rows), "rejected": a_rej}

    b_text = (src / B_FILE).read_text(encoding="utf-8")
    b_rows, b_rej = parse(b_text, B_ROW, "Ratio Mass")
    with open(out / "dataset-b.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ratio", "mass_g", "registry_sign", "units", "relation_to_dataset_a",
                    "expected_g_from_units", "deviation_pct", "ratio_over_16_equals_units"])
        for r in b_rows:
            u = units_value(r["units"]); exp = BASE * u
            w.writerow([r["ratio"], r["mass"], r["sign"], r["units"], r["relation"], round(exp, 4),
                        pct(float(r["mass"]), exp), abs(int(r["ratio"]) / 16 - u) < 1e-9])
    report["files"]["B"] = {"sha256": hashlib.sha256(b_text.encode()).hexdigest(),
                            "rows": len(b_rows), "rejected": b_rej}
    (out / "dataset-check.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: {"rows": v["rows"], "rejected": len(v["rejected"])} for k, v in report["files"].items()}))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
