"""E57 exploratory probe (Claude 17Z), setup copied from E56 (5e1b94f) on Genesis echo_governor_skeleton.py blob 63eb982. Read-only; no Genesis change.
Question (ChatGPT Run471 56G-y/N41, PROPOSED): when the per-entity callback faults, can anything in today's code tell the
caller whether graph effects happened? Arm A: callback writes a transitions edge, then raises on entity 2 turn 2.
Arm B (negative control): callback raises before any write. Arm C: fault-free baseline (does exchange() itself write?).
Real AlgorithmMatrix, ReshIdentity, PeCommunicator.exchange() and open_exchanges(); Lobby/Ayin are small stand-ins.
Usage: python3 -I probe.py <dir with skeleton>"""
import sys, json, types, hashlib
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
WORDS = ["seed", "alpha", "beta", "gamma", "delta"]; ENTS = ["seed", "alpha", "beta"]
class Injected(RuntimeError): pass
def gdigest(m):
    return hashlib.sha256(json.dumps({a: dict(b) for a, b in m.transitions.items()}, sort_keys=True).encode()).hexdigest()[:16]
def make(mode):
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m); r.anchor()
    for a, b in [("seed", "alpha"), ("alpha", "beta"), ("beta", "gamma"), ("gamma", "delta"), ("delta", "seed")]:
        m.transitions[a][b] += 3
    ag = lambda w: types.SimpleNamespace(department="d", entry_class="c", generality_score=0.5, definition_words=[w], ties=set(), neighborhood=None)
    lobby = types.SimpleNamespace(agents={w: ag(w) for w in WORDS}, study_groups={})
    ayin = types.SimpleNamespace(perceived={}, agentive_entities=lambda min_ties=1: [{"word": w} for w in ENTS])
    pe = g.PeCommunicator(m, lobby, r, ayin)
    orig = pe._entity_responds; calls = []
    def responds(word, said):
        calls.append(word)
        if mode != "C" and word == "alpha" and calls.count(word) == 2:
            if mode == "A": m.transitions["alpha"]["injected"] += 1   # partial side effect before the fault
            raise Injected("private text /home/x")
        return orig(word, said)
    pe._entity_responds = responds
    return pe, m, calls
def arm(mode):
    pe, m, calls = make(mode); before = gdigest(m); err = None; ret = None
    try: ret = pe.open_exchanges(max_entities=8, turns_each=4)
    except Injected as e: err = type(e).__name__
    after = gdigest(m)
    return {"raised": err, "returned": None if ret is None else len(ret), "graph_digest_changed": before != after,
            "injected_edge_present": "injected" in m.transitions.get("alpha", {}),
            "pe_exchanges_entities": [x.get("entity") for x in pe.exchanges], "entities_called": sorted(set(calls)),
            "resh_validate_after": pe.resh.validate()}
out = {k: arm(k) for k in "ABC"}
out["A_vs_B_distinguishable_by_caller"] = (out["A"]["raised"], out["A"]["returned"], out["A"]["pe_exchanges_entities"]) != (out["B"]["raised"], out["B"]["returned"], out["B"]["pe_exchanges_entities"])
print(json.dumps(out, indent=1, sort_keys=True))
