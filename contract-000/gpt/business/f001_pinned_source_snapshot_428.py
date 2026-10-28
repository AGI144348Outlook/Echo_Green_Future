#!/usr/bin/env python3
"""F-001 HOLD-only source snapshot gate (GPT proposal, Run428).

Validate all eight source files against Git blob SHA-1 pins from public
The-TAM-protocol commit d46456a18fe412398d0ae37ec5a8c4eebb44e0c9.
Only after ALL pass, stage immutable-by-convention copies in a NEW scratch
folder outside the source tree. The original claim_scan.py may be run against
this snapshot, writing its worksheet to another separate directory.

Not a secure multi-user filesystem transaction, rights clearance, or release
approval. Requires a trusted local parent directory; no GitHub network calls.
Usage: python3 -I -B f001_pinned_source_snapshot_428.py SRC NEW_SNAPSHOT
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile

SOURCE_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
PINS = {
    "README.md": "213bcfaf560dcc54fbb7ae79fad932e86b660357",
    "Article 1 Hacksilber": "237bd3335abdcc0f0465817dffe01ad6eaa86055",
    "Article 2 Water Weight Computes": "ec657c3fa0f70da9686fb1ae52983d28f77c6c4c",
    "The Color Dyed and Dental Records": "b525ad60ab37cb2d72ea43c40ba687b0fe2a348d",
    "Article 5": "c8c1bf617c0d81389f6c2408ed975131695857ff",
    "Article 6": "662d745f0b9b41236d1053cdbaa9351f7c020dd0",
    "Article 10": "e82be564872f636662652d34dcb8d3437559f84f",
    "Collective information": "710ad3cd4feeae7bafa329d7437a78df4c40cfa8",
}


def blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def no_symlink_components(path):
    path = Path(os.path.abspath(path))
    for item in (path, *path.parents):
        if item.is_symlink():
            raise ValueError(f"symlink path component forbidden: {item}")
    return path


def snapshot(src, dst, *, pins=None):
    pins = PINS if pins is None else pins  # override only for isolated tests, never CLI
    src = no_symlink_components(src)
    dst = no_symlink_components(dst)
    if not src.is_dir():
        raise ValueError("source must be a directory")
    if not dst.parent.is_dir():
        raise ValueError("snapshot parent must already exist")
    if dst.exists() or dst.is_symlink():
        raise ValueError("snapshot destination already exists")
    if src == dst or src in dst.parents or dst in src.parents:
        raise ValueError("snapshot and source must not contain one another")
    if not pins or len(pins) != len(set(pins)):
        raise ValueError("invalid pin set")
    payloads, hashes = {}, {}
    for name, pin in pins.items():
        if Path(name).name != name or name in (".", ".."):
            raise ValueError("pin names must be flat filenames")
        p = src / name
        if p.is_symlink():
            raise ValueError(f"source symlink forbidden: {name}")
        try:
            mode = p.stat(follow_symlinks=False).st_mode
        except FileNotFoundError:
            raise ValueError(f"required source missing: {name}") from None
        if not stat.S_ISREG(mode):
            raise ValueError(f"source not a regular file: {name}")
        raw = p.read_bytes()
        if not raw:
            raise ValueError(f"empty source: {name}")
        try:
            raw.decode("utf-8", "strict")
        except UnicodeDecodeError:
            raise ValueError(f"invalid UTF-8: {name}") from None
        actual = blob_sha1(raw)
        if actual != pin:
            raise ValueError(f"Git blob mismatch for {name}: {actual} != {pin}")
        payloads[name] = raw
        hashes[name] = {"git_blob": actual, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    stage = Path(tempfile.mkdtemp(prefix=".f001-hold-", dir=dst.parent))
    try:
        for name, raw in payloads.items():
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            fd = os.open(stage / name, flags, 0o600)
            with os.fdopen(fd, "wb") as f:
                f.write(raw)
                f.flush()
                os.fsync(f.fileno())
        receipt = {"status": "PREPARED_HOLD", "source_commit": SOURCE_COMMIT,
                   "files": hashes, "release_authorized": False}
        with open(stage / "SOURCE-SNAPSHOT-RECEIPT.json", "x", encoding="utf-8") as f:
            json.dump(receipt, f, sort_keys=True, indent=2)
            f.flush()
            os.fsync(f.fileno())
        # This is for a trusted local scratch parent, not hostile concurrent writers.
        if dst.exists() or dst.is_symlink():
            raise ValueError("destination appeared while staging")
        os.rename(stage, dst)
        return receipt
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        receipt = snapshot(argv[1], argv[2])
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
