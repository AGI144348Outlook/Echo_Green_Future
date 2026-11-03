#!/usr/bin/env python3
"""F-001 draft_557 custody containment regression harness. NOT YET EXECUTED.
Run only after prospective amendment to GitHub Issue #234. Offline stdlib.
No publication authority. Each case uses disposable temporary directories.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

SCRIPT = pathlib.Path(__file__).with_name("f001_custody_sidecar_draft_557.py")
OID = "a" * 40

def invoke(root, out):
    return subprocess.run(
        [sys.executable, "-I", str(SCRIPT), str(root),
         "--source-commit", OID, "--verifier-blob", OID,
         "--harness-blob", OID, "--out", str(out)],
        capture_output=True, text=True, timeout=15)

def main():
    cases = {}
    with tempfile.TemporaryDirectory(prefix="f001-558-") as d:
        base = pathlib.Path(d).resolve()
        evidence = base / "evidence"
        evidence.mkdir()
        (evidence / "observation.txt").write_text("synthetic only\n")
        outside = base / "receipt.json"
        good = invoke(evidence, outside)
        cases["valid_outside"] = (good.returncode == 0 and outside.is_file()
                                  and json.loads(outside.read_text())["release_status"] == "HOLD")
        cases["existing_output"] = invoke(evidence, outside).returncode != 0
        cases["inside_output"] = invoke(evidence, evidence / "receipt.json").returncode != 0
        nested = evidence / "nested"
        nested.mkdir()
        cases["nested_inside"] = invoke(evidence, nested / "receipt.json").returncode != 0
        alias = base / "alias"
        alias.symlink_to(evidence, target_is_directory=True)
        cases["symlink_parent_inside"] = invoke(evidence, alias / "receipt.json").returncode != 0
        output_link = base / "outlink.json"
        output_link.symlink_to(outside)
        cases["existing_output_symlink"] = invoke(evidence, output_link).returncode != 0
        cases["relative_output"] = invoke(evidence, pathlib.Path("receipt.json")).returncode != 0
        (evidence / "bad-link").symlink_to(outside)
        cases["nonregular_evidence"] = invoke(evidence, base / "fresh.json").returncode != 0
    expected = {"valid_outside", "existing_output", "inside_output", "nested_inside",
                "symlink_parent_inside", "existing_output_symlink", "relative_output",
                "nonregular_evidence"}
    assert set(cases) == expected
    for name, ok in cases.items():
        print(f"{name}: {'PASS' if ok else 'FAIL'}")
    return 0 if all(cases.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
