#!/usr/bin/env python3
"""HOLD-only verification of eight local TAM source bytes against externally supplied Git blob pins.

The pins JSON must be independently obtained from a trusted GitHub tree/commit;
this tool cannot authenticate its own pin manifest. It does not run a scanner or release a book.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

FILES = (
    "README.md", "Article 1 Hacksilber", "Article 2 Water Weight Computes",
    "The Color Dyed and Dental Records", "Article 5", "Article 6", "Article 10",
    "Collective information",
)
SCHEMA = "f001-trusted-git-pins/v1"
REPO = "AGI144348Outlook/The-TAM-protocol"
MAX_BYTES = 8_000_000
HEX40 = re.compile(r"[0-9a-f]{40}\Z")

class PinError(ValueError):
    pass

def unique_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise PinError("duplicate JSON key: " + key)
        obj[key] = value
    return obj

def git_blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def verify(source, pin_file, output):
    source, pin_file, output = Path(source), Path(pin_file), Path(output)
    if source.is_symlink() or not source.is_dir():
        raise PinError("source must be a real directory")
    root = source.resolve(strict=True)
    if pin_file.is_symlink() or not pin_file.is_file():
        raise PinError("pin manifest missing, not regular, or symlink")
    if root == pin_file.resolve() or root in pin_file.resolve().parents:
        raise PinError("trusted pins must be outside untrusted source directory")
    target = output.resolve(strict=False)
    if target == root or root in target.parents:
        raise PinError("receipt must be outside source directory")
    if output.is_symlink() or output.exists() or not output.parent.is_dir():
        raise PinError("receipt target exists, symlink, or parent missing")
    if pin_file.stat().st_size > 64_000:
        raise PinError("pin manifest too large")
    try:
        pins = json.loads(pin_file.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise PinError("invalid UTF-8 or JSON in pin manifest") from exc
    if not isinstance(pins, dict) or set(pins) != {"schema", "repository", "ref", "files"}:
        raise PinError("invalid pin manifest shape")
    if pins["schema"] != SCHEMA or pins["repository"] != REPO or not isinstance(pins["ref"], str) or not HEX40.fullmatch(pins["ref"]):
        raise PinError("unrecognized schema/repository or unpinned commit ref")
    rows = pins["files"]
    if not isinstance(rows, list) or len(rows) != len(FILES):
        raise PinError("pin list must contain exactly eight entries")
    expected = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"name", "git_blob_sha1"}:
            raise PinError("invalid pin row shape")
        name, digest = row["name"], row["git_blob_sha1"]
        if not isinstance(name, str) or not isinstance(digest, str) or not HEX40.fullmatch(digest):
            raise PinError("invalid name or git blob digest")
        if name in expected:
            raise PinError("duplicate source name")
        expected[name] = digest
    if set(expected) != set(FILES):
        raise PinError("missing or unexpected source name")
    verified = []
    for name in FILES:
        p = root / name
        if p.is_symlink() or not p.is_file():
            raise PinError("missing/nonregular/symlink source: " + name)
        if p.stat().st_size > MAX_BYTES:
            raise PinError("oversized source: " + name)
        raw = p.read_bytes()
        if not raw or len(raw) > MAX_BYTES:
            raise PinError("empty/oversized source: " + name)
        try:
            raw.decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise PinError("non-UTF-8 source: " + name) from exc
        actual = git_blob_sha1(raw)
        if actual != expected[name]:
            raise PinError("Git blob mismatch: " + name)
        verified.append({"name": name, "bytes": len(raw), "git_blob_sha1": actual,
                         "sha256": hashlib.sha256(raw).hexdigest()})
    receipt = {"schema": "f001-verified-git-pins/v1", "source_ref": pins["ref"],
               "repository": REPO, "source_count": len(verified), "files": verified,
               "status": "HOLD_SOURCE_PIN_MATCH_NOT_EDITORIAL_APPROVAL"}
    # Exclusive creation prevents overwriting an earlier receipt.
    with output.open("x", encoding="utf-8") as f:
        f.write(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return receipt

def main(argv):
    if len(argv) != 4:
        raise PinError("usage: gate <source-directory> <trusted-pins.json> <new-receipt.json>")
    receipt = verify(*argv[1:])
    print(json.dumps({"status": receipt["status"], "source_count": receipt["source_count"]}))

if __name__ == "__main__":
    try:
        main(sys.argv)
    except (PinError, OSError) as exc:
        print("F-001 HOLD: " + str(exc), file=sys.stderr)
        sys.exit(2)
