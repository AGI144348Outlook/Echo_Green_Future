#!/usr/bin/env python3
"""F-001 Run546: offline evidence manifest verifier. CANDIDATE, UNTESTED.
Never runs regression or CI. Invoke only after prospective issue registration.
"""
import hashlib
import pathlib
import sys

def main():
    if len(sys.argv) != 2:
        print("usage: verifier /absolute/evidence/directory", file=sys.stderr)
        return 2
    root = pathlib.Path(sys.argv[1])
    if not root.is_absolute() or not root.is_dir() or root.is_symlink():
        print("HOLD: evidence directory must be absolute, existing, non-symlink", file=sys.stderr)
        return 2
    manifest = root / "SHA256SUMS"
    if not manifest.is_file() or manifest.is_symlink():
        print("HOLD: manifest missing or symlink", file=sys.stderr)
        return 3
    required = {"README.txt", "checkout-path.txt", "checkout-head.txt",
                "start-utc.txt", "end-utc.txt", "verdict.txt",
                "orchestrator-exit-status.txt", "preflight.stdout",
                "preflight.stderr", "preflight-exit-status.txt"}
    actual = {p.name for p in root.iterdir() if p.is_file() and not p.is_symlink() and p.name != "SHA256SUMS"}
    if not required <= actual:
        print("HOLD: required evidence absent: " + repr(sorted(required - actual)), file=sys.stderr)
        return 4
    entries = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if len(line) < 67 or line[64:66] not in ("  ", " *"):
            print("HOLD: malformed manifest line", file=sys.stderr)
            return 5
        digest, name = line[:64], line[66:]
        if not all(c in "0123456789abcdefABCDEF" for c in digest) or "/" in name or name in ("", ".", "..") or name in entries:
            print("HOLD: unsafe or duplicate manifest entry", file=sys.stderr)
            return 5
        entries[name] = digest.lower()
    if set(entries) != actual:
        print("HOLD: manifest/file-set mismatch", file=sys.stderr)
        return 6
    for name, expected in entries.items():
        path = root / name
        if not path.is_file() or path.is_symlink():
            print("HOLD: missing or symlinked artifact", file=sys.stderr)
            return 7
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        if h.hexdigest() != expected:
            print("HOLD: digest mismatch for " + name, file=sys.stderr)
            return 8
    print("EVIDENCE_MANIFEST_INTERNALLY_CONSISTENT; NOT AUTHENTICATED; RELEASE HOLD")
    return 0

if __name__ == "__main__":
    sys.exit(main())
