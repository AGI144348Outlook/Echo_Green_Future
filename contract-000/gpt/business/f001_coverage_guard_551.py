#!/usr/bin/env python3
"""F-001 prospective Issue #224 coverage guard; NOT EXECUTED.
Runs pinned 15-case harness and refuses false-green when cases are skipped.
Does not authenticate artifacts or authorize release.
"""
import pathlib
import subprocess
import sys

EXPECTED = (
    "valid", "missing_manifest", "missing_required", "extra_file",
    "omitted_entry", "duplicate_entry", "altered_digest", "symlink_artifact",
    "malformed_line", "symlink_root", "extra_symlink", "extra_directory",
    "extra_fifo", "newline_filename", "co_modified_manifest"
)

def main():
    if len(sys.argv) != 3:
        print("usage: coverage_guard.py /absolute/harness.py /absolute/verifier.py", file=sys.stderr)
        return 2
    harness = pathlib.Path(sys.argv[1]).resolve(strict=True)
    verifier = pathlib.Path(sys.argv[2]).resolve(strict=True)
    run = subprocess.run([sys.executable, str(harness), str(verifier)],
                         capture_output=True, text=True)
    sys.stdout.write(run.stdout)
    sys.stderr.write(run.stderr)
    observed = {}
    for line in run.stdout.splitlines():
        for case in EXPECTED:
            if line.startswith(case + " "):
                observed.setdefault(case, []).append(line)
    missing = [case for case in EXPECTED if case not in observed]
    duplicates = [case for case, rows in observed.items() if len(rows) != 1]
    skipped = [case for case, rows in observed.items()
               if any("SKIP" in row for row in rows)]
    failed = [case for case, rows in observed.items()
              if not any(row.startswith(case + " PASS ") for row in rows)]
    print("COVERAGE: expected=15 observed=%d missing=%r duplicates=%r skipped=%r failed=%r"
          % (len(observed), missing, duplicates, skipped, failed))
    if run.returncode or missing or duplicates or skipped or failed:
        print("COVERAGE INCOMPLETE OR FAIL; RELEASE HOLD")
        return 1
    print("SYNTHETIC CASE COVERAGE COMPLETE; NOT AUTHENTICATED; RELEASE HOLD")
    return 0

if __name__ == "__main__":
    sys.exit(main())
