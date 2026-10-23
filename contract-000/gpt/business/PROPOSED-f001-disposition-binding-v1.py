#!/usr/bin/env python3
"""F-001 proposal: read-only Dataset A editorial record binding, NOT release authorization.

Exit 0: syntactically complete row-bound record (UNAUTHENTICATED).
Exit 1: invalid CSV or disposition record.
Exit 3: no disposition record / pending editorial action.
Exit 64: incorrect invocation.
Never sets release READY, edits files, or verifies Timothy's authority.
"""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

HEADER = [
    "object", "measured_g", "units", "registry_sign", "stated_deviation_pct",
    "term", "expected_g", "recomputed_deviation_pct", "stated_matches_recomputed",
]
TOP_KEYS = {"record_version", "dataset_a_sha256", "rows", "decision_reference"}
ROW_KEYS = {
    "row_index", "object", "measured_g", "units",
    "stated_deviation_pct", "recomputed_deviation_pct", "disposition", "explanation",
}
BOUND_KEYS = (
    "object", "measured_g", "units", "stated_deviation_pct", "recomputed_deviation_pct",
)
DECISIONS = {"RETAIN_STATED_WITH_DISCLOSURE", "CORRECT_STATED", "EXCLUDE_FROM_EDITION"}


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def report(status, errors, csv_digest=None, record_digest=None, flagged=None):
    print(json.dumps({
        "status": status,
        "binding": "PASS" if status == "RECORDED_UNAUTHENTICATED" else (
            "NOT_EVALUATED" if status == "PENDING" else "FAIL"),
        "source_pin_authenticated": False,
        "decision_reference_authenticated": False,
        "release": "HOLD",
        "dataset_a_sha256": csv_digest,
        "disposition_sha256": record_digest,
        "flagged_row_indices": flagged if flagged is not None else [],
        "errors": errors,
    }, indent=2))


def verify(csv_path, record_path):
    try:
        raw_csv = csv_path.read_bytes()
        csv_digest = hashlib.sha256(raw_csv).hexdigest()
        rows = list(csv.reader(io.StringIO(raw_csv.decode("utf-8-sig"), newline=""), strict=True))
        if not rows or rows[0] != HEADER:
            raise ValueError("Dataset A CSV header mismatch")
        if any(len(row) != len(HEADER) for row in rows[1:]):
            raise ValueError("Dataset A CSV malformed row width")
        if not rows[1:]:
            raise ValueError("Dataset A CSV has no data rows")
        if any(row[-1] not in ("True", "False") for row in rows[1:]):
            raise ValueError("Dataset A CSV has an invalid match flag")
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        report("INVALID", ["Dataset A CSV: " + str(exc)])
        return 1

    flagged = {}
    for index, row in enumerate(rows[1:], 2):
        if row[-1] == "False":
            flagged[index] = dict(zip(HEADER, row))
    indices = sorted(flagged)
    if not record_path.exists():
        report("PENDING", ["editorial record absent"], csv_digest, flagged=indices)
        return 3

    try:
        raw_record = record_path.read_bytes()
        record_digest = hashlib.sha256(raw_record).hexdigest()
        data = json.loads(raw_record.decode("utf-8"), object_pairs_hook=no_duplicate_keys)
        if not isinstance(data, dict) or set(data) != TOP_KEYS:
            raise ValueError("record top-level fields mismatch")
        if type(data["record_version"]) is not int or data["record_version"] != 1:
            raise ValueError("unsupported record version")
        if data["dataset_a_sha256"] != csv_digest:
            raise ValueError("stale Dataset A SHA-256 binding")
        ref = data["decision_reference"]
        if ref is not None and (not isinstance(ref, str) or not ref.strip()):
            raise ValueError("decision reference must be null or nonblank text")
        entries = data["rows"]
        if not isinstance(entries, list):
            raise ValueError("rows must be an array")
        if len(entries) != len(flagged):
            raise ValueError("record must cover exactly the flagged rows")
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != ROW_KEYS:
                raise ValueError("disposition row fields mismatch")
            index = entry["row_index"]
            if type(index) is not int or index not in flagged or index in seen:
                raise ValueError("missing, extra or duplicate flagged row index")
            seen.add(index)
            for key in BOUND_KEYS:
                if not isinstance(entry[key], str) or entry[key] != flagged[index][key]:
                    raise ValueError("row binding mismatch at " + key)
            if entry["disposition"] not in DECISIONS:
                raise ValueError("unrecognized disposition label")
            if not isinstance(entry["explanation"], str) or not entry["explanation"].strip():
                raise ValueError("disposition explanation is missing")
        if seen != set(flagged):
            raise ValueError("incomplete flagged-row coverage")
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        report("INVALID", ["editorial record: " + str(exc)], csv_digest,
               locals().get("record_digest"), indices)
        return 1

    report("RECORDED_UNAUTHENTICATED", [], csv_digest, record_digest, indices)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3 or any(arg.startswith("--") for arg in sys.argv[1:]):
        print("usage: python3 -I -B PROPOSED-f001-disposition-binding-v1.py <dataset-a.csv> <editorial-record.json>",
              file=sys.stderr)
        sys.exit(64)
    sys.exit(verify(Path(sys.argv[1]), Path(sys.argv[2])))
