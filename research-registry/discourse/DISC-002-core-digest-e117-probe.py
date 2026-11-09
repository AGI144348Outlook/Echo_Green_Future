# DISC-002 e117: predicate (i) external core-digest wrapper, PRE-REGISTERED at rdr e76c6b13 (2026-11-09 08Z)
# and named on Issue #13 comment 6735152403 before this harness existed. Read-only: imports Genesis blob
# 63eb9829 from a path given on argv; never edits it; no network; no file writes.
# Matrix: the real AlgorithmMatrix() (no-arg constructor, dicts only; SOURCE-OBSERVED lines 349-420).
# Declared deviation from the pre-registration text: the real A-000 has no "description" key, so C2
# sets one where none existed (it therefore also adds a key, overlapping C3). Prediction unchanged.
# Usage: python3 -I probe.py <skeleton.py> <fixture.json>
import sys, json, hashlib, importlib.util, copy
spec = importlib.util.spec_from_file_location("g", sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
FIX = json.load(open(sys.argv[2]))["sha256"]
def canon(d): return json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def core_ok(m):
    core = {k: v for k, v in m.known.get("A-000", {}).items() if not k.startswith("identity_")}
    return hashlib.sha256(canon(core)).hexdigest() == FIX
def fresh():
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m); r.anchor(); return m, r
PRED = {"C0": [True, True], "C1": [False, True], "C2": [False, True], "C3": [False, True], "C4": [True, True], "C5": [True, True]}
out = {}
m, r = fresh(); out["C0"] = [core_ok(m), r.validate()]
m, r = fresh(); m.known["A-000"]["name"] = "SOMETHING ELSE"; out["C1"] = [core_ok(m), r.validate()]
m, r = fresh(); m.known["A-000"]["description"] = "replaced"; out["C2"] = [core_ok(m), r.validate()]
m, r = fresh(); m.known["A-000"]["extra_key"] = 1; out["C3"] = [core_ok(m), r.validate()]
m, r = fresh(); m.known["A-000"]["identity_glyph"] = "X"; m.known["A-000"]["identity_meaning"] = "changed"; out["C4"] = [core_ok(m), r.validate()]
m, r = fresh(); a = m.known["A-000"]; m.known["A-000"] = {k: a[k] for k in reversed(list(a))}; out["C5"] = [core_ok(m), r.validate()]
out["match"] = {k: out[k] == PRED[k] for k in PRED}
out["matched"] = sum(out["match"].values())
print(json.dumps(out, sort_keys=True))
