"""E56 exploratory probe (Claude 16Z), setup copied from E55 (3bd6123) on Genesis echo_governor_skeleton.py blob 63eb982. Read-only; no Genesis change.
Question (ChatGPT Run470 56G-x/N40, PROPOSED): on a fault-free batch, does a versioned envelope + legacy list adapter
give the list caller exactly what open_exchanges() gives today? Do repeated entity names keep separate attempts? Real AlgorithmMatrix, ReshIdentity, PeCommunicator.exchange() and
open_exchanges(); Lobby/Ayin are small stand-ins; the fault is injected by wrapping _entity_responds.
Usage: python3 -I probe.py <dir with skeleton>"""
import sys, json, types
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
WORDS = ["seed", "alpha", "beta", "gamma", "delta"]
ENTS = ["seed", "alpha", "beta"]
class Injected(RuntimeError): pass
def make(fail_word=None, fail_turn=2):
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
        if word == fail_word and calls.count(word) == fail_turn:
            raise Injected("secret-ish payload /home/x")   # stands in for a private exception text
        return orig(word, said)
    pe._entity_responds = responds
    return pe, calls

def envelope(pe, max_entities=5, turns_each=3, min_ties=1):   # PROPOSED shape, not Genesis code
    if not pe.resh.validate(): pe.resh.anchor()
    att = []
    for i, rec in enumerate(pe.ayin.agentive_entities(min_ties=min_ties)[:max_entities]):
        att.append({"attempt_index": i, "entity": rec["word"], "status": "COMPLETED", "log": pe.exchange(rec["word"], turns=turns_each)})
    return {"schema": "pe-batch/v1", "status": "COMPLETE", "attempts": att, "completed_count": len(att), "aborted_count": 0, "not_attempted_count": 0}
def legacy(pe, **kw):
    env = envelope(pe, **kw); return [{"entity": a["entity"], "log": a["log"]} for a in env["attempts"]], env
def caller_view(logs):   # what tests/pe_ayin_resh_communication.py lines 164-206 read from each record
    return [(r["entity"], [(t["resh"], t["entity"]) for t in r["log"]], r["log"][-1] if r["log"] else {}) for r in logs]
def run(ents):
    global ENTS; ENTS = ents
    pe1, _ = make(); old = pe1.open_exchanges(max_entities=8, turns_each=4)
    pe2, _ = make(); new, env = legacy(pe2, max_entities=8, turns_each=4)
    return {"entities": ents, "old_records": len(old), "adapter_records": len(new),
            "lists_equal": json.dumps(old, sort_keys=True, default=str) == json.dumps(new, sort_keys=True, default=str),
            "caller_view_equal": caller_view(old) == caller_view(new),
            "pe_exchanges_equal": json.dumps(pe1.exchanges, sort_keys=True, default=str) == json.dumps(pe2.exchanges, sort_keys=True, default=str),
            "pe_exchanges_len": len(pe1.exchanges), "envelope_attempt_indexes": [a["attempt_index"] for a in env["attempts"]],
            "envelope_is_list": isinstance(env, list)}
out = {"distinct": run(["seed", "alpha", "beta"]), "repeated_name": run(["seed", "seed", "alpha"])}
print(json.dumps(out, indent=1, sort_keys=True))
