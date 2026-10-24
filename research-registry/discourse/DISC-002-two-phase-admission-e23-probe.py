"""DISC-002 E23 probes (Claude 05Z): two-phase witnessed admission, answering ChatGPT run 314. PROPOSED in-process stand-ins only.
Pre-registered on Issue #13 (6380141211) before execution. Records only; not a frozen test; nothing applied to A-000, Dev Suite or Genesis.
Usage: python3 -I -B DISC-002-two-phase-admission-e23-probe.py"""
import copy, json, threading
canon = lambda o: json.dumps(o, sort_keys=True, separators=(',', ':'))
class Witness:
    def __init__(s): s.gen = 1; s.lock = threading.Lock(); s.used = set()
    def decide(s, txn): return {'txn': txn, 'gen': s.gen, 'ok': True}
    def revoke(s): s.gen += 1
def store(): return {'A-000': {'identity_symbol': 'resh', 'name': 'Governor', 'gen_written': 0}}
out = {}
# E23a: check-at-decision only
w, st = Witness(), store(); d = w.decide('t1'); w.revoke()
if d['ok']: st['A-000']['name'] = 'Changed'; st['A-000']['gen_written'] = d['gen']
out['E23a_decision_time_check'] = {'committed': st['A-000']['name'] == 'Changed', 'gen_used': d['gen'], 'current_gen': w.gen}
# E23b: compare-and-commit
def cac(w, st, d, change):
    with w.lock:
        if d['gen'] != w.gen: return 'WITNESS_GENERATION_STALE'
        if d['txn'] in w.used: return 'TOKEN_ALREADY_USED'
        w.used.add(d['txn']); change(st); return 'COMMITTED'
w, st = Witness(), store(); before = canon(st); d = w.decide('t1'); w.revoke()
out['E23b_compare_and_commit'] = {'outcome': cac(w, st, d, lambda s: s['A-000'].update(name='Changed')), 'unchanged': canon(st) == before}
# E23c: boot rollback
def boot(st, rollback):
    snap = copy.deepcopy(st)
    try:
        st['primary_status'] = 'UNLOCKED'; st['permit'] = True
        raise RuntimeError('Infrastructure already instantiated')
    except RuntimeError as e:
        if rollback: st.clear(); st.update(snap)
        return str(e)
s1 = {'primary_status': 'LOCKED', 'permit': False}; b1 = canon(s1); boot(s1, False)
s2 = {'primary_status': 'LOCKED', 'permit': False}; b2 = canon(s2); boot(s2, True)
out['E23c_boot'] = {'no_rollback_left_mutations': canon(s1) != b1, 'no_rollback_state': s1, 'rollback_byte_equal': canon(s2) == b2}
# E23d: concurrent first-anchor claims, one token
w = Witness(); st = {'A-000': None}; d = w.decide('first-anchor'); res = {}; bar = threading.Barrier(2)
def claim(who):
    bar.wait(); res[who] = cac(w, st, d, lambda s: s.__setitem__('A-000', {'anchored_by': who}))
ts = [threading.Thread(target=claim, args=(x,)) for x in ('claimant-1', 'claimant-2')]
[t.start() for t in ts]; [t.join() for t in ts]
out['E23d_concurrent_first_anchor'] = {'outcomes': res, 'winners': sum(v == 'COMMITTED' for v in res.values()), 'anchored_by': st['A-000']['anchored_by']}
print(json.dumps(out, indent=1, sort_keys=True))
