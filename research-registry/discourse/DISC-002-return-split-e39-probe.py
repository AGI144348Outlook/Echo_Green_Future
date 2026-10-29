"""E39 probe (Claude, DISC-002 2026-10-29T13Z). Read-only use of dual-order-os
experiments/echo-classroom/priority_cards.py blob 27acd51 (branch
experiment/echo-swadesh-fresh-start @ df7d22c). Usage: python3 -I probe.py <path-to-priority_cards.py>
Question: does the classroom Recess selector distinguish a return to the same source
from a new encounter? Nothing is written anywhere."""
import sys, importlib.util, json
spec = importlib.util.spec_from_file_location('pc', sys.argv[1]); pc = importlib.util.module_from_spec(spec); spec.loader.exec_module(pc)
def run(steps):
    p = pc.PriorityCards(); p.set_recess(True); out = []
    for inv in steps:
        r = p.tick(inv)
        out.append((r['kind'], r.get('entry'), r.get('reason'), r.get('card')))
        if p.handover:
            for n in p.notes:
                if n['review']=='unreviewed': p.review(n['id'],'accepted')
            p.hand_over()
    return p, out
A = {'entity': {'seen': True}}                       # yellow word for 'speaker'/'addressee'
B = {'entity': {'seen': True}, 'the': {'seen': True}} # more coverage on the same entries
cases = {
 '1 same inventory x4': [A, A, A, A],
 '2 inventory grows, then same again': [A, A, B, B],
}
for name, steps in cases.items():
    p, out = run(steps)
    print(name); [print('   ', o) for o in out]
    print('    visited keys:', p.visited)
    print('    notes:', [(n['id'], n['source'], [ (e['entry'], e['revision'], e['source']) for e in n['evidence']]) for n in p.notes])
