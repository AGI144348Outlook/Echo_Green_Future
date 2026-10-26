#!/usr/bin/env python3
"""Bounded synthetic characterization of the exact original F-001 claim_scan.py.
Usage: python test_f001_claim_scan_380.py <path-to-claim_scan.py>
No TAM text is bundled, no editorial status is approved.
"""
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PIN = "31f3dcff486c4c8cc96d514eb425da86834d00c3"

def run(scanner):
    raw = Path(scanner).read_bytes()
    sha = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    if sha != PIN:
        raise ValueError(f"Original scanner Git blob mismatch: {sha} != {PIN}")
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        src, out = root / "src", root / "out"
        src.mkdir()
        (src / "README.md").write_text(
            "We demonstrated the ratio.\n\n"
            "We are demonstrating the ratio.\n\n"
            "Measured 2.5% deviation.\n\n"
            "Measured 2.5\\% deviation.\n\n"
            "It is exactly aligned.\n", encoding="utf-8")
        proc = subprocess.run([sys.executable, "-I", str(scanner), str(src), str(out)],
                              text=True, capture_output=True)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr)
        report = json.loads((out / "claims-report.json").read_text())
        with (out / "claims.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        texts = [r["sentence"] for r in rows]
        nested = subprocess.run([sys.executable, "-I", str(scanner), str(src), str(src / "nested")],
                                text=True, capture_output=True)
        checks = {
            "exact_source_git_blob": sha == PIN,
            "process_exits_zero_with_missing_seven_files": proc.returncode == 0,
            "report_missing_files_as_null": sum(x is None for x in report["source_files"].values()) == 7,
            "plain_demonstrated_recognized": any("demonstrated" in x for x in texts),
            "demonstrating_not_recognized": not any("demonstrating" in x for x in texts),
            "plain_percent_recognized": any("Measured 2.5% deviation" in x for x in texts),
            "escaped_percent_not_recognized": not any("Measured 2.5\\% deviation" in x for x in texts),
            "exactly_recognized": any("exactly aligned" in x for x in texts),
            "all_statuses_blank": all(not r["status"] for r in rows),
            "only_three_candidate_rows": len(rows) == 3,
            "report_row_count_matches_csv": report["rows"] == len(rows),
            "refuses_output_inside_source": nested.returncode != 0 and
                                           "refusing" in (nested.stdout + nested.stderr),
        }
        print(json.dumps({"scanner_blob_sha": sha, "checks": checks,
                          "passed": sum(checks.values()), "total": len(checks),
                          "candidate_sentences": texts,
                          "limitations": "synthetic fixture, not original TAM source replay"}, indent=2))
        return all(checks.values())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raise SystemExit(0 if run(Path(sys.argv[1]).resolve()) else 1)
