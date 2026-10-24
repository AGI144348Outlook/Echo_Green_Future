"""DISC-002 E29 characterization of ChatGPT run 320 E27e (split view). In-process stand-ins, not a frozen test.
One adapter holds the MAC key and hands each verifier its own chain; verifiers check MAC, predecessor links and the local head."""
import hashlib, hmac, json
KEY = b'adapter-held-key'
def tag(rec): return hmac.new(KEY, json.dumps(rec, sort_keys=True).encode(), 'sha256').hexdigest()
def chain(post_digests, epoch=1):
    prev, out = '0' * 64, []
    for seq, post in enumerate(post_digests, 1):
        rec = {'epoch': epoch, 'seq': seq, 'prev': prev, 'post': post, 'outcome': 'COMMITTED'}
        rec['mac'] = tag(rec); out.append(rec)
        prev = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()
    return out, prev
def local_verify(recs, head):
    prev = '0' * 64
    for r in recs:
        body = {k: v for k, v in r.items() if k != 'mac'}
        if r['prev'] != prev or not hmac.compare_digest(r['mac'], tag(body)): return 'REJECT'
        prev = hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest()
    return 'ADMITTED' if prev == head else 'REJECT'
def compare(views, independent_head=None):
    seen = {}
    for recs in views:
        for r in recs: seen.setdefault((r['epoch'], r['seq']), set()).add(r['post'])
    if any(len(v) > 1 for v in seen.values()): return 'FORK_DETECTED'
    return 'CONSISTENT' if independent_head is not None else 'UNPROVEN'
a, ha = chain(['aa' * 32, 'bb' * 32]); b, hb = chain(['aa' * 32, 'cc' * 32])   # same epoch/seq 2, different post
res = {
 'V1_local': local_verify(a, ha), 'V2_local': local_verify(b, hb),
 'same_epoch_seq_different_post': (a[1]['epoch'], a[1]['seq']) == (b[1]['epoch'], b[1]['seq']) and a[1]['post'] != b[1]['post'],
 'compare_both_views_no_custodian': compare([a, b]),
 'compare_one_view_no_custodian': compare([a]),
 'compare_one_view_with_custodian_head_of_b': ('CONSISTENT' if ha == hb else 'MISMATCH_vs_custodian'),
}
print(json.dumps(res, indent=1, sort_keys=True))
