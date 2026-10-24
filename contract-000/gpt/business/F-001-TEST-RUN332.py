#!/usr/bin/env python3
"""Prospective F-001 Run 332 isolated tests; Issue #50 published before execution.
Only public TAM sources; no writes to any repository; temporary output only.
"""
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PIN = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
ROOT = Path(__file__).resolve().parent
BUILDER = ROOT / "F-001-REBUILD-DATASETS-332.py"
CHECKER = ROOT / "F-001-CSV-PIN-CHECK-332.py"
BFILE = "Dataset_B_Binary_Matrix.md"
results = []

def run(*args):
    return subprocess.run(list(map(str, args)), capture_output=True, text=True)

def check(name, condition, detail=""):
    results.append({"name": name, "pass": bool(condition), "detail": str(detail)[:500]})

def rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

with tempfile.TemporaryDirectory(prefix="f001-run332-") as temp:
    tmp = Path(temp)
    clone, out = tmp / "tam", tmp / "delivery"
    c = run("git", "clone", "--quiet", "https://github.com/AGI144348Outlook/The-TAM-protocol.git", clone)
    check("clone public TAM", c.returncode == 0, c.stderr)
    if c.returncode == 0:
        co = run("git", "-C", clone, "checkout", "--quiet", PIN)
        check("checkout pinned commit", co.returncode == 0, co.stderr)
        if co.returncode == 0:
            build = run(sys.executable, "-I", "-B", BUILDER, clone, out)
            check("builder exits 0", build.returncode == 0, build.stderr)
            if build.returncode == 0:
                a, b = rows(out / "dataset-a.csv"), rows(out / "dataset-b.csv")
                report = json.loads((out / "dataset-check.json").read_text(encoding="utf-8"))
                check("A 6 B 8 zero rejected", len(a) == 6 and len(b) == 8 and
                      all(report["files"][k]["rejected"] == [] for k in ("A", "B")))
                check("pinned source SHA and commit", report["source_commit"] == PIN and
                      report["files"]["A"]["git_blob"] == "b62c970a660e0a6685b58db1ef121690daa4fce7" and
                      report["files"]["B"]["git_blob"] == "12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4")
                check("B 1/16 exact finite decimal", b[0]["expected_g_from_units"] == "0.85625" and b[0]["mass_g"] == "0.85",
                      b[0]["expected_g_from_units"])
                check("A source inequality preserved", a[-1]["stated_deviation_pct"] == "<0.01")
                check("A method remains unknown", all(r["calculation_method_from_source"] == "UNKNOWN" for r in a))
                check("A tolerance label is explicit", "within_0_01_pct_points_of_recomputed" in a[0] and
                      "stated_matches_recomputed" not in a[0])
                check("exactly two Gerah flags", [i for i, r in enumerate(a) if r["terminology_conflict"]] == [5] and
                      [i for i, r in enumerate(b) if r["terminology_conflict"]] == [0])
                ok = run(sys.executable, "-I", "-B", CHECKER, clone, PIN, out)
                check("existing pin checker extended and passes", ok.returncode == 0, ok.stderr + ok.stdout[:500])
                wrong = run(sys.executable, "-I", "-B", CHECKER, clone, "deadbeef", out)
                check("wrong pin denied", wrong.returncode != 0, wrong.stdout[:500])
                with (out / "dataset-a.csv").open("a", encoding="utf-8") as f:
                    f.write("\n")
                tampered_delivery = run(sys.executable, "-I", "-B", CHECKER, clone, PIN, out)
                check("altered delivered CSV denied", tampered_delivery.returncode != 0, tampered_delivery.stdout[:500])
                tamperclone = tmp / "tam-mutated"
                shutil.copytree(clone, tamperclone)
                source = tamperclone / BFILE
                source.write_bytes(source.read_bytes().replace(b"0.85g", b"0.86g", 1))
                mutated = run(sys.executable, "-I", "-B", BUILDER, tamperclone, tmp / "bad-source-output")
                check("mutated source denied before output", mutated.returncode != 0 and
                      not (tmp / "bad-source-output" / "dataset-a.csv").exists(), mutated.stderr[:500])
                missingclone = tmp / "tam-missing"
                shutil.copytree(clone, missingclone)
                (missingclone / BFILE).unlink()
                missing = run(sys.executable, "-I", "-B", BUILDER, missingclone, tmp / "missing-output")
                check("missing source denied", missing.returncode != 0, missing.stderr[:500])
                check("builder invalid args denied", run(sys.executable, "-I", "-B", BUILDER).returncode != 0)
                check("checker invalid args denied", run(sys.executable, "-I", "-B", CHECKER).returncode != 0)
                status = run("git", "-C", clone, "status", "--porcelain")
                check("pinned source clone unchanged", status.returncode == 0 and not status.stdout.strip())
print(json.dumps({"pretest_issue": 50, "tests": results, "passed": sum(x["pass"] for x in results),
                  "total": len(results)}, indent=2))
sys.exit(0 if results and all(x["pass"] for x in results) else 1)
