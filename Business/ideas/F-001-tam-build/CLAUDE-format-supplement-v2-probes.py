"""F-001 §127 J1-J6 probe of GPT format supplement v2 (blob 96223a9). Synthetic only."""
import hashlib, importlib.util, io, json, os, struct, sys, tempfile, zipfile
SRC = sys.argv[1]
spec = importlib.util.spec_from_file_location('v2', SRC); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def members(z, mime_type=zipfile.ZIP_STORED, mime=b'application/epub+zip'):
    z.writestr(zipfile.ZipInfo('mimetype'), mime, compress_type=mime_type)
    z.writestr('META-INF/container.xml', b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
    z.writestr('OPS/package.opf', b'<package xmlns="http://www.idpf.org/2007/opf"><metadata/><manifest><item id="c" href="c.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="c"/></spine></package>', compress_type=zipfile.ZIP_DEFLATED)
    z.writestr('OPS/c.xhtml', b'<html xmlns="http://www.w3.org/1999/xhtml"><body><p>x</p></body></html>', compress_type=zipfile.ZIP_DEFLATED)

def epub(**kw):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z: members(z, **kw)
    return b.getvalue()

def split(data):
    e = data.rfind(b'PK\x05\x06'); size, off = struct.unpack_from('<II', data, e + 12)
    return data[:off], data[off:off + size], bytearray(data[e:e + 22])

PAY = os.urandom(4096)
def j1():
    body, cd, eocd = split(epub()); struct.pack_into('<I', eocd, 16, len(body) + len(PAY))
    return body + PAY + cd + bytes(eocd)
def j2():
    d = epub(); body, cd, eocd = split(d); struct.pack_into('<I', eocd, 16, len(d) + len(PAY))
    return d + PAY + cd + bytes(eocd)
def j3(): return epub(mime_type=zipfile.ZIP_DEFLATED, mime=b'text/plain')
def j4():
    class NS(io.RawIOBase):  # non-seekable sink forces data descriptors
        def __init__(s): s.b = bytearray()
        def writable(s): return True
        def write(s, x): s.b += x; return len(x)
    s = NS()
    with zipfile.ZipFile(s, 'w') as z: members(z)
    d = bytes(s.b); fl = struct.unpack_from('<H', d, 6)[0]
    return d, fl
def j5():
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        members(z); z.writestr('OPS2', b'file'); z.writestr(zipfile.ZipInfo('OPS2/'), b'')
    return b.getvalue()
def j6():
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        members(z); z.comment = b'note PK\x05\x06' + b'\x11' * 18
    return b.getvalue()

def pdf():
    out = bytearray(b'%PDF-1.4\n'); offs = []
    objs = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>', b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 10 10] >>']
    for i, o in enumerate(objs, 1): offs.append(len(out)); out += b'%d 0 obj\n' % i + o + b'\nendobj\n'
    x = len(out); out += b'xref\n0 4\n0000000000 65535 f \n' + b''.join(b'%010d 00000 n \n' % o for o in offs)
    out += b'trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % x
    return bytes(out)

cases = {'J0': epub(), 'J1': j1(), 'J2': j2(), 'J3': j3(), 'J4': None, 'J5': j5(), 'J6': j6()}
d4, flag4 = j4(); cases['J4'] = d4
res = {}
with tempfile.TemporaryDirectory() as t:
    pp = os.path.join(t, 'b.pdf'); open(pp, 'wb').write(pdf())
    for k, d in cases.items():
        ep = os.path.join(t, k + '.epub'); open(ep, 'wb').write(d)
        before = hashlib.sha256(open(ep, 'rb').read()).hexdigest()
        r = m.check_package(ep, pp)
        after = hashlib.sha256(open(ep, 'rb').read()).hexdigest()
        zf_ok = None
        try:
            with zipfile.ZipFile(io.BytesIO(d)) as z: zf_ok = z.testzip() is None
        except Exception as e: zf_ok = 'zipfile:' + type(e).__name__
        res[k] = {'supplement': r['supplement'], 'issues': r['issues'], 'release': r['release'], 'unchanged': before == after, 'bytes': len(d), 'zipfile_reads_ok': zf_ok}
res['J4']['local_flag_bits'] = flag4
res['J1']['payload_in_file'] = PAY in cases['J1']; res['J2']['payload_in_file'] = PAY in cases['J2']
print(json.dumps(res, indent=1, sort_keys=True))
