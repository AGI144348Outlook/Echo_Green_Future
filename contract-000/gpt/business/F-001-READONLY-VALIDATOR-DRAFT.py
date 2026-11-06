"""F-001 draft source-byte validator; offline, read-only; NOT rights clearance.
No tests executed. This is preparation only. Never writes to source files.
"""
import hashlib
import json
from pathlib import Path

def inspect_span(source: bytes, expected_sha256: str, start: int, end: int, expected_text: str):
    if hashlib.sha256(source).hexdigest() != expected_sha256:
        return {"status": "REJECT", "reason": "SOURCE_DIGEST_MISMATCH"}
    try:
        content = source.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return {"status": "REJECT", "reason": "INVALID_UTF8"}
    if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool):
        return {"status": "REJECT", "reason": "INVALID_RANGE"}
    if not 0 <= start < end <= len(content):
        return {"status": "REJECT", "reason": "INVALID_RANGE"}
    if content[start:end] != expected_text:
        return {"status": "REJECT", "reason": "TEXT_MISMATCH"}
    # Grapheme boundary checks intentionally NOT implemented: fail closed.
    return {"status": "REVIEW", "reason": "GRAPHEME_GATE_UNIMPLEMENTED",
            "source_sha256": expected_sha256, "codepoint_range": [start, end]}

def inspect_file(path: str, expected_sha256: str, start: int, end: int, expected_text: str):
    return inspect_span(Path(path).read_bytes(), expected_sha256, start, end, expected_text)

if __name__ == "__main__":
    raise SystemExit("Library-only draft. No CLI execution or release authority.")
