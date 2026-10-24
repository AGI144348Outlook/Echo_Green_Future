#!/usr/bin/env python3
"""Run 333 prospective local synthetic tests; preregistered Issue #51.
Tests parser/output ordering, NOT source-pin authentication or release readiness.
"""
import contextlib
import csv
import importlib.util
import io
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("candidate", ROOT / "F-001-REBUILD-DATASETS-332.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
# Synthetic fixtures are not the pinned TAM Git clone. Bypass only this boundary
# to isolate and exercise the parser/output ordering. Run 332 tested real pins.
mod.source_pins = lambda _src: {mod.A_FILE: mod.PIN_A_BLOB, mod.B_FILE: mod.PIN_B_BLOB}

A = [
    "Source: Synthetic test fixture, not historical evidence",
    "Object Description Measured Mass (g) Indus Registry Logic (13.7g Base) Calculated Deviation Biblical/Hebrew Term",
    "Object Alpha 136.98g 10.0 Units (UU) -0.01\\% Alpha",
    "Object Beta 68.52g 5.0 Units (U+V) +0.03\\% Beta",
    "Object Gamma 13.71g 1.0 Unit (U) +0.07\\% Gamma",
    "Object Delta 6.86g 0.5 Unit (Half) +0.14\\% Delta",
    "Object Epsilon 3.42g 0.25 Unit (Quarter) -0.03\\% Epsilon",
    "Object Zeta 1.71g 0.125 Unit (Eighth) <0.01\\% Gerah (test term)",
]
B = [
    "This table is a synthetic test fixture.",
    "Ratio Mass (g) Registry Sign Logical Invariant Relation to Dataset A",
    "1 0.85g (Stroke) 1/16 Unit Trace/Gerah Base",
    "2 1.71g (II) 1/8 Unit Synthetic 2",
    "4 3.42g (IIII) 1/4 Unit Synthetic 4",
    "8 6.85g Harrow 1/2 Unit Synthetic 8",
    "16 13.70g Jar (U) 1.00 Unit Synthetic 16",
    "32 27.40g U+II 2.00 Units Synthetic 32",
    "80 68.50g U+V 5.00 Units Synthetic 80",
    "160 137.00g UU 10.0 Units Synthetic 160",
]
tests = []
def record(name, passed, detail):
    tests.append({"case": name, "pass": bool(passed), "observation": detail})

def run_case(name, a_lines, b_lines, expect_success):
    with tempfile.TemporaryDirectory(prefix="f001-333-") as td:
        src = Path(td) / "synthetic-src"
        src.mkdir()
        (src / mod.A_FILE).write_text("\n".join(a_lines) + "\n", encoding="utf-8")
        (src / mod.B_FILE).write_text("\n".join(b_lines) + "\n", encoding="utf-8")
        out = Path(td) / "deliverables"
        error = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                mod.main(src, out)
        except Exception as e:
            error = type(e).__name__ + ": " + str(e)
        exists = out.exists()
        csvs = [p.name for p in out.glob("*.csv")] if exists else []
        success = error is None and exists and len(csvs) == 2 and (out / "dataset-check.json").exists()
        if expect_success:
            record(name, success, "success=" + str(success) + "; error=" + str(error))
        else:
            record(name, error is not None and not exists and not csvs,
                   "error=" + str(error) + "; output_dir=" + str(exists) + "; csvs=" + str(csvs))
        if name == "P0" and success:
            with (out / "dataset-b.csv").open(encoding="utf-8", newline="") as f:
                b = list(csv.DictReader(f))
            with (out / "dataset-a.csv").open(encoding="utf-8", newline="") as f:
                a = list(csv.DictReader(f))
            record("P4", b[0]["expected_g_from_units"] == "0.85625" and
                   a[-1]["stated_deviation_pct"] == "<0.01",
                   "B[0] exact=" + b[0]["expected_g_from_units"] +
                   "; A[-1] stated=" + a[-1]["stated_deviation_pct"])

run_case("P0", A, B, True)
run_case("P1", A, B[:-1], False)
run_case("P2", A + ["this is not a dataset row"], B, False)
run_case("P3", [x.replace("Gerah (test term)", "Unqualified (test term)") for x in A], B, False)
print(json.dumps({"issue": 51, "tests": tests, "passed": sum(t["pass"] for t in tests),
                  "total": len(tests), "source_pins": "stubbed for synthetic fixtures",
                  "release": "HOLD"}, indent=2))
raise SystemExit(0 if len(tests) == 5 and all(t["pass"] for t in tests) else 1)
