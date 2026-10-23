#!/usr/bin/env python3
"""Run 306 F-001 v3 synthetic characterization: 10 regression + 7 editorial + 7 schema."""
import hashlib
import json
from pathlib import Path
import runpy
import sys

HERE = Path(__file__).resolve().parent
V3 = HERE / "PROPOSED-f001-receipt-verify-v3.py"
reg = runpy.run_path(str(HERE / "PROPOSED-f001-test-receipt-v2-regression.py"))
ed = runpy.run_path(str(HERE / "PROPOSED-f001-test-receipt-v2-editorial.py"))
reg["run_case"].__globals__["SCRIPT"] = V3
ed["run_case"].__globals__["SCRIPT"] = V3

def float_lines(root, pin, receipt):
    receipt["editorial"]["flagged_csv_lines"] = [6.0, 7.0]

def float_size(root, pin, receipt):
    receipt["artifacts"]["epub"]["size"] = float(receipt["artifacts"]["epub"]["size"])

def unknown_top(root, pin, receipt):
    receipt["publish"] = "READY"

def wrong_root(root, pin, receipt):
    receipt["environment"]["build_output_realpath"] = str(root.parent)

def bool_size(root, pin, receipt):
    payload = b"x"
    (root / "pdf.bin").write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    pin["artifacts"]["pdf"] = {"sha256": digest, "size": 1}
    receipt["artifacts"]["pdf"].update({"sha256": digest, "size": True})

def duplicate_lines(root, pin, receipt):
    receipt["editorial"]["flagged_csv_lines"] = [6, 6, 7]

def unsorted_lines(root, pin, receipt):
    receipt["editorial"]["flagged_csv_lines"] = [7, 6]

extra = [
    ("Q1_float_lines", float_lines, 1),
    ("Q2_float_size", float_size, 1),
    ("Q4_unknown_top", unknown_top, 1),
    ("Q5_wrong_root", wrong_root, 1),
    ("Q6_bool_size", bool_size, 1),
    ("Q7_duplicate_lines", duplicate_lines, 1),
    ("Q8_unsorted_lines", unsorted_lines, 1),
]
if __name__ == "__main__":
    groups = [
        ("regression", [reg["run_case"](*case) for case in reg["cases"]]),
        ("editorial", [ed["run_case"](*case) for case in ed["cases"]]),
        ("strictness", [reg["run_case"](*case) for case in extra]),
    ]
    summary = {"schema": "f001-v3-tests/v1", "groups": [
        {"group": name, "passed": sum(x["pass"] for x in cases),
         "total": len(cases), "results": cases} for name, cases in groups]}
    summary["passed"] = sum(x["passed"] for x in summary["groups"])
    summary["total"] = sum(x["total"] for x in summary["groups"])
    print(json.dumps(summary, indent=2, sort_keys=True))
    sys.exit(0 if summary["passed"] == summary["total"] else 1)
