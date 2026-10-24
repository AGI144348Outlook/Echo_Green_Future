"""F-001 §126 probe H1-H6 on GPT format supplement v1 (blob eeccb2d). Synthetic only."""
import importlib.util, io, os, sys, tempfile, zipfile, zlib, struct, hashlib, json, unicodedata
spec = importlib.util.spec_from_file_location('supp', sys.argv[1]); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)

def pdf(tail=b''):
    objs = [b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n',
            b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n',
            b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 10 10] >>\nendobj\n']
    out = b'%PDF-1.4\n'; offs = []
    for o in objs: offs.append(len(out)); out += o
    x = len(out)
    out += b'xref\n0 4\n0000000000 65535 f \n' + b''.join(b'%010d 00000 n \n' % o for o in offs)
    out += b'trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % x
    return out + tail

def spoof_pdf():
    body = b'1 0 obj\n2 0 obj\n3 0 obj\n/Type /Catalog\n/Type /Pages\n/Type /Page\n/Root 1 0 R\n'
    out = b'%PDF-1.4\n%junk\nstream\n' + body + b'endstream\n'
    x = len(out); out += b'xref\n0 0\nstartxref\n%d\n%%%%EOF\n' % x
    return out

def epub(names_data):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), b'application/epub+zip')
        for n, d in names_data: z.writestr(n, d, compress_type=zipfile.ZIP_DEFLATED)
    return b.getvalue()

def hidden_payload_epub():
    raw = epub([('a.xhtml', b'<html/>'), ('hidden.bin', b'\0' * (1 << 20))])
    # patch hidden.bin declared size and CRC to 0 in local header and central dir
    z = zipfile.ZipFile(io.BytesIO(raw)); info = z.getinfo('hidden.bin'); data = bytearray(raw)
    lh = info.header_offset; struct.pack_into('<I', data, lh + 14, 0); struct.pack_into('<I', data, lh + 22, 0)
    cd = raw.rfind(b'PK\x01\x02' + raw[raw.find(b'PK\x01\x02')+4:raw.find(b'PK\x01\x02')+4][:0])
    pos = 0
    while True:
        pos = raw.find(b'PK\x01\x02', pos)
        if pos < 0: break
        nlen = struct.unpack_from('<H', raw, pos + 28)[0]
        if raw[pos+46:pos+46+nlen] == b'hidden.bin':
            struct.pack_into('<I', data, pos + 16, 0); struct.pack_into('<I', data, pos + 24, 0)
        pos += 4
    return bytes(data)

def name_mismatch_epub():
    raw = bytearray(epub([('a.xhtml', b'<html/>')]))
    i = raw.find(b'a.xhtml')  # first occurrence = local header
    raw[i:i+7] = b'b.xhtml'; return bytes(raw)

def run(label, ep, pd):
    d = tempfile.mkdtemp(); e = os.path.join(d, 'b.epub'); p = os.path.join(d, 'b.pdf')
    open(e, 'wb').write(ep); open(p, 'wb').write(pd)
    h0 = [hashlib.sha256(open(x, 'rb').read()).hexdigest() for x in (e, p)]
    r = S.check_package(e, p)
    h1 = [hashlib.sha256(open(x, 'rb').read()).hexdigest() for x in (e, p)]
    print(json.dumps({'case': label, 'supplement': r['supplement'], 'issues': r['issues'], 'obs': r['observations'],
                      'hold': r['release'] == 'HOLD', 'unchanged': h0 == h1}))

good = epub([('a.xhtml', b'<html/>')])
run('control', good, pdf())
run('H1', good, spoof_pdf())
nfc = unicodedata.normalize('NFC', 'café.xhtml'); nfd = unicodedata.normalize('NFD', nfc)
run('H2', epub([(nfc, b'1'), (nfd, b'2')]), pdf())
run('H3', hidden_payload_epub(), pdf())
run('H4', name_mismatch_epub(), pdf())
poly = pdf() + good
run('H5', poly, poly)
run('H6-64', good, pdf(b'\0' * 63))   # pdf() already ends with one \n after %%EOF -> 64 tail bytes
run('H6-65', good, pdf(b'\0' * 64))
