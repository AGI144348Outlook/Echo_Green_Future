#!/usr/bin/env python3
"""F-001 claim-chain draft gate. UNTESTED; not a release authorization.
Usage: python3 -I claim_chain_gate_573.py <source-dir> <out-dir>
Requires the exact claim_scan.py FILES/TRIGGERS/sentences implementation to
be reviewed before any claim of semantic equivalence. No network or writes.
"""
import csv, hashlib, json, sys
from collections import Counter
from pathlib import Path

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def check(src, out):
    errors = []
    report_path = out / "claims-report.json"
    worksheet_path = out / "claims.csv"
    if not report_path.is_file() or not worksheet_path.is_file():
        return ["missing report or worksheet"]
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        with worksheet_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required = {"file", "sentence_no", "triggers", "sentence", "status"}
            if not required.issubset(set(reader.fieldnames or [])):
                return ["missing worksheet columns"]
            rows = list(reader)
    except (ValueError, OSError, UnicodeError, csv.Error) as exc:
        return ["invalid input: " + type(exc).__name__]
    source_files = report.get("source_files")
    if not isinstance(source_files, dict) or not source_files:
        return ["missing source file map"]
    for name, expected in source_files.items():
        path = src / name
        try:
            if not isinstance(name, str) or path.resolve().is_relative_to(src.resolve()) is False:
                errors.append("unsafe source path"); continue
            if not isinstance(expected, str) or len(expected) != 64:
                errors.append("missing source fingerprint: " + str(name)); continue
            if not path.is_file() or sha256(path.read_bytes()) != expected:
                errors.append("source fingerprint mismatch: " + name)
        except (OSError, ValueError, TypeError):
            errors.append("unreadable source: " + str(name))
    if report.get("rows") != len(rows):
        errors.append("report/worksheet row count mismatch")
    per_file = Counter(row.get("file", "") for row in rows)
    if any(name not in source_files for name in per_file):
        errors.append("worksheet references unregistered source")
    for name, count in report.get("per_file", {}).items():
        if per_file[name] != count:
            errors.append("per-file row count mismatch: " + name)
    seen = set()
    for row in rows:
        key = (row.get("file"), row.get("sentence_no"), row.get("sentence"))
        if key in seen:
            errors.append("duplicate worksheet row")
        seen.add(key)
        if (row.get("status") or "").strip().lower() not in {"claimed", "inferred", "test", "cut", "sourced"}:
            errors.append("unreviewed status")
    # This gate intentionally does NOT certify sentence alignment, reviewer
    # authority, cut removal, source licensing, or built-artifact fingerprints.
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    problems = check(Path(sys.argv[1]), Path(sys.argv[2]))
    for item in problems:
        print("FAIL", item)
    if not problems:
        print("PASS structural checks only; RELEASE HOLD")
    sys.exit(bool(problems))
