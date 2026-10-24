# GPT-owned Run 332 draft, source copied from shared blob fa3a62f and modified P1-P4.
# NOT APPROVED FOR RELEASE; prospective test issue #50.
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
import csv, hashlib, json, re, subprocess, sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

BASE = 13.7  # source value; original floating-point deviation calculation retained
BASE_EXACT = Decimal("13.7")
PIN_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
PIN_A_BLOB = "b62c970a660e0a6685b58db1ef121690daa4fce7"
PIN_B_BLOB = "12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4"
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


def exact_mass(units):
    f = Fraction(units)
    value = BASE_EXACT * Decimal(f.numerator) / Decimal(f.denominator)
    return format(value.normalize(), "f")


def source_pins(src):
    """Fail closed before writing; git blob = sha1(b'blob '+len+NUL+raw bytes)."""
    cmd = lambda *args: subprocess.run(["git", "-C", str(src), *args],
                                       capture_output=True, text=True)
    head = cmd("rev-parse", "HEAD")
    if head.returncode or head.stdout.strip() != PIN_COMMIT:
        raise ValueError("TAM source commit differs from pinned commit")
    status = cmd("status", "--porcelain")
    if status.returncode or status.stdout.strip():
        raise ValueError("TAM source clone is dirty or git status failed")
    blobs = {}
    for name, expected in ((A_FILE, PIN_A_BLOB), (B_FILE, PIN_B_BLOB)):
        data = (src / name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") +
                            bytes([0]) + data).hexdigest()
        if blob != expected:
            raise ValueError("TAM source blob mismatch: " + name)
        blobs[name] = blob
    return blobs


def main(src, out):
    src, out = Path(src).resolve(), Path(out).resolve()
    if out == src or src in out.parents:
        sys.exit("refusing to write inside the source clone")
    pins = source_pins(src)
    out.mkdir(parents=True, exist_ok=True)
    report = {"base_g_per_unit": BASE, "source_commit": PIN_COMMIT, "files": {}}

    a_text = (src / A_FILE).read_text(encoding="utf-8")
    a_rows, a_rej = parse(a_text, A_ROW, "Object Description")
    with open(out / "dataset-a.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["object", "measured_g", "units", "registry_sign", "stated_deviation_pct", "term",
                    "expected_g", "recomputed_deviation_pct", "within_0_01_pct_points_of_recomputed",
                    "calculation_method_from_source", "terminology_conflict"])
        for r in a_rows:
            u = float(r["units"]); exp = BASE * u; rec = pct(float(r["mass"]), exp)
            stated = r["dev"]
            ok = (abs(rec) < 0.01) if stated.startswith("<") else abs(float(stated) - rec) <= 0.01
            conflict = "SOURCE_UNRESOLVED" if "gerah" in r["term"].lower() else ""
            w.writerow([r["object"], r["mass"], r["units"], r["sign"], stated, r["term"],
                        exact_mass(r["units"]), rec, ok, "UNKNOWN", conflict])
    report["files"]["A"] = {"sha256": hashlib.sha256(a_text.encode()).hexdigest(),
                            "git_blob": pins[A_FILE],
                            "rows": len(a_rows), "rejected": a_rej}

    b_text = (src / B_FILE).read_text(encoding="utf-8")
    b_rows, b_rej = parse(b_text, B_ROW, "Ratio Mass")
    with open(out / "dataset-b.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ratio", "mass_g", "registry_sign", "units", "relation_to_dataset_a",
                    "expected_g_from_units", "deviation_pct", "ratio_over_16_equals_units",
                    "terminology_conflict"])
        for r in b_rows:
            u = units_value(r["units"]); exp = BASE * u
            conflict = "SOURCE_UNRESOLVED" if "gerah" in " ".join(r.values()).lower() else ""
            w.writerow([r["ratio"], r["mass"], r["sign"], r["units"], r["relation"],
                        exact_mass(r["units"]), pct(float(r["mass"]), exp),
                        abs(int(r["ratio"]) / 16 - u) < 1e-9, conflict])
    report["files"]["B"] = {"sha256": hashlib.sha256(b_text.encode()).hexdigest(),
                            "git_blob": pins[B_FILE],
                            "rows": len(b_rows), "rejected": b_rej}
    if len(a_rows) != 6 or len(b_rows) != 8 or a_rej or b_rej:
        raise ValueError("unexpected source row counts or rejected source lines")
    if sum("gerah" in r["term"].lower() for r in a_rows) != 1 or sum(
            "gerah" in " ".join(r.values()).lower() for r in b_rows) != 1:
        raise ValueError("unexpected Gerah source occurrence count")
    (out / "dataset-check.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: {"rows": v["rows"], "rejected": len(v["rejected"])} for k, v in report["files"].items()}))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
