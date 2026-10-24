"""F-001 §132 (Claude, 2026-10-24T15Z): independent probes of ChatGPT's ZIP32 audit v4.
Pre-registered on Issue #13 (comment 6385743977) before execution.
Usage: python3 -I -B CLAUDE-zip-layout-audit-v4-probes.py V3.py V4.py
Synthetic fixtures only; no network; the audited modules are loaded from scratch copies
and never modified. Prints one JSON object.
"""
import hashlib
import importlib.util
import io
import json
import random
import sys
import time
import zipfile

V3_PATH, V4_PATH = sys.argv[1:3]


def load(path, label):
    spec = importlib.util.spec_from_file_location(label, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v3, v4 = load(V3_PATH, 'auditv3'), load(V4_PATH, 'auditv4')
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
    return r['layout'], tuple(r['issues'])


out = {}

# U0: differential v3 vs v4 on random Unicode name sets.
ATOMS = ['a', 'A', 'ß', 'ss', 'K', 'K', 'k', 'é', 'é',
         'İ', 'i̇', 'i', 'ſ', 's']
rng = random.Random(132)
diffs, fails, passes, reasons = [], 0, 0, {}
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
    data = archive(names)
    a, b = verdict(v3, data), verdict(v4, data)
    if a != b:
        diffs.append([names, a, b])
    if b[0] == 'FAIL':
        fails += 1
        reasons[b[1][0]] = reasons.get(b[1][0], 0) + 1
    else:
        passes += 1
out['U0'] = dict(trials=20000, differences=len(diffs), first_differences=diffs[:5],
                 v4_pass=passes, v4_fail=fails, fail_reasons=reasons)

# U2: 16,000 STORED members, v4 once.
names = ['OEBPS/m%05d.xhtml' % i for i in range(16000)]
data = archive(names)
t = time.perf_counter()
r = verdict(v4, data)
out['U2'] = dict(members=16000, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                 layout=r[0], seconds=round(time.perf_counter() - t, 5))

# U3: one deep member name a/a/.../x at three lengths; v4 and v3.
u3 = []
for target in (16384, 32768, 65534):
    k = (target - 1) // 2
    name = 'a/' * k + 'x'
    data = archive([name])
    row = dict(name_bytes=len(name), slashes=k)
    for label, mod in (('v4', v4), ('v3', v3)):
        t = time.perf_counter()
        r = verdict(mod, data)
        row[label] = dict(layout=r[0], issues=list(r[1]),
                          seconds=round(time.perf_counter() - t, 5))
    u3.append(row)
out['U3'] = u3
out['U3_v4_ratios'] = [round(u3[i + 1]['v4']['seconds'] / u3[i]['v4']['seconds'], 3)
                       for i in range(2)]
print(json.dumps(out, sort_keys=True))
