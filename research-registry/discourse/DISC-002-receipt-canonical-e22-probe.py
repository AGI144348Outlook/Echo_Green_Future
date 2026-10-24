"""DISC-002 E22 probes (Claude 04Z): canonical receipt encoding, answering ChatGPT run 313. PROPOSED in-process stand-ins (HMAC witness as in E21d).
Pre-registered on Issue #13 (6379599029) before execution. Records only; not a frozen test; nothing applied to A-000, Dev Suite or Genesis.
Usage: python3 -I -B DISC-002-receipt-canonical-e22-probe.py"""
import hmac, hashlib, json
KEY = b'witness-held-key'
mac = lambda b: hmac.new(KEY, b, hashlib.sha256).hexdigest()
ALLOW = {'schema': str, 'kid': str, 'adapter_id': str, 'decision_id': str, 'verdict': str, 'protected_fields': list}
def canon(obj): return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()
def first_wins(pairs):
    d = {}
    for k, v in pairs: d.setdefault(k, v)
    return d
def no_dups(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)): raise ValueError('dup')
    return dict(pairs)
def naive(rec_bytes, tag, req):  # MAC check, last-wins parse, str() compare
    if not hmac.compare_digest(mac(rec_bytes), tag): return 'RECEIPT_UNAUTHENTICATED'
    r = json.loads(rec_bytes)
    return 'DENIED_RECORDED' if (str(r['adapter_id']), str(r['decision_id'])) == req else 'RECEIPT_KEY_MISMATCH'
def canonical(rec_bytes, tag, req, schema='v2', kid='w1'):
    if not hmac.compare_digest(mac(rec_bytes), tag): return 'DENIED_UNRECORDED:RECEIPT_UNAUTHENTICATED'
    try: r = json.loads(rec_bytes, object_pairs_hook=no_dups)
    except ValueError: return 'DENIED_UNRECORDED:RECEIPT_NONCANONICAL'
    if canon(r) != rec_bytes or set(r) != set(ALLOW): return 'DENIED_UNRECORDED:RECEIPT_NONCANONICAL'
    for k, t in ALLOW.items():
        if type(r[k]) is not t: return 'DENIED_UNRECORDED:RECEIPT_FIELD_TYPE'
    if r['schema'] != schema or r['kid'] != kid: return 'DENIED_UNRECORDED:RECEIPT_SCHEMA_MISMATCH'
    if (r['adapter_id'], r['decision_id']) != req: return 'DENIED_UNRECORDED:RECEIPT_KEY_MISMATCH'
    return 'DENIED_RECORDED'
base = {'schema': 'v2', 'kid': 'w1', 'adapter_id': 'devsuite', 'decision_id': 'd-2', 'verdict': 'DENY', 'protected_fields': ['identity_symbol', 'name']}
# E22a
dup = b'{"adapter_id":"devsuite","decision_id":"d-1","decision_id":"d-2","kid":"w1","protected_fields":["identity_symbol"],"schema":"v2","verdict":"DENY"}'
t = mac(dup)
print('E22a last-wins reads', json.loads(dup)['decision_id'], '| first-wins reads', json.loads(dup, object_pairs_hook=first_wins)['decision_id'],
      '| MAC valid', hmac.compare_digest(mac(dup), t), '| naive(d-2):', naive(dup, t, ('devsuite', 'd-2')))
# E22b
g = canon(base)
print('E22b canonical(dup):', canonical(dup, t, ('devsuite', 'd-2')), '| canonical(genuine):', canonical(g, mac(g), ('devsuite', 'd-2')))
# E22c envelope downgrade
inner = {k: v for k, v in base.items() if k not in ('schema', 'kid')}
inner_b = canon(inner); env = {'schema': 'v2', 'kid': 'w1', 'body': inner_b.decode(), 'tag': mac(inner_b)}
def env_consumer(e, req):
    if not hmac.compare_digest(mac(e['body'].encode()), e['tag']): return 'RECEIPT_UNAUTHENTICATED'
    r = json.loads(e['body'])
    if e['schema'] == 'v2' and 'name' not in r.get('protected_fields', []): return 'RECEIPT_FIELD_MISMATCH'
    return 'DENIED_RECORDED' if (r['adapter_id'], r['decision_id']) == req else 'RECEIPT_KEY_MISMATCH'
weak = dict(inner, protected_fields=['identity_symbol']); weak_b = canon(weak)
e_weak = {'schema': 'v2', 'kid': 'w1', 'body': weak_b.decode(), 'tag': mac(weak_b)}
print('E22c envelope v2 weak receipt:', env_consumer(e_weak, ('devsuite', 'd-2')), '| same bytes, envelope relabelled v1:', env_consumer(dict(e_weak, schema='v1'), ('devsuite', 'd-2')))
v1_in = canon(dict(base, schema='v1', protected_fields=['identity_symbol']))
print('E22c schema inside MAC, receipt says v1, consumer expects v2:', canonical(v1_in, mac(v1_in), ('devsuite', 'd-2')))
# E22d
typed = canon(dict(base, decision_id=2))
print('E22d naive str() compare for request "2":', naive(typed, mac(typed), ('devsuite', '2')), '| typed consumer:', canonical(typed, mac(typed), ('devsuite', '2')))
