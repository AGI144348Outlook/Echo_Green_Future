#!/usr/bin/env python3
"""F-001 Run 341 draft caller-owned stage session. UNTESTED; release always HOLD.

Launches one pinned Run-339 gate process, captures *its actual* exit/stdout,
requires exactly one stage absent before invocation, then launches the pinned
Run-340 read-only consumer against that same capture. Unlike Run-340 alone,
the operator cannot supply an old successful stdout/exit pair.

Usage (all paths absolute; staging root must already exist):
  python3 -I -B F-001-STAGE-SESSION-341.py \
    --source /path/to/pinned-tam-clone \
    --builder /path/to/F-001-REBUILD-DATASETS-332.py \
    --root /private/stages \
    --gate /path/to/F-001-DATASET-STAGE-GATE-339.py \
    --consumer /path/to/F-001-STAGE-CONSUMER-340.py

Draft source only. No tests executed. Prospective plan: Echo_Green_Future #53.
No release, account, spending, outreach or publication capability.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

PIN_GATE_BLOB = "25f0130b9dd92bcc175ed6191a467fd75cc45856"
PIN_CONSUMER_BLOB = "ebbef366599c8eaa62a4f031b5a985ae765c6c54"
PREFIX = "f001-candidate-"
GATE_TIMEOUT = 180
CONSUMER_TIMEOUT = 60
MAX_CAPTURE = 16_384


def reject(reason):
    raise ValueError(reason)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            reject("duplicate JSON key: " + key)
        result[key] = value
    return result


def decode_json_object(data, label):
    if len(data) > MAX_CAPTURE:
        reject(label + " exceeds capture limit")
    value = json.loads(data.decode("utf-8"), object_pairs_hook=unique_pairs)
    if not isinstance(value, dict):
        reject(label + " is not a JSON object")
    return value


def canonical_root(value):
    raw = os.fspath(value)
    if not os.path.isabs(raw) or os.path.normpath(raw) != raw:
        reject("staging root must be normalized and absolute")
    if os.path.realpath(raw) != raw:
        reject("staging root or ancestor uses a symlink")
    root = Path(raw)
    if not root.is_dir():
        reject("staging root does not exist")
    return root


def pin_script(value, expected, label):
    raw = os.fspath(value)
    if not os.path.isabs(raw) or os.path.normpath(raw) != raw:
        reject(label + " must be normalized and absolute")
    if os.path.realpath(raw) != raw:
        reject(label + " uses a symlink or symlinked ancestor")
    path = Path(raw)
    if not stat.S_ISREG(path.lstat().st_mode):
        reject(label + " is not a regular file")
    data = path.read_bytes()
    if len(data) > 500_000:
        reject(label + " exceeds script size bound")
    digest = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") +
                          b"\\x00" + data).hexdigest()
    if digest != expected:
        reject(label + " Git blob differs from independently pinned draft")
    return path


def stage_names(root):
    # Names only; never follow stage symlinks when discovering candidates.
    return {entry.name for entry in os.scandir(root)
            if entry.name.startswith(PREFIX)}


def run_checked(argv, timeout):
    return subprocess.run(argv, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=timeout, check=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--builder", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--gate", required=True)
    parser.add_argument("--consumer", required=True)
    args = parser.parse_args()
    try:
        root = canonical_root(args.root)
        gate = pin_script(args.gate, PIN_GATE_BLOB, "gate")
        consumer = pin_script(args.consumer, PIN_CONSUMER_BLOB, "consumer")
        # Builder/source pins are checked by the gate itself; this caller
        # independently pins the gate and consumer scripts it is executing.
        before = stage_names(root)
        gate_run = run_checked([sys.executable, "-I", "-B", str(gate),
                                args.source, args.builder, str(root)],
                               GATE_TIMEOUT)
        after = stage_names(root)
        created = after - before
        if gate_run.returncode != 0:
            reject("fresh gate process exited nonzero: " +
                   str(gate_run.returncode))
        if len(created) != 1:
            reject("expected exactly one newly created stage, got " +
                   str(len(created)))
        name = next(iter(created))
        stage = root / name
        if not stat.S_ISDIR(stage.lstat().st_mode):
            reject("new stage is not a real directory")
        notice = decode_json_object(gate_run.stdout, "fresh gate stdout")
        if (set(notice) != {"status", "stage", "attestation"} or
                notice["status"] != "STAGED_ONLY" or
                notice["stage"] != str(stage) or
                notice["attestation"] != "VERIFIED-STAGE.json"):
            reject("fresh gate stdout does not identify new stage")

        # Only a private, freshly captured stdout file is handed to consumer.
        # Never accept --gate-stdout or --gate-exit from an external caller.
        with tempfile.TemporaryDirectory(prefix="f001-current-call-") as td:
            capture = Path(td) / "gate.stdout"
            capture.write_bytes(gate_run.stdout)
            check = run_checked([sys.executable, "-I", "-B", str(consumer),
                                 "--gate-stdout", str(capture),
                                 "--gate-exit", str(gate_run.returncode),
                                 "--staging-root", str(root)], CONSUMER_TIMEOUT)
        if check.returncode != 0:
            reject("pinned stage consumer rejected fresh stage")
        receipt = decode_json_object(check.stdout, "consumer stdout")
        if (receipt.get("stage_consistency") != "PASS" or
                receipt.get("release") != "HOLD" or
                receipt.get("stage") != str(stage) or
                not isinstance(receipt.get("output_hashes"), dict)):
            reject("consumer returned inconsistent stage report")
        print(json.dumps({"session": "CONSISTENT_CURRENT_INVOCATION",
                          "release": "HOLD", "stage": str(stage),
                          "gate_exit": gate_run.returncode,
                          "consumer_exit": check.returncode,
                          "note": "not a release receipt"}, sort_keys=True))
        return 0
    except (OSError, UnicodeError, ValueError, TypeError,
            subprocess.TimeoutExpired) as exc:
        print(json.dumps({"session": "REJECTED", "release": "HOLD",
                          "reason": str(exc)[:400]}, sort_keys=True),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
