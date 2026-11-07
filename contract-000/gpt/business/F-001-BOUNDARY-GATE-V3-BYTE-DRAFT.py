"""F-001 source span verifier v3 — DRAFT, UNTESTED.
Offsets are UTF-8 byte offsets, half-open [start,end). No release authority.
All results require human rights/editorial approval and full UAX #29 review.
"""
import hashlib
import unicodedata

def inspect_span(source: bytes, source_digest: str, start: int, end: int, expected: str):
    if hashlib.sha256(source).hexdigest() != source_digest:
        return {"status":"REJECT","reason":"SOURCE_DIGEST_MISMATCH"}
    try:
        full = source.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return {"status":"REJECT","reason":"INVALID_UTF8"}
    if full.startswith("\ufeff"):
        return {"status":"REJECT","reason":"BOM_PRESENT"}
    if any(type(x) is not int for x in (start,end)) or not 0 <= start < end <= len(source):
        return {"status":"REJECT","reason":"INVALID_BYTE_RANGE"}
    try:
        left = source[:start].decode("utf-8", "strict")
        selected = source[start:end].decode("utf-8", "strict")
        right = source[end:].decode("utf-8", "strict")
    except UnicodeDecodeError:
        return {"status":"REJECT","reason":"SPLIT_UTF8_CODEPOINT"}
    if selected != expected:
        return {"status":"REJECT","reason":"TEXT_MISMATCH"}
    def continuation(ch):
        return (unicodedata.combining(ch) != 0 or
                unicodedata.category(ch) in ("Mn","Me") or
                ch in ("\u200d","\ufe0f"))
    if (left and selected and (continuation(selected[0]) or left[-1] == "\u200d")) or (
        right and selected and (continuation(right[0]) or selected[-1] == "\u200d")):
        return {"status":"REJECT_REVIEW","reason":"POSSIBLE_SPLIT_GRAPHEME"}
    if "\u200b" in (left[-1:] + selected + right[:1]):
        return {"status":"REJECT_REVIEW","reason":"INVISIBLE_FORMAT_CHAR"}
    return {"status":"REVIEW","reason":"FULL_UAX29_AND_RIGHTS_UNVERIFIED",
            "source_sha256":source_digest,"utf8_byte_range":[start,end],
            "codepoint_range":[len(left),len(left)+len(selected)]}

if __name__ == "__main__":
    raise SystemExit("DRAFT ONLY: no automatic execution or release authority")
