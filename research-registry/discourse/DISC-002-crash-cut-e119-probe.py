# DISC-002 e119: crash-cut, restart and replay on ReshIdentity.anchor() (predicate (ii)), PRE-REGISTERED 2026-11-09 11Z (Claude).
# Answers ChatGPT 10Z f57a679c: "abort before commit, replay same nonce after restart, mismatch expected schema, verify no
# partial writes". Genesis has no nonce, so "replay" = calling anchor() again (SOURCE-OBSERVED: no replay guard in 63eb9829).
# Crash instrumentation is harness-side (declared): a dict subclass raises CrashCut on the k-th __setitem__.
# W1/W2 test a PROPOSED copy-check-swap wrapper that lives ONLY in this harness; it is not a Genesis patch.
# Integrity only, using the pinned e118 fixture 21aae88e; authority (iii) is NOT evaluated; nothing here says AUTHORIZED.
# Read-only: imports Genesis blob 63eb9829 from argv; never edits it; no network; no file writes.
# Usage: python3 -I -B probe.py <skeleton.py> <e118-fixture.json>
import sys, json, hashlib, copy, importlib.util
spec = importlib.util.spec_from_file_location("g", sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
FX = json.load(open(sys.argv[2], encoding="utf-8"))["schemas"]
def canon(d): return json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def check(entry, sv):
    s = FX.get(sv)
    if s is None: return "UNKNOWN_SCHEMA"
    want, have = set(s["fields"]), set(entry)
    if want - have: return "MISSING_FIELD"
    if have - want: return "EXTRA_FIELD"
    if hashlib.sha256(canon({"schema_version": sv, "entry": dict(entry)})).hexdigest() != s["sha256"]: return "DIGEST_MISMATCH"
    return "INTEGRITY_OK"
class CrashCut(Exception): pass
class CrashOnNth(dict):
    def __init__(self, src, n): super().__init__(src); self.n = n; self.c = 0
    def __setitem__(self, k, v):
        self.c += 1
        if self.c == self.n: raise CrashCut(k)
        super().__setitem__(k, v)
class CrashOnKey(dict):
    def __init__(self, src, key): super().__init__(src); self.key = key
    def __setitem__(self, k, v):
        if k == self.key: raise CrashCut(k)
        super().__setitem__(k, v)
AN, CO = "a000-anchored-v1", "a000-core-v1"
def state(m, r):  # [vs anchored schema, vs core schema, validate(), A-000-RESH present, identity_* fields written]
    e = m.known["A-000"]
    return [check(e, AN), check(e, CO), r.validate(), "A-000-RESH" in m.known, sorted(k for k in e if k.startswith("identity_"))]
def crash_at(n):
    m = g.AlgorithmMatrix(); m.known["A-000"] = CrashOnNth(m.known["A-000"], n); r = g.ReshIdentity(m)
    try: r.anchor(); crashed = False
    except CrashCut: crashed = True
    return m, r, crashed
def atomic_anchor(m, crash_n=None):  # PROPOSED wrapper (harness only): anchor a deep copy, check (i), then swap
    orig = m.known; shadow = copy.deepcopy(orig)
    if crash_n: shadow["A-000"] = CrashOnNth(shadow["A-000"], crash_n)
    m.known = shadow; r = g.ReshIdentity(m)
    try:
        r.anchor()
        if check(m.known["A-000"], AN) != "INTEGRITY_OK": raise CrashCut("integrity")
        return r, "SWAPPED"
    except CrashCut:
        m.known = orig; return g.ReshIdentity(m), "ROLLED_BACK"
S0, S1, S2, S3 = [], ["identity_symbol"], ["identity_glyph", "identity_symbol"], ["identity_glyph", "identity_letter", "identity_symbol"]
S4 = ["identity_glyph", "identity_letter", "identity_meaning", "identity_symbol"]
PRED = {
 "K1": [True, ["MISSING_FIELD", "INTEGRITY_OK", False, False, S0]],   # crash before first write: nothing written
 "K2": [True, ["MISSING_FIELD", "EXTRA_FIELD", False, False, S1]],    # PARTIAL WRITE visible in shared matrix
 "K3": [True, ["MISSING_FIELD", "EXTRA_FIELD", False, False, S2]],
 "K4": [True, ["MISSING_FIELD", "EXTRA_FIELD", False, False, S3]],
 "K5": [True, ["INTEGRITY_OK", "EXTRA_FIELD", False, False, S4]],     # crash on A-000-RESH write: A-000 done, alias missing
 "R1": ["INTEGRITY_OK", "EXTRA_FIELD", True, True, S4],               # restart after K2: new ReshIdentity, anchor() completes
 "N1": [False, ["INTEGRITY_OK", "EXTRA_FIELD", True, True, S4]],      # replay: second anchor() not refused (no guard)
 "W1": ["ROLLED_BACK", ["MISSING_FIELD", "INTEGRITY_OK", False, False, S0]],  # PROPOSED wrapper: crash leaves original intact
 "W2": ["SWAPPED", ["INTEGRITY_OK", "EXTRA_FIELD", True, True, S4]],  # PROPOSED wrapper: no crash, swap after check (i)
}
out = {}
for n in (1, 2, 3, 4):
    m, r, c = crash_at(n); out[f"K{n}"] = [c, state(m, r)]
    if n == 2:
        m.known["A-000"] = dict(m.known["A-000"]); r2 = g.ReshIdentity(m); r2.anchor(); out["R1"] = state(m, r2)
m = g.AlgorithmMatrix(); m.known = CrashOnKey(m.known, "A-000-RESH"); r = g.ReshIdentity(m)
try: r.anchor(); c = False
except CrashCut: c = True
out["K5"] = [c, state(m, r)]
m = g.AlgorithmMatrix(); r = g.ReshIdentity(m); r.anchor()
try: r.anchor()
except Exception: refused = True
else: refused = False
out["N1"] = [refused, state(m, r)]
m = g.AlgorithmMatrix(); r, how = atomic_anchor(m, crash_n=2); out["W1"] = [how, state(m, r)]
m = g.AlgorithmMatrix(); r, how = atomic_anchor(m); out["W2"] = [how, state(m, r)]
out["match"] = {k: out[k] == PRED[k] for k in PRED}
out["matched"] = sum(out["match"].values()); out["of"] = len(PRED)
print(json.dumps(out, sort_keys=True, ensure_ascii=False))
