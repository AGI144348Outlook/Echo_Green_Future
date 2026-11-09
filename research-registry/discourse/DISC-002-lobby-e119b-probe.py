# DISC-002 e119b (Claude 12Z): ReshIdentity.anchor() third write target = hebrew_lobby resh agent definition_words.
# EXPLORATORY, NOT pre-registered (declared). Read-only on Genesis blob 63eb9829 from argv; stand-in lobby/agent via SimpleNamespace (harness-side).
# Run WITHOUT -I so PYTHONHASHSEED is honored: PYTHONHASHSEED=<n> python3 -B probe.py <skeleton.py>
import sys, importlib.util, types
spec = importlib.util.spec_from_file_location("g", sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
m = g.AlgorithmMatrix()
agent = types.SimpleNamespace(definition_words=["head", "beginning"])
lobby = types.SimpleNamespace(agents={"resh": agent})
r = g.ReshIdentity(m, lobby); r.anchor()
print("L1 lobby_mutated", agent.definition_words != ["head", "beginning"])
print("L2 order", ",".join(agent.definition_words))
r.anchor(); print("L3 len_after_replay", len(agent.definition_words))
