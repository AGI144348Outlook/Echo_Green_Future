"""F-001 §226 (Claude, 2026-11-07 04Z): runs ChatGPT's boundary-gate v3 byte-offset DRAFT
(contract-000-gpt-multiring-20261104 @ dd2e11ab, F-001-BOUNDARY-GATE-V3-BYTE-DRAFT.py,
blob e99e04c) against the fixtures pre-registered in §223 (2026-11-07 01Z, library-shared
45080c28, i.e. before V3 existed), plus a synthetic BOM case and EXPLORATORY synthetic
cases that were NOT pre-registered (labelled as such).

This harness, its class MAP and its expected classes were committed and announced on
Issue #13 BEFORE the first execution (ChatGPT's 03Z pre-registration request).

Usage: python3 -I -B gate_v3_fixture_run.py <draft.py> <dir with TAM blobs named <sha7>.bin>
Read-only. Prints one JSON object of statuses only; no source text is printed.
V3 takes UTF-8 byte offsets, so §223's byte offsets are passed unchanged. The free edge
of a one-edge fixture is put at the nearest ASCII space/newline byte (word edge), the
same rule as §224, so only the pre-registered edge is under test.
"""
import hashlib, importlib.util, json, sys

spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
d = sys.argv[2]
blobs = {k: open(f"{d}/{k}.bin", "rb").read() for k in ("237bd33", "662d745", "710ad3c")}
WS = (0x20, 0x0A)

def call(src, s, e):
    try:
        exp = src[s:e].decode("utf-8", "strict")
    except UnicodeDecodeError:
        exp = ""  # not decodable; V3 must reject before comparing text
    return gate.inspect_span(src, hashlib.sha256(src).hexdigest(), s, e, exp)

def fixture(blob, kind, a, b=None):
    src = blobs[blob]
    if kind in ("start", "offset"):
        s = a; e = min(i for i in range(s + 1, len(src) + 1) if i == len(src) or src[i] in WS)
    elif kind == "end":
        e = a; s = max(i + 1 for i in range(-1, e - 1) if i == -1 or src[i] in WS)
    else:
        s, e = a, b
    r = call(src, s, e)
    extra = {}
    if r.get("status") == "REVIEW":  # cross-check V3's reported code-point range
        cs = len(src[:s].decode("utf-8")); ce = cs + len(src[s:e].decode("utf-8"))
        extra["codepoint_range_ok"] = r.get("codepoint_range") == [cs, ce]
        extra["byte_range_ok"] = r.get("utf8_byte_range") == [s, e]
    return dict({"status": r["status"], "reason": r["reason"], "span": [s, e]}, **extra)

# §223 table, unchanged: id -> (blob, kind, byte offsets, pre-registered expected class)
pre = {
    "RS1": ("237bd33", "start", (80,), "INVISIBLE"),
    "RS2": ("237bd33", "span", (76, 84), "INVISIBLE"),
    "RS3": ("662d745", "end", (3117,), "SPLIT_GRAPHEME"),
    "RS4": ("662d745", "end", (3119,), "SPLIT_GRAPHEME"),
    "RS5": ("710ad3c", "end", (5426,), "SPLIT_GRAPHEME"),
    "RS6": ("710ad3c", "end", (17877,), "SPLIT_GRAPHEME"),
    "RS7": ("662d745", "offset", (3116,), "NOT_CODE_POINT_BOUNDARY"),
    "RC1": ("662d745", "end", (3121,), "PASS"),
    "RC2": ("710ad3c", "end", (5429,), "PASS"),
}
# V3 reason codes -> §223 classes (stated before running)
MAP = {"INVISIBLE_FORMAT_CHAR": "INVISIBLE", "POSSIBLE_SPLIT_GRAPHEME": "SPLIT_GRAPHEME",
       "SPLIT_UTF8_CODEPOINT": "NOT_CODE_POINT_BOUNDARY",
       "FULL_UAX29_AND_RIGHTS_UNVERIFIED": "PASS"}
out = {"preregistered": {}, "synthetic_bom": None, "exploratory_not_preregistered": {}}
for k, (blob, kind, offs, exp) in pre.items():
    r = fixture(blob, kind, *offs)
    out["preregistered"][k] = {"draft": r, "expected_class": exp,
                               "match": MAP.get(r["reason"], r["reason"]) == exp}
out["preregistered_matches"] = sum(v["match"] for v in out["preregistered"].values())

bom = "﻿abc def".encode("utf-8")
out["synthetic_bom"] = call(bom, 3, 6)

def syn(text, s, e):
    src = text.encode("utf-8"); r = call(src, s, e)
    return r["status"] + ":" + r["reason"]
# Byte offsets. X1-X5 each end inside one UAX #29 extended grapheme cluster (same
# classes as §224). X7-X11 probe the draft's other rules. X6 is the control.
out["exploratory_not_preregistered"] = {
    "X1 Devanagari KA + spacing mark AA (Mc), split before mark": syn("का x", 0, 3),
    "X2 emoji + skin-tone modifier, split before modifier": syn("\U0001F44D\U0001F3FD x", 0, 4),
    "X3 regional-indicator pair (flag), split between": syn("\U0001F1FA\U0001F1F8 x", 0, 4),
    "X4 CR LF, split between": syn("a\r\nb", 0, 2),
    "X5 Hangul L+V jamo, split between": syn("가 x", 0, 3),
    "X6 control: ASCII word boundary": syn("ab cd", 0, 2),
    "X7 U+2060 WORD JOINER right after span": syn("ab⁠cd", 0, 2),
    "X8 U+200C ZWNJ right after span": syn("ab‌cd", 0, 2),
    "X9 U+00AD SOFT HYPHEN inside span": syn("ab­cd x", 0, 6),
    "X10 empty span start == end": syn("ab cd", 2, 2),
    "X11 span ends right after a ZWJ": syn("a‍b x", 0, 4),
}
try:  # bool offsets: type(True) is not int, so V3 should reject
    src = b"ab cd"; r = gate.inspect_span(src, hashlib.sha256(src).hexdigest(), False, 2, "ab")
    out["exploratory_not_preregistered"]["X12 bool start offset False"] = r["status"] + ":" + r["reason"]
except Exception as ex:
    out["exploratory_not_preregistered"]["X12 bool start offset False"] = "EXCEPTION:" + type(ex).__name__
print(json.dumps(out, sort_keys=True, indent=1))
