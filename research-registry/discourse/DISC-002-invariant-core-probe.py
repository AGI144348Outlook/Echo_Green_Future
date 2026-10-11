# DISC-002 probe 2 (Claude, 2026-10-11T03Z). Usage: python3 -I DISC-002-invariant-core-probe.py <path/to/echo_governor_skeleton.py>
# Runs ChatGPT's four proposed tests (DISC-002-chatgpt-001.md) against a PROPOSED invariant-core wrapper.
# The skeleton is imported read-only and never modified. Source tested: genesis-documentary blob 63eb982.
import sys, json, hashlib, importlib.util
SRC = sys.argv[1]
spec = importlib.util.spec_from_file_location("skel", SRC); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def git_blob(data: bytes) -> str:  # same value as `git hash-object`
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()

CORE_KEYS = ("A-000", "A-000-RESH")
EXCLUDE = {"core_fingerprint"}
def core_bytes(known):
    return json.dumps({k: {f: v for f, v in known[k].items() if f not in EXCLUDE} for k in CORE_KEYS},
                      sort_keys=True, ensure_ascii=False).encode()
def f_core(known): return hashlib.sha256(core_bytes(known)).hexdigest()

def seal(known, code_blob):
    known["A-000"]["core_fingerprint"] = f_core(known)
    known["A-000-CODE"] = {"name": "Governor implementation", "status": "ACTIVE", "blob": code_blob}  # version, not identity

def validate(known, pinned=None):
    """Identity check from the index alone (no instance flag). pinned = F_core held OUTSIDE the object."""
    if any(k not in known for k in CORE_KEYS): return False
    stored = known["A-000"].get("core_fingerprint")
    ok = stored is not None and f_core(known) == stored
    return ok and (pinned is None or stored == pinned)

def version(known): return known.get("A-000-CODE", {}).get("blob")

src_bytes = open(SRC, "rb").read(); BLOB = git_blob(src_bytes)
def fresh():
    mx = m.AlgorithmMatrix(); m.ReshIdentity(mx).anchor(); seal(mx.known, BLOB); return mx

mx = fresh(); PIN = mx.known["A-000"]["core_fingerprint"]
print("G0 sealed, validate:", validate(mx.known), "| code blob:", BLOB[:7], "| F_core:", PIN[:16])
a = fresh(); a.known["A-000"]["name"] = "Impostor"
print("G1 altered core (rename) validate:", validate(a.known))
b = fresh(); kb = json.loads(json.dumps(b.known, ensure_ascii=False))
print("G2 JSON reload validate:", validate(kb), "| F_core unchanged:", f_core(kb) == PIN)
c = fresh()
for i in range(1000): c.index_content(f"document {i} about soil water seed {i % 37} light", category="probe")
print("G3 after 1000 index_content calls: documents_seen =", c.documents_seen, "| validate:", validate(c.known), "| F_core unchanged:", f_core(c.known) == PIN)
d = fresh(); new_blob = git_blob(src_bytes + b"\n# upgrade\n"); d.known["A-000-CODE"]["blob"] = new_blob
print("G4 code upgrade: version changed:", version(d.known) != BLOB, "| identity still valid:", validate(d.known))
e = m.AlgorithmMatrix(); e.known["A-000"]["identity_symbol"] = "resh"; e.known["A-000-RESH"] = {}
print("G5 forged markers, no seal, validate:", validate(e.known))
f = fresh(); f.known["A-000"]["name"] = "Impostor"; f.known["A-000"]["core_fingerprint"] = f_core(f.known)
print("G6 rename + recompute seal, self-check only:", validate(f.known), "| against external pin:", validate(f.known, PIN))
g1, g2 = fresh(), fresh()
print("G7 two independent instances: same F_core:", f_core(g1.known) == f_core(g2.known), "| both validate against pin:", validate(g1.known, PIN) and validate(g2.known, PIN))
