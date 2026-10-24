"""F-001 §125 (Claude 08Z): probes G1-G6 of ChatGPT's format smoke gate v1 (blob 4620cc7).
Pre-registered on Issue #13 comment 6381744846 before execution. Synthetic fixtures only.
Usage: python3 -I -B CLAUDE-format-smoke-gate-v1-probes.py PATH/TO/smoke_gate.py
"""
import importlib.util, io, os, sys, tempfile, threading, zipfile, pyexpat

spec = importlib.util.spec_from_file_location('gate', sys.argv[1]); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
CONTAINER = b'<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="OEBPS/c.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'
def opf(items):
    man = ''.join(f'<item id="i{n}" href="{h}" media-type="{m}"/>' for n, (h, m) in enumerate(items))
    spine = ''.join(f'<itemref idref="i{n}"/>' for n, (h, m) in enumerate(items) if m == 'application/xhtml+xml')
    return ('<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
            f'<dc:title>T</dc:title></metadata><manifest>{man}</manifest><spine>{spine}</spine></package>').encode()
XHTML = b'<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>c</title></head><body><p>Text</p></body></html>'
def epub(members):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), b'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', CONTAINER, compress_type=zipfile.ZIP_DEFLATED)
        for name, data in members:
            z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
    return b.getvalue()
def pdf_min():
    objs = [b'1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n', b'2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n',
            b'3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 10 10]>>endobj\n']
    out = b'%PDF-1.4\n'; offs = []
    for o in objs: offs.append(len(out)); out += o
    x = len(out); out += b'xref\n0 4\n0000000000 65535 f \n' + b''.join(b'%010d 00000 n \n' % o for o in offs)
    return out + b'trailer<</Size 4/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF\n' % x
def run(name, fn):
    try: print(f'{name}: PASS {fn()}')
    except ValueError as e: print(f'{name}: FAIL {e}')
base = [('OEBPS/c.opf', opf([('ch1.xhtml', 'application/xhtml+xml')])), ('OEBPS/ch1.xhtml', XHTML)]
run('control EPUB', lambda: g.check_epub(epub(base)))
run('control PDF', lambda: g.check_pdf(pdf_min()))
# G1: corrupt a non-spine member's compressed bytes (CRC mismatch on read).
e = bytearray(epub(base + [('OEBPS/cover.jpg', b''.join(__import__('hashlib').sha256(b'%d' % n).digest() for n in range(125)))]))
i = e.find(b'OEBPS/cover.jpg') + len('OEBPS/cover.jpg')   # local header name end; incompressible 4,000 bytes follow
for k in range(i + 100, i + 120): e[k] ^= 0xFF
z = zipfile.ZipFile(io.BytesIO(bytes(e)))
print('G1 testzip() of the fixture:', z.testzip())
run('G1 corrupt non-spine member', lambda: g.check_epub(bytes(e)))
# G2: case-only duplicate members.
run('G2 case-only duplicates', lambda: g.check_epub(epub(base + [('OEBPS/CH1.xhtml', XHTML)])))
# G3: billion laughs in the spine XHTML.
ents = '<!ENTITY a0 "lol">' + ''.join(f'<!ENTITY a{n} "{("&a%d;" % (n-1)) * 10}">' for n in range(1, 10))
bomb = (f'<?xml version="1.0"?><!DOCTYPE html [{ents}]><html xmlns="http://www.w3.org/1999/xhtml"><body><p>&a9;</p></body></html>').encode()
print('G3 expat version:', pyexpat.EXPAT_VERSION)
t = threading.Thread(target=lambda: run('G3 billion laughs', lambda: g.check_epub(epub([base[0], ('OEBPS/ch1.xhtml', bomb)]))), daemon=True)
t.start(); t.join(20); print('G3 finished within 20 s:', not t.is_alive())
# G4: object-less "PDF" with only an xref keyword at the pointer.
fake = b'%PDF-1.4\nthis is not a pdf\n'; x = len(fake); fake += b'xref\nnothing\nstartxref\n%d\n%%%%EOF\n' % x
run('G4 object-less PDF', lambda: g.check_pdf(fake))
# G5: NUL padding after %%EOF.
run('G5 NUL padding after EOF', lambda: g.check_pdf(pdf_min() + b'\x00' * 16))
# G6: FIFO with no writer.
d = tempfile.mkdtemp(); fifo = os.path.join(d, 'book.epub'); os.mkfifo(fifo)
pdfp = os.path.join(d, 'book.pdf'); open(pdfp, 'wb').write(pdf_min())
r = {}; t = threading.Thread(target=lambda: r.setdefault('x', g.check_package(fifo, pdfp)), daemon=True); t.start(); t.join(10)
print('G6 returned within 10 s:', not t.is_alive(), r.get('x', {}).get('smoke'), r.get('x', {}).get('issues'))
