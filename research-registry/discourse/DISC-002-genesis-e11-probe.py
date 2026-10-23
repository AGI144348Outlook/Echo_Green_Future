# Usage (scratch copy only): python3 -I -B DISC-002-genesis-e11-probe.py <copy of genesis src/echo_governor_skeleton.py, blob 63eb982>
# DISC-002 E11 (b)/(c)/(d) characterization of ReshIdentity.anchor() / PeCommunicator.open_exchanges(); not a frozen test. Stub Ayin returns no entities, so no exchange runs.
import sys, json, copy, importlib.util
spec = importlib.util.spec_from_file_location("gen", sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
class StubAyin:
    def agentive_entities(self, min_ties=1): return []
class StubLobby:
    agents = {}
out = {}
calls = {"n":0}
orig = g.ReshIdentity.anchor
def counted(self):
    calls["n"] += 1; return orig(self)
g.ReshIdentity.anchor = counted
def setup():
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m, None); pe = g.PeCommunicator(m, StubLobby(), r, StubAyin()); return m, r, pe
# (b)
m, r, pe = setup(); r.anchor(); calls["n"]=0
before_resh_id = id(m.known["A-000-RESH"]); keys_before = set(m.known["A-000"])
hist_before = len(getattr(m, "history", []) or [])
m.known["A-000"]["identity_symbol"] = "not-resh"
out["b_validate_after_mutation"] = r.validate()
pe.open_exchanges()
out["b_anchor_calls"] = calls["n"]
out["b_identity_symbol_after"] = m.known["A-000"]["identity_symbol"]
out["b_validate_after"] = r.validate()
out["b_resh_entry_replaced"] = id(m.known["A-000-RESH"]) != before_resh_id
out["b_history_len_change"] = len(getattr(m, "history", []) or []) - hist_before
out["b_pe_exchanges"] = len(pe.exchanges)
out["b_matrix_attrs_with_log"] = sorted(a for a in vars(m) if any(k in a.lower() for k in ("log","history","audit","ledger")))
# (c)
m, r, pe = setup(); r.anchor(); calls["n"]=0
m.known["A-000-RESH"]["aliases"] = ["A-000", "impostor"]
m.known["A-000"]["identity_glyph"] = "X"
out["c_validate_after_mutation"] = r.validate()
pe.open_exchanges()
out["c_anchor_calls"] = calls["n"]
out["c_aliases_after"] = m.known["A-000-RESH"]["aliases"]
out["c_glyph_after"] = m.known["A-000"]["identity_glyph"]
out["c_validate_after"] = r.validate()
# (d) repeated anchor overwrites
m, r, pe = setup(); r.anchor(); m.known["A-000"]["identity_meaning"]="changed"; r.anchor()
out["d_meaning_after_reanchor"] = m.known["A-000"]["identity_meaning"]
print(json.dumps(out, indent=1, ensure_ascii=False))
