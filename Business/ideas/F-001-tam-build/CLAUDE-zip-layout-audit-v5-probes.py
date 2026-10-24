"""F-001 §133 (Claude, 2026-10-24T16Z): independent probes of ChatGPT's ZIP32 audit v5.
Pre-registered on Issue #13 (comment 6386357117) before execution.
Usage: python3 -I -B CLAUDE-zip-layout-audit-v5-probes.py V3.py V4.py V5.py
Synthetic fixtures only; no network; the audited modules are loaded from scratch copies
and never modified. Prints one JSON object.
"""
import bisect
import hashlib
import importlib.util
import io
import json
import random
import statistics
import sys
import time
import unicodedata
import zipfile

V3_PATH, V4_PATH, V5_PATH = sys.argv[1:4]


def load(path, label):
    spec = importlib.util.spec_from_file_location(label, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v3, v4, v5 = load(V3_PATH, 'auditv3'), load(V4_PATH, 'auditv4'), load(V5_PATH, 'auditv5')
MIME = b'application/epub+zip'
BASE = [('mimetype', MIME, zipfile.ZIP_STORED),
        ('META-INF/container.xml', b'<container/>', zipfile.ZIP_DEFLATED)]


def archive(names):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        for name, data, method in BASE + [(n, b'' if n.endswith('/') else b'x',
                                           zipfile.ZIP_STORED) for n in names]:
            info = zipfile.ZipInfo(name, (2000, 1, 1, 0, 0, 0))
            info.compress_type = method
            z.writestr(info, data)
    return buf.getvalue()


def verdict(mod, data):
    before = hashlib.sha256(data).hexdigest()
    r = mod.check_package_bytes(data)
    assert hashlib.sha256(data).hexdigest() == before
    assert r['release'] == 'HOLD' and r['readiness'] == 'BLOCKED'
    assert r['publication_authorization'] == 'ABSENT'
    return r['layout'], tuple(r['issues'])


def timed(mod, data):
    t = time.perf_counter()
    r = verdict(mod, data)
    return r, time.perf_counter() - t


def ancestor_block(names):
    """Re-implementation of v5's sort+bisect block alone, timed separately."""
    allnames = ['mimetype', 'META-INF/container.xml'] + names
    t = time.perf_counter()
    normalized = {unicodedata.normalize('NFC', n.rstrip('/')).casefold() for n in allnames}
    s = sorted(normalized)
    for n in allnames:
        if n.endswith('/'):
            continue
        p = unicodedata.normalize('NFC', n).casefold() + '/'
        at = bisect.bisect_left(s, p)
        if at < len(s) and s[at].startswith(p):
            break
    return time.perf_counter() - t


out = {}

# V0: differential v3 / v4 / v5 on random Unicode name sets straddling '/' in sort order.
ATOMS = ['a', 'A', 'ß', 'ss', 'K', 'K', 'k', 'é', 'é',
         'İ', 'i̇', 'i', 'ſ', 's', '-', '.x', '0']
rng = random.Random(133)
diffs, reasons = [], {}
for trial in range(20000):
    names = []
    for _ in range(rng.randint(2, 6)):
        depth = rng.randint(1, 3)
        comps = [''.join(rng.choice(ATOMS) for _ in range(rng.randint(1, 2)))
                 for _ in range(depth)]
        name = 'OEBPS/' + '/'.join(comps)
        if rng.random() < 0.2:
            name += '/'
        names.append(name)
    try:
        data = archive(names)
    except ValueError:
        continue
    a, b, c = verdict(v3, data), verdict(v4, data), verdict(v5, data)
    if not (a == b == c):
        diffs.append([names, a, b, c])
    key = c[1][0] if c[1] else 'PASS'
    reasons[key] = reasons.get(key, 0) + 1
out['V0'] = dict(trials=20000, differences=len(diffs), first_differences=diffs[:5],
                 outcomes=reasons)

# V1: member-count scaling, median of 3, plus the ancestor block alone.
v1 = []
for n in (2000, 4000, 8000, 16000):
    names = ['OEBPS/m%05d.xhtml' % i for i in range(n)]
    data = archive(names)
    ts, layout = [], None
    for _ in range(3):
        r, s = timed(v5, data)
        ts.append(s)
        layout = r[0]
    blk = statistics.median(ancestor_block(names) for _ in range(3))
    v1.append(dict(members=n, layout=layout, median_s=round(statistics.median(ts), 5),
                   ancestor_block_s=round(blk, 5)))
out['V1'] = v1
out['V1_total_ratios'] = [round(v1[i + 1]['median_s'] / v1[i]['median_s'], 3) for i in range(3)]
out['V1_block_ratios'] = [round(v1[i + 1]['ancestor_block_s'] / v1[i]['ancestor_block_s'], 3)
                          for i in range(3)]
out['V1_block_share_16k'] = round(v1[-1]['ancestor_block_s'] / v1[-1]['median_s'], 4)

# V2: one deep member name a/a/.../x at three lengths; v5 and v4.
v2 = []
for target in (16384, 32768, 65528):
    k = (target - 1) // 2
    name = 'OEBPS/' + 'a/' * (k - 3) + 'x'
    data = archive([name])
    row = dict(name_bytes=len(name.encode()))
    for label, mod in (('v5', v5), ('v4', v4)):
        r, s = timed(mod, data)
        row[label] = dict(layout=r[0], issues=list(r[1]), seconds=round(s, 5))
    v2.append(row)
out['V2'] = v2
out['V2_v5_ratios'] = [round(v2[i + 1]['v5']['seconds'] / v2[i]['v5']['seconds'], 3) for i in range(2)]
out['V2_v4_ratios'] = [round(v2[i + 1]['v4']['seconds'] / v2[i]['v4']['seconds'], 3) for i in range(2)]

# V3: adversarial sort, long names sharing all but the last characters, no '/'.
# Names are stored twice (local + central header), so the 64 MiB archive bound
# caps the count near 480 at ~65,000 bytes each.
v3rows = []
for label, ch, nbytes in (('latin', 'a', 1), ('cjk', '一', 3)):
    body = ch * ((64990 - 6 - 10) // nbytes)
    names = ['OEBPS/' + body + '%06d' % i for i in range(480)]
    data = archive(names)
    r, s = timed(v5, data)
    v3rows.append(dict(kind=label, members=480, name_bytes=len(names[0].encode()),
                       archive_bytes=len(data), layout=r[0], issues=list(r[1]),
                       seconds=round(s, 4), ancestor_block_s=round(ancestor_block(names), 4)))
out['V3'] = v3rows

# V4: file 'OEBPS/d' plus directory entry 'OEBPS/d/' (and child) differ only by trailing '/'.
v4rows = {}
for case, names in (('file+dir', ['OEBPS/d', 'OEBPS/d/']),
                    ('file+child', ['OEBPS/d', 'OEBPS/d/c'])):
    data = archive(names)
    v4rows[case] = {lab: list(verdict(m, data)) for lab, m in (('v3', v3), ('v4', v4), ('v5', v5))}
out['V4'] = v4rows
print(json.dumps(out, sort_keys=True))
