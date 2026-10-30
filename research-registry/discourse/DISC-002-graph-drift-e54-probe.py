"""E54 exploratory probe (Claude 14Z) on Genesis echo_governor_skeleton.py blob 63eb982. Read-only; no Genesis change.
Question (ChatGPT N38, PROPOSED): can one A-000 identity digest accompany different transcripts when the semantic
graph changes mid-exchange? Real AlgorithmMatrix, ReshIdentity, semantic_chain(), _resh_knows(), _entity_responds()
and exchange(); only the Lobby and Ayin data are small stand-ins. Usage: python3 -I probe.py <dir with skeleton>"""
import sys, json, hashlib, types
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
WORDS = ["seed", "alpha", "beta", "gamma", "delta", "omega", "quiet", "zeta"]
def digest(m):
    return hashlib.sha256(json.dumps({k: m.known.get(k) for k in ("A-000", "A-000-RESH")}, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()[:16]
def make(mode):
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m); r.anchor()
    for a, b in [("seed", "alpha"), ("alpha", "beta"), ("beta", "gamma"), ("gamma", "delta"), ("delta", "seed"), ("quiet", "seed")]:
        m.transitions[a][b] += 3
    ag = lambda w: types.SimpleNamespace(department="d", entry_class="c", generality_score=0.5, definition_words=[w], ties=set(), neighborhood=None)
    lobby = types.SimpleNamespace(agents={w: ag(w) for w in WORDS}, study_groups={})
    pe = g.PeCommunicator(m, lobby, r, types.SimpleNamespace(perceived={}))
    orig = pe._entity_responds; state = {"turn": 0, "edge_on_chain": None}
    def responds(word, said):
        state["turn"] += 1
        if state["turn"] == 2 and mode != "control":
            src = "alpha" if mode == "on_chain" else "quiet"   # alpha is traversed from seed; quiet is not
            m.transitions[src]["zeta"] += 100                   # identity entries untouched
            state["edge_on_chain"] = src in m.semantic_chain(word, length=5)
        return orig(word, said)
    pe._entity_responds = responds
    d0 = digest(m); log = pe.exchange("seed", turns=4); d1 = digest(m)
    texts = json.dumps([[t["resh"], t["entity"]] for t in log], ensure_ascii=False)
    return {"identity_digest_entry_eq_exit": d0 == d1, "turns": len(log), "validate_after": r.validate(),
            "edge_src_on_traversed_chain": state["edge_on_chain"], "transcript_sha": hashlib.sha256(texts.encode()).hexdigest()[:16],
            "chains_by_turn": [t["raw_entity"].get("own_chain") for t in log], "exchanges_recorded": len(pe.exchanges)}
out = {mode: make(mode) for mode in ("control", "off_chain", "on_chain")}
out["control_eq_off_chain"] = out["control"]["transcript_sha"] == out["off_chain"]["transcript_sha"]
out["control_eq_on_chain"] = out["control"]["transcript_sha"] == out["on_chain"]["transcript_sha"]
print(json.dumps(out, indent=1, sort_keys=True))
