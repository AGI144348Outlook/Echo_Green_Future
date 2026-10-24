#!/usr/bin/env python3
"""Prospectively registered T0-T7 on GitHub Issue #38; synthetic only."""
import hashlib
import importlib.util
import io
import json
import re
import struct
import tempfile
import zipfile
from pathlib import Path

SOURCE = Path(__file__).with_name('PROPOSED-f001-format-supplement-v2.py')
spec = importlib.util.spec_from_file_location('f001_v2', SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def make_epub(mode):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        z.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', b'<container/>')
        z.writestr('OPS/package.opf', b'<package/>')
        z.writestr('OPS/chapter.xhtml', b'<html/>')
        z.writestr('images/cover.jpg', b'CRC_COVER_SENTINEL_001', compress_type=zipfile.ZIP_STORED)
        if mode == 'nfc':
            z.writestr('OPS/caf\u00e9.xhtml', b'1')
            z.writestr('OPS/cafe\u0301.xhtml', b'2')
        if mode == 'casefold':
            z.writestr('OPS/Chapter.xhtml', b'1')
            z.writestr('OPS/chapter.XHTML', b'2')
        if mode == 'hidden':
            z.writestr('hidden.bin', b'A' * 1048576, compress_type=zipfile.ZIP_DEFLATED)
        if mode == 'empty':
            z.writestr('empty.bin', b'', compress_type=zipfile.ZIP_DEFLATED)
    data = bytearray(buf.getvalue())
    if mode == 'hidden':
        # Central-directory CRC and uncompressed size are falsely declared zero.
        idx = data.index(b'PK\x01\x02', data.index(b'hidden.bin'))
        # The last central directory entry is hidden.bin, find its header precisely.
        entries = [m.start() for m in re.finditer(re.escape(b'PK\x01\x02'), data)]
        idx = entries[-1]
        assert data[idx + 46:idx + 56] == b'hidden.bin'
        struct.pack_into('<I', data, idx + 16, 0)
        struct.pack_into('<I', data, idx + 24, 0)
    if mode == 'crc':
        data = bytearray(bytes(data).replace(b'CRC_COVER_SENTINEL_001', b'XRC_COVER_SENTINEL_001', 1))
    if mode == 'prefix':
        data = bytearray(b'JUNK' + data)
    if mode == 'suffix':
        data.extend(b'JUNK')
    return bytes(data)


def make_pdf():
    b = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>']
    for n, obj in enumerate(objects, 1):
        offsets.append(len(b))
        b.extend(f'{n} 0 obj\n'.encode() + obj + b'\nendobj\n')
    xref = len(b)
    b.extend(f'xref\n0 {len(offsets)}\n'.encode())
    b.extend(b'0000000000 65535 f \n')
    for off in offsets[1:]:
        b.extend(f'{off:010d} 00000 n \n'.encode())
    b.extend(f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    return bytes(b)


def main():
    cases = [('T0', 'control', True), ('T1', 'nfc', False),
             ('T2', 'hidden', False), ('T3', 'empty', True),
             ('T4', 'casefold', False), ('T5', 'crc', False),
             ('T6', 'prefix', False), ('T7', 'suffix', False)]
    results = []
    with tempfile.TemporaryDirectory(prefix='f001-319-') as d:
        epub, pdf = Path(d) / 'book.epub', Path(d) / 'book.pdf'
        for case, mode, expected in cases:
            epub.write_bytes(make_epub(mode))
            pdf.write_bytes(make_pdf())
            before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (epub, pdf)]
            report = mod.check_package(epub, pdf)
            after = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (epub, pdf)]
            actual = report['supplement'] == 'PASS'
            ok = (actual == expected and before == after and
                  report['release'] == 'HOLD' and report['readiness'] == 'BLOCKED' and
                  report['publication_authorization'] == 'ABSENT' and
                  report['full_conformance_verified'] is False)
            results.append({'case': case, 'mode': mode, 'expected': 'PASS' if expected else 'FAIL',
                            'observed': report['supplement'], 'ok': ok,
                            'issues': report['issues'], 'unchanged': before == after})
    output = {'schema': 'f001-format-supplement-v2-test/v1', 'planned': len(cases),
              'matched': sum(x['ok'] for x in results), 'cases': results}
    print(json.dumps(output, sort_keys=True, indent=2))
    if output['matched'] != len(cases):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
