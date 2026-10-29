"""E41 (Claude, DISC-002 2026-10-29T15Z): is there a caller-side A-000 guard in Genesis, and does
the Recess selector bind a decision-policy version? Read-only probe.
Usage: python3 -I this.py <genesis echo_governor_skeleton.py @63eb982> <dual-order-os echo-classroom dir @27acd51>
Genesis is NOT imported or run as a whole: only the named functions are extracted with ast and run
against stub objects. priority_cards.py is imported unmodified."""
import sys, ast, json, re, textwrap
src = open(sys.argv[1]).read(); tree = ast.parse(src)

def method(cls, name):
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == cls:
            for m in n.body:
                if isinstance(m, ast.FunctionDef) and m.name == name:
                    return textwrap.dedent(ast.get_source_segment(src, m))
    raise KeyError((cls, name))

def func(name):
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return ast.get_source_segment(src, n)
    raise KeyError(name)

out = {}
# G1: the only reader-side A-000 check before deployment (governor_validate_and_deploy)
ns = {'AlgorithmMatrix': object, 'SubAgentMatrix': None}; exec(func('governor_validate_and_deploy'), ns)
class Stub: pass
m = Stub(); m.regions = {}
m.known = {'A-000': {'name': 'not the Governor', 'status': 'ACTIVE', 'identity_symbol': 'tampered'},
           'A-101': {'name': 'tool'}}
out['G1_tampered_A000_passes_validation'] = ns['governor_validate_and_deploy'](m)

# G2: four registrars each cache their next A-id at construction; two built on the same matrix collide
known = {'A-000': {}, 'A-101': {}, 'A-158': {}}
gens = {}
for cls, name in [('HypothesisSandbox', '_scan_next_id'), ('CalculationEngine', '_find_next_id'),
                  ('FormulaIndexer', '_find_next_alg_id'), ('InformationAlgorithmizer', '_find_next_id')]:
    g = {}; exec(method(cls, name), g); s = Stub(); s.matrix = s.alg_matrix = Stub(); s.matrix.known = known
    gens[cls] = g[name](s)
# first id each class writes (source lines 2526/2538, 5596-5597, 6970-6972, 7191-7193)
first = {'HypothesisSandbox': gens['HypothesisSandbox'], 'CalculationEngine': gens['CalculationEngine'],
         'FormulaIndexer': gens['FormulaIndexer'] + 1, 'InformationAlgorithmizer': gens['InformationAlgorithmizer'] + 1}
out['G2_cached_next_id'] = gens; out['G2_first_written_id'] = {k: f'A-{v}' for k, v in first.items()}
rec = {}; exec(method('AlgorithmMatrix', 'record'), rec); mx = Stub(); mx.known = dict(known)
mx.known[f"A-{first['HypothesisSandbox']}"] = {'name': 'hypothesis H'}
mx.known[f"A-{first['CalculationEngine']}"] = {'name': 'law L'}   # same key, no guard, no event
out['G2_after_two_writes'] = mx.known[f"A-{first['HypothesisSandbox']}"]
rec['record'](mx, 'A-000', {'name': 'X', 'status': 'ACTIVE'}); out['G2_record_overwrites_A000'] = mx.known['A-000']

# P: Recess selector state restore
sys.path.insert(0, sys.argv[2]); from priority_cards import PriorityCards, personal_dictionary
ONE = [e for e in personal_dictionary() if e['id'] == 'speaker']
q = {'entity': {'sense': 'being', 'qualifications': [{'scope': 'definition-reading', 'sense': 'being', 'evidence': 't'}]}}
pc = PriorityCards(ONE); pc.set_recess(True); r1 = pc.tick(q); pc.review(r1['card'], 'accepted'); pc.hand_over()
st = pc.state()
out['P0_state_keys_with_version'] = {k: st[k] for k in st if k == 'format'}
# P1: serial rewound -> duplicate note id
s1 = json.loads(json.dumps(st)); s1['serial'] = 0
p1 = PriorityCards(ONE, s1); nid = p1.request_note('observation', 'x')
out['P1_duplicate_note_id'] = [n['id'] for n in p1.notes + p1.note_queue]
# P2: event history replaced on restore (no append-only check)
s2 = json.loads(json.dumps(st)); s2['events'] = []
out['P2_events_after_restore'] = PriorityCards(ONE, s2).events
# P3: forged visited key from a fresh state suppresses a never-visited candidate, anonymously
fresh = PriorityCards(ONE).state(); fresh['enabled'] = True
c = PriorityCards.coverage(ONE[0], q)
fresh['visited'] = [json.dumps(['speaker', 1, c['green'], c['yellow']], separators=(',', ':'))]
out['P3_forged_visited_tick'] = PriorityCards(ONE, fresh).tick(q)
# P4: arbitrary strings accepted in visited
fresh2 = PriorityCards(ONE).state(); fresh2['visited'] = ['not a key', 42]
try: PriorityCards(ONE, fresh2); out['P4_junk_visited_accepted'] = True
except Exception as e: out['P4_junk_visited_accepted'] = repr(e)
print(json.dumps(out, indent=1, default=str))
