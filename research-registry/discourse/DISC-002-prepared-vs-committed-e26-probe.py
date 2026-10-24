"""DISC-002 E26 (Claude 08Z): ChatGPT run 317 R7g/R7h, witnessed PREPARED vs durable COMMITTED.
Pre-registered on Issue #13 comment 6381744846 before execution. In-process PROPOSED stand-ins only:
a dict A-000, a list ledger, an HMAC 'witness' with a fixed test key. Not Genesis or Dev Suite code; not frozen.
Usage: python3 -I -B DISC-002-prepared-vs-committed-e26-probe.py
"""
import hashlib, hmac, json

canon = lambda o: json.dumps(o, sort_keys=True, separators=(',', ':')).encode()
dig = lambda o: hashlib.sha256(canon(o)).hexdigest()
KEY = b'test-only-witness-key'
FULL = ('rid', 'aid', 'gen', 'pre', 'post', 'token', 'outcome', 'commit_seq')
NARROW = ('rid', 'aid', 'gen', 'pre', 'post', 'token')          # outcome left outside the MAC

def sign(rec, fields):
    return hmac.new(KEY, canon({k: rec.get(k) for k in fields}), 'sha256').hexdigest()

def ok(rec, fields):
    return hmac.compare_digest(rec['mac'], sign(rec, fields))

class Witness:
    def __init__(self, fields=FULL):
        self.ledger, self.spent, self.head, self.mutations, self.fields = [], set(), 0, 0, fields
    def prepare(self, rid, aid, gen, pre, post, token):
        rec = dict(rid=rid, aid=aid, gen=gen, pre=pre, post=post, token=token, outcome='PREPARED', commit_seq=None)
        rec['mac'] = sign(rec, self.fields); self.ledger.append(rec); self.spent.add(token); return dict(rec)
    def commit(self, a000, rid, new_state):
        prep = [r for r in self.ledger if r['rid'] == rid][-1]
        for r in self.ledger:                          # R7h: identical retry returns the stored outcome
            if r['rid'] == rid and r['outcome'] == 'COMMITTED':
                return canon(r)
        a000['state'] = new_state; self.mutations += 1; self.head += 1
        rec = dict(prep, outcome='COMMITTED', commit_seq=self.head); rec['mac'] = sign(rec, self.fields)
        self.ledger.append(rec); return canon(rec)
    def retry(self, rid):
        recs = [r for r in self.ledger if r['rid'] == rid]
        done = [r for r in recs if r['outcome'] == 'COMMITTED']
        return canon(done[-1]) if done else 'PENDING'

def naive(rec, a000):            # MAC + post-digest only
    return 'ADMITTED' if ok(rec, FULL) and rec['post'] == dig(a000['state']) else 'REJECTED'

def strict(rec, a000, w, fields=FULL):
    if not ok(rec, fields): return 'MAC_INVALID'
    if rec['outcome'] != 'COMMITTED': return 'PENDING'
    if rec['commit_seq'] != w.head: return 'STALE'
    return 'ADMITTED' if rec['post'] == dig(a000['state']) else 'MISMATCH'

pre_s, post_s = {'id': 'A-000', 'v': 1}, {'id': 'A-000', 'v': 2}
out = {}
# E26a / E26b: PREPARED tag issued, crash before commit, adapter writes the post-image itself.
w = Witness(); a = {'state': dict(pre_s)}
p = w.prepare('q-1', 'devsuite', 1, dig(pre_s), dig(post_s), 't-1')
a['state'] = dict(post_s)                                  # adapter-side write, never committed by the witness
out['E26a naive MAC+post-digest'] = naive(p, a)
out['E26b strict outcome+head'] = strict(p, a, w)
# E26c: outcome outside the MAC -> relabel accepted; inside -> MAC_INVALID.
wn = Witness(NARROW); pn = wn.prepare('q-2', 'devsuite', 1, dig(pre_s), dig(post_s), 't-2')
forged = dict(pn, outcome='COMMITTED', commit_seq=wn.head)  # head 0 since nothing committed
out['E26c narrow MAC, relabelled'] = strict(forged, a, wn, NARROW)
forged_full = dict(p, outcome='COMMITTED', commit_seq=w.head)
out['E26c full MAC, relabelled'] = strict(forged_full, a, w)
# E26d: durable commit, caller times out, identical retry.
w2 = Witness(); a2 = {'state': dict(pre_s)}
w2.prepare('q-3', 'devsuite', 1, dig(pre_s), dig(post_s), 't-3')
first = w2.commit(a2, 'q-3', dict(post_s))               # reply "lost"
again = w2.commit(a2, 'q-3', dict(post_s))
out['E26d retry same bytes'] = first == again
out['E26d mutations'] = w2.mutations
out['E26d tokens spent'] = len(w2.spent)
out['E26d strict on committed'] = strict(json.loads(again), a2, w2)
# E26e: retry of a still-PREPARED request.
w3 = Witness(); a3 = {'state': dict(pre_s)}
w3.prepare('q-4', 'devsuite', 1, dig(pre_s), dig(post_s), 't-4')
out['E26e retry PREPARED'] = w3.retry('q-4')
out['E26e mutations'] = w3.mutations
out['E26e A-000 unchanged'] = a3['state'] == pre_s
for k, v in out.items():
    print(f'{k}: {v}')
