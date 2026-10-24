#!/usr/bin/env python3
"""F-001 read-only composition of two independently proposed format gates.

NON-AUTHORITATIVE. Every outcome remains release=HOLD/readiness=BLOCKED.
Uses exact Git blob pins for gate source and checks the same artifact bytes
with both gate implementations. Neither gate proves conformance or provenance.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

GATES = (
    ("smoke", "PROPOSED-f001-format-smoke-gate-v1.py", "4620cc790bcced579b89fdb5d636ee0280c2fec7"),
    ("supplement", "PROPOSED-f001-format-supplement-v2.py", "96223a9ad1f43910c18b670e43b51ed266d1b854"),
)
MAX_SOURCE_BYTES = 128 * 1024


def git_blob_sha1(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def pinned_gate(directory, label, filename, expected_blob):
    path = directory / filename
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) |
                 getattr(os, "O_NONBLOCK", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_SOURCE_BYTES:
            raise ValueError(label + " source not bounded regular file")
        with os.fdopen(os.dup(fd), "rb") as handle:
            data = handle.read(MAX_SOURCE_BYTES + 1)
        after = os.fstat(fd)
        attrs = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
        if len(data) != before.st_size or attrs(before) != attrs(after):
            raise ValueError(label + " source changed during read")
    finally:
        os.close(fd)
    actual = git_blob_sha1(data)
    if actual != expected_blob:
        raise ValueError(label + " source pin mismatch: expected " + expected_blob + ", got " + actual)
    # The *verified bytes*, not a later path lookup, are compiled and loaded.
    scope = {"__name__": "f001_pinned_" + label, "__file__": str(path)}
    exec(compile(data, str(path), "exec"), scope)
    for fn in ("check_epub", "check_pdf"):
        if not callable(scope.get(fn)):
            raise ValueError(label + " missing " + fn)
    return scope


def check(epub_path, pdf_path, source_dir=None):
    result = {
        "schema": "f001-dual-format-preflight/v1",
        "product_id": "F-001",
        "composition": "FAIL",
        "release": "HOLD",
        "readiness": "BLOCKED",
        "publication_authorization": "ABSENT",
        "full_conformance_verified": False,
        "source_authenticated_independently": False,
        "issues": [],
        "gate_results": {},
        "artifact_sha256": {},
        "source_git_blobs": {label: sha for label, _, sha in GATES},
        "limitations": [
            "PDF marker checks do not validate the object graph or rendering",
            "No EPUBCheck, accessibility, editorial, rights, or independent source authentication",
            "In-process gate execution is not a sandbox; use only reviewed pinned scripts",
            "Source and input ancestor directories are not protected against same-UID substitution",
        ],
    }
    try:
        root = Path(source_dir) if source_dir is not None else Path(__file__).resolve().parent
        modules = {label: pinned_gate(root, label, filename, blob)
                   for label, filename, blob in GATES}
        # One bounded read per artifact; identical byte objects reach both gates.
        inputs = {}
        for kind, path in (("epub", epub_path), ("pdf", pdf_path)):
            data = modules["smoke"]["bounded_file"](path)
            inputs[kind] = data
            result["artifact_sha256"][kind] = hashlib.sha256(data).hexdigest()
        for label, module in modules.items():
            detail = {"status": "PASS", "issues": [], "observations": {}}
            for kind, data in inputs.items():
                try:
                    detail["observations"][kind] = module["check_" + kind](data)
                except Exception as exc:
                    detail["status"] = "FAIL"
                    detail["issues"].append(kind + ": " + type(exc).__name__ + ": " + str(exc))
            result["gate_results"][label] = detail
            result["issues"].extend(label + ": " + s for s in detail["issues"])
        if not result["issues"]:
            result["composition"] = "PASS"
    except Exception as exc:
        result["issues"].append("preflight: " + type(exc).__name__ + ": " + str(exc))
    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: dual-format-preflight-v1.py BOOK.epub BOOK.pdf")
    result = check(sys.argv[1], sys.argv[2])
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["composition"] == "PASS" else 1)
