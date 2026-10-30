"""E58 exploratory probe (Claude 18Z), setup copied from E57 (e96ad3a) on Genesis echo_governor_skeleton.py blob 63eb982. Read-only; no Genesis change.
Question (ChatGPT Run473 56G-aa/N43, PROPOSED): a reference observer of `matrix.transitions` (canonical JSON, sha256, version tag)
taken at attempt start and at abort. Run N43's four falsifiers on the real code, plus a write to A-000's own `known` entry.
Arms: ABA (write then restore an edge, then raise), OUTSIDE (write lobby + matrix.known["A-000"], then raise),
CHANGED (leave an edge, then raise), FAILED (callback puts an unserialisable key in transitions, then raise),
CONTROL (raise before any write). Classifier = N41 + 17Z one-way rule + N43 scope: only a changed digest upgrades.
Real AlgorithmMatrix, ReshIdentity, PeCommunicator.open_exchanges(); Lobby/Ayin are small stand-ins.
Usage: python3 -I probe.py <dir with skeleton>"""
import sys, json, types, hashlib
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
WORDS = ["seed", "alpha", "beta", "gamma", "delta"]; ENTS = ["seed", "alpha", "beta"]
SCOPE = {"scope": "matrix.transitions", "canon": "json-sort_keys-v1", "hash": "sha256"}
class Injected(RuntimeError): pass
def observe(m):
    try:
        return hashlib.sha256(json.dumps({a: dict(b) for a, b in m.transitions.items()}, sort_keys=True).encode()).hexdigest()[:16]
    except Exception:
        return None   # observation unavailable
def classify(before, after):
    if before is None or after is None: return {"graph_digest_changed": None, "effects": "UNKNOWN"}
    if before != after: return {"graph_digest_changed": True, "effects": "OBSERVED_CHANGED", "within": SCOPE["scope"]}
    return {"graph_digest_changed": False, "effects": "UNKNOWN"}
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
        if word == "alpha" and calls.count(word) == 2:
            if mode == "ABA":
                m.transitions["alpha"]["injected"] += 1; m.transitions["alpha"]["injected"] -= 1
                del m.transitions["alpha"]["injected"]
            elif mode == "OUTSIDE":
                lobby.agents["alpha"].ties.add("injected"); m.known["A-000"]["status"] = "TAMPERED"
            elif mode == "CHANGED":
                m.transitions["alpha"]["injected"] += 1
            elif mode == "FAILED":
                m.transitions["alpha"][("tuple", "key")] = 1
            raise Injected("private text /home/x")
        return orig(word, said)
    pe._entity_responds = responds
    return pe, m, lobby
def arm(mode):
    pe, m, lobby = make(mode); before = observe(m); err = None
    try: pe.open_exchanges(max_entities=8, turns_each=4)
    except Injected as e: err = type(e).__name__
    after = observe(m)
    return {"raised": err, **classify(before, after),
            "real_effect_outside_scope": bool(lobby.agents["alpha"].ties) or m.known["A-000"].get("status") != "ACTIVE",
            "a000_status_after": m.known["A-000"].get("status"), "resh_validate_after": pe.resh.validate(),
            "pe_exchanges_entities": [x.get("entity") for x in pe.exchanges]}
out = {"observer": SCOPE, **{k: arm(k) for k in ["CONTROL", "ABA", "OUTSIDE", "CHANGED", "FAILED"]}}
out["any_NONE_emitted"] = any(v.get("effects") == "NONE" for k, v in out.items() if isinstance(v, dict) and "effects" in v)
print(json.dumps(out, indent=1, sort_keys=True))
