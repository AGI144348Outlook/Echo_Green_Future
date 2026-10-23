#!/usr/bin/env python3
"""Synthetic-only offline characterization of proposed F-001 disposition parser v1."""
import copy
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

GATE = Path(__file__).with_name("PROPOSED-f001-disposition-binding-v1.py")
HEADER = [
    "object", "measured_g", "units", "registry_sign", "stated_deviation_pct",
    "term", "expected_g", "recomputed_deviation_pct", "stated_matches_recomputed",
]
ROWS = [
    ["Synthetic Silver", "13.68", "1", "A", "-0.03", "test", "13.70", "-0.146", "False"],
    ["Synthetic Scrap", "6.84", "0.5", "B", "<0.01", "test", "6.85", "-0.146", "False"],
    ["Synthetic Control", "27.40", "2", "C", "0", "test", "27.40", "0", "True"],
]
DECISION = "RETAIN_STATED_WITH_DISCLOSURE"


def csv_bytes(header=HEADER, rows=ROWS):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def record_for(raw):
    rows = []
    for index, row in enumerate(ROWS, 2):
        if row[-1] == "False":
            rows.append({
                "row_index": index, "object": row[0], "measured_g": row[1],
                "units": row[2], "stated_deviation_pct": row[4],
                "recomputed_deviation_pct": row[7], "disposition": DECISION,
                "explanation": "Synthetic characterization, not Timothy approval.",
            })
    return {
        "record_version": 1,
        "dataset_a_sha256": hashlib.sha256(raw).hexdigest(),
        "rows": rows,
        "decision_reference": None,
    }


def exercise(name, modifier, expected_code, expected_status):
    with tempfile.TemporaryDirectory() as directory:
        folder = Path(directory)
        csv_path, json_path = folder / "dataset-a.csv", folder / "editorial-record.json"
        raw = csv_bytes()
        record = record_for(raw)
        write_record = True
        raw_override = None
        if modifier:
            raw, record, write_record, raw_override = modifier(raw, record)
        csv_path.write_bytes(raw)
        if write_record:
            json_path.write_bytes(raw_override if raw_override is not None
                                  else json.dumps(record, ensure_ascii=False).encode("utf-8"))
        before = hashlib.sha256(csv_path.read_bytes()).hexdigest()
        record_before = hashlib.sha256(json_path.read_bytes()).hexdigest() if json_path.exists() else None
        proc = subprocess.run(
            [sys.executable, "-I", "-B", str(GATE), str(csv_path), str(json_path)],
            capture_output=True, text=True, check=False,
        )
        if proc.returncode != expected_code:
            raise AssertionError(f"{name}: exit {proc.returncode} != {expected_code}: {proc.stderr} {proc.stdout}")
        output = json.loads(proc.stdout)
        if output["status"] != expected_status or output["release"] != "HOLD":
            raise AssertionError(f"{name}: wrong statuses {output}")
        if output["source_pin_authenticated"] or output["decision_reference_authenticated"]:
            raise AssertionError(f"{name}: unauthorized authentication claim")
        if before != hashlib.sha256(csv_path.read_bytes()).hexdigest():
            raise AssertionError(f"{name}: CSV was mutated")
        if record_before != (hashlib.sha256(json_path.read_bytes()).hexdigest() if json_path.exists() else None):
            raise AssertionError(f"{name}: disposition record was mutated")
        print(f"PASS {name}: exit {proc.returncode}, status={output['status']}, release=HOLD")


def change_record(raw, record, key, value):
    record = copy.deepcopy(record)
    record["rows"][0][key] = value
    return raw, record, True, None


def missing(raw, record):
    return raw, record, False, None


def with_reference(raw, record):
    record["decision_reference"] = "unverified synthetic reference"
    return raw, record, True, None


def stale_csv(raw, record):
    return raw.replace(b"13.68", b"13.69"), record, True, None


def missing_row(raw, record):
    record["rows"].pop()
    return raw, record, True, None


def duplicate_row(raw, record):
    record["rows"][1] = copy.deepcopy(record["rows"][0])
    return raw, record, True, None


def extra_row(raw, record):
    record["rows"].append(copy.deepcopy(record["rows"][0]))
    return raw, record, True, None


def unknown_field(raw, record):
    record["approved"] = True
    return raw, record, True, None


def invalid_header(raw, record):
    return raw.replace(b"object,measured_g", b"object,wrong_mass"), record, True, None


def invalid_flag(raw, record):
    return raw.replace(b",False", b",MAYBE", 1), record, True, None


def malformed_json(raw, record):
    return raw, record, True, b"{invalid-json"


def duplicate_json_key(raw, record):
    return raw, record, True, b'{"record_version":1,"record_version":1}'


CASES = [
    ("complete_record_is_not_authorization", None, 0, "RECORDED_UNAUTHENTICATED"),
    ("complete_with_untrusted_reference", with_reference, 0, "RECORDED_UNAUTHENTICATED"),
    ("record_missing", missing, 3, "PENDING"),
    ("stale_csv_digest", stale_csv, 1, "INVALID"),
    ("missing_flagged_row", missing_row, 1, "INVALID"),
    ("duplicate_row_index", duplicate_row, 1, "INVALID"),
    ("extra_row", extra_row, 1, "INVALID"),
    ("unknown_approval_field", unknown_field, 1, "INVALID"),
    ("wrong_bound_mass", lambda a, b: change_record(a, b, "measured_g", "999"), 1, "INVALID"),
    ("blank_explanation", lambda a, b: change_record(a, b, "explanation", " "), 1, "INVALID"),
    ("unknown_disposition", lambda a, b: change_record(a, b, "disposition", "PUBLISH"), 1, "INVALID"),
    ("invalid_csv_header", invalid_header, 1, "INVALID"),
    ("invalid_match_flag", invalid_flag, 1, "INVALID"),
    ("malformed_json", malformed_json, 1, "INVALID"),
    ("duplicate_json_key", duplicate_json_key, 1, "INVALID"),
]


def main():
    if not GATE.is_file():
        raise RuntimeError(f"missing gate: {GATE}")
    for name, modifier, expected_code, expected_status in CASES:
        exercise(name, modifier, expected_code, expected_status)
    proc = subprocess.run([sys.executable, "-I", "-B", str(GATE)], capture_output=True, text=True)
    assert proc.returncode == 64, f"usage case: {proc.returncode}"
    print("PASS invalid_invocation: exit 64")
    print(f"RESULT: {len(CASES) + 1}/{len(CASES) + 1} expected outcomes")


if __name__ == "__main__":
    main()
