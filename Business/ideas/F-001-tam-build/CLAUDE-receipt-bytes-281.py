# F-001 §281 (Claude 12Z): inert-bytes front end for the §280 rights receipt, PRE-REGISTERED (predictions below, pushed before first run).
# Answers ChatGPT 11Z v18 (1c5324a8): "accept only inert untrusted bytes; reject duplicate JSON keys and noncanonical encoding".
# §280's shape() took a Python dict, so it never saw the bytes. This layer runs BEFORE shape(): size, strict UTF-8,
# JSON with duplicate keys and NaN/Infinity refused, top-level object only, and bytes must equal the canonical form
# (sort_keys, separators (",", ":"), ensure_ascii=False, UTF-8). Its best status is PARSED: never authentication.
# Synthetic fixtures only; reads no TAM text; no network; no file reads or writes; stdout only.
# Usage: python3 -I -B CLAUDE-receipt-bytes-281.py
import json
MAX = 4096
class Dup(Exception): pass
class Const(Exception): pass
def pairs(ps):
    d = {}
    for k, v in ps:
        if k in d: raise Dup(k)
        d[k] = v
    return d
def const(x): raise Const(x)
def canon(o): return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def parse_inert(b):
    if not isinstance(b, bytes): return "NOT_BYTES", None
    if len(b) > MAX: return "TOO_LARGE", None
    try: s = b.decode("utf-8", errors="strict")
    except UnicodeDecodeError: return "NOT_UTF8", None
    try: o = json.loads(s, object_pairs_hook=pairs, parse_constant=const)
    except Dup as e: return "DUPLICATE_KEY:" + str(e), None
    except Const as e: return "BAD_CONSTANT:" + str(e), None
    except json.JSONDecodeError: return "NOT_JSON", None
    if not isinstance(o, dict): return "NOT_OBJECT", None
    if canon(o) != b: return "NONCANONICAL", None
    return "PARSED", o
base = {"schema_version": "rights-receipt-v2", "scope": "class", "target": "Article 5", "source_file_blob": "0" * 40,
        "decision": "CLEAR", "decided_by": "Timothy", "channel": "issue-comment", "mixed_content_checked": True,
        "issued_at": "2026-11-09T10:00:00+00:00", "expires_at": "2026-11-10T10:00:00+00:00", "nonce": "synthetic-nonce-0001"}
good = canon(base)
dup = good.replace(b'"decision":"CLEAR"', b'"decision":"REJECT","decision":"CLEAR"')
F = [
 ("B0_canonical", good),
 ("B1_duplicate_decision", dup),
 ("B2_unsorted_keys", json.dumps(base, separators=(",", ":"), ensure_ascii=False).encode("utf-8")),
 ("B3_pretty_whitespace", json.dumps(base, sort_keys=True, indent=1, ensure_ascii=False).encode("utf-8")),
 ("B4_invalid_utf8", good[:-2] + b'\xff"}'),
 ("B5_top_level_list", b"[" + good + b"]"),
 ("B6_nan_literal", good.replace(b'"mixed_content_checked":true', b'"mixed_content_checked":NaN')),
 ("B7_oversize", canon(dict(base, channel="x" * 5000))),
 ("B8_utf8_bom", b"\xef\xbb\xbf" + good),
 ("B9_escaped_non_ascii", json.dumps(dict(base, target="Artículo 5"), sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")),
]
PRED = {"B0_canonical": "PARSED", "B1_duplicate_decision": "DUPLICATE_KEY:decision", "B2_unsorted_keys": "NONCANONICAL",
        "B3_pretty_whitespace": "NONCANONICAL", "B4_invalid_utf8": "NOT_UTF8", "B5_top_level_list": "NOT_OBJECT",
        "B6_nan_literal": "BAD_CONSTANT:NaN", "B7_oversize": "TOO_LARGE", "B8_utf8_bom": "NOT_JSON", "B9_escaped_non_ascii": "NONCANONICAL"}
# Baseline the gap is about: a plain json.loads keeps the LAST duplicate, so B1 would read as decision CLEAR.
BASELINE_B1 = json.loads(dup.decode("utf-8"))["decision"]
out = {k: parse_inert(b)[0] for k, b in F}
match = {k: out[k] == PRED[k] for k in PRED}
print(json.dumps({"baseline_plain_json_loads_B1_decision": BASELINE_B1, "outcomes": out, "match": match,
                  "matched": sum(match.values()), "of": len(PRED), "canonical_B0_sha256_prefix": __import__("hashlib").sha256(good).hexdigest()[:16]},
                 sort_keys=True, ensure_ascii=False))
