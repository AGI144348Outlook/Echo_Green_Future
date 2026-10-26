#!/usr/bin/env python3
"""F-001 HOLD-only claim-ledger/source binding preflight (GPT Run 377).

Usage: python3 -I f001_claims_binding_377.py SOURCE_DIR SCAN_OUTPUT_DIR
Read-only; accepts only a structurally complete claim_scan.py worksheet, never
attests claim truth, manuscript inclusion, ownership, or publication readiness.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

FILES = ["README.md", "Article 1 Hacksilber", "Article 2 Water Weight Computes",
         "The Color Dyed and Dental Records", "Article 5", "Article 6",
         "Article 10", "Collective information"]
TRIGGERS = {
    "certainty": r"\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\b",
    "percent": r"\d+(\.\d+)?\s?%",
    "accuracy": r"\b(accura(te|cy)|precision|precise(ly)?|correlat(es|ed|ion))\b",
    "superlative": r"\b(only|exactly|always|never|impossible)\b",
}
HEADER = ["file", "sentence_no", "triggers", "sentence", "status"]
DONE = {"claimed", "inferred", "test", "cut", "sourced"}


def scan_rows(raw, filename):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}",
                  raw.decode("utf-8", "replace")) if s.strip()]
    rows = []
    for i, sentence in enumerate(sentences, 1):
        hits = [name for name, rx in TRIGGERS.items()
                if re.search(rx, sentence, re.I)]
        if hits:
            rows.append({"file": filename, "sentence_no": str(i),
                         "triggers": ";".join(hits), "sentence": sentence})
    return rows


def check(src, out):
    src, out = Path(src), Path(out)
    errors, expected, hashes = [], [], {}
    per_file, per_trigger = {}, Counter()
    for name in FILES:
        p = src / name
        if p.is_symlink() or not p.is_file():
            errors.append(f"source missing, nonfile or symlink: {name}")
            continue
        raw = p.read_bytes()
        hashes[name] = hashlib.sha256(raw).hexdigest()
        found = scan_rows(raw, name)
        expected.extend(found)
        per_file[name] = len(found)
        for row in found:
            per_trigger.update(row["triggers"].split(";"))
    rep_path, csv_path = out / "claims-report.json", out / "claims.csv"
    report, rows = None, []
    if rep_path.is_symlink() or not rep_path.is_file():
        errors.append("missing or symlinked claims-report.json")
    else:
        try:
            report = json.loads(rep_path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError, OSError) as exc:
            errors.append(f"unreadable claims-report.json: {type(exc).__name__}")
    if csv_path.is_symlink() or not csv_path.is_file():
        errors.append("missing or symlinked claims.csv")
    else:
        try:
            with csv_path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                if reader.fieldnames != HEADER:
                    errors.append("claim CSV header mismatch")
                rows = list(reader)
        except (UnicodeError, csv.Error, OSError) as exc:
            errors.append(f"unreadable claims.csv: {type(exc).__name__}")
    if report is not None:
        if not isinstance(report, dict):
            errors.append("report must be an object")
        else:
            if report.get("source_files") != hashes:
                errors.append("report source SHA-256 mismatch or incomplete source set")
            if report.get("per_file") != per_file:
                errors.append("report per-file counts mismatch")
            if report.get("per_trigger") != dict(per_trigger):
                errors.append("report trigger counts mismatch")
            if report.get("rows") != len(expected):
                errors.append("report total count mismatch")
    if len(rows) != len(expected):
        errors.append(f"claim row count mismatch: actual={len(rows)} expected={len(expected)}")
    for i, (row, want) in enumerate(zip(rows, expected), 1):
        if any(row.get(k) != want[k] for k in want):
            errors.append(f"claim row {i} differs from source candidate")
        if (row.get("status") or "").strip().lower() not in DONE:
            errors.append(f"claim row {i} has open/invalid status")
        if None in row:
            errors.append(f"claim row {i} has extra CSV columns")
    return {"project": "F-001", "status": "HOLD",
            "structurally_reviewable": not errors, "release_authorized": False,
            "source_count": len(hashes), "candidate_count": len(expected),
            "errors": errors}


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    result = check(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["structurally_reviewable"] else 1)


if __name__ == "__main__":
    main()
