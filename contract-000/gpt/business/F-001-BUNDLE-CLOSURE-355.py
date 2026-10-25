#!/usr/bin/env python3
"""F-001 draft bundle-closure preflight; never a publication authorization.

Run 354 verifies pinned manifest and 11 file digests, but not directory
membership. This wrapper refuses unlisted root entries and unsafe link types.
The pre/post snapshots are NOT an atomic snapshot against hostile writers.
Usage: python3 -I -B F-001-BUNDLE-CLOSURE-355.py BUNDLE_DIR MANIFEST_SHA256
"""
import importlib.util
import json
import os
import stat
import sys
from pathlib import Path

EVIDENCE = ("editorial", "rights", "attribution", "independent_rebuild",
            "epubcheck", "ace", "pdf_review", "listing_parity")
EXPECTED = frozenset(("manifest.json", "stage-receipt.json", "ebook.epub",
                      "ebook.pdf") + tuple(n + ".json" for n in EVIDENCE))


def reject(reason):
    raise ValueError(reason)


def snapshot(root):
    """Read-only Linux/POSIX directory-fd membership and inode metadata."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    fd = os.open(root, flags)
    try:
        before = os.fstat(fd)
        names = os.listdir(fd)
        if len(names) != len(EXPECTED) or set(names) != EXPECTED:
            reject("bundle has missing or unlisted root entries")
        rows = []
        for name in sorted(names):
            info = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                reject(name + ": nonregular, symlink, or hardlinked entry")
            rows.append((name, info.st_dev, info.st_ino, info.st_size,
                         info.st_mtime_ns, info.st_ctime_ns, info.st_nlink))
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_mtime_ns,
                before.st_ctime_ns) != (after.st_dev, after.st_ino,
                                        after.st_mtime_ns, after.st_ctime_ns):
            reject("bundle directory changed during enumeration")
        return (after.st_dev, after.st_ino, tuple(rows))
    finally:
        os.close(fd)


def load_base():
    path = Path(__file__).with_name("F-001-BUNDLE-BYTE-VERIFY-354.py")
    spec = importlib.util.spec_from_file_location("f001_byte_verifier_354", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(root, expected_manifest_sha256):
    pre = snapshot(root)
    result = load_base().verify(root, expected_manifest_sha256)
    post = snapshot(root)
    if pre != post:
        reject("bundle membership or metadata changed across verification")
    if (result.get("result") != "BYTE_CONSISTENT_ONLY" or
            result.get("release") != "HOLD" or
            result.get("publication_authorized") is not False or
            result.get("files_hashed") != 11):
        reject("base byte-verifier receipt is not the required HOLD result")
    return {"project": "F-001", "result": "CLOSED_BYTE_CONSISTENT_ONLY",
            "release": "HOLD", "publication_authorized": False,
            "manifest_sha256": result["manifest_sha256"],
            "files_hashed": 11, "root_entries": len(EXPECTED),
            "warning": "Not atomic, trusted provenance, rights, accessibility or release approval"}


def main(argv):
    try:
        if len(argv) != 3:
            reject("usage: closure.py BUNDLE_DIR MANIFEST_SHA256")
        print(json.dumps(verify(argv[1], argv[2]), sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, UnicodeError, AttributeError) as exc:
        print(json.dumps({"project": "F-001", "result": "REJECTED",
                          "release": "HOLD", "publication_authorized": False,
                          "reason": str(exc)[:200]}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
