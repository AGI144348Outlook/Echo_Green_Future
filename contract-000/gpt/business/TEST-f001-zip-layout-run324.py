"""F-001 Run 324 preregistered T0–T9 synthetic ZIP32 v3/v4 characterization.
Pre-test: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/43
No private data, paid inference, CI, publication, or source mutation.
Usage: python3 -I -B TEST-f001-zip-layout-run324.py V3.py V4.py
"""
import hashlib
import importlib.util
import io
import json
import struct
import sys
import time
import unicodedata
import zipfile
import zlib

V3_PATH, V4_PATH = sys.argv[1:3]
def load(path, label):
    spec = importlib.util.spec_from_file_location(label, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj
v3, v4 = load(V3_PATH, "auditv3"), load(V4_PATH, "auditv4")
MIME = b'application/epub+zip'
CONTAINER = (b'<?xml version="1.0"?><container version="1.0" '
             b'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
             b'<rootfile full-path="OEBPS/c.opf" media-type="application/oebps-package+xml"/>'
             b'</rootfiles></container>')
OPF = b'<package xmlns="http://www.idpf.org/2007/opf" version="3.0"></package>'
TEXT = b'<html xmlns="http://www.w3.org/1999/xhtml"><body>synthetic</body></html>'
BASE = [('mimetype', MIME, 0), ('META-INF/container.xml', CONTAINER, 8),
        ('OEBPS/c.opf', OPF, 8), ('OEBPS/ch.xhtml', TEXT, 8)]

def archive(extra=()):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        for name, data, method in [*BASE, *extra]:
            zi = zipfile.ZipInfo(name, (2000, 1, 1, 0, 0, 0))
            zi.compress_type = method
            z.writestr(zi, data)
    return b.getvalue()

def descriptor_mimetype():
    members = [(b'mimetype', MIME, 0, 8),
               (b'META-INF/container.xml', CONTAINER, 8, 0),
               (b'OEBPS/c.opf', OPF, 8, 0)]
    b = bytearray()
    cd = []
    for name, data, method, flags in members:
        off = len(b)
        crc = zlib.crc32(data)
        if method == 8:
            co = zlib.compressobj(6, zlib.DEFLATED, -15)
            payload = co.compress(data) + co.flush()
        else:
            payload = data
        lc, ls, lu = (0, 0, 0) if flags & 8 else (crc, len(payload), len(data))
        b.extend(struct.pack('<IHHHHHIIIHH', 0x04034b50, 20, flags, method, 0, 0,
                             lc, ls, lu, len(name), 0))
        b.extend(name)
        b.extend(payload)
        if flags & 8:
            b.extend(b'PK\\x07\\x08')
            b.extend(struct.pack('<III', crc, len(payload), len(data)))
        cd.append((name, crc, len(payload), len(data), method, flags, off))
    cd_start = len(b)
    for name, crc, comp, uncomp, method, flags, off in cd:
        b.extend(struct.pack('<IHHHHHHIIIHHHHHII', 0x02014b50, 20, 20, flags, method,
                             0, 0, crc, comp, uncomp, len(name), 0, 0, 0, 0, 0, off))
        b.extend(name)
    b.extend(struct.pack('<IHHHHIIH', 0x06054b50, 0, 0, len(cd), len(cd),
                         len(b)-cd_start, cd_start, 0))
    return bytes(b)

def bad_crc():
    b = bytearray(archive())
    struct.pack_into('<I', b, 14, 0)  # local mimetype CRC
    cd = b.find(b'PK\\x01\\x02')
    assert cd > 0
    struct.pack_into('<I', b, cd + 16, 0)  # central mimetype CRC
    return bytes(b)

def result(tool, data):
    before = hashlib.sha256(data).hexdigest()
    outcome = tool.check_package_bytes(data)
    assert hashlib.sha256(data).hexdigest() == before, 'input changed'
    assert outcome['release'] == 'HOLD'
    assert outcome['readiness'] == 'BLOCKED'
    assert outcome['publication_authorization'] == 'ABSENT'
    return outcome['layout'], outcome['issues'][:1], before

cases = {
 'T0': (archive(), 'PASS'),
 'T1': (archive([('OEBPS/a', b'x', 0), ('OEBPS/a/ch.xhtml', TEXT, 8)]), 'FAIL'),
 'T2': (archive([('OEBPS/a/', b'', 0), ('OEBPS/a/ch.xhtml', TEXT, 8)]), 'PASS'),
 'T3': (archive([('OEBPS/A', b'x', 0), ('OEBPS/a/ch.xhtml', TEXT, 8)]), 'FAIL'),
 'T4': (archive([('OEBPS/é', b'x', 0), ('OEBPS/e\\u0301/ch.xhtml', TEXT, 8)]), 'FAIL'),
 'T5': (archive([('OEBPS/a/one.xhtml', TEXT, 8), ('OEBPS/b/two.xhtml', TEXT, 8)]), 'PASS'),
 'T6': (descriptor_mimetype(), 'PASS'),
 'T8': (bad_crc(), 'FAIL'),
}
records = {}
failed = []
for key, (data, expected) in cases.items():
    v3lay, v3issues, pin = result(v3, data)
    v4lay, v4issues, _ = result(v4, data)
    ok = v3lay == v4lay == expected
    records[key] = dict(expected=expected, v3=v3lay, v4=v4lay,
                        v3_issues=v3issues, v4_issues=v4issues,
                        sha256=pin, ok=ok)
    if not ok:
        failed.append(key)

# T7: independent v4 scaling diagnostic. Do not run quadratic v3 at large n.
result(v4, archive([('OEBPS/warm%04d.txt' % i, b'x', 0) for i in range(50)]))
timings = {}
for n in (2000, 4000):
    data = archive([('OEBPS/f%05d.txt' % i, b'x', 0) for i in range(n)])
    start = time.perf_counter()
    layout, issues, pin = result(v4, data)
    elapsed = time.perf_counter() - start
    timings[n] = dict(seconds=round(elapsed, 5), layout=layout, bytes=len(data), sha256=pin)
ratio = timings[4000]['seconds'] / max(timings[2000]['seconds'], 1e-9)
ok = all(v['layout'] == 'PASS' and v['seconds'] < 5 for v in timings.values()) and ratio < 3
records['T7'] = dict(expected='PASS both; <5s each; ratio <3', measured=timings,
                     ratio=round(ratio, 4), ok=ok)
if not ok:
    failed.append('T7')
records['T9'] = dict(expected='all HOLD/BLOCKED, absent publication authorization, unchanged bytes',
                     checked_cases=list(cases)+['T7'], ok=True)
print(json.dumps(dict(schema='f001-run324-test-evidence/v1',
                      source_v3_sha256=hashlib.sha256(open(V3_PATH,'rb').read()).hexdigest(),
                      source_v4_sha256=hashlib.sha256(open(V4_PATH,'rb').read()).hexdigest(),
                      records=records, failures=failed, passed=10-len(failed), total=10),
                 indent=2, ensure_ascii=False))
raise SystemExit(0 if not failed else 1)
