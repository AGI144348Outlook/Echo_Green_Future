#!/usr/bin/env python3
"""F-001 Run 350 draft stage session with verified private script snapshots. UNTESTED; release always HOLD.

Launches one pinned Run-344 gate process, captures *its actual* exit/stdout,
requires exactly one stage absent before invocation, then launches the pinned
Run-347 read-only consumer against that same capture. Unlike Run-340 alone,
the operator cannot supply an old successful stdout/exit pair.

Usage (all paths absolute; staging root must already exist):
  python3 -I -B F-001-STAGE-SESSION-349.py \
    --source /path/to/pinned-tam-clone \
    --builder /path/to/F-001-REBUILD-DATASETS-332.py \
    --root /private/stages \
    --gate /path/to/F-001-DATASET-STAGE-GATE-344.py \
    --consumer /path/to/F-001-STAGE-CONSUMER-347.py

Draft source only. Prospective tests: Echo_Green_Future Issue #53 (Run 349, pretest comment 6398566090).
Run 350: validate exact HOLD receipt schema, propagate staged output hashes and provenance.\nRun 349: snapshot pinned gate and consumer in a fresh private directory.
Run 348: integrate Run 347 bounded descriptor consumer; Run 346 POSIX child process groups and selector-driven stdout/stderr draining;
reject over-limit output while child runs; kill same-session descendants.
This is NOT a quota on stage-file writes or hostile-filesystem isolation.
No release, account, spending, outreach or publication capability.
"""
import argparse
import hashlib
import json
import os
import signal
import selectors
import time
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

PIN_GATE_BLOB = "5d5bb8f85db7f21c50ca71625e82c51102fed088"
PIN_CONSUMER_BLOB = "b2a97390ba39959cd2f86a5e51ea186348f31fb2"
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


