# DISC-002 probe (Claude, 2026-10-11). Usage: python3 -I DISC-002-a000-probe.py <path/to/echo_governor_skeleton.py>
# Source tested: genesis-documentary blob 63eb982989b4f3478d649430b555c8f4ba755c27
import sys, json, hashlib, importlib.util
spec = importlib.util.spec_from_file_location("skel", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def fresh():
    mx = m.AlgorithmMatrix(); r = m.ReshIdentity(mx); r.anchor(); return mx, r
mx, r = fresh(); print("T1 anchored validate:", r.validate())
# T2: tamper A-000 identity core (name/status) keeping identity_symbol
mx.known["A-000"]["name"]="Impostor"; mx.known["A-000"]["status"]="RETIRED"
print("T2 after renaming A-000 to Impostor/RETIRED, validate:", r.validate())
# T3: forge: a fresh matrix with only the two marker fields, never anchored via ReshIdentity
mx2 = m.AlgorithmMatrix(); mx2.known["A-000"]["identity_symbol"]="resh"; mx2.known["A-000-RESH"]={}
r2 = m.ReshIdentity(mx2); r2._anchored=True
print("T3 forged markers (empty A-000-RESH) validate:", r2.validate())
# T4: serialization round trip: known survives JSON but _anchored flag does not
mx3, r3 = fresh(); blob = json.dumps(mx3.known, sort_keys=True, ensure_ascii=False)
mx4 = m.AlgorithmMatrix(); mx4.known = json.loads(blob); r4 = m.ReshIdentity(mx4)
print("T4 reloaded matrix, new ReshIdentity, validate:", r4.validate())
# T5: content fingerprint of identity core, excluding the fingerprint field (self-certifying, not a fixed point)
def core(k): return json.dumps({x: {f:v for f,v in k[x].items() if f!="fingerprint"} for x in ("A-000","A-000-RESH")}, sort_keys=True, ensure_ascii=False).encode()
mx5, _ = fresh(); fp = hashlib.sha256(core(mx5.known)).hexdigest(); mx5.known["A-000"]["fingerprint"]=fp
print("T5 fingerprint stored, recompute matches:", hashlib.sha256(core(mx5.known)).hexdigest()==fp)
mx5.known["A-000"]["name"]="Impostor"
print("T5b after rename, recompute matches:", hashlib.sha256(core(mx5.known)).hexdigest()==fp)
print("T6 fp:", fp[:16])
