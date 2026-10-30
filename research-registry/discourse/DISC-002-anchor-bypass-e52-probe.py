"""E52 exploratory probe (Claude 12Z) on Genesis echo_governor_skeleton.py blob 63eb982. Read-only; no Genesis change."""
import sys, json, hashlib, copy
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
def digest(m):
    ids = {k: m.known.get(k) for k in ("A-000", "A-000-RESH")}
    return hashlib.sha256(json.dumps(ids, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()[:16]
class Counting(g.AlgorithmMatrix):
    def __init__(self):
        super().__init__(); self.gen = 0
    def record(self, k, v):
        self.gen += 1; super().record(k, v)
out = {}
# C1: in-place mutation of A-000 between turns without record()
m = Counting(); r = g.ReshIdentity(m); r.anchor()
g0, d0 = m.gen, digest(m)
m.known["A-000"]["identity_meaning"] = "patched"          # no record()
out["C1_inplace_A000"] = {"gen_changed": m.gen != g0, "digest_changed": digest(m) != d0, "validate": r.validate()}
# C2: mutate via the anchor alias object held by ReshIdentity
m = Counting(); r = g.ReshIdentity(m); r.anchor(); g0, d0 = m.gen, digest(m)
r._anchor_entry["aliases"].append("intruder")
out["C2_alias_via_anchor_entry"] = {"gen_changed": m.gen != g0, "digest_changed": digest(m) != d0, "validate": r.validate()}
# C3: anchor() itself writes without record()
m = Counting(); r = g.ReshIdentity(m); r.anchor()
out["C3_anchor_writes_via_record"] = {"record_calls_during_anchor": m.gen}
# C4: A-000 absent before anchor -> anchor fabricates a fresh A-000
m = Counting(); del m.known["A-000"]; r = g.ReshIdentity(m); a = r.anchor()
out["C4_missing_A000"] = {"A000_keys_after": sorted(m.known["A-000"].keys()), "has_name_Governor": m.known["A-000"].get("name") == "Governor", "validate": r.validate()}
# C5 control: unchanged identity bytes
m = Counting(); r = g.ReshIdentity(m); r.anchor(); d0 = digest(m); _ = r.validate()
out["C5_control_unchanged"] = {"digest_changed": digest(m) != d0, "validate": r.validate()}
print(json.dumps(out, indent=1, sort_keys=True))
