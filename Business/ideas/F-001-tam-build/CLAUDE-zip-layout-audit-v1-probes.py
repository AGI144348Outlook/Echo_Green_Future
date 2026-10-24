"""F-001 §129 (Claude 12Z): probes of ChatGPT's ZIP32 layout audit v1
(mirror-chatgpt-root blob a2360718). Synthetic fixtures only; records only.
Usage: python3 -I -B CLAUDE-zip-layout-audit-v1-probes.py PATH/TO/audit.py
Pre-registered on Issue #13 comment 6383943411 before execution."""
import hashlib, importlib.util, io, os, struct, sys, zipfile, zlib

spec = importlib.util.spec_from_file_location('audit', sys.argv[1])
audit = importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)
DT = (2026, 10, 24, 12, 0, 0)
PAY = hashlib.sha256(b'claude-12z').digest() * 128  # 4 KiB deterministic payload
OPF = (b'<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
       b'unique-identifier="id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
       b'<dc:identifier id="id">x</dc:identifier><dc:title>T</dc:title><dc:language>en</dc:language>'
       b'</metadata><manifest><item id="c" href="ch1.xhtml" media-type="application/xhtml+xml"/>'
       b'</manifest><spine><itemref idref="c"/></spine></package>')
CON = (b'<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:'
       b'xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" '
       b'media-type="application/oebps-package+xml"/></rootfiles></container>')
XH = b'<html xmlns="http://www.w3.org/1999/xhtml"><head><title>T</title></head><body><p>x</p></body></html>'

def zi(name, method=zipfile.ZIP_DEFLATED):
    i = zipfile.ZipInfo(name, DT); i.compress_type = method; return i

def epub(extra_names=(), comment=b'', central_comment=None, ch1_extra=None):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        z.writestr(zi('mimetype', zipfile.ZIP_STORED), b'application/epub+zip')
        z.writestr(zi('META-INF/container.xml'), CON)
        z.writestr(zi('OEBPS/content.opf'), OPF)
        i = zi('OEBPS/ch1.xhtml')
        if central_comment is not None: i.comment = central_comment
        z.writestr(i, XH)
        for n in extra_names: z.writestr(zi(n), XH)
        z.comment = comment
    return b.getvalue()

def local_extra(data, name, payload):
    """Insert payload into the local header extra field of `name`, shift later offsets."""
    zf = zipfile.ZipFile(io.BytesIO(data)); infos = zf.infolist()
    tgt = next(i for i in infos if i.filename == name)
    off = tgt.header_offset
    nlen, xlen = struct.unpack_from('<HH', data, off + 26)
    ins = off + 30 + nlen + xlen
    blob = struct.pack('<HH', 0xCAFE, len(payload)) + payload
    d = bytearray(data[:ins] + blob + data[ins:])
    struct.pack_into('<H', d, off + 28, xlen + len(blob))
    return fix_offsets(bytes(d), ins, len(blob))

def fix_offsets(d, at, delta):
    d = bytearray(d)
    e = d.rfind(b'PK\x05\x06')
    n, size, cdo = struct.unpack_from('<HII', d, e + 10)
    cdo2 = cdo + delta if cdo >= at else cdo
    struct.pack_into('<I', d, e + 16, cdo2)
    c = cdo2
    for _ in range(n):
        lo = struct.unpack_from('<I', d, c + 42)[0]
        if lo >= at: struct.pack_into('<I', d, c + 42, lo + delta)
        nl, xl, cl = struct.unpack_from('<HHH', d, c + 28)
        c += 46 + nl + xl + cl
    return bytes(d)

def deflate_tail(data, name, payload):
    """Append payload after the DEFLATE stream end inside `name`'s compressed extent."""
    zf = zipfile.ZipFile(io.BytesIO(data)); tgt = next(i for i in zf.infolist() if i.filename == name)
    off = tgt.header_offset; nlen, xlen = struct.unpack_from('<HH', data, off + 26)
    ins = off + 30 + nlen + xlen + tgt.compress_size
    d = bytearray(data[:ins] + payload + data[ins:])
    struct.pack_into('<I', d, off + 18, tgt.compress_size + len(payload))
    d = bytearray(fix_offsets(bytes(d), ins, len(payload)))
    e = d.rfind(b'PK\x05\x06'); n, cdo = struct.unpack_from('<H', d, e + 10)[0], struct.unpack_from('<I', d, e + 16)[0]
    c = cdo
    for _ in range(n):
        nl, xl, cl = struct.unpack_from('<HHH', d, c + 28)
        if bytes(d[c+46:c+46+nl]) == name.encode():
            struct.pack_into('<I', d, c + 20, tgt.compress_size + len(payload))
        c += 46 + nl + xl + cl
    return bytes(d)

def crafted_comment():
    base = epub()
    # fake EOCD inside the comment whose own comment-length ends exactly at EOF
    tail = b'XY'
    fake = b'PK\x05\x06' + b'\x01' * 16 + struct.pack('<H', len(tail))
    return epub(comment=fake + tail)

CASES = [
    ('L0', 'control minimal EPUB', lambda: epub(), 'PASS'),
    ('L1', 'J6 comment PK\\x05\\x06 + 18 non-zero bytes', lambda: epub(comment=b'PK\x05\x06' + b'\x01' * 18), 'PASS'),
    ('L2', 'comment with end-anchored fake EOCD', crafted_comment, 'FAIL'),
    ('L3', '4 KiB in local extra field of OEBPS/ch1.xhtml', lambda: local_extra(epub(), 'OEBPS/ch1.xhtml', PAY), 'PASS'),
    ('L4', '4 KiB in central file comment', lambda: epub(central_comment=PAY), 'PASS'),
    ('L5', '4 KiB EOCD archive comment', lambda: epub(comment=PAY), 'PASS'),
    ('L6', '4 KiB after DEFLATE end-of-stream inside compressed extent', lambda: deflate_tail(epub(), 'OEBPS/ch1.xhtml', PAY), 'PASS'),
    ('L7a', 'OCF-forbidden trailing full stop name', lambda: epub(extra_names=['OEBPS/ch1.xhtml.']), 'PASS'),
    ('L7b', 'OCF-forbidden colon name', lambda: epub(extra_names=['OEBPS/a:b.xhtml']), 'PASS'),
]
ok = 0
for cid, desc, make, pred in CASES:
    data = make(); h0 = hashlib.sha256(data).hexdigest()
    r = audit.check_package_bytes(data)
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z: zr = 'reads' if z.testzip() is None else 'crc-bad'
    except Exception as exc: zr = 'rejects:' + type(exc).__name__
    assert hashlib.sha256(data).hexdigest() == h0 and r['release'] == 'HOLD' and r['readiness'] == 'BLOCKED'
    hit = r['layout'] == pred; ok += hit
    print(f"{cid}\t{desc}\tpred={pred}\tobs={r['layout']}\t{'as predicted' if hit else 'NOT as predicted'}\t"
          f"zipfile={zr}\tlen={len(data)}\tsha256={h0[:12]}\t{'; '.join(r['issues'])}")
print(f'{ok}/{len(CASES)} as predicted')
