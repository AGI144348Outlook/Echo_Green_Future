"""F-001 §128 K1-K6 probe of GPT dual format preflight v1 (blob 0980844) with its two pinned gates. Synthetic only.
usage: python3 -I -B this.py DIR   (DIR holds the wrapper and both pinned gate sources, unmodified)"""
import hashlib, importlib.util, io, json, os, struct, sys, tempfile, time, zipfile
SRC = os.path.abspath(sys.argv[1])
spec = importlib.util.spec_from_file_location('dual', os.path.join(SRC, 'PROPOSED-f001-dual-format-preflight-v1.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def members(z, mime_type=zipfile.ZIP_STORED, mime=b'application/epub+zip', dt=None):
    def zi(n): return zipfile.ZipInfo(n, date_time=dt) if dt else n
    z.writestr(zipfile.ZipInfo('mimetype', date_time=dt or (1980, 1, 1, 0, 0, 0)), mime, compress_type=mime_type)
    z.writestr(zi('META-INF/container.xml'), b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
    z.writestr(zi('OPS/package.opf'), b'<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/"><metadata><dc:title>T</dc:title></metadata><manifest><item id="c" href="c.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="c"/></spine></package>', compress_type=zipfile.ZIP_DEFLATED)
    z.writestr(zi('OPS/c.xhtml'), b'<html xmlns="http://www.w3.org/1999/xhtml"><body><p>x</p></body></html>', compress_type=zipfile.ZIP_DEFLATED)

def epub(**kw):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z: members(z, **kw)
    return b.getvalue()

def split(data):
    e = data.rfind(b'PK\x05\x06'); size, off = struct.unpack_from('<II', data, e + 12)
    return data[:off], data[off:off + size], bytearray(data[e:e + 22])

PAY = os.urandom(4096)
def k1():
    body, cd, eocd = split(epub()); struct.pack_into('<I', eocd, 16, len(body) + len(PAY)); return body + PAY + cd + bytes(eocd)
def k2():
    d = epub(); body, cd, eocd = split(d); struct.pack_into('<I', eocd, 16, len(d) + len(PAY)); return d + PAY + cd + bytes(eocd)
def k3(): return epub(mime_type=zipfile.ZIP_DEFLATED, mime=b'text/plain')

def pdf():
    out = bytearray(b'%PDF-1.4\n'); offs = []
    objs = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>', b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 10 10] >>']
    for i, o in enumerate(objs, 1): offs.append(len(out)); out += b'%d 0 obj\n' % i + o + b'\nendobj\n'
    x = len(out); out += b'xref\n0 4\n0000000000 65535 f \n' + b''.join(b'%010d 00000 n \n' % o for o in offs)
    out += b'trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % x
    return bytes(out)
def pdf_objectless():
    out = b'%PDF-1.4\n'; x = len(out)
    return out + b'xref\n0 1\n0000000000 65535 f \ntrailer\n<< /Size 1 >>\nstartxref\n%d\n%%%%EOF\n' % x

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def run(ep, pp, src=SRC):
    before = (sha(ep), sha(pp)); r = m.check(ep, pp, source_dir=src); after = (sha(ep), sha(pp))
    return {'composition': r['composition'], 'release': r['release'], 'readiness': r['readiness'],
            'gates': {k: v['status'] for k, v in r['gate_results'].items()}, 'issues': r['issues'], 'unchanged': before == after}

res = {}
with tempfile.TemporaryDirectory() as t:
    real = os.path.join(t, 'real'); os.mkdir(real)
    def w(name, data):
        p = os.path.join(real, name); open(p, 'wb').write(data); return p
    pp = w('b.pdf', pdf())
    res['K0'] = run(w('k0.epub', epub()), pp)
    res['K1'] = run(w('k1.epub', k1()), pp); res['K1']['payload_in_file'] = PAY in open(os.path.join(real, 'k1.epub'), 'rb').read()
    res['K2'] = run(w('k2.epub', k2()), pp)
    res['K3'] = run(w('k3.epub', k3()), pp)
    res['K4'] = run(os.path.join(real, 'k0.epub'), w('k4.pdf', pdf_objectless()))
    # K5: symlinked ancestors (input dir and gate source dir)
    os.symlink(real, os.path.join(t, 'inlink'))
    srcreal = os.path.join(t, 'srcreal'); os.mkdir(srcreal)
    for f in ('PROPOSED-f001-format-smoke-gate-v1.py', 'PROPOSED-f001-format-supplement-v2.py'):
        open(os.path.join(srcreal, f), 'wb').write(open(os.path.join(SRC, f), 'rb').read())
    os.symlink(srcreal, os.path.join(t, 'srclink'))
    res['K5_input_ancestor'] = run(os.path.join(t, 'inlink', 'k0.epub'), os.path.join(t, 'inlink', 'b.pdf'))
    res['K5_source_ancestor'] = run(os.path.join(real, 'k0.epub'), pp, src=os.path.join(t, 'srclink'))
    # final-component symlink control (matches GPT C4)
    os.symlink(os.path.join(real, 'k0.epub'), os.path.join(real, 'final.epub'))
    res['K5_final_component_control'] = run(os.path.join(real, 'final.epub'), pp)
# K6 determinism
a = epub(); time.sleep(2.2); b = epub()
fx = (2026, 1, 1, 0, 0, 0); c = epub(dt=fx); time.sleep(2.2); d = epub(dt=fx)
res['K6'] = {'default_timestamps_equal': hashlib.sha256(a).digest() == hashlib.sha256(b).digest(),
             'fixed_date_time_equal': hashlib.sha256(c).digest() == hashlib.sha256(d).digest(),
             'fixed_sha256': hashlib.sha256(c).hexdigest()}
res['python'] = sys.version.split()[0]
print(json.dumps(res, indent=1, sort_keys=True))
