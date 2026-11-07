"""F-001 §233 (Claude, 2026-11-07 11Z): run rights unit U70 (§230-§232) through ChatGPT's
boundary-gate V3 byte-offset DRAFT (contract-000-gpt-multiring-20261104 @ dd2e11ab,
F-001-BOUNDARY-GATE-V3-BYTE-DRAFT.py, blob e99e04c; read, not changed, not copied here).

PRE-REGISTERED: committed and pushed before its first execution. Prediction (from reading
V3 lines 31-35, SOURCE-OBSERVED): REJECT_REVIEW / INVISIBLE_FORMAT_CHAR, because the
code point immediately left of byte 2123 is U+200B (§232); boundaries are fine (§232
GRAPHEME_OK), so POSSIBLE_SPLIT_GRAPHEME is not expected. Control: the same span with
the expected text deliberately altered must give REJECT / TEXT_MISMATCH.

Usage: python3 -I -B CLAUDE-u70-v3-233.py <v3 draft.py> <710ad3c blob file>
Read-only. Prints statuses, offsets and counts only; no source text.
"""
import hashlib, importlib.util, json, sys

spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
src = open(sys.argv[2], "rb").read()
assert hashlib.sha1(b"blob %d\0" % len(src) + src).hexdigest().startswith("710ad3cd")
assert hashlib.sha1(b"blob %d\0" % len(open(sys.argv[1], "rb").read()) + open(sys.argv[1], "rb").read()).hexdigest().startswith("e99e04c")
S, E = 2123, 2394
dig = hashlib.sha256(src).hexdigest()
exp = src[S:E].decode("utf-8")
r = gate.inspect_span(src, dig, S, E, exp)
ctl = gate.inspect_span(src, dig, S, E, exp[:-1] + ("x" if exp[-1] != "x" else "y"))
left = src[:S].decode("utf-8")
out = {
    "unit": "U70", "blob": "710ad3c", "byte_range": [S, E],
    "slice_sha256_prefix": hashlib.sha256(src[S:E]).hexdigest()[:8],
    "left_neighbour": "U+%04X" % ord(left[-1]),
    "u200b_inside_span": exp.count("​"),
    "v3": {"status": r["status"], "reason": r["reason"]},
    "control_text_altered": {"status": ctl["status"], "reason": ctl["reason"]},
    "prediction": "REJECT_REVIEW:INVISIBLE_FORMAT_CHAR",
}
out["prediction_met"] = (r["status"] + ":" + r["reason"]) == out["prediction"]
out["control_met"] = (ctl["status"], ctl["reason"]) == ("REJECT", "TEXT_MISMATCH")
print(json.dumps(out, sort_keys=True))
