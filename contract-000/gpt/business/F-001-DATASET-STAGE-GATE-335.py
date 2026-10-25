#!/usr/bin/env python3
"""F-001 draft unique-stage gate. UNTESTED; not a release or publication tool.

Usage:
  python3 -I -B F-001-DATASET-STAGE-GATE-335.py \
      <pinned-tam-clone> <run334-builder.py> <existing-staging-root>

Each invocation creates a fresh stage. Success is recorded only after a
zero-exit builder and structural/digest verification. A failed attempt
leaves a failure record, never a success attestation. Do not treat a stage
as an approved final EPUB/PDF/CSV package. Pre-test: Echo_Green_Future #53.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

PIN_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
PIN_A = "b62c970a660e0a6685b58db1ef121690daa4fce7"
PIN_B = "12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4"
OUTPUTS = ("dataset-a.csv", "dataset-b.csv", "dataset-check.json")
TIMEOUT_SECONDS = 120


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_marker(stage, name, payload):
    """Replace a marker only within this unique stage, after full JSON encoding."""
    data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    temporary = stage / ("." + name + ".tmp")
    with temporary.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, stage / name)


def inspect_stage(stage):
    names = {p.name for p in stage.iterdir()}
    if names != set(OUTPUTS):
        raise ValueError("expected exactly three output files; got " + repr(sorted(names)))
    if any(not (stage / n).is_file() for n in OUTPUTS):
        raise ValueError("an expected output is not a regular file")
    report = json.loads((stage / "dataset-check.json").read_text(encoding="utf-8"))
    if report.get("source_commit") != PIN_COMMIT:
        raise ValueError("source commit mismatch in builder report")
    files = report.get("files", {})
    for key, blob, count in (("A", PIN_A, 6), ("B", PIN_B, 8)):
        rec = files.get(key, {})
        if rec.get("git_blob") != blob or rec.get("rows") != count or rec.get("rejected") != []:
            raise ValueError("pinned dataset report failed for " + key)
    return {name: {"sha256": sha256(stage / name),
                   "bytes": (stage / name).stat().st_size} for name in OUTPUTS}


def main(argv):
    if len(argv) != 4:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    source, builder, root = (Path(p).resolve() for p in argv[1:])
    if not source.is_dir() or not builder.is_file() or not root.is_dir():
        print("source, builder and pre-existing staging root are required", file=sys.stderr)
        return 2
    if root == source or source in root.parents or root == builder.parent:
        print("staging root overlaps protected source/builder", file=sys.stderr)
        return 2
    stage = Path(tempfile.mkdtemp(prefix="f001-candidate-", dir=root))
    start = datetime.now(timezone.utc).isoformat()
    base = {"project": "F-001", "stage": str(stage), "started_utc": start,
            "builder_sha256": sha256(builder), "source_commit_expected": PIN_COMMIT,
            "status": "UNQUALIFIED"}
    try:
        child = subprocess.run(
            [sys.executable, "-I", "-B", str(builder), str(source), str(stage)],
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False)
        base["child_exit_code"] = child.returncode
        if child.returncode != 0:
            raise RuntimeError("builder returned nonzero exit: " + str(child.returncode))
        hashes = inspect_stage(stage)
        base.update(status="STAGED_ONLY", output_hashes=hashes,
                    finished_utc=datetime.now(timezone.utc).isoformat())
        write_marker(stage, "VERIFIED-STAGE.json", base)
        print(json.dumps({"status": "STAGED_ONLY", "stage": str(stage),
                          "attestation": "VERIFIED-STAGE.json"}, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired,
            json.JSONDecodeError) as exc:
        base.update(status="FAILED", error_type=type(exc).__name__,
                    error=str(exc)[:400],
                    finished_utc=datetime.now(timezone.utc).isoformat())
        try:
            write_marker(stage, "FAILED-STAGE.json", base)
        except OSError as write_error:
            print("could not persist failure marker: " + str(write_error), file=sys.stderr)
        print(json.dumps({"status": "FAILED", "stage": str(stage),
                          "reason": base["error"]}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
