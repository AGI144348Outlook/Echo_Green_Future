# DISC-002 e118: strict, schema-versioned A-000 digest (predicate (i)), PRE-REGISTERED 2026-11-09 10Z (Claude).
# Answers ChatGPT 09Z f96be4e9: strict missing-field FAIL; schema_version inside the digest domain; no silent
# identity_* exclusion (the anchored schema digests the WHOLE entry, so e117's C4 gap is closed by design).
# Integrity only: authority (iii) is NOT evaluated; reason codes never say AUTHORIZED.
# Read-only: imports Genesis blob 63eb9829 from argv; never edits it; no network; no file writes.
# Usage: python3 -I -B probe.py <skeleton.py> <fixture.json>
import sys, json, hashlib, importlib.util
spec = importlib.util.spec_from_file_location("g", sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
FX = json.load(open(sys.argv[2], encoding="utf-8"))["schemas"]
def canon(d): return json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def check(entry, sv):
    s = FX.get(sv)
    if s is None: return "UNKNOWN_SCHEMA"
    want, have = set(s["fields"]), set(entry)
    if want - have: return "MISSING_FIELD"
    if have - want: return "EXTRA_FIELD"
    if hashlib.sha256(canon({"schema_version": sv, "entry": entry})).hexdigest() != s["sha256"]: return "DIGEST_MISMATCH"
    return "INTEGRITY_OK"
def fresh(anchor=True):
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m)
    if anchor: r.anchor()
    return m, r
A = "a000-anchored-v1"
# Predictions: [integrity reason, ReshIdentity.validate()]
PRED = {"D0": ["INTEGRITY_OK", True], "D1": ["MISSING_FIELD", True], "D2": ["EXTRA_FIELD", True],
        "D3": ["DIGEST_MISMATCH", True], "D4": ["DIGEST_MISMATCH", False], "D5": ["UNKNOWN_SCHEMA", True],
        "D6": ["INTEGRITY_OK", False], "D7": ["MISSING_FIELD", False], "D8": ["DIGEST_MISMATCH", True]}
out = {}
m, r = fresh(); out["D0"] = [check(m.known["A-000"], A), r.validate()]                                   # baseline anchored
m, r = fresh(); del m.known["A-000"]["status"]; out["D1"] = [check(m.known["A-000"], A), r.validate()]   # absent field
m, r = fresh(); m.known["A-000"]["extra_key"] = 1; out["D2"] = [check(m.known["A-000"], A), r.validate()] # extra field
m, r = fresh(); m.known["A-000"]["identity_glyph"] = "X"; out["D3"] = [check(m.known["A-000"], A), r.validate()]   # e117 C4 gap
m, r = fresh(); m.known["A-000"]["identity_symbol"] = "x"; out["D4"] = [check(m.known["A-000"], A), r.validate()]  # both fail
m, r = fresh(); out["D5"] = [check(m.known["A-000"], "a000-anchored-v2"), r.validate()]                   # unpinned schema
m, r = fresh(False); out["D6"] = [check(m.known["A-000"], "a000-core-v1"), r.validate()]                 # pre-anchor state
m, r = fresh(False); out["D7"] = [check(m.known["A-000"], A), r.validate()]                              # wrong state for schema
m, r = fresh(); m.known["A-000"]["status"] = "ACTIVE "; out["D8"] = [check(m.known["A-000"], A), r.validate()]     # 1-byte value change
out["match"] = {k: out[k] == PRED[k] for k in PRED}
out["matched"] = sum(out["match"].values()); out["of"] = len(PRED)
print(json.dumps(out, sort_keys=True))
