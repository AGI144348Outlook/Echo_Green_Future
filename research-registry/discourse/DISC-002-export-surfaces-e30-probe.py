"""DISC-002 E30 (Claude 12Z): ChatGPT run 321 candidate (its "E29"): diagnostic_snapshot vs authorized_export,
as in-process stand-ins wrapped around a scratch copy of Dev Suite pwa/python/algorithm_matrix.py (blob f7cf465).
Run: python3 -I -B this.py <scratch copy>. HMAC with a custodian key held outside the wrapper stands in for a
witness; not a signature scheme, not durable, not a frozen test; not executed against the deployed PWA."""
import hashlib, hmac, importlib.util, json, sys
spec = importlib.util.spec_from_file_location('am', sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
H = lambda o: hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
CUSTODIAN_KEY = b'custodian-stand-in'          # held by the custodian, never by the wrapper's caller
custodian = {'epoch': 2, 'head': None}        # independently held head (stand-in)

def token(actor, scope, op, epoch, head, key=CUSTODIAN_KEY):
    body = {'actor': actor, 'scope': scope, 'op': op, 'epoch': epoch, 'head': head}
    return dict(body, mac=hmac.new(key, json.dumps(body, sort_keys=True).encode(), 'sha256').hexdigest())

class Surfaces:
    def __init__(self, rt):
        self.rt = rt; rt.run_boot_handshake()
        self.content_pin = {k: H(v.get('storage')) for k, v in rt.sub_matrices.items()}  # pinned at boot
        custodian['head'] = H({'layout': rt.digest, 'content': self.content_pin})
    def diagnostic_snapshot(self):
        s = self.rt.snapshot()
        cur = {k: H(v.get('storage')) for k, v in self.rt.sub_matrices.items()}
        return {'system_state': s['system_state'], 'layout_ok': s['system_state']['alg_002_status'],
                'content': 'CONSISTENT' if cur == self.content_pin else 'MISMATCH',
                'sub_matrices': {k: {x: y for x, y in v.items() if x != 'storage'} for k, v in s['sub_matrices'].items()}}
    def authorized_export(self, tok, matrix_id):
        if not isinstance(tok, dict) or 'mac' not in tok: return ('DENY', 'no capability')
        body = {k: tok.get(k) for k in ('actor', 'scope', 'op', 'epoch', 'head')}
        good = hmac.new(CUSTODIAN_KEY, json.dumps(body, sort_keys=True).encode(), 'sha256').hexdigest()
        if not hmac.compare_digest(good, str(tok['mac'])): return ('DENY', 'capability MAC invalid')
        if body['op'] != 'export' or body['scope'] != matrix_id: return ('DENY', 'wrong scope or op')
        if body['epoch'] != custodian['epoch'] or body['head'] != custodian['head']: return ('DENY', 'stale epoch or head')
        d = self.diagnostic_snapshot()
        if not d['layout_ok']: return ('DENY', 'layout invalid')
        if d['content'] != 'CONSISTENT': return ('DENY', 'content UNPROVEN against pin')
        return ('ALLOW', self.rt.storage(matrix_id, actor=body['actor']))

def fresh():
    s = Surfaces(m.AlgorithmMatrixRuntime()); return s, next(iter(s.rt.sub_matrices))
def leak(r, secret): return secret in json.dumps(r, ensure_ascii=False, default=str)

s, k = fresh(); t = token(m.GOVERNOR, k, 'export', 2, custodian['head'])
print('base: export with valid token ->', s.authorized_export(t, k)[0])
print('dev-suite: storage(k) with NO actor argument ->', type(s.rt.storage(k)).__name__, '(actor defaults to GOVERNOR)')
s, k = fresh(); t = token(m.GOVERNOR, k, 'export', 2, custodian['head'])
s.rt.sub_matrices[k]['storage'] = {'secret': 'S3CRET'}; s.rt.sub_matrices[k]['glyph'] = 'X'
d = s.diagnostic_snapshot(); r = s.authorized_export(t, k)
print('(a) layout tamper: diagnostic layout_ok', d['layout_ok'], 'leaks storage', leak(d, 'S3CRET'), '| export', r, '| raw snapshot() leaks', leak(s.rt.snapshot(), 'S3CRET'))
s, k = fresh(); t = token(m.GOVERNOR, k, 'export', 2, custodian['head'])
s.rt.sub_matrices[k]['storage'] = {'secret': 'S3CRET'}
d = s.diagnostic_snapshot()
print('(b) storage tamper: alg_002', s.rt.alg_002(), '| content', d['content'], '| export', s.authorized_export(t, k), '| raw storage() returns tampered', s.rt.storage(k) == {'secret': 'S3CRET'})
s, k = fresh(); k2 = list(s.rt.sub_matrices)[1]
for name, tk in [('stale epoch', token(m.GOVERNOR, k, 'export', 1, custodian['head'])),
                 ('wrong scope', token(m.GOVERNOR, k2, 'export', 2, custodian['head'])),
                 ('stale head', token(m.GOVERNOR, k, 'export', 2, 'old')),
                 ('forged key', token(m.GOVERNOR, k, 'export', 2, custodian['head'], key=b'adapter-key'))]:
    r = s.authorized_export(tk, k); print('(c)', name, '->', r, '| leaks', leak(r, 'storage'))
print('(d) diagnostic snapshot as token ->', s.authorized_export(s.diagnostic_snapshot(), k))
