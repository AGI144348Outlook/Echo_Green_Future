#!/usr/bin/env python3
"""F-001 offline bundle byte-consistency check, NOT a release or authenticity gate.

Requires a separately recorded SHA-256 pin for manifest.json. If the same
untrusted party chooses the manifest and the pin, the check proves only
internal byte consistency. Never authorizes sale or publication.
Usage: python3 -I -B F-001-BUNDLE-BYTE-VERIFY-354.py BUNDLE_DIR EXPECTED_MANIFEST_SHA256
"""
import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
from pathlib import Path

GATE = Path(__file__).with_name("F-001-PACKAGE-EVIDENCE-GATE-353.py")
spec = importlib.util.spec_from_file_location("f001_shape_gate_353", GATE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

FILES = {
    "stage": ("stage-receipt.json", 1_048_576),
    "epub": ("ebook.epub", 100_000_000),
    "pdf": ("ebook.pdf", 100_000_000),
}
for _name in gate.EVIDENCE:
    FILES[_name] = (_name + ".json", 1_048_576)


def fail(message):
    raise ValueError(message)


def read_regular(root_fd, filename, limit):
    """Hash a fixed basename from a pinned directory fd; refuse symlinks/FIFOs."""
    if filename in ("", ".", "..") or "/" in filename or "\\" in filename:
        fail("invalid fixed basename")
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    fd = os.open(filename, flags, dir_fd=root_fd)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
            fail(filename + ": nonregular or exceeds limit")
        h = hashlib.sha256()
        data = bytearray() if filename == "manifest.json" else None
        count = 0
        while True:
            chunk = os.read(fd, min(65536, limit - count + 1))
            if not chunk:
                break
            count += len(chunk)
            if count > limit:
                fail(filename + ": exceeds limit while reading")
            h.update(chunk)
            if data is not None:
                data.extend(chunk)
        after = os.fstat(fd)
        if (count != before.st_size or count != after.st_size or
                before.st_ino != after.st_ino or
                before.st_dev != after.st_dev or
                before.st_mtime_ns != after.st_mtime_ns):
            fail(filename + ": changed while reading")
        return h.hexdigest(), count, bytes(data) if data is not None else None
    finally:
        os.close(fd)


def verify(root, expected_manifest_sha256):
    gate.digest(expected_manifest_sha256, "external manifest pin")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    root_fd = os.open(root, flags)
    try:
        manifest_hash, _, raw = read_regular(root_fd, "manifest.json", 65_536)
        if manifest_hash != expected_manifest_sha256:
            fail("manifest pin mismatch")
        manifest = json.loads(raw.decode("utf-8"), object_pairs_hook=gate.unique_pairs,
                              parse_constant=lambda x: gate.reject("nonfinite JSON: " + x))
        gate.validate(manifest)  # shape, source/dataset pins, HOLD
        expected = {"stage": manifest["stage"]["receipt_sha256"],
                    "epub": manifest["artifacts"]["epub"]["sha256"],
                    "pdf": manifest["artifacts"]["pdf"]["sha256"]}
        expected.update(manifest["evidence"])
        for key, (filename, cap) in FILES.items():
            actual_hash, actual_size, _ = read_regular(root_fd, filename, cap)
            if actual_hash != expected[key]:
                fail(filename + ": digest mismatch")
            if key in ("epub", "pdf") and actual_size != manifest["artifacts"][key]["bytes"]:
                fail(filename + ": byte size mismatch")
        return {"project": "F-001", "result": "BYTE_CONSISTENT_ONLY",
                "release": "HOLD", "publication_authorized": False,
                "files_hashed": len(FILES), "manifest_sha256": manifest_hash,
                "warning": "Not independent provenance, editorial, rights, a11y or release approval"}
    finally:
        os.close(root_fd)


def main(argv):
    try:
        if len(argv) != 3:
            fail("usage: verifier.py BUNDLE_DIR EXPECTED_MANIFEST_SHA256")
        result = verify(argv[1], argv[2])
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, UnicodeError) as exc:
        print(json.dumps({"project": "F-001", "result": "REJECTED", "release": "HOLD",
                          "publication_authorized": False, "reason": str(exc)[:180]},
                         sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
