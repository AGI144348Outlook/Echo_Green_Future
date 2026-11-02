#!/usr/bin/env python3
"""F-001 candidate: stricter offline flat evidence manifest verifier. UNTESTED.
Verifies internal consistency only, never authenticity or publication readiness.
"""
import hashlib
import pathlib
import re
import sys

REQUIRED = {"README.txt", "checkout-path.txt", "checkout-head.txt",
            "start-utc.txt", "end-utc.txt", "verdict.txt",
            "orchestrator-exit-status.txt", "preflight.stdout",
            "preflight.stderr", "preflight-exit-status.txt"}
LINE = re.compile(r"^([0-9a-fA-F]{64}) ([ *])(.+)$")

def main(argv):
    if len(argv) != 2:
        print("usage: verifier /absolute/evidence/directory", file=sys.stderr)
        return 2
    root = pathlib.Path(argv[1])
    if not root.is_absolute() or root.is_symlink() or not root.is_dir():
        print("HOLD: invalid evidence root", file=sys.stderr)
        return 2
    # Reject *all* unlisted types, including symlinks, subdirectories, and
    # special files. Run546 silently excluded symlinked extras from 'actual'.
    children = list(root.iterdir())
    for p in children:
        if p.is_symlink() or not p.is_file() or "\n" in p.name or "\r" in p.name:
            print("HOLD: unsafe evidence entry: " + repr(p.name), file=sys.stderr)
            return 3
    names = {p.name for p in children}
    if "SHA256SUMS" not in names or not REQUIRED <= names:
        print("HOLD: missing manifest or mandatory evidence", file=sys.stderr)
        return 4
    actual = names - {"SHA256SUMS"}
    entries = {}
    try:
        lines = (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        for line in lines:
            m = LINE.fullmatch(line)
            if not m:
                raise ValueError("malformed line")
            digest, _, name = m.groups()
            if name in ("", ".", "..") or "/" in name or "\\" in name or name in entries:
                raise ValueError("unsafe or duplicate name")
            entries[name] = digest.lower()
        if set(entries) != actual:
            raise ValueError("file-set mismatch")
        for name, expected in entries.items():
            p = root / name
            if p.is_symlink() or not p.is_file():
                raise ValueError("artifact changed type")
            h = hashlib.sha256()
            with p.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(chunk)
            if h.hexdigest() != expected:
                raise ValueError("digest mismatch: " + name)
    except (OSError, UnicodeError, ValueError) as exc:
        print("HOLD: " + str(exc), file=sys.stderr)
        return 5
    print("EVIDENCE_MANIFEST_INTERNALLY_CONSISTENT; NOT AUTHENTICATED; RELEASE HOLD")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
