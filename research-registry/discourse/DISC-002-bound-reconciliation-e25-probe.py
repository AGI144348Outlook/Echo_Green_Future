"""DISC-002 E25 (Claude 07Z): digest-only vs witness-bound reconciliation; R7b retry; R7c overlap.
Pre-registered on Issue #13 comment 6381209283 before execution. In-process PROPOSED stand-ins only:
a dict A-000, a list ledger, an HMAC 'witness' with a fixed test key. Not Genesis or Dev Suite code; not frozen.
Usage: python3 -I -B DISC-002-bound-reconciliation-e25-probe.py
"""
import hashlib, hmac, json, sys

canon = lambda o: json.dumps(o, sort_keys=True, separators=(',', ':')).encode()
dig = lambda o: hashlib.sha256(canon(o)).hexdigest()
KEY = b'test-only-witness-key'
tag = lambda rid, aid, gen, post: hmac.new(KEY, canon([rid, aid, gen, post]), 'sha256').hexdigest()

def digest_only(ledger, a000):
    """Classify every intent without outcome by digest alone (the E24 reconciler)."""
    done = {e['rid'] for e in ledger if e['kind'] == 'outcome'}
    for e in ledger:
        if e['kind'] == 'intent' and e['rid'] not in done:
            d = dig(a000['state'])
            return 'ADMIT:post-image' if d == e['post'] else ('pre-image' if d == e['pre'] else 'unknown')
    return 'nothing-pending'

def bound(ledger, a000, head_gen):
    """Admit only a witness-tagged post-image for the ledger head generation."""
    done = {e['rid'] for e in ledger if e['kind'] == 'outcome'}
    for e in ledger:
        if e['kind'] == 'intent' and e['rid'] not in done:
            stamp = a000.get('stamp')
            if not stamp or not hmac.compare_digest(stamp['tag'], tag(stamp['rid'], stamp['aid'], stamp['gen'], dig(a000['state']))):
                return 'QUARANTINED:no-valid-witness-tag'
            if stamp['gen'] != head_gen:
                return 'STALE:tag-for-generation-%d-head-%d' % (stamp['gen'], head_gen)
            if stamp['rid'] != e['rid'] or dig(a000['state']) != e['post']:
                return 'QUARANTINED:tag-for-other-request'
            return 'ADMIT:bound'
    return 'nothing-pending'

res = {}
pre = {'name': 'Echo', 'generation': 1}; post = {'name': 'Echo', 'generation': 2, 'alias': 'R'}
intent = {'kind': 'intent', 'rid': 'q-1', 'aid': 'adapter-A', 'pre': dig(pre), 'post': dig(post), 'gen': 2}
# E25a/b: clean E24b rollback (A-000 back at pre-image, intent without outcome), then an unrelated writer
ledger = [intent]; a000 = {'state': dict(pre)}
a000['state'] = dict(post)                      # impostor recreates the exact post-image bytes, no stamp
res['E25a_digest_only'] = digest_only(ledger, a000)
res['E25b_bound'] = bound(ledger, a000, head_gen=2)
# E25c: ABA replay of an older, correctly tagged post-image after the head generation advanced to 3
old = {'state': dict(post), 'stamp': {'rid': 'q-1', 'aid': 'adapter-A', 'gen': 2, 'tag': tag('q-1', 'adapter-A', 2, dig(post))}}
ledger_c = [intent, {'kind': 'outcome', 'rid': 'q-1'}, {'kind': 'intent', 'rid': 'q-2', 'aid': 'adapter-A', 'pre': dig(post), 'post': 'x', 'gen': 3}]
res['E25c_digest_only'] = digest_only(ledger_c, old)
res['E25c_bound'] = bound(ledger_c, old, head_gen=3)

# E25d/e: a stand-in witness with idempotent retry and compare-and-swap on generation
class Witness:
    def __init__(self): self.gen, self.outcomes, self.consumed = 1, {}, set()
    def commit(self, rid, token, expected_gen, post_digest):
        if rid in self.outcomes:
            o = self.outcomes[rid]
            return o if o['post'] == post_digest else {'result': 'REJECTED:conflicting-retry', 'rid': rid}
        if token in self.consumed: return {'result': 'REJECTED:token-consumed'}
        if expected_gen != self.gen: return {'result': 'GENERATION_STALE', 'rid': rid}
        self.consumed.add(token); self.gen += 1
        o = {'result': 'COMMITTED', 'rid': rid, 'gen': self.gen, 'post': post_digest,
             'tag': tag(rid, 'adapter-A', self.gen, post_digest)}
        self.outcomes[rid] = o; return o
w = Witness()
first = w.commit('q-1', 't-1', 1, dig(post))
retry = w.commit('q-1', 't-1', 1, dig(post))      # reply lost, identical retry
res['E25d_identical_retry_same_outcome'] = retry == first and retry['result'] == 'COMMITTED'
res['E25d_tokens_consumed'] = len(w.consumed)
res['E25d_conflicting_retry'] = w.commit('q-1', 't-1', 1, dig({'name': 'Impostor'}))['result']
w2 = Witness()
a = w2.commit('q-a', 't-a', 1, dig({'v': 'a'})); b = w2.commit('q-b', 't-b', 1, dig({'v': 'b'}))
res['E25e_overlap'] = [a['result'], b['result']]
res['E25e_commits'] = sum(x['result'] == 'COMMITTED' for x in (a, b))
print(json.dumps({'python': sys.version.split()[0], 'results': res}, indent=1))
