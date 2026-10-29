"""Synthetic A-000 recursive child / 3x3x3 glyph toy; not Genesis execution.
Prospective test plan: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/106
"""
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json

GLYPHS = tuple('אבגדהוזחטיכלמנסעפצקרשתךםןףץ')

class Cube:
    def __init__(self):
        assert len(GLYPHS) == len(set(GLYPHS)) == 27
        self.nodes = {(i//9, (i//3)%3, i%3): g for i,g in enumerate(GLYPHS)}
        self.loads = {g: () for g in GLYPHS}
        self.edges, self.candidates, self.events = {}, [], []

    def load(self, g, words):
        if g not in self.loads: raise ValueError('unknown glyph')
        self.loads[g] = tuple(words)
        self.events.append(('LOAD', g, tuple(words)))

    def combine(self, *glyphs):
        if not glyphs or any(g not in self.loads for g in glyphs):
            raise ValueError('unknown combination')
        spec = {'glyphs': glyphs, 'loads': [self.loads[g] for g in glyphs]}
        digest = sha256(json.dumps(spec, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        item = {'id': f'COM-{len(self.candidates)+1:04d}', 'digest': digest,
                'spec': spec, 'executed': False, 'status': 'INERT'}
        self.candidates.append(deepcopy(item))
        self.events.append(('COMBINE', item['id'], digest))
        return deepcopy(item)

class Index:
    def __init__(self):
        self.entries = {'Alg-000': {'id': 'Alg-000', 'parts': ['Alg-000'], 'active': True}}
        self.children, self.events = [], []

    def spawn(self, name):
        if name == 'Alg-000' or name in self.entries: raise ValueError('duplicate')
        child = {'id': name, 'parts': ['Alg-000', name], 'parent': 'Alg-000',
                 'version': 1, 'active': True}
        self.entries[name] = deepcopy(child)
        self.children.append(name)
        self.events.append(('SPAWN', name))
        return deepcopy(child)

    def replace(self, old, new, actor, reason):
        if old not in self.children or new in self.entries or new == 'Alg-000' or not actor or not reason:
            raise ValueError('invalid integration')
        child = {'id': new, 'parts': ['Alg-000', new], 'parent': 'Alg-000',
                 'version': self.entries[old]['version'] + 1,
                 'active': True, 'supersedes': old}
        self.entries[old]['active'] = False
        self.entries[new] = deepcopy(child)
        self.children[self.children.index(old)] = new
        self.events.append(('INTEGRATE_REPLACEMENT', old, new, actor, reason))
        return deepcopy(child)

def run():
    n = 0
    def check(v, name):
        nonlocal n
        assert v, name
        n += 1
    c, r = Cube(), Index()
    check(len(GLYPHS) == 27 and len(set(GLYPHS)) == 27, 'unique glyphs')
    check(len(c.nodes) == 27 and all(len(k) == 3 and all(x in range(3) for x in k) for k in c.nodes), 'fixed 3^3')
    before = deepcopy(c.nodes)
    c.load('ר', ['identity']); check(c.nodes == before, 'load leaves positions fixed')
    check(c.edges == {}, 'load creates no graph ties')
    a = c.combine('ר','ע'); check(a['status'] == 'INERT' and not a['executed'], 'no execution')
    check(c.events[-1][1] == a['id'] and len(c.candidates) == 1, 'separate log')
    b = c.combine('ר','ע'); check(a['digest'] == b['digest'] and a['id'] != b['id'], 'repeat digest')
    c.load('ע', ['perception']); d = c.combine('ר','ע')
    check(a['digest'] != d['digest'] and c.nodes == before, 'semantic load separate')
    try: c.combine('NOT-GLYPH'); check(False, 'reject unknown')
    except ValueError: check(len(c.candidates) == 3, 'reject unknown')
    x,y = r.spawn('Alg-001'),r.spawn('Alg-002')
    check(x['parts'] == ['Alg-000','Alg-001'] and y['parts'] == ['Alg-000','Alg-002'], 'two children')
    check(r.entries['Alg-000']['parts'] == ['Alg-000'], 'root identity retained')
    old = deepcopy(r.entries['Alg-001'])
    new = r.replace('Alg-001','Alg-003','reviewer','upgrade')
    check(new['supersedes'] == 'Alg-001' and new['version'] == 2 and r.events[-1][0] == 'INTEGRATE_REPLACEMENT', 'logged replacement')
    check(not r.entries['Alg-001']['active'] and r.entries['Alg-001']['parts'] == old['parts'], 'old retained')
    snap = deepcopy((r.entries,r.children,r.events))
    try: r.replace('Alg-002','Alg-004','','reason'); check(False,'deny missing actor')
    except ValueError: check(snap == (r.entries,r.children,r.events), 'deny without mutation')
    try: r.spawn('Alg-002'); check(False,'deny duplicate')
    except ValueError: check(len(r.entries) == 4, 'deny duplicate')
    check(r.entries['Alg-003']['parts'] == ['Alg-000','Alg-003'], 'new parent link')
    check(round((Decimal('13.7')-Decimal('11.4'))/Decimal('11.4')*100,2) == Decimal('20.18') and round((Decimal('13.7')-Decimal('11.4'))/Decimal('13.7')*100,2) == Decimal('16.79'), 'two mass denominators')
    check(Decimal('13.7')-Decimal('11.33') == Decimal('2.37'), 'separate standards')
    print(f'PASS {n}/{n} synthetic controls; no Genesis execution, no archaeological mass verification')

if __name__ == '__main__': run()
