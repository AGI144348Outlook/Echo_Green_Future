#!/usr/bin/env python3
"""F-001 review-only gate for the shared *legacy* 9/8-column dataset rebuild.

Not the pinned Run334 11/9-column stage and never publication authorization.
Usage: python f001_legacy_dataset_preflight_375.py <output-directory>
Read-only; refuses incomplete rows, rejected parses, stale or malformed CSVs.
"""
import csv
import json
import sys
from pathlib import Path

SCHEMA = {
    "A": ("dataset-a.csv", ("object", "measured_g", "units", "registry_sign",
          "stated_deviation_pct", "term", "expected_g", "recomputed_deviation_pct",
          "stated_matches_recomputed"), 6),
    "B": ("dataset-b.csv", ("ratio", "mass_g", "registry_sign", "units",
          "relation_to_dataset_a", "expected_g_from_units", "deviation_pct",
          "ratio_over_16_equals_units"), 8),
}


def inspect(folder):
    folder = Path(folder)
    errors = []
    report_path = folder / "dataset-check.json"
    if report_path.is_symlink() or not report_path.is_file():
        return ["missing or symlinked dataset-check.json"]
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        return [f"unreadable report: {type(exc).__name__}"]
    if not isinstance(report, dict) or not isinstance(report.get("files"), dict):
        return ["malformed report files object"]
    if report.get("not_written_zero_rows"):
        errors.append("builder refused at least one zero-row CSV")
    for key, (name, header, count) in SCHEMA.items():
        meta = report["files"].get(key)
        if not isinstance(meta, dict):
            errors.append(f"{key}: missing report record")
            continue
        if type(meta.get("rows")) is not int or meta["rows"] != count:
            errors.append(f"{key}: report row count is not {count}")
        if meta.get("rejected") != []:
            errors.append(f"{key}: rejected rows not empty")
        path = folder / name
        if path.is_symlink() or not path.is_file():
            errors.append(f"{key}: missing or symlinked CSV")
            continue
        try:
            with path.open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                actual_header = next(reader, None)
                rows = list(reader)
        except (OSError, UnicodeError, csv.Error) as exc:
            errors.append(f"{key}: unreadable CSV: {type(exc).__name__}")
            continue
        if actual_header != list(header):
            errors.append(f"{key}: unexpected header")
        if len(rows) != count:
            errors.append(f"{key}: CSV row count is not {count}")
        if any(len(row) != len(header) for row in rows):
            errors.append(f"{key}: inconsistent row width")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: preflight.py <output-directory>")
    problems = inspect(sys.argv[1])
    print(json.dumps({"status": "HOLD" if problems else "REVIEW_ONLY_PASS",
                      "release_authorized": False, "errors": problems}, indent=2))
    sys.exit(1 if problems else 0)