def pin_script_bytes(value, expected, label):
    """Read and hash one bounded POSIX descriptor, never later execute its path."""
    raw = os.fspath(value)
    if not os.path.isabs(raw) or os.path.normpath(raw) != raw:
        reject(label + " must be normalized and absolute")
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        reject("POSIX O_NOFOLLOW is required")
    if os.path.realpath(raw) != raw:
        reject(label + " uses a symlink or symlinked ancestor")
    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    fd = os.open(raw, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            reject(label + " is not a regular file")
        if before.st_size > 500_000:
            reject(label + " exceeds script size bound")
        parts = bytearray()
        while True:
            chunk = os.read(fd, min(65_536, 500_001 - len(parts)))
            if not chunk:
                break
            parts.extend(chunk)
            if len(parts) > 500_000:
                reject(label + " exceeds script size bound during read")
        after = os.fstat(fd)
        if any(getattr(before, field) != getattr(after, field) for field in
               ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")):
            reject(label + " changed while being read")
        if len(parts) != after.st_size:
            reject(label + " changed length while being read")
    finally:
        os.close(fd)
    data = bytes(parts)
    digest = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") +
                          b"\x00" + data).hexdigest()
    if digest != expected:
        reject(label + " Git blob differs from independently pinned draft")
    return data


def write_private_script(root, name, data):
    """Write validated bytes exclusively into a fresh private 0700 directory."""
    path = root / name
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(path, 0o400)
    return path


def stage_names(root):
    # Names only; never follow stage symlinks when discovering candidates.
    return {entry.name for entry in os.scandir(root)
            if entry.name.startswith(PREFIX)}


def kill_process_group(pid):
    """Best-effort cleanup of subprocess descendants in this POSIX session.

    A child may exit while a grandchild survives with inherited descriptors.
    Group isolation is required before using killpg. This is not a guarantee
    against children that deliberately detach into a different session.
    """
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_checked(argv, timeout):
    """Run a pinned child with incremental, per-stream bounded pipe capture.

    Each pipe is drained while the child runs, so a flood cannot fill a
    TemporaryFile before the limit is checked. This bounds captured output,
    NOT files the child writes elsewhere or descendants that detach sessions.
    """
    if os.name != "posix":
        reject("stage session requires POSIX process-group isolation")
    proc = subprocess.Popen(
        argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, start_new_session=True, bufsize=0)
    out, err = bytearray(), bytearray()
    deadline = time.monotonic() + timeout
    sel = selectors.DefaultSelector()
    sel.register(proc.stdout, selectors.EVENT_READ, out)
    sel.register(proc.stderr, selectors.EVENT_READ, err)
    try:
        while sel.get_map():
            # If the leader exits, close its process group before waiting
            # for pipe EOF; descendants may otherwise hold the pipe open.
            if proc.poll() is not None:
                kill_process_group(proc.pid)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(argv, timeout)
            for key, _ in sel.select(min(0.2, remaining)):
                chunk = os.read(key.fileobj.fileno(), 8192)
                if chunk:
                    if len(key.data) + len(chunk) > MAX_CAPTURE:
                        reject("child output exceeds per-stream capture bound")
                    key.data.extend(chunk)
                else:
                    sel.unregister(key.fileobj)
                    key.fileobj.close()
        remaining = deadline - time.monotonic()
        if proc.poll() is None and remaining <= 0:
            raise subprocess.TimeoutExpired(argv, timeout)
        code = proc.wait(timeout=max(0.001, remaining))
        return subprocess.CompletedProcess(argv, code, bytes(out), bytes(err))
    finally:
        sel.close()
        kill_process_group(proc.pid)
        if proc.poll() is None:
            proc.wait(timeout=2)
        if proc.stdout is not None and not proc.stdout.closed:
            proc.stdout.close()
        if proc.stderr is not None and not proc.stderr.closed:
            proc.stderr.close()


# These independent coordinator pins are intentionally redundant with the
# already-verified consumer: they reject unexpected receipt schema drift.
PIN_SOURCE_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
EXPECTED_CSV_SHA256 = {
    "dataset-a.csv": "989d83c16568f23a97251d93919068f3a5e726c738644625af909b278f395fdb",
    "dataset-b.csv": "ff442e48acaf00900a3bc3d7900bf987995355a34226b749dbd5b81878e2f7c0",
}
EXPECTED_OUTPUTS = frozenset(("dataset-a.csv", "dataset-b.csv", "dataset-check.json"))


def validate_receipt_shape(receipt, stage):
    """Validate the pinned consumer's exact HOLD schema before stage-only handoff.

    This is not an independent file read or release authorization: consumer 347
    has already verified bytes and hashes. The caller rejects schema drift.
    """
    if not isinstance(receipt, dict) or set(receipt) != {
            "stage_consistency", "release", "stage", "output_hashes"}:
        reject("consumer receipt has missing or unexpected keys")
    if (receipt["stage_consistency"] != "PASS" or
            receipt["release"] != "HOLD" or
            receipt["stage"] != stage):
        reject("consumer receipt identity/status mismatch")
    outputs = receipt["output_hashes"]
    if not isinstance(outputs, dict) or set(outputs) != EXPECTED_OUTPUTS:
        reject("consumer receipt has missing or unexpected outputs")
    for name, record in outputs.items():
        if not isinstance(record, dict) or set(record) != {"sha256", "bytes"}:
            reject("consumer output record schema mismatch: " + name)
        digest, size = record["sha256"], record["bytes"]
        if (not isinstance(digest, str) or len(digest) != 64 or
                any(ch not in "0123456789abcdef" for ch in digest)):
            reject("consumer output digest invalid: " + name)
        if type(size) is not int or size <= 0 or size > 5_000_000:
            reject("consumer output size invalid: " + name)
        if name in EXPECTED_CSV_SHA256 and digest != EXPECTED_CSV_SHA256[name]:
            reject("consumer CSV pin mismatch: " + name)
    return outputs


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
        gate_bytes = pin_script_bytes(args.gate, PIN_GATE_BLOB, "gate")
        consumer_bytes = pin_script_bytes(args.consumer, PIN_CONSUMER_BLOB, "consumer")
        with tempfile.TemporaryDirectory(prefix="f001-pinned-scripts-") as private_dir:
            private_root = Path(private_dir)
            gate = write_private_script(private_root, "gate.py", gate_bytes)
            consumer = write_private_script(private_root, "consumer.py", consumer_bytes)
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
            verified_hashes = validate_receipt_shape(receipt, str(stage))
            print(json.dumps({"session": "CONSISTENT_CURRENT_INVOCATION",
                              "receipt_type": "STAGING_ONLY",
                              "release": "HOLD", "stage": str(stage),
                              "source_commit_expected": PIN_SOURCE_COMMIT,
                              "pinned_gate_git_blob": PIN_GATE_BLOB,
                              "pinned_consumer_git_blob": PIN_CONSUMER_BLOB,
                              "verified_output_hashes": verified_hashes,
                              "gate_exit": gate_run.returncode,
                              "consumer_exit": check.returncode,
                              "note": "not a release receipt; rights/editorial/packaging still HOLD"},
                             sort_keys=True))
            return 0
    except (OSError, UnicodeError, ValueError, TypeError,
            subprocess.TimeoutExpired) as exc:
        print(json.dumps({"session": "REJECTED", "release": "HOLD",
                          "reason": str(exc)[:400]}, sort_keys=True),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
