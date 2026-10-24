#!/usr/bin/env python3
"""Run 334 prospective Issue #52 tests: synthetic X4 and real pinned TAM X1/parity.
Not a release or rights approval.
"""
import contextlib
import csv
import importlib.util
import io
import json
import tempfile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("candidate", ROOT / "F-001-REBUILD-DATASETS-334.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
# Synthetic fixtures are not the pinned TAM Git clone. Bypass only this boundary
# to isolate and exercise the parser/output ordering. Run 332 tested real pins.
real_source_pins = mod.source_pins
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

# New prospective X4 destination controls (all temp synthetic files).
def make_fixture(td, bad_b=False):
    src = Path(td) / "src"
    src.mkdir()
    (src / mod.A_FILE).write_text("\n".join(A) + "\n", encoding="utf-8")
    (src / mod.B_FILE).write_text("\n".join(B[:-1] if bad_b else B) + "\n", encoding="utf-8")
    return src

def call(src, out):
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            mod.main(src, out)
        return None
    except Exception as exc:
        return type(exc).__name__ + ": " + str(exc)

with tempfile.TemporaryDirectory(prefix="f001-334-") as td:
    src = make_fixture(td)
    out = Path(td) / "existing-empty"
    out.mkdir()
    err = call(src, out)
    record("X4-empty-dir", err is None and all((out / f).exists() for f in
           ("dataset-a.csv", "dataset-b.csv", "dataset-check.json")), "error=" + str(err))
    originals = {p.name: p.read_bytes() for p in out.iterdir()}
    err = call(src, out)
    unchanged = {p.name: p.read_bytes() for p in out.iterdir()} == originals
    record("X4-valid-rerun", bool(err and "nonempty" in err and unchanged),
           "error=" + str(err) + "; old_files_remain=" + str(unchanged))
    bad = Path(td) / "bad-src"
    bad.mkdir()
    (bad / mod.A_FILE).write_text("\n".join(A) + "\n", encoding="utf-8")
    (bad / mod.B_FILE).write_text("\n".join(B[:-1]) + "\n", encoding="utf-8")
    err = call(bad, out)
    unchanged = {p.name: p.read_bytes() for p in out.iterdir()} == originals
    record("X4-bad-rerun", bool(err and "nonempty" in err and unchanged),
           "error=" + str(err) + "; stale_files_still_present=" + str(unchanged))
    fresh = Path(td) / "bad-fresh"
    err = call(bad, fresh)
    record("X4-bad-fresh", bool(err and not fresh.exists()), "error=" + str(err))
    file_out = Path(td) / "output-is-file"
    file_out.write_text("sentinel", encoding="utf-8")
    err = call(src, file_out)
    record("X4-file-destination", bool(err and "non-directory" in err and
           file_out.read_text(encoding="utf-8") == "sentinel"), "error=" + str(err))

# Source-pinned parity and skip-worktree control; clone prepared by workflow.
if len(sys.argv) != 2:
    raise SystemExit("Usage: F-001-TEST-RUN334.py <clean-tam-clone-at-pin>")
tam = Path(sys.argv[1]).resolve()
mod.source_pins = real_source_pins
old_spec = importlib.util.spec_from_file_location("previous", ROOT / "F-001-REBUILD-DATASETS-332.py")
old = importlib.util.module_from_spec(old_spec)
old_spec.loader.exec_module(old)
with tempfile.TemporaryDirectory(prefix="f001-334-pinned-") as td:
    out_new, out_old = Path(td) / "new", Path(td) / "old"
    err_new, err_old = call(tam, out_new), None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            old.main(tam, out_old)
    except Exception as exc:
        err_old = type(exc).__name__ + ": " + str(exc)
    files = ("dataset-a.csv", "dataset-b.csv", "dataset-check.json")
    parity = err_new is None and err_old is None and all(
        (out_new / f).read_bytes() == (out_old / f).read_bytes() for f in files)
    record("PIN-parity", parity, "new=" + str(err_new) + "; old=" + str(err_old) +
           "; equal=" + str(parity))
    if err_new is None:
        with (out_new / "dataset-b.csv").open(encoding="utf-8", newline="") as f:
            b = list(csv.DictReader(f))
        with (out_new / "dataset-a.csv").open(encoding="utf-8", newline="") as f:
            a = list(csv.DictReader(f))
        record("PIN-precision", b[0]["expected_g_from_units"] == "0.85625" and
               a[-1]["stated_deviation_pct"] == "<0.01",
               "exact=" + b[0]["expected_g_from_units"] + "; stated=" + a[-1]["stated_deviation_pct"])
    else:
        record("PIN-precision", False, "source-pinned build failed")
    subprocess.run(["git", "-C", str(tam), "update-index", "--skip-worktree", mod.B_FILE],
                   check=True, capture_output=True, text=True)
    b_path = tam / mod.B_FILE
    before = b_path.read_bytes()
    if b"0.85g" not in before:
        record("X1-hidden-byte", False, "fixture token absent; control not executed")
    else:
        b_path.write_bytes(before.replace(b"0.85g", b"0.86g", 1))
        status = subprocess.run(["git", "-C", str(tam), "status", "--porcelain"],
                                check=True, capture_output=True, text=True).stdout.strip()
        tampered_out = Path(td) / "hidden-out"
        err = call(tam, tampered_out)
        record("X1-hidden-byte", status == "" and bool(err and "blob mismatch" in err)
               and not tampered_out.exists(), "status_empty=" + str(status == "") +
               "; error=" + str(err))

print(json.dumps({"issue": 52, "tests": tests, "passed": sum(t["pass"] for t in tests),
                  "total": len(tests), "source_pins": "stubbed for synthetic fixtures",
                  "release": "HOLD"}, indent=2))
raise SystemExit(0 if len(tests) == 13 and all(t["pass"] for t in tests) else 1)
