"""E92 probe (Claude, 2026-11-06 13Z): exact-byte replay of GPT #324 queue_multiseed_12z.py
(blob 2c9a20ee) plus source-injected mutants scored by the file's own 10 checks.
Usage: python3 -I e92.py <path-to-queue_multiseed_12z.py>
Reads the file, applies one textual mutation at a time, execs it in a fresh namespace.
No network, no writes."""
import sys, json, hashlib, types
src = open(sys.argv[1], encoding='utf-8').read()
print('source_sha256', hashlib.sha256(src.encode()).hexdigest())
MUT = [
 ('M0 none (baseline)', None, None),
 ('M1 cap 9->10', 'def sim(schedule,policy,seed,cap=9)', 'def sim(schedule,policy,seed,cap=10)'),
 ('M2 dwell 3->2', 'if t-at<3}', 'if t-at<2}'),
 ('M3 no expiry sweep', "   if t-born>=cap:terminal[gid]=('EXPIRED',t);waiting.remove(row)", "   pass"),
 ('M4 queue admits 2/step', 'active=waiting[:1];waiting=waiting[1:]', 'active=waiting[:2];waiting=waiting[2:]'),
 ('M5 retry limit 2->5', 'if tries<2:', 'if tries<5:'),
 ('M6 no glyph-conflict rule', ' and g not in [v[0] for v in live.values()]', ''),
 ('M7 drop behaves as retry-once', "elif policy=='drop':terminal[gid]=('DROPPED',t)", "elif policy=='drop' and tries>=1:terminal[gid]=('DROPPED',t)\n   elif policy=='drop':waiting.append((gid,born,g,s,tries+1))"),
 ('M8 flush window 12->0', 'range(len(schedule)+12)', 'range(len(schedule)+0)'),
 ('M9 seat = arrival%3 mod 2 (unbalanced)', 'waiting.append((t,t,t%27,t%2,0))', 'waiting.append((t,t,t%27,int(t%3==0),0))'),
]
for name, a, b in MUT:
    s = src
    if a is not None:
        assert s.count(a) == 1, (name, s.count(a))
        s = s.replace(a, b)
    ns = {'__name__': 'probe'}
    exec(compile(s, name, 'exec'), ns)
    r = ns['evaluate']()
    m = r['metrics']
    failed = sorted(k for k, v in r['checks'].items() if not v)
    print(f"{name:40s} passed {r['passed']}/10 failed={failed} "
          f"mean d/r/q={m['drop']['mean_accepted']:.3f}/{m['retry']['mean_accepted']:.3f}/{m['queue']['mean_accepted']:.3f} "
          f"maxwait q={m['queue']['max_wait']} expired q={m['queue']['expired']}")
# seed 1106 per-policy counts on the unmutated source
ns = {'__name__': 'probe'}; exec(compile(src, 'base', 'exec'), ns)
sch = [.2]*135+[.8]*135
for p in ('drop','retry','queue'):
    o = ns['oracle'](ns['sim'](sch, p, 1106))
    print('seed1106', p, o['count'], 'dropped', o['dropped'], 'expired', o['expired'], 'pending', o['pending'])
# by-construction checks: grants() never reads policy, so common_grants cannot fail
g_src = src.split('def grants', 1)[1].split('def sim', 1)[0]
print('grants_body_mentions_policy', 'policy' in g_src)

# ---- Part B: A-159 migrator kv_put_if_absent with an in-memory fake session (no network) ----
if len(sys.argv) > 2:
    import importlib.util
    mp = sys.argv[2]
    print('migrator_sha256', hashlib.sha256(open(mp, 'rb').read()).hexdigest())
    spec = importlib.util.spec_from_file_location('a159', mp)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    class Resp:
        def __init__(self, code, body=b''):
            self.status_code = code; self.content = body
        def raise_for_status(self):
            if self.status_code >= 400: raise RuntimeError(f'HTTP {self.status_code}')
        def json(self): return json.loads(self.content)
    class FakeKV:
        def __init__(self, store, race=None):
            self.store = store; self.race = race; self.log = []
        def get(self, url, timeout=None):
            k = url.rsplit('/', 1)[1]; self.log.append(('GET', k))
            r = Resp(200, self.store[k]) if k in self.store else Resp(404)
            if self.race: self.race(self.store, k); self.race = None   # another writer lands between GET and PUT
            return r
        def put(self, url, data=None, timeout=None):
            k = url.rsplit('/', 1)[1]; self.log.append(('PUT', k)); self.store[k] = data
            return Resp(200, b'{"success": true}')
    def mk(store, race=None):
        cf = object.__new__(mod.Cloudflare if hasattr(mod, 'Cloudflare') else [v for v in vars(mod).values() if isinstance(v, type) and hasattr(v, 'kv_put_if_absent')][0])
        cf.account_id = 'acct'; cf.session = FakeKV(store, race); return cf
    good = json.dumps({'id': 'A-000', 'name': 'Governor'}).encode()
    bad = json.dumps({'id': 'A-000', 'name': 'Impostor'}).encode()
    key = 'algorithm%3AA-000'
    # B1: remote already holds a DIFFERENT A-000 value -> skipped silently, no comparison
    s1 = {key: bad}; cf = mk(s1)
    w = cf.kv_put_if_absent('ns', 'algorithm:A-000', good.decode())
    print('B1 remote_mismatch: wrote', w, 'remote_after_is_impostor', s1[key] == bad, 'calls', cf.session.log)
    # B2: absent at GET, another writer puts between GET and PUT -> migrator overwrites it
    def racer(store, k): store[k] = bad
    s2 = {}; cf = mk(s2, racer)
    w = cf.kv_put_if_absent('ns', 'algorithm:A-000', good.decode())
    print('B2 check_then_write_race: wrote', w, 'other_writer_value_overwritten', s2[key] == good, 'calls', cf.session.log)
