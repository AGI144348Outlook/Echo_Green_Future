#!/usr/bin/env python3
"""F-001 HOLD-only eight-source preflight; never invokes the claim scanner.

Usage: python f001_source_preflight_434.py <tam-clone-dir> <manifest-output.json>
Does not modify source files; output must be outside source clone and not exist.
"""
import hashlib
import json
import sys
from pathlib import Path

FILES = (
    "README.md", "Article 1 Hacksilber", "Article 2 Water Weight Computes",
    "The Color Dyed and Dental Records", "Article 5", "Article 6", "Article 10",
    "Collective information",
)
MAX_SOURCE_BYTES = 8_000_000


class PreflightError(ValueError):
    pass


def preflight(source, output):
    source = Path(source)
    output = Path(output)
    if source.is_symlink() or not source.is_dir():
        raise PreflightError("source must be a real directory, not a symlink")
    root = source.resolve(strict=True)
    target = output.resolve(strict=False)
    if target == root or root in target.parents:
        raise PreflightError("manifest must be outside the source clone")
    if output.is_symlink() or output.exists():
        raise PreflightError("manifest target already exists or is a symlink")
    if not output.parent.is_dir():
        raise PreflightError("manifest parent directory must already exist")

    entries = []
    for name in FILES:
        p = root / name
        if p.is_symlink() or not p.is_file():
            raise PreflightError("required source missing, not a regular file or symlink: " + name)
        if p.stat().st_size > MAX_SOURCE_BYTES:
            raise PreflightError("source exceeds size cap: " + name)
        raw = p.read_bytes()
        if not raw:
            raise PreflightError("empty source: " + name)
        try:
            raw.decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise PreflightError("invalid UTF-8: " + name) from exc
        entries.append({"name": name, "bytes": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()})
    manifest = {"schema": "f001-source-preflight/v1", "source_count": len(entries),
                "files": entries, "status": "SOURCE_INPUTS_PRESENT_NOT_CLAIMS_REVIEWED"}
    # Deliberately no output path, timestamp or filesystem location in the receipt.
    serialized = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    # Exclusive create ensures an existing receipt is never silently overwritten.
    with output.open("x", encoding="utf-8") as f:
        f.write(serialized)
    return manifest


def main(argv):
    if len(argv) != 3:
        raise PreflightError("usage: preflight <source-directory> <new-manifest.json>")
    result = preflight(argv[1], argv[2])
    print(json.dumps({"status": result["status"], "source_count": result["source_count"]}))


if __name__ == "__main__":
    try:
        main(sys.argv)
    except (PreflightError, OSError) as exc:
        print("F-001 PREFLIGHT HOLD: " + str(exc), file=sys.stderr)
        sys.exit(2)
