"""F-001 §130 probe (Claude, 2026-10-24T13Z): independent review of GPT strict
ZIP32 audit v2 (blob 0b78031). Synthetic fixtures only; records, not a gate.
Usage: python3 -I -B f001_v2_review_n_probe.py PATH/TO/PROPOSED-f001-zip-layout-audit-v2.py OUTDIR
"""
import importlib.util, io, json, os, resource, struct, subprocess, sys, zipfile, zlib, hashlib

AUDIT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
spec = importlib.util.spec_from_file_location('v2', AUDIT)
v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)
DT = (2026, 10, 24, 0, 0, 0)
CONTAINER = (b'<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
             b'<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
OPF = b'<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0"/>'
XHTML = b'<html xmlns="http://www.w3.org/1999/xhtml"><body><p>synthetic</p></body></html>'
results = []

def rec(cid, expect, res, note=''):
    results.append(dict(id=cid, expected=expect, layout=res['layout'], issues=res['issues'],
                        release=res['release'], as_expected=(res['layout'] == expect), note=note))

def build(extra_members=(), stored_names=()):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype', DT), b'application/epub+zip', zipfile.ZIP_STORED)
        for n, d in [('META-INF/container.xml', CONTAINER), ('OEBPS/content.opf', OPF), ('OEBPS/ch1.xhtml', XHTML), *extra_members]:
            z.writestr(zipfile.ZipInfo(n, DT), d, zipfile.ZIP_STORED if n in stored_names else zipfile.ZIP_DEFLATED)
    return b.getvalue()

# N0
n0 = build(); rec('N0', 'PASS', v2.check_package_bytes(n0))

# N1: STORED member, compressed extent = file_size + 4 KiB payload
def stored_smuggle():
    body, payload = XHTML, b'X' * 4096
    out, cd, entries = bytearray(), bytearray(), []
    members = [('mimetype', b'application/epub+zip', b''), ('META-INF/container.xml', CONTAINER, b''),
               ('OEBPS/content.opf', OPF, b''), ('OEBPS/ch1.xhtml', body, payload)]
    for name, data, tail in members:
        nb, off, crc = name.encode(), len(out), zlib.crc32(data)
        comp, unc = len(data) + len(tail), len(data)
        out += struct.pack('<IHHHHHIIIHH', 0x04034b50, 20, 0, 0, 0, 0x5821, crc, comp, unc, len(nb), 0) + nb + data + tail
        cd += struct.pack('<IHHHHHHIIIHHHHHII', 0x02014b50, 20, 20, 0, 0, 0, 0x5821, crc, comp, unc, len(nb), 0, 0, 0, 0, 0, off) + nb
    cdo = len(out); out += cd
    out += struct.pack('<IHHHHIIH', 0x06054b50, 0, 0, len(members), len(members), len(cd), cdo, 0)
    return bytes(out)
n1 = stored_smuggle(); r1 = v2.check_package_bytes(n1)
with zipfile.ZipFile(io.BytesIO(n1)) as z:
    rd = z.read('OEBPS/ch1.xhtml')
rec('N1', 'PASS', r1, f'zipfile read {len(rd)} bytes; payload present in archive: {n1.count(b"X"*4096)==1}')

# N2/N3: Info-ZIP
src = os.path.join(OUT, 'src'); os.makedirs(os.path.join(src, 'META-INF'), exist_ok=True); os.makedirs(os.path.join(src, 'OEBPS'), exist_ok=True)
for p, d in [('mimetype', b'application/epub+zip'), ('META-INF/container.xml', CONTAINER), ('OEBPS/content.opf', OPF), ('OEBPS/ch1.xhtml', XHTML)]:
    with open(os.path.join(src, p), 'wb') as f: f.write(d)
    os.utime(os.path.join(src, p), (1792800000, 1792800000))
def izip(path, flags0, flags9):
    if os.path.exists(path): os.remove(path)
    subprocess.run(['zip', '-q', *flags0, path, 'mimetype'], cwd=src, check=True)
    subprocess.run(['zip', '-q', '-r', *flags9, path, 'META-INF', 'OEBPS'], cwd=src, check=True)
    return open(path, 'rb').read()
n2 = izip(os.path.join(OUT, 'n2.epub'), ['-0'], ['-9']); rec('N2', 'FAIL', v2.check_package_bytes(n2))
n3 = izip(os.path.join(OUT, 'n3.epub'), ['-X0'], ['-X9']); rec('N3', 'PASS', v2.check_package_bytes(n3))

# N4: pandoc EPUB3
md = os.path.join(OUT, 'n4.md'); open(md, 'w').write('---\ntitle: Synthetic\nlang: en\n---\n\n# One\n\nSynthetic text.\n')
env = dict(os.environ, SOURCE_DATE_EPOCH='1792800000')
p = subprocess.run(['pandoc', md, '-o', os.path.join(OUT, 'n4.epub'), '-t', 'epub3'], env=env, capture_output=True)
if p.returncode == 0:
    n4 = open(os.path.join(OUT, 'n4.epub'), 'rb').read(); rec('N4', 'PASS', v2.check_package_bytes(n4), 'pandoc ' + subprocess.run(['pandoc', '--version'], capture_output=True, text=True).stdout.split('\n')[0])
else:
    results.append(dict(id='N4', expected='PASS', layout='NOT RUN', note=p.stderr.decode()[:200]))

# N5a: declared 65 MiB
big = b'\0' * (65 * 1024 * 1024)
n5a = build(extra_members=[('OEBPS/big.bin', big)]); rec('N5a', 'FAIL', v2.check_package_bytes(n5a))
# N5b: declared 1000 bytes, inflates to 65 MiB (patch sizes in local and central headers)
co = zlib.compressobj(9, zlib.DEFLATED, -15); comp = co.compress(big) + co.flush()
n5b = bytearray(build(extra_members=[('OEBPS/small.bin', b'\0' * 1000)]))
# rebuild with big payload but rewrite uncompressed size field to 1000
bb = io.BytesIO()
with zipfile.ZipFile(bb, 'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype', DT), b'application/epub+zip', zipfile.ZIP_STORED)
    for n, d in [('META-INF/container.xml', CONTAINER), ('OEBPS/content.opf', OPF), ('OEBPS/ch1.xhtml', XHTML)]:
        z.writestr(zipfile.ZipInfo(n, DT), d, zipfile.ZIP_DEFLATED)
