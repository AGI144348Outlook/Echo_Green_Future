#!/usr/bin/env python3
"""F-001 custody regression harness v561. Prospective test only; NOT EXECUTED.
Requires a new prospective amendment to Issue #234 before running.
Offline, synthetic, disposable directories; no publication authority.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

SCRIPT = pathlib.Path(__file__).with_name("f001_custody_sidecar_draft_557.py")
OID = "a" * 40
EXPECTED = (
    "valid_outside", "existing_output", "inside_output", "nested_inside",
    "symlink_parent_inside", "existing_output_symlink", "relative_output",
    "nonregular_evidence",
)

def invoke(root, out):
    return subprocess.run(
        [sys.executable, "-I", "-B", str(SCRIPT), str(root),
         "--source-commit", OID, "--verifier-blob", OID,
         "--harness-blob", OID, "--out", str(out)],
        capture_output=True, text=True, timeout=15, check=False,
    )

def main():
    observations = {}
    with tempfile.TemporaryDirectory(prefix="f001-561-") as d:
        base = pathlib.Path(d).resolve()
        evidence = base / "evidence"
        evidence.mkdir()
        (evidence / "observation.txt").write_text("synthetic only\n")
        outside = base / "receipt.json"
        good = invoke(evidence, outside)
        try:
            receipt = json.loads(outside.read_text()) if outside.is_file() else {}
        except (ValueError, OSError):
            receipt = {}
        observations["valid_outside"] = (
            good.returncode == 0
            and receipt.get("release_status") == "HOLD"
            and receipt.get("independent_witness") is None
            and len(receipt.get("evidence_files", [])) == 1
        )
        observations["existing_output"] = invoke(evidence, outside).returncode != 0
        observations["inside_output"] = invoke(evidence, evidence / "receipt.json").returncode != 0
        nested = evidence / "nested"
        nested.mkdir()
        observations["nested_inside"] = invoke(evidence, nested / "receipt.json").returncode != 0
        alias = base / "alias"
        alias.symlink_to(evidence, target_is_directory=True)
        observations["symlink_parent_inside"] = invoke(evidence, alias / "receipt.json").returncode != 0
        output_link = base / "outlink.json"
        output_link.symlink_to(outside)
        observations["existing_output_symlink"] = invoke(evidence, output_link).returncode != 0
        observations["relative_output"] = invoke(evidence, pathlib.Path("receipt.json")).returncode != 0
        (evidence / "bad-link").symlink_to(outside)
        observations["nonregular_evidence"] = invoke(evidence, base / "fresh.json").returncode != 0
    complete = set(observations) == set(EXPECTED)
    for name in EXPECTED:
        print(f"{name}: {'PASS' if observations.get(name) is True else 'FAIL'}")
    print(f"coverage: {len(observations)}/{len(EXPECTED)}; complete={complete}")
    return 0 if complete and all(observations.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
