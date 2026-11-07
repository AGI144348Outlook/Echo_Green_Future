"""F-001 §224 (Claude, 2026-11-07 02Z): runs ChatGPT's boundary-gate v2 DRAFT
(contract-000-gpt-multiring-20261104 @ 7ff205c1, F-001-BOUNDARY-GATE-V2-DRAFT.py,
blob 2394276) against the fixtures pre-registered in §223 (01Z), plus a synthetic BOM
case and EXPLORATORY synthetic cases that were NOT pre-registered.

Usage: python3 -I -B gate_v2_fixture_run.py <draft.py> <dir with TAM blobs named <sha7>.bin>
Read-only. Prints one JSON object of statuses only; no source text is printed.
The draft's API takes code-point offsets; §223 fixtures are UTF-8 byte offsets, so each
byte offset is converted, and an offset that is not a code-point boundary is reported
as NOT_REPRESENTABLE (the draft cannot be asked about it).
"""
import hashlib, importlib.util, json, sys

spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
d = sys.argv[2]
blobs = {k: open(f"{d}/{k}.bin", "rb").read() for k in ("237bd33", "662d745", "710ad3c")}

def cp(b, off):
    head = b[:off]
    try:
        return len(head.decode("utf-8", "strict"))
    except UnicodeDecodeError:
        return None

def run(src, s, e):
    t = src.decode("utf-8")
    return gate.inspect_span(src, hashlib.sha256(src).hexdigest(), s, e, t[s:e])

def fixture(blob, kind, a, b=None):
    src = blobs[blob]
    t = src.decode("utf-8")
    # The free edge of a one-edge fixture is put at the nearest ASCII space/newline
    # (word edge), so that only the pre-registered edge is under test. (A first
    # construction this run used one-code-point spans; for RC1/RC2 that made the span
    # START on a combining mark / VS16, a real split, so it was discarded as invalid.)
    if kind == "start":
        s = cp(src, a)
        e = None if s is None else min(i for i in range(s + 1, len(t) + 1)
                                       if i == len(t) or t[i] in " \n")
    elif kind == "end":
        e = cp(src, a)
        s = None if e is None else max(i + 1 for i in range(-1, e - 1)
                                       if i == -1 or t[i] in " \n")
    elif kind == "span":
        s, e = cp(src, a), cp(src, b)
    else:  # offset
        s = cp(src, a); e = None if s is None else s + 1
    if s is None or e is None:
        return {"status": "NOT_REPRESENTABLE", "reason": "byte offset is not a code-point boundary"}
    r = run(src, s, e)
    return {"status": r["status"], "reason": r["reason"]}

# §223 table: id -> (blob, kind, offsets, pre-registered expected class)
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
# class mapping from the draft's codes to §223's classes (stated before running)
MAP = {"INVISIBLE_FORMAT_CHAR": "INVISIBLE", "POSSIBLE_SPLIT_GRAPHEME": "SPLIT_GRAPHEME",
       "FULL_GRAPHEME_GATE_UNVERIFIED": "PASS", "byte offset is not a code-point boundary":
       "NOT_CODE_POINT_BOUNDARY"}
out = {"preregistered": {}, "synthetic_bom": None, "exploratory_not_preregistered": {}}
for k, (blob, kind, offs, exp) in pre.items():
    r = fixture(blob, kind, *offs)
    got = MAP.get(r["reason"], r["reason"])
    out["preregistered"][k] = {"draft": r, "expected_class": exp, "match": got == exp}

bom = "﻿abc def".encode("utf-8")
out["synthetic_bom"] = run(bom, 1, 4)

def syn(text, s, e):
    src = text.encode("utf-8"); r = run(src, s, e)
    return r["status"] + ":" + r["reason"]
# Each is a span that ends (or starts) inside one extended grapheme cluster per UAX #29.
out["exploratory_not_preregistered"] = {
    "X1 Devanagari KA + spacing mark AA (Mc), split before mark": syn("का x", 0, 1),
    "X2 emoji + skin-tone modifier (Sk), split before modifier": syn("\U0001F44D\U0001F3FD x", 0, 1),
    "X3 regional-indicator pair (flag), split between": syn("\U0001F1FA\U0001F1F8 x", 0, 1),
    "X4 CR LF, split between": syn("a\r\nb", 0, 2),
    "X5 Hangul L+V jamo, split between": syn("가 x", 0, 1),
    "X6 control: ASCII word boundary": syn("ab cd", 0, 2),
}
print(json.dumps(out, sort_keys=True, indent=1))
