#!/usr/bin/env python3
"""F-001 proposal: read-only, pinned v5 report consistency gate. NEVER release approval.

Checks a locally pinned v5 script, exact Dataset A bytes, a stored v5 JSON report,
and fresh v5 output against the same inputs. User-supplied hashes are NOT trusted
publication authority. Exit 0 consistent/HOLD; 1 inconsistent/HOLD; 64 usage.
The audited v5 script blob is fixed here to avoid executing arbitrary caller code.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

EXPECTED_V5_GIT_BLOB = "f8c2b4b29f9fffb1bc3d65f4f1fdf56954b7a4f0"
MAX_SCRIPT = 1_048_576
MAX_REPORT = 1_048_576
MAX_CSV = 1_048_576
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
REPORT_KEYS = {"status", "binding", "source_pin_authenticated",
               "decision_reference_authenticated", "release", "dataset_a_sha256",
               "disposition_sha256", "flagged_csv_lines", "errors"}


def read_regular(path, limit):
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("not a regular file: " + str(path))
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(limit + 1)
        if len(data) > limit:
            raise ValueError("input exceeds byte limit: " + str(path))
        return data
    finally:
        os.close(fd)


def no_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key: " + key)
        obj[key] = value
    return obj


def no_constant(value):
    raise ValueError("nonfinite JSON constant: " + value)


def parse_report(raw):
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicate_keys,
                      parse_constant=no_constant)
    if not isinstance(data, dict) or set(data) != REPORT_KEYS:
        raise ValueError("v5 report schema mismatch")
    return data


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify(args):
    issues = []
    result = {"schema": "f001-v5-report-gate/v1", "integrity": "FAIL",
              "release": "HOLD", "source_pin_authenticated": False,
              "approval_authenticated": False, "publication_authorization": "ABSENT",
              "dataset_a_sha256": None, "v5_report_sha256": None,
              "v5_status": None, "flagged_csv_lines": [], "issues": issues}
    try:
        if not isinstance(args.expected_dataset_sha256, str) or not HEX64.fullmatch(args.expected_dataset_sha256):
            raise ValueError("expected Dataset A SHA-256 must be lowercase hex")
        if not HEX64.fullmatch(args.expected_report_sha256):
            raise ValueError("expected v5 report SHA-256 must be lowercase hex")
        script = read_regular(args.v5_script, MAX_SCRIPT)
        if git_blob_sha(script) != EXPECTED_V5_GIT_BLOB:
            raise ValueError("v5 script differs from fixed reviewed Git blob")
        csv_bytes = read_regular(args.dataset_a, MAX_CSV)
        csv_sha = hashlib.sha256(csv_bytes).hexdigest()
        result["dataset_a_sha256"] = csv_sha
        if csv_sha != args.expected_dataset_sha256:
            raise ValueError("Dataset A differs from pinned SHA-256")
        report_bytes = read_regular(args.report_json, MAX_REPORT)
        report_sha = hashlib.sha256(report_bytes).hexdigest()
        result["v5_report_sha256"] = report_sha
        if report_sha != args.expected_report_sha256:
            raise ValueError("stored v5 report differs from pinned SHA-256")
        saved = parse_report(report_bytes)
        proc = subprocess.run([sys.executable, "-I", "-B", str(args.v5_script.resolve()),
                               str(args.dataset_a.resolve()), str(args.disposition_record), csv_sha],
                              stdin=subprocess.DEVNULL, capture_output=True, timeout=5,
                              check=False)
        if len(proc.stdout) > MAX_REPORT or len(proc.stderr) > 8192:
            raise ValueError("v5 output exceeds bound")
        if proc.returncode not in (0, 3):
            raise ValueError("v5 failed validation, exit " + str(proc.returncode))
        observed = parse_report(proc.stdout)
        if observed != saved:
            raise ValueError("stored v5 report differs from freshly computed v5 result")
        if observed["release"] != "HOLD" or observed["source_pin_authenticated"] is not False or observed["decision_reference_authenticated"] is not False:
            raise ValueError("v5 report asserts release or authentication")
        if observed["dataset_a_sha256"] != csv_sha:
            raise ValueError("v5 report not bound to Dataset A bytes")
        lines = observed["flagged_csv_lines"]
        if (not isinstance(lines, list) or any(type(x) is not int for x in lines)
                or lines != [6, 7]):
            raise ValueError("actual F-001 Dataset A flags must be exactly CSV lines 6 and 7")
        if (proc.returncode == 3 and (observed["status"] != "PENDING" or observed["binding"] != "NOT_EVALUATED")):
            raise ValueError("pending report has inconsistent status")
        if (proc.returncode == 0 and (observed["status"] != "RECORDED_UNAUTHENTICATED" or observed["binding"] != "PASS")):
            raise ValueError("recorded report has inconsistent status")
        # Detect input mutation during verification. This is not a concurrent-swap proof.
        if (read_regular(args.v5_script, MAX_SCRIPT) != script or
            read_regular(args.dataset_a, MAX_CSV) != csv_bytes or
            read_regular(args.report_json, MAX_REPORT) != report_bytes):
            raise ValueError("an input changed during verification")
        result["v5_status"] = observed["status"]
        result["flagged_csv_lines"] = lines
        result["integrity"] = "PASS"
    except (OSError, ValueError, TypeError, UnicodeError, json.JSONDecodeError,
            subprocess.TimeoutExpired, RecursionError) as exc:
        issues.append(str(exc))
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset-a", required=True, type=Path)
    p.add_argument("--disposition-record", required=True, type=Path)
    p.add_argument("--v5-script", required=True, type=Path)
    p.add_argument("--report-json", required=True, type=Path)
    p.add_argument("--expected-dataset-sha256", required=True)
    p.add_argument("--expected-report-sha256", required=True)
    args = p.parse_args(argv)
    result = verify(args)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["integrity"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
