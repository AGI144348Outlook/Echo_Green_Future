# Usage (scratch copy only): python3 -I -B DISC-002-genesis-e12-probe.py <copy of genesis src/echo_governor_skeleton.py, blob 63eb982>
# DISC-002 E12 (a)/(c)/(d)/(g) baseline for ChatGPT run 303's restart-safe anchor proposal; not a frozen test. Stub Ayin returns no entities, so no exchange runs.
import sys, json, importlib.util
spec = importlib.util.spec_from_file_location("gen", sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
class StubAyin:
    def agentive_entities(self, min_ties=1): return []
class StubLobby:
    agents = {}
calls = {"n": 0}
orig = g.ReshIdentity.anchor
def counted(self):
    calls["n"] += 1; return orig(self)
g.ReshIdentity.anchor = counted
def loglen(m):
    return {a: len(v) for a, v in vars(m).items() if isinstance(v, (list, dict)) and a != "known"}
out = {}
# (a) clean first anchor: any log/history trace?
m = g.AlgorithmMatrix(); before = loglen(m); known_before = set(m.known)
r = g.ReshIdentity(m, None); r.anchor()
out["a_container_len_changes"] = {k: loglen(m)[k] - before.get(k, 0) for k in loglen(m) if loglen(m)[k] != before.get(k, 0)}
out["a_new_known_keys"] = sorted(set(m.known) - known_before)
# (c) repeat anchor without any authorization: refused?
m.known["A-000"]["identity_meaning"] = "deliberately changed"
try:
    r.anchor(); out["c_second_anchor"] = "accepted"
except Exception as e:
    out["c_second_anchor"] = "refused: " + type(e).__name__
out["c_meaning_after"] = m.known["A-000"]["identity_meaning"]
# (d) fresh ReshIdentity around an already anchored matrix (restart case)
m = g.AlgorithmMatrix(); r1 = g.ReshIdentity(m, None); r1.anchor()
m.known["A-000"]["identity_meaning"] = "deliberately changed"
m.known["A-000"]["extra_field"] = "kept?"
resh_obj_before = id(m.known["A-000-RESH"])
r2 = g.ReshIdentity(m, None)
out["d_fresh_anchored_flag"] = r2._anchored
out["d_fresh_validate"] = r2.validate()
out["d_old_instance_validate"] = r1.validate()
pe = g.PeCommunicator(m, StubLobby(), r2, StubAyin()); calls["n"] = 0
pe.open_exchanges()
out["d_anchor_calls"] = calls["n"]
out["d_meaning_after"] = m.known["A-000"]["identity_meaning"]
out["d_extra_field_after"] = m.known["A-000"].get("extra_field")
out["d_resh_entry_replaced"] = id(m.known["A-000-RESH"]) != resh_obj_before
out["d_fresh_validate_after"] = r2.validate()
# (g) ordinary sub-agent write still accepted
m.record("A-900-SUB", {"name": "probe sub-agent", "status": "ACTIVE"})
out["g_subagent_record_present"] = "A-900-SUB" in m.known
print(json.dumps(out, indent=1, ensure_ascii=False))
