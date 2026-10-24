# E35 (Claude 22Z, not pre-registered): ReshIdentity re-anchor after tamper, stub matrix.
import importlib.util, sys, copy, json
spec = importlib.util.spec_from_file_location("gov", sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
class M: pass
m = M(); m.known = {"A-000": {"name": "Governor", "status": "ACTIVE"}}
r = g.ReshIdentity(m); r.anchor()
print("after anchor valid:", r.validate())
# T1: tamper identity_symbol only
m.known["A-000"]["identity_symbol"] = "x"; print("T1 valid:", r.validate())
if not r.validate(): r.anchor()          # what open_exchanges() does
print("T1 after re-anchor valid:", r.validate(), "symbol:", m.known["A-000"]["identity_symbol"])
# T2: tamper a non-identity field
m.known["A-000"]["status"] = "TAMPERED"; print("T2 valid (status tampered):", r.validate(), m.known["A-000"]["status"])
# T3: tamper symbol and status together, then re-anchor
m.known["A-000"]["identity_symbol"] = "x"
if not r.validate(): r.anchor()
print("T3 after re-anchor valid:", r.validate(), "status:", m.known["A-000"]["status"])
# T4: alias entry rewritten
m.known["A-000-RESH"]["aliases"] = ["intruder"]; print("T4 valid (aliases rewritten):", r.validate())
