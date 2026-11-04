#!/usr/bin/env python3
"""F-001 v579 offline pinned runner, revision 583. NOT EXECUTED.
Pre-test: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/258
Usage: python3 -I -B F001-PINNED-RUNNER-583.py --repo /path/to/clone --evidence /path/to/new.json
Requires a local Git clone with the pinned objects; never fetches from network.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import platform
import subprocess
import sys
import tempfile

GATE = "acba01c80431598cde5d1e56dd12f66bb104ad65"
HARNESS = "dc9ae2c37f1852b7dfdc50f37c7b4794dda08967"
ISSUE = "https://github.com/AGI144348Outlook/Echo_Green_Future/issues/258"

def git_blob(repo, sha):
    # -C removes dependence on the caller's working directory.
    p = subprocess.run(["git", "-C", str(repo), "cat-file", "blob", sha],
                       capture_output=True, check=False, timeout=15)
    if p.returncode:
        raise RuntimeError("missing pinned Git blob " + sha)
    verify = subprocess.run(["git", "-C", str(repo), "hash-object", "--stdin"],
                            input=p.stdout, capture_output=True, check=True, timeout=15)
    if verify.stdout.decode("ascii").strip() != sha:
        raise RuntimeError("Git blob identity mismatch " + sha)
    return p.stdout

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=pathlib.Path, required=True)
    ap.add_argument("--evidence", type=pathlib.Path, required=True)
    args = ap.parse_args()
    repo = args.repo.resolve(strict=True)
    if not repo.is_dir():
        raise RuntimeError("repository path is not a directory")
    # Ensure this path resolves to a Git worktree. This is not a provenance
    # guarantee; pinned blob identity below is the actual source gate.
    check = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, timeout=15)
    if check.returncode:
        raise RuntimeError("repository path is not a Git worktree")
    gate, harness = git_blob(repo, GATE), git_blob(repo, HARNESS)
    evidence = {
        "pretest_issue": ISSUE, "gate_blob": GATE, "harness_blob": HARNESS,
        "gate_sha256": hashlib.sha256(gate).hexdigest(),
        "harness_sha256": hashlib.sha256(harness).hexdigest(),
        "python": platform.python_version(), "platform": platform.platform(),
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "observations": "raw execution output; requires same-thread interpretation",
    }
    with tempfile.TemporaryDirectory(prefix="f001-pinned-") as tmp:
        g, h = pathlib.Path(tmp) / "gate.py", pathlib.Path(tmp) / "harness.py"
        g.write_bytes(gate)
        h.write_bytes(harness)
        try:
            run = subprocess.run([sys.executable, "-I", "-B", str(h), str(g)],
                                 cwd=tmp, capture_output=True, text=True, timeout=45)
            evidence.update(exit_code=run.returncode, stdout=run.stdout, stderr=run.stderr,
                            timed_out=False)
        except subprocess.TimeoutExpired as exc:
            evidence.update(exit_code=None, stdout=repr(exc.stdout),
                            stderr=repr(exc.stderr), timed_out=True)
    # Exclusive creation: never overwrite prior evidence, even on a failed test.
    with args.evidence.open("x", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("Evidence:", args.evidence, "exit:", evidence["exit_code"])
    print("Post actual observations to Issue #258; this does not authorize release.")
    return 124 if evidence["timed_out"] else evidence["exit_code"]

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print("FAIL STOP (no completed test evidence):", exc, file=sys.stderr)
        sys.exit(2)
