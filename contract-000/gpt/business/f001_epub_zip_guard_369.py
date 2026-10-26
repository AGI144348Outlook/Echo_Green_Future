#!/usr/bin/env python3
"""F-001 draft-only, read-only EPUB ZIP preflight. NOT a release authorization.

Use before the existing epub_check.py. This is a bounded central-directory
screen, not EPUBCheck, an EPUB content parser, or an anti-malware scanner.
Never extracts or modifies archive members. Python standard library only.
"""
import json
import os
import stat
import sys
import unicodedata
import zipfile
from pathlib import Path

MIMETYPE = b"application/epub+zip"
DEFAULT_LIMITS = {
    "max_archive_bytes": 32 * 1024 * 1024,
    "max_entries": 500,
    "max_member_uncompressed": 16 * 1024 * 1024,
    "max_total_uncompressed": 64 * 1024 * 1024,
    "max_compression_ratio": 200,
}

class Reject(ValueError):
    pass


def guard(path, *, limits=None):
    cfg = dict(DEFAULT_LIMITS)
    if limits:
        if any(k not in cfg or not isinstance(v, int) or v < 1 for k, v in limits.items()):
            raise ValueError("invalid limits")
        cfg.update(limits)
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise Reject("input must be a regular non-symlink file")
    if path.stat().st_size > cfg["max_archive_bytes"]:
        raise Reject("archive byte budget exceeded")
    try:
        with zipfile.ZipFile(path, "r", allowZip64=True) as z:
            infos = z.infolist()
            if not infos or len(infos) > cfg["max_entries"]:
                raise Reject("ZIP entry count out of bounds")
            first = infos[0]
            if first.filename != "mimetype" or first.compress_type != zipfile.ZIP_STORED:
                raise Reject("mimetype must be first and stored")
            if first.file_size != len(MIMETYPE) or z.read(first) != MIMETYPE:
                raise Reject("invalid EPUB mimetype")
            seen = set()
            total = 0
            for info in infos:
                name = unicodedata.normalize("NFC", info.filename)
                if not name or name.startswith("/") or "\\" in name or ":" in name.split("/")[0]:
                    raise Reject("unsafe ZIP member path")
                parts = name.rstrip("/").split("/")
                if any(p in ("", ".", "..") for p in parts):
                    raise Reject("unsafe ZIP member path segment")
                if any(ord(c) < 32 or ord(c) == 127 for c in name):
                    raise Reject("ZIP member contains control characters")
                if name in seen:
                    raise Reject("duplicate ZIP member")
                seen.add(name)
                mode = (info.external_attr >> 16) & 0o170000
                if mode == stat.S_IFLNK:
                    raise Reject("ZIP symlink member")
                if info.flag_bits & 1:
                    raise Reject("encrypted ZIP member")
                if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    raise Reject("unsupported ZIP compression")
                if info.file_size > cfg["max_member_uncompressed"]:
                    raise Reject("ZIP member size budget exceeded")
                total += info.file_size
                if total > cfg["max_total_uncompressed"]:
                    raise Reject("ZIP total size budget exceeded")
                if info.file_size > 65536 and info.file_size / max(1, info.compress_size) > cfg["max_compression_ratio"]:
                    raise Reject("ZIP compression ratio budget exceeded")
            return {"status": "HOLD_PASSED_ZIP_PREFLIGHT", "entries": len(infos),
                    "declared_uncompressed_bytes": total, "limits": cfg,
                    "scope": "ZIP metadata and mimetype only; full EPUB/rights checks NOT RUN"}
    except (zipfile.BadZipFile, zipfile.LargeZipFile, EOFError, OSError, RuntimeError) as e:
        raise Reject("unreadable ZIP archive: " + type(e).__name__) from e


def main(argv):
    if len(argv) != 2:
        print("usage: python3 -I -B f001_epub_zip_guard_369.py file.epub", file=sys.stderr)
        return 2
    try:
        print(json.dumps(guard(argv[1]), sort_keys=True))
        return 0
    except (Reject, ValueError) as e:
        print(json.dumps({"status": "REJECT", "reason": str(e)}))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
