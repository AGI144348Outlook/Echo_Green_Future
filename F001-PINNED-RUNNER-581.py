#!/usr/bin/env python3
"""F-001 pinned v579 synthetic test runner. NOT EXECUTED. PRE-TEST Issue #258.

Run only in a local clone containing the pinned Git objects:
  python3 -I -B F001-PINNED-RUNNER-581.py
No network, external API, manuscript, CI, publication or account actions.
Creates an evidence JSON in the working directory; refuses missing/mismatched blobs.
"""
import datetime
import hashlib
import json
import os
import pathlib
import platform
import subprocess
import sys
import tempfile

GATE = "acba01c80431598cde5d1e56dd12f66bb104ad65"
HARNESS = "dc9ae2c37f1852b7dfdc50f37c7b4794dda08967"
ISSUE = "https://github.com/AGI144348Outlook/Echo_Green_Future/issues/258"

def git_blob(sha):
    p = subprocess.run(["git", "cat-file", "-p", sha], capture_output=True)
    if p.returncode:
        raise RuntimeError("pinned Git blob unavailable: " + sha)
    verify = subprocess.run(["git", "hash-object", "--stdin"], input=p.stdout,
                            capture_output=True, check=True)
    if verify.stdout.decode().strip() != sha:
        raise RuntimeError("Git blob mismatch: " + sha)
    return p.stdout

def main():
    gate, harness = git_blob(GATE), git_blob(HARNESS)
    evidence = {
        "pretest_issue": ISSUE, "gate_blob": GATE, "harness_blob": HARNESS,
        "gate_sha256": hashlib.sha256(gate).hexdigest(),
        "harness_sha256": hashlib.sha256(harness).hexdigest(),
        "python": platform.python_version(), "platform": platform.platform(),
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "observations": "raw output; interpretation requires same-thread review"
    }
    with tempfile.TemporaryDirectory(prefix="f001-pinned-") as tmp:
        g, h = pathlib.Path(tmp) / "gate.py", pathlib.Path(tmp) / "harness.py"
        g.write_bytes(gate)
        h.write_bytes(harness)
        run = subprocess.run([sys.executable, "-I", "-B", str(h), str(g)],
                             cwd=tmp, capture_output=True, text=True, timeout=45)
        evidence.update(exit_code=run.returncode, stdout=run.stdout,
                        stderr=run.stderr)
    path = pathlib.Path("F001-V579-OBSERVATIONS-581.json")
    with path.open("x", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("Evidence written:", path, "exit:", evidence["exit_code"])
    print("Post observed results and limitations to Issue #258; do not mark release ready.")
    return evidence["exit_code"]

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print("NOT EXECUTED / FAIL STOP:", exc, file=sys.stderr)
        sys.exit(2)
