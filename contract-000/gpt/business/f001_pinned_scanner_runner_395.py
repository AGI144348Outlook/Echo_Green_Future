#!/usr/bin/env python3
"""F-001 HOLD-only exact-source claim scanner replay. No publication or release authority.

Usage: python3 -I -B f001_pinned_scanner_runner_395.py <TAM-clone> <claim_scan.py> <new-output-dir>
Input pins refer to The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9
and Echo_Green_Future library-shared claim_scan.py@31f3dcff486c4c8cc96d514eb425da86834d00c3.
"""
import csv
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

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
MAX_FILE_BYTES = 1_000_000


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def checked_bytes(path, expected):
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise ValueError("unreadable or symlink input: " + str(path)) from exc
    try:
        s = os.fstat(fd)
        if not stat.S_ISREG(s.st_mode) or s.st_size > MAX_FILE_BYTES:
            raise ValueError("nonregular or oversized input: " + str(path))
        with os.fdopen(fd, "rb", closefd=False) as f:
            data = f.read(MAX_FILE_BYTES + 1)
    finally:
        os.close(fd)
    if len(data) > MAX_FILE_BYTES or git_blob(data) != expected:
        raise ValueError("source blob mismatch: " + str(path))
    return data


def replay(src, scanner, out, pins=PINS, scanner_pin=SCANNER_BLOB, expected_rows=42):
    src, scanner, out = Path(src).absolute(), Path(scanner).absolute(), Path(out).absolute()
    if not src.is_dir() or src.is_symlink():
        raise ValueError("source directory absent or symlink")
    if out.exists() or out == src or src in out.parents or out in src.parents:
        raise ValueError("output must be new and outside source")
    if scanner.parent == out or scanner == out or out in scanner.parents:
        raise ValueError("output conflicts with scanner")
    # Validate every input before creating any output.
    source_data = {name: checked_bytes(src / name, pin) for name, pin in pins.items()}
    scanner_data = checked_bytes(scanner, scanner_pin)
    with tempfile.TemporaryDirectory(prefix="f001-pin-") as tmp:
        snap = Path(tmp)
        for name, data in source_data.items():
            (snap / name).write_bytes(data)
        snap_scanner = snap / "claim_scan.py"
        snap_scanner.write_bytes(scanner_data)
        out.mkdir(parents=True, exist_ok=False)
        p = subprocess.run([sys.executable, "-I", "-B", str(snap_scanner),
                            str(snap), str(out)], capture_output=True,
                           text=True, timeout=20, check=False)
    if p.returncode != 0:
        raise ValueError("original scanner failed: " + p.stderr[:500])
    report = json.loads((out / "claims-report.json").read_text(encoding="utf-8"))
    with (out / "claims.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != expected_rows or report["rows"] != expected_rows:
        raise ValueError("unexpected candidate count")
    if set(report["source_files"]) != set(pins):
        raise ValueError("missing or extra source report entries")
    for name, data in source_data.items():
        if report["source_files"].get(name) != hashlib.sha256(data).hexdigest():
            raise ValueError("source SHA256 report mismatch: " + name)
    if any(row["status"] != "" for row in rows):
        raise ValueError("scanner returned preapproved status")
    if sum(report["per_file"].values()) != expected_rows:
        raise ValueError("per-file count mismatch")
    receipt = {"project": "F-001", "readiness": "HOLD",
               "source_commit": SOURCE_COMMIT, "scanner_blob": scanner_pin,
               "source_blobs": pins, "rows": expected_rows,
               "source_sha256": report["source_files"],
               "note": "Candidate extraction only; no factual/rights/editorial approval."}
    (out / "f001-source-replay-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    try:
        print(json.dumps(replay(*sys.argv[1:]), sort_keys=True))
    except (ValueError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        sys.exit("HOLD: " + str(exc))
