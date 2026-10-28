#!/usr/bin/env python3
"""F-001 HOLD-only scanner preflight: read-only exact-source checks.

Run: python3 -I -B f001_scanner_preflight_411.py <TAM-clone> <claim_scan.py>
Never publishes, changes source files, or approves editorial claims.
Source pins: Run393 exact eight-source Git blobs at TAM d46456a; scanner blob: library-shared 31f3dcf.
"""
import hashlib, json, os, stat, sys
from pathlib import Path

PROJECT = "F-001"
STATUS = "HOLD / NOT LAUNCH-READY"
SOURCE_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
SCANNER_BLOB = "31f3dcff486c4c8cc96d514eb425da86834d00c3"
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
MAX_FILE_BYTES = 2 * 1024 * 1024


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def read_regular_bounded(path):
    # No symlinks or non-regular files, even if the target exists.
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_FILE_BYTES:
        raise ValueError("not a bounded regular file: " + path.name)
    with path.open("rb") as stream:
        raw = stream.read(MAX_FILE_BYTES + 1)
    if len(raw) != st.st_size or len(raw) > MAX_FILE_BYTES:
        raise ValueError("file size changed: " + path.name)
    if path.lstat().st_size != st.st_size:
        raise ValueError("file changed during read: " + path.name)
    return raw


def audit_sources(src, scanner, pins=PINS, scanner_pin=SCANNER_BLOB):
    src, scanner = Path(src), Path(scanner)
    if not src.is_dir() or src.is_symlink():
        raise ValueError("source must be a real directory")
    rows = []
    for name, expected in pins.items():
        raw = read_regular_bounded(src / name)
        actual = git_blob(raw)
        if actual != expected:
            raise ValueError("source Git blob mismatch: " + name)
        rows.append({"file": name, "git_blob": actual, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
    scanner_raw = read_regular_bounded(scanner)
    if git_blob(scanner_raw) != scanner_pin:
        raise ValueError("original scanner Git blob mismatch")
    return {"project": PROJECT, "status": STATUS, "source_commit_claim": SOURCE_COMMIT,
            "source_file_count": len(rows), "sources": rows, "scanner_git_blob": scanner_pin,
            "scanner_execution": "NOT RUN", "release_authorized": False}


def main(argv):
    if len(argv) != 3:
        print("usage: python3 -I -B f001_scanner_preflight_411.py <TAM-clone> <claim_scan.py>", file=sys.stderr)
        return 2
    try:
        print(json.dumps({"audit": "PASS", **audit_sources(argv[1], argv[2])}, sort_keys=True))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"audit": "FAIL", "project": PROJECT, "status": STATUS, "reason": str(exc),
                          "scanner_execution": "NOT RUN", "release_authorized": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
