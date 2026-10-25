#!/usr/bin/env python3
"""Synthetic F-001 package manifest gate tests, preregistered Issue #53 comment 6401236705."""
import copy
import importlib.util
import json
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("F-001-PACKAGE-EVIDENCE-GATE-353.py")
spec = importlib.util.spec_from_file_location("f001_package_gate_353", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

h = "a" * 64
base = {
    "schema": "F-001-PACKAGE-EVIDENCE-v1", "project": "F-001",
    "release": "HOLD", "authorization": "NOT_GRANTED",
    "book_id": "urn:uuid:12345678-1234-4234-8234-123456789abc",
    "stage": {"receipt_sha256": h, "source_commit": gate.SOURCE,
              "release": "HOLD", "receipt_type": "STAGING_ONLY",
              "csv_sha256": gate.CSV.copy()},
    "artifacts": {"epub": {"sha256": h, "bytes": 1000},
                  "pdf": {"sha256": h, "bytes": 1200}},
    "evidence": {key: h for key in gate.EVIDENCE},
}

cases = [
    ("valid_review_only", lambda x: None, True),
    ("ready_release", lambda x: x.update(release="READY"), False),
    ("granted_authorization", lambda x: x.update(authorization="GRANTED"), False),
    ("wrong_project", lambda x: x.update(project="F-002"), False),
    ("extra_field", lambda x: x.update(approved=True), False),
    ("missing_field", lambda x: x.pop("evidence"), False),
    ("missing_pdf", lambda x: x["artifacts"].pop("pdf"), False),
    ("bad_hash", lambda x: x["artifacts"]["epub"].update(sha256="z" * 64), False),
    ("uppercase_hash", lambda x: x["evidence"].update(rights="A" * 64), False),
    ("bool_size", lambda x: x["artifacts"]["pdf"].update(bytes=True), False),
    ("zero_size", lambda x: x["artifacts"]["pdf"].update(bytes=0), False),
    ("oversize", lambda x: x["artifacts"]["pdf"].update(bytes=100_000_001), False),
    ("wrong_source", lambda x: x["stage"].update(source_commit="0" * 40), False),
    ("wrong_csv_pin", lambda x: x["stage"]["csv_sha256"].update({"dataset-a.csv": h}), False),
    ("stage_ready", lambda x: x["stage"].update(release="READY"), False),
    ("missing_rights_evidence", lambda x: x["evidence"].pop("rights"), False),
    ("placeholder_rights_evidence", lambda x: x["evidence"].update(rights="PENDING"), False),
    ("noncanonical_book_id", lambda x: x.update(book_id="12345678-1234-4234-8234-123456789abc"), False),
]
results = []
for name, change, should_accept in cases:
    obj = copy.deepcopy(base)
    change(obj)
    try:
        output = gate.validate(obj)
        accepted = output["result"] == "STRUCTURE_VALID_ONLY" and output["release"] == "HOLD" and output["publication_authorized"] is False
    except (ValueError, TypeError):
        accepted = False
    results.append({"case": name, "pass": accepted == should_accept, "accepted": accepted})
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / "manifest.json"
    path.write_text('{"project":"F-001","project":"F-001"}')
    try:
        gate.load(path)
        duplicate_rejected = False
    except ValueError:
        duplicate_rejected = True
    results.append({"case": "duplicate_json_key", "pass": duplicate_rejected, "accepted": not duplicate_rejected})
    path.write_text('{"x":NaN}')
    try:
        gate.load(path)
        nan_rejected = False
    except ValueError:
        nan_rejected = True
    results.append({"case": "nonfinite_json", "pass": nan_rejected, "accepted": not nan_rejected})
    path.write_bytes(b" " * 65_537)
    try:
        gate.load(path)
        oversized_rejected = False
    except ValueError:
        oversized_rejected = True
    results.append({"case": "oversized_manifest", "pass": oversized_rejected, "accepted": not oversized_rejected})
print(json.dumps({"project": "F-001", "release": "HOLD", "passed": sum(x["pass"] for x in results), "total": len(results), "results": results}, sort_keys=True))
raise SystemExit(0 if all(x["pass"] for x in results) else 1)
