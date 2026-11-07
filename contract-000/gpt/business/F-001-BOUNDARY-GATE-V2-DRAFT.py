"""F-001 conservative Unicode source-boundary gate v2 (DRAFT; UNTESTED).
Read-only. No normalization, no rights/editorial/release decisions.
Offsets are Python codepoint indices, not UTF-8 byte offsets.
False negatives are possible: this is not a complete UAX #29 grapheme segmenter.
"""
import hashlib
import unicodedata

def inspect_span(source: bytes, source_digest: str, start: int, end: int, expected: str):
    if hashlib.sha256(source).hexdigest() != source_digest:
        return {"status": "REJECT", "reason": "SOURCE_DIGEST_MISMATCH"}
    try:
        text = source.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return {"status": "REJECT", "reason": "INVALID_UTF8"}
    if text.startswith("\ufeff"):
        return {"status": "REJECT", "reason": "BOM_PRESENT"}
    if any(type(x) is not int for x in (start, end)) or not 0 <= start < end <= len(text):
        return {"status": "REJECT", "reason": "INVALID_RANGE"}
    if text[start:end] != expected:
        return {"status": "REJECT", "reason": "TEXT_MISMATCH"}
    def continuation(ch):
        return (unicodedata.combining(ch) != 0 or
                unicodedata.category(ch) in ("Mn", "Me") or
                ch in ("\u200d", "\ufe0f"))
    for pos in (start, end):
        if 0 < pos < len(text) and (continuation(text[pos]) or text[pos-1] == "\u200d"):
            return {"status": "REJECT_REVIEW", "reason": "POSSIBLE_SPLIT_GRAPHEME"}
    if "\u200b" in text[max(0, start-1):min(len(text), end+1)]:
        return {"status": "REJECT_REVIEW", "reason": "INVISIBLE_FORMAT_CHAR"}
    # Conservative: no full Unicode grapheme segmentation; never grant clearance.
    return {"status": "REVIEW", "reason": "FULL_GRAPHEME_GATE_UNVERIFIED",
            "source_sha256": source_digest, "codepoint_range": [start, end]}

if __name__ == "__main__":
    raise SystemExit("Draft library function only; no CLI execution or release authority")
