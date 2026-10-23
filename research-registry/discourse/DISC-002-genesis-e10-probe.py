# DISC-002 2026-10-23T15Z (Claude): characterization probe, NOT a frozen test. Usage: python3 -I -B DISC-002-genesis-e10-probe.py <dir holding an unchanged copy of genesis-documentary:src/echo_governor_skeleton.py (blob 63eb982)>
import sys, json, hashlib, copy
sys.path.insert(0, sys.argv[1]); import echo_governor_skeleton as G
def fresh():
    m = G.AlgorithmMatrix(); m.regions = {"R1": {"words": {"alpha","beta","gamma"}, "size": 3}}; return m
def dep(m): return G.governor_validate_and_deploy(m)["status"]
out = {}
# G12: ReshIdentity.anchor() rewrites A-000 in place and adds A-000-RESH
m = fresh(); before = copy.deepcopy(m.known["A-000"]); r = G.ReshIdentity(m); r.anchor()
out["G12_resh_entry"] = "A-000-RESH" in m.known; out["G12_validate"] = r.validate(); out["G12_deploy_after_anchor"] = dep(m)
# G13: impostor via direct assignment after anchor; Resh.validate() and deploy
m2 = fresh(); r2 = G.ReshIdentity(m2); r2.anchor()
m2.known["A-000"] = {"name": "Impostor", "status": "ACTIVE", "identity_symbol": "resh"}
out["G13_impostor_resh_validate"] = r2.validate(); out["G13_impostor_deploy"] = dep(m2)
# G14: SUSPENDED -> ACTIVE by direct mutation, no transition anywhere
m3 = fresh(); m3.known["A-000"]["status"] = "SUSPENDED"; s1 = dep(m3); m3.known["A-000"]["status"] = "ACTIVE"; out["G14_suspend_then_direct_reactivate"] = [s1, dep(m3)]
# G15: protecting record() only (subclass refusing A-000) does not stop direct dict writes
class Guarded(G.AlgorithmMatrix):
    def record(self, k, e):
        if k == "A-000": raise PermissionError("A-000 protected")
        super().record(k, e)
m4 = Guarded(); m4.regions = {"R1": {"words": {"a","b"}, "size": 2}}
try: m4.record("A-000", {"name": "X", "status": "ACTIVE"}); out["G15_record"] = "allowed"
except PermissionError: out["G15_record"] = "refused"
m4.known["A-000"] = {"name": "X", "status": "ACTIVE"}; out["G15_direct_then_deploy"] = dep(m4)
# G16: deploy itself writes into known (sub-agent entries) -> known cannot be frozen whole
m5 = fresh(); n0 = len(m5.known); dep(m5); out["G16_known_grows_on_deploy"] = len(m5.known) - n0
# G17: scratch-only external two-domain check (not in source): identity digest over name, lifecycle chain held outside
def idg(e, schema="genesis-a000/v1"): return hashlib.sha256(json.dumps({"schema": schema, "name": e.get("name")}, sort_keys=True).encode()).hexdigest()
class Witness:  # stands in for the independent trust anchor + ledger
    def __init__(s, m): s.id = idg(m.known["A-000"]); s.life = [("ACTIVE", 1)]
    def transition(s, state): s.life.append((state, s.life[-1][1] + 1))
    def admit(s, m):
        e = m.known.get("A-000")
        if e is None: return "DELETED"
        if idg(e) != s.id: return "IDENTITY_MISMATCH"
        if e.get("status") != s.life[-1][0]: return "LIFECYCLE_MISMATCH"
        if s.life[-1][0] != "ACTIVE": return "NOT_ACTIVE"
        return "ADMIT"
m6 = fresh(); w = Witness(m6); res = {"baseline": w.admit(m6)}
m6.known["A-000"]["status"] = "SUSPENDED"; res["direct_suspend_unlogged"] = w.admit(m6)
w.transition("SUSPENDED"); res["logged_suspend"] = w.admit(m6); res["identity_digest_unchanged"] = idg(m6.known["A-000"]) == w.id
m6.known["A-000"]["status"] = "ACTIVE"; res["direct_reactivate_unlogged"] = w.admit(m6)
w.transition("ACTIVE"); res["logged_reactivate"] = w.admit(m6); res["lifecycle_version"] = w.life[-1][1]
m6.known["A-000"] = {"name": "Impostor", "status": "ACTIVE"}; res["impostor"] = w.admit(m6)
m7 = fresh(); w7 = Witness(m7); G.ReshIdentity(m7).anchor(); res["after_resh_anchor_name_only_schema"] = w7.admit(m7)
m7.known.pop("A-000"); res["pop"] = w7.admit(m7)
out["G17_scratch_witness"] = res
print(json.dumps(out, indent=1))
