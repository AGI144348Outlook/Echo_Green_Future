#!/usr/bin/env python3
"""F-001 claim-chain structural gate v576 (UNTESTED, RELEASE HOLD).
Usage: python3 -I F001-CLAIM-CHAIN-GATE-576.py SOURCE_DIR OUTPUT_DIR
This gate cannot independently reconstruct scanner sentences or establish rights.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HEX64 = re.compile(r"[0-9a-fA-F]{64}\Z")
STATUSES = {"claimed", "inferred", "test", "cut", "sourced"}
REQUIRED = {"file", "sentence_no", "triggers", "sentence", "status"}

def check(src, out):
    errors = []
    try:
        with (out / "claims-report.json").open(encoding="utf-8") as f:
            report = json.load(f)
        with (out / "claims.csv").open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if not REQUIRED.issubset(reader.fieldnames or []):
                return ["missing worksheet columns"]
            rows = list(reader)
    except (OSError, ValueError, UnicodeError, csv.Error) as exc:
        return ["invalid report or worksheet: " + type(exc).__name__]
    if not isinstance(report, dict):
        return ["report must be object"]
    files = report.get("source_files")
    if not isinstance(files, dict) or not files:
        return ["missing source file map"]
    try:
        root = src.resolve(strict=True)
    except OSError:
        return ["source root unavailable"]
    for name, digest in files.items():
        if not isinstance(name, str) or not name or Path(name).is_absolute() or ".." in Path(name).parts:
            errors.append("unsafe source name"); continue
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            errors.append("invalid source digest: " + name); continue
        try:
            path = src / name
            resolved = path.resolve(strict=True)
            if not resolved.is_relative_to(root) or path.is_symlink():
                errors.append("source path escapes root or is symlink: " + name); continue
            if not resolved.is_file():
                errors.append("not a source file: " + name); continue
            if hashlib.sha256(resolved.read_bytes()).hexdigest() != digest.lower():
                errors.append("source fingerprint mismatch: " + name)
        except (OSError, ValueError):
            errors.append("unreadable source: " + name)
    per_file = Counter()
    seen = set()
    for row in rows:
        name = row.get("file", "")
        per_file[name] += 1
        if name not in files:
            errors.append("worksheet references unregistered source")
        key = (name, row.get("sentence_no"), row.get("sentence"))
        if key in seen:
            errors.append("duplicate worksheet row")
        seen.add(key)
        if not str(row.get("sentence_no", "")).isdigit() or int(row["sentence_no"]) < 1:
            errors.append("invalid sentence index")
        if not (row.get("sentence") or "").strip():
            errors.append("empty sentence")
        if (row.get("status") or "").strip().lower() not in STATUSES:
            errors.append("unreviewed status")
    if type(report.get("rows")) is not int or report["rows"] != len(rows):
        errors.append("report/worksheet row count mismatch")
    counts = report.get("per_file")
    if not isinstance(counts, dict) or set(counts) != set(files):
        errors.append("per_file keys differ from source_files")
    elif any(type(v) is not int or v < 0 or per_file[k] != v for k, v in counts.items()):
        errors.append("per_file count mismatch")
    # Not yet verified: scanner FILES completeness, trigger parsing/counts,
    # exact sentence correspondence, reviewer authority, licensing, output cuts.
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: gate SOURCE_DIR OUTPUT_DIR")
    problems = check(Path(sys.argv[1]), Path(sys.argv[2]))
    for problem in problems:
        print("FAIL", problem)
    if not problems:
        print("PASS structural checks only; RELEASE HOLD")
    sys.exit(bool(problems))
