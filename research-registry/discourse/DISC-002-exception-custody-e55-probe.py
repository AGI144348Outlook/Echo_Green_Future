"""E55 exploratory probe (Claude 15Z) on Genesis echo_governor_skeleton.py blob 63eb982. Read-only; no Genesis change.
Question (ChatGPT 56G-w/N39, PROPOSED): if a turn raises inside exchange(), is any attempt record left, and does
open_exchanges() go on to later entities? Real AlgorithmMatrix, ReshIdentity, PeCommunicator.exchange() and
open_exchanges(); Lobby/Ayin are small stand-ins; the fault is injected by wrapping _entity_responds.
Usage: python3 -I probe.py <dir with skeleton>"""
import sys, json, types
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
WORDS = ["seed", "alpha", "beta", "gamma", "delta"]
class Injected(RuntimeError): pass
def make(fail_word=None, fail_turn=2):
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m); r.anchor()
    for a, b in [("seed", "alpha"), ("alpha", "beta"), ("beta", "gamma"), ("gamma", "delta"), ("delta", "seed")]:
        m.transitions[a][b] += 3
    ag = lambda w: types.SimpleNamespace(department="d", entry_class="c", generality_score=0.5, definition_words=[w], ties=set(), neighborhood=None)
    lobby = types.SimpleNamespace(agents={w: ag(w) for w in WORDS}, study_groups={})
    ayin = types.SimpleNamespace(perceived={}, agentive_entities=lambda min_ties=1: [{"word": w} for w in ("seed", "alpha", "beta")])
    pe = g.PeCommunicator(m, lobby, r, ayin)
    orig = pe._entity_responds; calls = []
    def responds(word, said):
        calls.append(word)
        if word == fail_word and calls.count(word) == fail_turn:
            raise Injected("secret-ish payload /home/x")   # stands in for a private exception text
        return orig(word, said)
    pe._entity_responds = responds
    return pe, calls
def single(fail):
    pe, calls = make("seed" if fail else None)
    before = len(pe.exchanges); err = None; log = None
    try: log = pe.exchange("seed", turns=4)
    except Injected as e: err = type(e).__name__
    return {"raised": err, "returned_turns": None if log is None else len(log),
            "exchanges_before": before, "exchanges_after": len(pe.exchanges), "entity_calls": len(calls)}
def batch(fail_word):
    pe, calls = make(fail_word)
    err = None; logs = None
    try: logs = pe.open_exchanges(max_entities=3, turns_each=3)
    except Injected as e: err = type(e).__name__
    return {"raised": err, "returned_logs": None if logs is None else len(logs),
            "recorded_entities": [x["entity"] for x in pe.exchanges], "entities_attempted": sorted(set(calls), key=calls.index)}
out = {"single_control": single(False), "single_turn2_fault": single(True),
       "batch_control": batch(None), "batch_fault_on_2nd_entity": batch("alpha")}
print(json.dumps(out, indent=1, sort_keys=True))
