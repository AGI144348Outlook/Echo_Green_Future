#!/usr/bin/env python3
"""F-001 supplementary HOLD-only source-report consistency checker (Run 363).

Read-only candidate. Complements, but does NOT replace, the pinned Run 334
builder / Run 344 gate / Run 347 consumer / Run 351 coordinator. Its source
SHA-256 reference values are from a previous GPT source read, not a publisher
signature or proof of source rights. Exit 0 = fields consistent, NEVER release.

Usage: python3 -I -B F-001-REPORT-PIN-363.py <dataset-check.json>
"""
import json
import os
from pathlib import Path
import stat
import sys

MAX_REPORT_BYTES = 100_000
PIN_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
PINS = {
    "A": {
        "sha256": "48437f58ee74a9a0226d901d1291b6c104764648fe7760ebbc91b74b6ba6a302",
        "git_blob": "b62c970a660e0a6685b58db1ef121690daa4fce7",
        "rows": 6,
    },
    "B": {
        "sha256": "bc16da657b19317e110cdcf4159a9118aa89f2cfc4f8183e7e3f1d94f2eb3b81",
        "git_blob": "12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4",
        "rows": 8,
    },
}


def no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key: " + key)
        obj[key] = value
    return obj


def no_nonfinite(value):
    raise ValueError("nonfinite JSON constant: " + value)


def decode_strict(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=no_duplicates,
                      parse_constant=no_nonfinite)


def read_bounded_regular(path):
    """POSIX: reject final symlink, directory/FIFO and oversized files."""
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        raise ValueError("POSIX O_NOFOLLOW required")
    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    fd = os.open(os.fspath(path), flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError("report is not a regular file")
        if before.st_size > MAX_REPORT_BYTES:
            raise ValueError("report exceeds byte limit")
        chunks, length = [], 0
        while True:
            chunk = os.read(fd, min(65536, MAX_REPORT_BYTES + 1 - length))
            if not chunk:
                break
            chunks.append(chunk)
            length += len(chunk)
            if length > MAX_REPORT_BYTES:
                raise ValueError("report exceeds byte limit during read")
        after = os.fstat(fd)
        if any(getattr(before, key) != getattr(after, key) for key in
               ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")):
            raise ValueError("report changed while reading")
        if length != after.st_size:
            raise ValueError("report length changed while reading")
        return b"".join(chunks)
    finally:
        os.close(fd)


def validate(report):
    """Return an explicit HOLD result for any report shape or value."""
    errors = []
    if type(report) is not dict or set(report) != {"base_g_per_unit", "source_commit", "files"}:
        return {"status": "HOLD", "consistent": False, "errors": ["REPORT_SHAPE"]}
    if type(report["base_g_per_unit"]) not in (int, float) or report["base_g_per_unit"] != 13.7:
        errors.append("BASE_MISMATCH")
    if report["source_commit"] != PIN_COMMIT:
        errors.append("SOURCE_COMMIT_MISMATCH")
    files = report["files"]
    if type(files) is not dict or set(files) != {"A", "B"}:
        return {"status": "HOLD", "consistent": False, "errors": errors + ["FILES_SHAPE"]}
    for key in ("A", "B"):
        rec = files[key]
        if type(rec) is not dict or set(rec) != {"sha256", "git_blob", "rows", "rejected"}:
            errors.append(key + "_SHAPE")
            continue
        for field in ("sha256", "git_blob", "rows"):
            if (field == "rows" and type(rec[field]) is not int) or rec[field] != PINS[key][field]:
                errors.append(key + "_" + field.upper() + "_MISMATCH")
        if type(rec["rejected"]) is not list or rec["rejected"]:
            errors.append(key + "_REJECTED")
    return {"status": "HOLD", "consistent": not errors, "errors": errors}


def verify_path(path):
    try:
        return validate(decode_strict(read_bounded_regular(path)))
    except (OSError, ValueError, UnicodeError, TypeError, RecursionError) as exc:
        return {"status": "HOLD", "consistent": False,
                "errors": ["INPUT_REJECTED: " + str(exc)]}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: python3 -I -B F-001-REPORT-PIN-363.py <dataset-check.json>", file=sys.stderr)
        return 2
    result = verify_path(Path(argv[0]))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["consistent"] else 1


if __name__ == "__main__":
    sys.exit(main())
