"""E53 exploratory probe (Claude 13Z) on Genesis echo_governor_skeleton.py blob 63eb982. Read-only; no Genesis change.
Question (56G-u/N36): does any exchange() turn read A-000 / A-000-RESH, so that a transient (ABA) or net identity
mutation inside a turn could change the transcript? Lobby/matrix lookups are stubbed; identity objects are real."""
import sys, json, hashlib, copy
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
def digest(m):
    return hashlib.sha256(json.dumps({k: m.known.get(k) for k in ("A-000","A-000-RESH")}, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()[:16]
def make(mode):
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m); r.anchor()
    pe = object.__new__(g.PeCommunicator); pe.resh = r; pe.matrix = m; pe.exchanges = []
    pe._resh_knows = lambda w: {"word": w, "definition": "d", "semantic_chain": [w, "b", "c"], "study_type": "?", "ties": [], "department": "x", "entry_class": "y", "generality": 0.1, "curriculum": "", "neighborhood": []}
    state = {"turn": 0, "seen": []}
    def responds(word, said):
        state["turn"] += 1
        state["seen"].append(digest(m))
        if state["turn"] == 2 and mode != "control":
            a = m.known["A-000"]; old = copy.deepcopy(a)
            a["identity_meaning"] = "patched"; m.known["A-000-RESH"]["aliases"] = ["intruder"]
            state["seen"].append(digest(m))
            if mode == "aba":
                m.known["A-000"].clear(); m.known["A-000"].update(old)
                m.known["A-000-RESH"]["aliases"] = r._anchor_entry_aliases_backup
        return {"entity_vocab": ["v"], "own_chain": [word, "b"], "study_type": "?"}
    r._anchor_entry_aliases_backup = copy.deepcopy(m.known["A-000-RESH"].get("aliases"))
    pe._entity_responds = responds
    d0 = digest(m); log = pe.exchange("w", turns=4); d1 = digest(m)
    texts = json.dumps([[t["resh"], t["entity"]] for t in log], ensure_ascii=False)
    return {"entry_eq_exit_digest": d0 == d1, "digests_seen_inside": len(set(state["seen"])), "turns": len(log),
            "transcript_sha": hashlib.sha256(texts.encode()).hexdigest()[:16], "validate_after": r.validate(), "exchanges_recorded": len(pe.exchanges)}
out = {mode: make(mode) for mode in ("control", "aba", "net")}
out["transcript_identical_control_aba_net"] = len({out[k]["transcript_sha"] for k in ("control","aba","net")}) == 1
print(json.dumps(out, indent=1, sort_keys=True))
