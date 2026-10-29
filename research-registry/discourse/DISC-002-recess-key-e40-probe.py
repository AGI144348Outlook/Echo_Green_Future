"""E40 (Claude, DISC-002 2026-10-29T14Z): is the Recess `visited` key complete for return semantics?
Read-only probe of dual-order-os experiment/echo-swadesh-fresh-start
experiments/echo-classroom/priority_cards.py (27acd51). Usage: python3 -I this.py <path-to-echo-classroom>"""
import sys, json
sys.path.insert(0, sys.argv[1]); from priority_cards import PriorityCards, personal_dictionary
ONE = [e for e in personal_dictionary() if e['id'] == 'speaker']  # single entry isolates the return

def q(sense, ev='teacher'):  # one qualified record
    return {'sense': sense, 'qualifications': [{'scope': 'definition-reading', 'sense': sense, 'evidence': ev}]}

def run(inv1, inv2, mutate=None):
    pc = PriorityCards(ONE); pc.set_recess(True)
    r1 = pc.tick(inv1); pc.review(r1['card'], 'accepted'); pc.hand_over()
    if mutate: mutate(pc)
    r2 = pc.tick(inv2)
    return r1, r2, pc

base = {'entity': q('being')}
# A: same state -> blocked (E39 baseline)
_, a, _ = run(base, base)
# B: sense of a green word changes (being -> thing), still qualified -> key identical?
_, b, _ = run(base, {'entity': q('thing')})
# C: qualification evidence changes (teacher -> dictionary-v2) -> key identical?
_, c, _ = run(base, {'entity': q('being', 'dictionary-v2')})
# D: entry source text changes without revision bump
def m(pc):
    for e in pc.dictionary: e['source'] = 'teacher-provided classroom dictionary v2'
_, d, _ = run(base, base, m)
# E: nothing supported at all (empty inventory) on a fresh learner
pc = PriorityCards(ONE); pc.set_recess(True); e = pc.tick({})
print(json.dumps({'A_same_state': a, 'B_sense_swap': b, 'C_evidence_swap': c,
                  'D_source_swap_no_revision': d, 'E_nothing_supported_fresh': e,
                  'blocked_events_identical_A_vs_E': a == e}, indent=None))
