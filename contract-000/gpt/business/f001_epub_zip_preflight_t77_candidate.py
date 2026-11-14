"""F-001 EPUB ZIP preflight v2 — GPT-owned, DRAFT / UNTESTED.

Single-backslash ZIP path refusal is proposed; no test or certification yet.\n\nThis gate is additive to f001_epub_structure_gate_t72.py, not a substitute
for its OPF/spine validation or rights/accessibility/PDF review.
"""
from zipfile import ZipFile, ZIP_STORED, BadZipFile

MIMETYPE = b"application/epub+zip"
MAX_MEMBER_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024
MAX_MEMBERS = 4096
MAX_COMPRESSION_RATIO = 200

class EPUBPreflightError(ValueError):
    pass

def inspect_zip(path):
    """Read metadata first; reject dangerous sizes before decompressing entries.

    Returns structural evidence only. Does not assert EPUB conformance.
    """
    try:
        with ZipFile(path) as z:
            members = z.infolist()
            if not members or len(members) > MAX_MEMBERS:
                raise EPUBPreflightError("invalid ZIP member count")
            names = [m.filename for m in members]
            if len(names) != len(set(names)):
                raise EPUBPreflightError("duplicate ZIP names")
            first = members[0]
            if (first.filename != "mimetype" or
                    first.compress_type != ZIP_STORED or
                    first.file_size != len(MIMETYPE)):
                raise EPUBPreflightError("mimetype must be first and stored")
            if z.read(first) != MIMETYPE:
                raise EPUBPreflightError("wrong mimetype content")
            total = 0
            for member in members:
                name = member.filename
                if (not name or name.startswith("/") or "\\" in name or
                        any(part in ("", ".", "..") for part in name.rstrip("/").split("/"))):
                    raise EPUBPreflightError("unsafe ZIP path")
                if member.flag_bits & 1:
                    raise EPUBPreflightError("encrypted member")
                if member.file_size > MAX_MEMBER_BYTES:
                    raise EPUBPreflightError("member too large")
                total += member.file_size
                if total > MAX_TOTAL_BYTES:
                    raise EPUBPreflightError("archive too large")
                if member.file_size and (member.compress_size == 0 or
                        member.file_size > MAX_COMPRESSION_RATIO * member.compress_size):
                    raise EPUBPreflightError("compression ratio exceeds budget")
            return {"status": "ZIP_PREFLIGHT_ONLY", "members": len(members),
                    "declared_uncompressed_bytes": total}
    except (BadZipFile, OSError, RuntimeError) as exc:
        raise EPUBPreflightError("unreadable ZIP") from exc
