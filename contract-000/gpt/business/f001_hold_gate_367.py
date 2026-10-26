#!/usr/bin/env python3
"""F-001 offline HOLD evidence preflight. NEVER certifies rights or authorizes release.

Usage: python3 f001_hold_gate_367.py receipt.json artifact-directory
Exit 0 only for a structurally complete, hash-bound HOLD review package.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_RECEIPT = 1024 * 1024
MAX_ARTIFACT = 100 * 1024 * 1024
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TYPES = {"epub": ".epub", "pdf": ".pdf", "csv": ".csv"}

class HoldError(ValueError):
    pass

def no_duplicates(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise HoldError(f"duplicate JSON key: {k}")
        obj[k] = v
    return obj

def fail_constant(value):
    raise HoldError(f"nonfinite JSON constant: {value}")

def require_text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 4096:
        raise HoldError(f"missing or invalid {label}")
    return value

def verify(receipt, artifact_dir):
    rp = Path(receipt)
    root = Path(artifact_dir)
    if rp.is_symlink() or not rp.is_file() or rp.stat().st_size > MAX_RECEIPT:
        raise HoldError("receipt missing, symlink or oversized")
    if root.is_symlink() or not root.is_dir():
        raise HoldError("artifact directory missing or symlink")
    try:
        data = json.loads(rp.read_text(encoding="utf-8"),
                          object_pairs_hook=no_duplicates, parse_constant=fail_constant)
    except (UnicodeError, json.JSONDecodeError) as e:
        raise HoldError(f"invalid JSON: {e}") from e
    if not isinstance(data, dict):
        raise HoldError("receipt must be an object")
    if data.get("project_id") != "F-001" or data.get("mode") != "HOLD":
        raise HoldError("only F-001 HOLD review is permitted")
    approval = data.get("approval")
    if not isinstance(approval, dict) or approval.get("publication_authorized") is not False:
        raise HoldError("publication must be explicitly unauthorized in this gate")
    source = data.get("source")
    if not isinstance(source, dict):
        raise HoldError("source evidence missing")
    require_text(source.get("repository"), "source repository")
    if not HEX40.fullmatch(str(source.get("commit", ""))):
        raise HoldError("source commit is not a pinned Git SHA")
    require_text(source.get("rights_evidence"), "rights evidence reference")
    require_text(source.get("rights_reviewer"), "rights reviewer")
    editorial = data.get("editorial")
    if not isinstance(editorial, dict):
        raise HoldError("editorial evidence missing")
    require_text(editorial.get("reviewer"), "editorial reviewer")
    claims = editorial.get("claims")
    if not isinstance(claims, list) or not claims:
        raise HoldError("claim evidence missing")
    seen = set()
    for c in claims:
        if not isinstance(c, dict):
            raise HoldError("malformed claim")
        key = require_text(c.get("id"), "claim id")
        if key in seen:
            raise HoldError("duplicate claim id")
        seen.add(key)
        if c.get("status") not in ("sourced", "cut", "inferred", "test", "claimed"):
            raise HoldError(f"unreviewed claim {key}")
        require_text(c.get("evidence"), f"claim evidence {key}")
    package = data.get("package")
    if not isinstance(package, dict) or not str(package.get("identifier", "")).startswith("urn:uuid:"):
        raise HoldError("stable package identifier missing")
    files = package.get("artifacts")
    if not isinstance(files, list) or len(files) < 3 or len(files) > 30:
        raise HoldError("expected bounded EPUB/PDF/CSV artifact set")
    seen_paths, kinds = set(), set()
    for a in files:
        if not isinstance(a, dict) or a.get("kind") not in TYPES:
            raise HoldError("unsupported artifact kind")
        kind = a["kind"]
        name = a.get("path")
        if not isinstance(name, str) or not name or name != Path(name).name or name in (".", "..") or "\\" in name or "/" in name:
            raise HoldError("artifact path must be a basename")
        if name in seen_paths or not name.lower().endswith(TYPES[kind]):
            raise HoldError("duplicate path or wrong extension")
        seen_paths.add(name)
        kinds.add(kind)
        expected = a.get("sha256")
        if not isinstance(expected, str) or not HEX64.fullmatch(expected):
            raise HoldError("missing artifact digest")
        path = root / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_ARTIFACT:
            raise HoldError("artifact missing, symlink or oversized")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                digest.update(chunk)
        if digest.hexdigest() != expected:
            raise HoldError(f"digest mismatch: {name}")
    if kinds != set(TYPES):
        raise HoldError("must include EPUB, PDF and CSV")
    return "HOLD: syntactic/hash review passed; rights and contents NOT independently certified"

def main(argv):
    if len(argv) != 3:
        print("usage: f001_hold_gate_367.py receipt.json artifact-directory", file=sys.stderr)
        return 2
    try:
        print(verify(argv[1], argv[2]))
        return 0
    except (HoldError, OSError) as exc:
        print(f"FAIL CLOSED: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
