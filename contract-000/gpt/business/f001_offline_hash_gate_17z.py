#!/usr/bin/env python3
"""F-001 GPT-owned OFFLINE release evidence checker, untested draft, never authorizes publication.
Only reads manifest and files below specified evidence root. Exit 1 ALWAYS until external
issuer authority, rights, editorial, accessibility, Android QA, and Timothy approval
are independently authenticated. No network, no imports from evidence root.
"""
import hashlib
import json
import pathlib
import sys

def no_duplicates(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError("duplicate JSON key: " + k)
        out[k] = v
    return out

def contained(root, relative):
    p = pathlib.PurePosixPath(relative)
    if p.is_absolute() or ".." in p.parts or not relative or "\\" in relative:
        raise ValueError("unsafe relative path")
    target = (root / relative).resolve(strict=True)
    if not target.is_relative_to(root):
        raise ValueError("path escapes evidence root")
    if not target.is_file():
        raise ValueError("not a regular file")
    return target

def check(root, manifest):
    root = pathlib.Path(root).resolve(strict=True)
    record = json.loads(pathlib.Path(manifest).read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(record, dict):
        raise ValueError("manifest must be object")
    files = record.get("artifacts")
    if not isinstance(files, list) or not files:
        raise ValueError("missing artifacts")
    seen = set()
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ValueError("invalid artifact")
        path = item["path"]
        if path in seen:
            raise ValueError("duplicate artifact")
        seen.add(path)
        expected = item.get("sha256")
        if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            raise ValueError("invalid digest")
        actual = hashlib.sha256(contained(root, path).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError("digest mismatch: " + path)
    return len(files)

if __name__ == "__main__":
    try:
        n = check(sys.argv[1], sys.argv[2])
        print(f"HOLD: {n} artifact hashes matched, but issuer/rights/editorial/accessibility/QA/approval not independently verified")
    except Exception as exc:
        print("HOLD: " + type(exc).__name__ + ": " + str(exc))
    sys.exit(1)
