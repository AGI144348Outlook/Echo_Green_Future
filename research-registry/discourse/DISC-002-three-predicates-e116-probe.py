import sys, importlib.util, json, hashlib
spec = importlib.util.spec_from_file_location("g", sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
class M:  # minimal stand-in exposing only .known, as validate()/anchor() read
    def __init__(s): s.known = {"A-000": {"name": "Governor", "status": "ACTIVE", "description": "core"}}
out = {}
m = M(); r = g.ReshIdentity(m); r.anchor()
out["P0_after_anchor"] = r.validate()
# P1 (predicate i): replace every core field of A-000, keep only identity_symbol
m.known["A-000"] = {"identity_symbol": "resh", "name": "SOMETHING ELSE", "description": "replaced"}
out["P1_core_replaced_validate"] = r.validate()
# P2 (predicate ii): no lineage record exists to compare against
out["P2_lineage_attrs"] = sorted(a for a in vars(r) if "hash" in a or "digest" in a or "lineage" in a or "version" in a)
# P3 (predicate iii): fresh instance, set _anchored by hand, no trust root consulted
m2 = M(); m2.known["A-000"]["identity_symbol"] = "resh"; m2.known["A-000-RESH"] = {}
r2 = g.ReshIdentity(m2); r2._anchored = True
out["P3_forged_no_anchor_call_validate"] = r2.validate()
print(json.dumps(out, sort_keys=True))