pre = bytearray(bb.getvalue())
# hand-append bomb member before CD by rebuilding manually
eocd = pre.rfind(b'PK\x05\x06'); cnt, cds, cdo = struct.unpack_from('<HII', pre, eocd + 10)
locals_, cdir = pre[:cdo], pre[cdo:cdo + cds]
nb = b'OEBPS/small.bin'; crc = zlib.crc32(b'\0' * 1000); off = len(locals_)
locals_ += struct.pack('<IHHHHHIIIHH', 0x04034b50, 20, 0, 8, 0, 0x5821, crc, len(comp), 1000, len(nb), 0) + nb + comp
cdir += struct.pack('<IHHHHHHIIIHHHHHII', 0x02014b50, 20, 20, 0, 8, 0, 0x5821, crc, len(comp), 1000, len(nb), 0, 0, 0, 0, 0, off) + nb
n5b = bytes(locals_ + cdir + struct.pack('<IHHHHIIH', 0x06054b50, 0, 0, cnt + 1, cnt + 1, len(cdir), len(locals_), 0))
before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
r5b = v2.check_package_bytes(n5b)
after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rec('N5b', 'FAIL', r5b, f'maxrss KiB before {before} after {after}; compressed {len(comp)} bytes')

# N6: cp437 non-ASCII name without UTF-8 flag
# zipfile writes non-ASCII names as UTF-8 with flag 0x800, so patch an ASCII placeholder to cp437 byte 0x82 (e-acute)
n6 = build(extra_members=[('OEBPS/Q.xhtml', XHTML)]).replace(b'OEBPS/Q.xhtml', b'OEBPS/\x82.xhtml')
assert n6.count(b'OEBPS/\x82.xhtml') == 2
rec('N6', 'PASS', v2.check_package_bytes(n6), 'name bytes cp437 0x82, flag 0x800 unset')

# N7: CLI exit codes
def cli(path):
    return subprocess.run([sys.executable, '-I', '-B', AUDIT, path], capture_output=True).returncode
good = os.path.join(OUT, 'n0.epub'); open(good, 'wb').write(n0)
bad = os.path.join(OUT, 'n2c.epub'); open(bad, 'wb').write(n2)
link = os.path.join(OUT, 'link.epub')
if os.path.lexists(link): os.remove(link)
os.symlink(good, link)
codes = dict(pass_file=cli(good), fail_file=cli(bad), missing=cli(os.path.join(OUT, 'nope.epub')), symlink=cli(link))
results.append(dict(id='N7', expected=dict(pass_file=3, fail_file=1, missing=1, symlink=1), observed=codes,
                    as_expected=codes == dict(pass_file=3, fail_file=1, missing=1, symlink=1)))

for name, data in [('N0', n0), ('N1', n1), ('N5b', n5b), ('N6', n6)]:
    results.append(dict(id=name + '-sha256', sha256=hashlib.sha256(data).hexdigest()[:12]))
print(json.dumps(dict(python=sys.version.split()[0], audit_sha256=hashlib.sha256(open(AUDIT, 'rb').read()).hexdigest(), results=results), indent=1))
