"""Claude probes R0-R12 for GPT's PROPOSED-f001-zip-layout-audit-v3.py (blob 9eb0566).

Records only. Pre-registered on Issue #13 (comment 6385121457) before execution.
Usage: python3 -I -B CLAUDE-zip-layout-audit-v3-probes.py PATH/TO/v3.py WORKDIR
Synthetic text only; no network; does not modify the audited file.
"""
import importlib.util
import io
import json
import os
import struct
import subprocess
import sys
import time
import unicodedata
import zipfile
import zlib

SRC, WORK = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('v3', SRC)
v3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3)

MIME = b'application/epub+zip'
CONTAINER = (b'<?xml version="1.0"?><container version="1.0" '
             b'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
             b'<rootfile full-path="OEBPS/c.opf" media-type="application/oebps-package+xml"/>'
             b'</rootfiles></container>')
TEXT = b'Synthetic chapter text for a probe. ' * 20


def raw_zip(members):
    """members: dicts name(bytes), data, method, flags, desc ('sig'|'nosig'|None),
    local_flags (optional), crc (optional override), share_with (index) ."""
    out = bytearray()
    central = []
    for m in members:
        data = m['data']
        crc = m.get('crc', zlib.crc32(data))
        if m['method'] == 8:
            c = zlib.compressobj(9, zlib.DEFLATED, -15)
            payload = c.compress(data) + c.flush()
        else:
            payload = data
        flags = m.get('flags', 0)
        lflags = m.get('local_flags', flags)
        off = len(out)
        if 'share_with' in m:
            central.append(dict(central[m['share_with']], name=m['name']))
            continue
        lc, lcomp, lun = (0, 0, 0) if flags & 8 else (crc, len(payload), len(data))
        out += struct.pack('<IHHHHHIIIHH', 0x04034b50, 20, lflags, m['method'], 0, 0x21,
                           lc, lcomp, lun, len(m['name']), 0) + m['name'] + payload
        if flags & 8:
            if m.get('desc') == 'sig':
                out += b'PK\x07\x08'
            out += struct.pack('<III', crc, len(payload), len(data))
        central.append(dict(name=m['name'], flags=flags, method=m['method'], crc=crc,
                            comp=len(payload), un=len(data), off=off))
    cd = len(out)
    for c in central:
        out += struct.pack('<IHHHHHHIIIHHHHHII', 0x02014b50, 20, 20, c['flags'], c['method'],
                           0, 0x21, c['crc'], c['comp'], c['un'], len(c['name']), 0, 0, 0, 0,
                           0, c['off']) + c['name']
    out += struct.pack('<IHHHHIIH', 0x06054b50, 0, 0, len(central), len(central),
                       len(out) - cd, cd, 0)
    return bytes(out)


def base(extra=()):
    return [dict(name=b'mimetype', data=MIME, method=0),
            dict(name=b'META-INF/container.xml', data=CONTAINER, method=8),
            *extra]


def zf_epub(dirs=False):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype', (2000, 1, 1, 0, 0, 0)), MIME, zipfile.ZIP_STORED)
        if dirs:
            z.writestr(zipfile.ZipInfo('META-INF/', (2000, 1, 1, 0, 0, 0)), b'')
            z.writestr(zipfile.ZipInfo('OEBPS/', (2000, 1, 1, 0, 0, 0)), b'')
        for n, d in (('META-INF/container.xml', CONTAINER), ('OEBPS/ch1.xhtml', TEXT)):
            z.writestr(zipfile.ZipInfo(n, (2000, 1, 1, 0, 0, 0)), d, zipfile.ZIP_DEFLATED)
    return buf.getvalue()


def verdict(data):
    r = v3.check_package_bytes(data)
    assert r['release'] == 'HOLD' and r['readiness'] == 'BLOCKED'
    return r['layout'], (r['issues'] or [''])[0]


cases = {}
cases['R0'] = zf_epub()
cases['R1'] = raw_zip(base([dict(name=b'OEBPS/a.txt', data=TEXT, method=0, flags=8, desc='sig')]))
cases['R2'] = raw_zip(base([dict(name=b'OEBPS/b.txt', data=TEXT, method=8, flags=8, desc='nosig')]))
cases['R3'] = raw_zip([dict(name=b'mimetype', data=MIME, method=0, flags=8, desc='sig'),
                       dict(name=b'META-INF/container.xml', data=CONTAINER, method=8)])
cases['R4'] = raw_zip(base([dict(name=b'OEBPS/c.txt', data=TEXT, method=8, flags=4)]))
cases['R5'] = raw_zip(base([dict(name=b'OEBPS/\xff\xfe.txt', data=TEXT, method=8, flags=0x800)]))
nfc = unicodedata.normalize('NFC', 'OEBPS/é.txt').encode()
nfd = unicodedata.normalize('NFD', 'OEBPS/é.txt').encode()
cases['R6'] = raw_zip(base([dict(name=nfc, data=TEXT, method=8, flags=0x800),
                            dict(name=nfd, data=TEXT, method=8, flags=0x800)]))
cases['R7'] = raw_zip(base([dict(name=b'OEBPS/d.txt', data=TEXT, method=8, flags=0, local_flags=2)]))
cases['R8'] = raw_zip(base([dict(name=b'OEBPS/e.txt', data=TEXT, method=8),
                            dict(name=b'OEBPS/f.txt', data=TEXT, method=8, share_with=2)]))
cases['R9'] = raw_zip(base([dict(name=b'OEBPS/g.txt', data=TEXT, method=8, crc=0x12345678)]))
cases['R10'] = zf_epub(dirs=True)

md = os.path.join(WORK, 'r11.md')
with open(md, 'w') as f:
    f.write('% Probe\n\n# One\n\nSynthetic text.\n')
r11 = os.path.join(WORK, 'r11.epub')
subprocess.run(['pandoc', md, '-o', r11, '--metadata', 'lang=en'], check=True,
               env=dict(os.environ, SOURCE_DATE_EPOCH='1700000000'))
cases['R11'] = open(r11, 'rb').read()

results = {}
for k, data in cases.items():
    before = bytes(data)
    results[k] = verdict(data)
    assert data == before

timings = {}
for n in (2000, 4000):
    data = raw_zip(base([dict(name=b'OEBPS/f%05d.txt' % i, data=b'x', method=0) for i in range(n)]))
    t = time.perf_counter()
    lay = verdict(data)
    timings[n] = (round(time.perf_counter() - t, 3), lay[0], len(data))
ratio = timings[4000][0] / timings[2000][0]
results['R12'] = dict(t2000=timings[2000], t4000=timings[4000], ratio=round(ratio, 2),
                      extrapolated_65534_s=round(timings[4000][0] * (65534 / 4000) ** 2, 1))
print(json.dumps(results, indent=1))
