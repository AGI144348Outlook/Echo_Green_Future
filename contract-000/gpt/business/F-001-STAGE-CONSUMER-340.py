#!/usr/bin/env python3
"""F-001 draft read-only stage-consumer check. UNTESTED; NEVER release approval.

Usage:
 python3 -I -B F-001-STAGE-CONSUMER-340.py \
   --gate-stdout captured-current-invocation.stdout \
   --gate-exit 0 --staging-root /private/preexisting/stages

The caller must capture stdout and the OS exit status from the SAME fresh
Run-339 stage-gate invocation. Reusing an old stdout/exit pair is not
detectable here; the coordinator must bind them to its own invocation.
This verifier only checks consistency of one untrusted draft stage.
It cannot approve editorial claims, rights, publication, or payments.
See prospective tests on Echo_Green_Future Issue #53. NOT EXECUTED.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

PIN_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
PIN_A = "b62c970a660e0a6685b58db1ef121690daa4fce7"
PIN_B = "12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4"
PIN_BUILDER_BLOB = "e8af6e5f011ec3e827c94737c717937944924eb8"
EXPECTED_CSV_SHA256 = {
    "dataset-a.csv": "989d83c16568f23a97251d93919068f3a5e726c738644625af909b278f395fdb",
    "dataset-b.csv": "ff442e48acaf00900a3bc3d7900bf987995355a34226b749dbd5b81878e2f7c0",
}
OUTPUTS = ("dataset-a.csv", "dataset-b.csv", "dataset-check.json")
MAX_FILE_BYTES = 5_000_000


def reject(message):
    raise ValueError(message)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            reject("duplicate JSON key: " + key)
        result[key] = value
    return result


def read_json(path, limit):
    data = path.read_bytes()
    if len(data) > limit:
        reject("oversized JSON input: " + path.name)
    value = json.loads(data.decode("utf-8"), object_pairs_hook=unique_pairs)
    if not isinstance(value, dict):
        reject("expected JSON object: " + path.name)
    return value


def canonical_existing_dir(value):
    raw = os.fspath(value)
    if not os.path.isabs(raw) or os.path.normpath(raw) != raw:
        reject("directory must use normalized absolute path")
    if os.path.realpath(raw) != raw:
        reject("symlinked directory or ancestor not allowed")
    path = Path(raw)
    if not path.is_dir():
        reject("directory does not exist")
    return path


def regular_file(path):
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        reject("not a regular file: " + path.name)
    size = path.stat().st_size
    if size > MAX_FILE_BYTES:
        reject("oversized stage file: " + path.name)
    return path.read_bytes()


def verify(stage, report):
    if set(report) != {"status", "stage", "attestation"}:
        reject("gate stdout must contain only its expected three keys")
    if report["status"] != "STAGED_ONLY" or report["attestation"] != "VERIFIED-STAGE.json":
        reject("gate stdout is not a successful stage notice")
    if report["stage"] != str(stage):
        reject("gate stdout stage path differs from selected stage")
    if {p.name for p in stage.iterdir()} != set(OUTPUTS) | {"VERIFIED-STAGE.json"}:
        reject("unexpected/missing stage files or a failure marker")
    marker = read_json(stage / "VERIFIED-STAGE.json", 100_000)
    if (marker.get("project"), marker.get("status"), marker.get("stage"),
            marker.get("source_commit_expected")) != (
            "F-001", "STAGED_ONLY", str(stage), PIN_COMMIT):
        reject("marker identity, status, stage or source commit mismatch")
    expected_inputs = {
        "builder_git_blob": PIN_BUILDER_BLOB,
        "source_commit": PIN_COMMIT,
        "source_a_git_blob": PIN_A,
        "source_b_git_blob": PIN_B,
    }
    for field in ("verified_inputs_before", "verified_inputs_after"):
        if marker.get(field) != expected_inputs:
            reject("source/builder pin evidence mismatch: " + field)
    expected_hashes = marker.get("output_hashes")
    if not isinstance(expected_hashes, dict) or set(expected_hashes) != set(OUTPUTS):
        reject("missing or unexpected output-hash entries")
    for name in OUTPUTS:
        raw = regular_file(stage / name)
        actual = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        if expected_hashes[name] != actual:
            reject("stage file changed since gate attestation: " + name)
        if name in EXPECTED_CSV_SHA256 and actual["sha256"] != EXPECTED_CSV_SHA256[name]:
            reject("CSV does not match independent reference: " + name)
    source_report = read_json(stage / "dataset-check.json", 100_000)
    if source_report.get("source_commit") != PIN_COMMIT:
        reject("dataset-check source commit mismatch")
    records = source_report.get("files")
    if not isinstance(records, dict) or set(records) != {"A", "B"}:
        reject("dataset-check requires exactly A and B records")
    for key, blob, count in (("A", PIN_A, 6), ("B", PIN_B, 8)):
        record = records[key]
        if not isinstance(record, dict) or (record.get("git_blob"), record.get("rows"),
                                           record.get("rejected")) != (blob, count, []):
            reject("dataset-check row/source mismatch: " + key)
    return {name: expected_hashes[name] for name in OUTPUTS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate-stdout", required=True)
    parser.add_argument("--gate-exit", type=int, required=True)
    parser.add_argument("--staging-root", required=True)
    args = parser.parse_args()
    try:
        if args.gate_exit != 0:
            reject("current gate invocation exited nonzero")
        root = canonical_existing_dir(args.staging_root)
        stdout_path = Path(args.gate_stdout)
        if not stdout_path.is_file() or stdout_path.is_symlink():
            reject("captured gate stdout must be an ordinary file")
        report = read_json(stdout_path, 16_384)
        stage_name = report.get("stage")
        if not isinstance(stage_name, str):
            reject("gate stdout missing stage path")
        stage = canonical_existing_dir(stage_name)
        if stage.parent != root or not stage.name.startswith("f001-candidate-"):
            reject("stage is not a direct child of the specified root")
        hashes = verify(stage, report)
        print(json.dumps({"stage_consistency": "PASS", "release": "HOLD",
                          "stage": str(stage), "output_hashes": hashes}, sort_keys=True))
        return 0
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        print(json.dumps({"stage_consistency": "FAIL", "release": "HOLD",
                          "reason": str(exc)[:300]}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
