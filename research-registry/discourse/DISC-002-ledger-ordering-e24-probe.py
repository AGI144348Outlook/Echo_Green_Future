"""DISC-002 E24 (Claude 06Z): ordering of A-000 mutation and ledger records.
In-process stand-ins only (dict A-000, list ledger with injectable failure).
Pre-registered on Issue #13 comment 6380654869. Not durability; shape only.
"""
import copy, hashlib, json

canon = lambda o: json.dumps(o, sort_keys=True, separators=(',', ':')).encode()
dig = lambda o: hashlib.sha256(canon(o)).hexdigest()

class Ledger:
    def __init__(self): self.rows = []; self.fail_on = None
    def append(self, row):
        if self.fail_on and row['kind'] == self.fail_on:
            raise IOError('ledger write failed: ' + row['kind'])
        self.rows.append(dict(row))

def fresh(): return {'id': 'A-000', 'identity_symbol': 'R', 'name': 'Resh', 'generation': 1}

def mutate_then_record(a, led, req):
    a.update(req['change'])
    led.append({'kind': 'outcome', 'req': req['id'], 'result': 'COMMITTED', 'post': dig(a)})
    return 'RECORDED'

def intent_apply_outcome(a, led, req, crash_after_apply=False):
    pre = copy.deepcopy(a)
    led.append({'kind': 'intent', 'req': req['id'], 'pre': dig(pre), 'post': dig({**pre, **req['change']})})
    a.update(req['change'])
    if crash_after_apply:
        raise SystemExit('simulated crash')  # no wrapper runs
    try:
        led.append({'kind': 'outcome', 'req': req['id'], 'result': 'COMMITTED', 'post': dig(a)})
        return 'RECORDED'
    except IOError as e:
        a.clear(); a.update(pre)
        return 'DENIED_UNRECORDED (%s)' % e

def reconcile(a, led):
    done = {r['req'] for r in led.rows if r['kind'] == 'outcome'}
    out = []
    for r in led.rows:
        if r['kind'] == 'intent' and r['req'] not in done:
            cur = dig(a)
            state = 'RECONCILE_PENDING:post-image' if cur == r['post'] else 'RECONCILE_PENDING:pre-image' if cur == r['pre'] else 'RECONCILE_PENDING:unknown'
            out.append((r['req'], state))
    return out

req = {'id': 'q-1', 'change': {'name': 'Impostor', 'generation': 2}}
res = {}
# E24a
a, led = fresh(), Ledger(); led.fail_on = 'outcome'; before = dig(a)
try: r = mutate_then_record(a, led, req)
except IOError as e: r = 'EXCEPTION:%s' % e
res['E24a'] = {'reported': r, 'a000_changed': dig(a) != before, 'receipts': len(led.rows)}
# E24b
a, led = fresh(), Ledger(); led.fail_on = 'outcome'; before = canon(a)
r = intent_apply_outcome(a, led, req)
res['E24b'] = {'reported': r, 'a000_byte_equal': canon(a) == before, 'ledger_kinds': [x['kind'] for x in led.rows]}
# E24c
a, led = fresh(), Ledger()
try: intent_apply_outcome(a, led, req, crash_after_apply=True)
except SystemExit: pass
res['E24c'] = {'reconcile': reconcile(a, led), 'a000_changed': a['name'] == 'Impostor'}
print(json.dumps(res, indent=1))
