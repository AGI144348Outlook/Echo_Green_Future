#!/usr/bin/env python3
"""Run 318 Issue #37 preregistered S0-S5 synthetic cases; no real artifacts."""
import hashlib
import importlib.util
import io
import json
import re
import stat
import tempfile
import zipfile
from pathlib import Path

GATE = Path(__file__).with_name('PROPOSED-f001-format-supplement-v1.py')
spec = importlib.util.spec_from_file_location('f001_supplement', GATE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

CONTAINER = b'''<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="OPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'''
OPF = b'''<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Test</dc:title></metadata><manifest><item id="ch" href="chapter.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="ch"/></spine></package>'''
XHTML = b'''<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Test</title></head><body><p>Test content</p></body></html>'''


def epub_bytes(mode):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        z.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', CONTAINER)
        z.writestr('OPS/package.opf', OPF)
        z.writestr('OPS/chapter.xhtml', XHTML)
        z.writestr('images/cover.jpg', b'COVER_SENTINEL_1234', compress_type=zipfile.ZIP_STORED)
        if mode == 'casefold':
            z.writestr('Text/ch1.xhtml', XHTML)
            z.writestr('text/CH1.xhtml', XHTML)
        if mode == 'symlink':
            info = zipfile.ZipInfo('OPS/link.xhtml')
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            z.writestr(info, 'chapter.xhtml')
    data = b.getvalue()
    if mode == 'crc':
        needle = b'COVER_SENTINEL_1234'
        assert data.count(needle) == 1
        data = data.replace(needle, b'XOVER_SENTINEL_1234', 1)
    return data


def pdf_bytes(mode):
    if mode == 'fake-pdf':
        b = b'%PDF-1.4\n'
        off = len(b)
        return b + b'xref\n0 1\n0000000000 65535 f \ntrailer\n<< /Size 1 >>\n' + f'startxref\n{off}\n%%EOF\n'.encode()
    b = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    objects = [
        b'<< /Type /Catalog /Pages 2 0 R >>',
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>',
        b'<< /Length 0 >>\nstream\n\nendstream',
    ]
    for n, obj in enumerate(objects, 1):
        offsets.append(len(b))
        b.extend(f'{n} 0 obj\n'.encode() + obj + b'\nendobj\n')
    xref = len(b)
    b.extend(f'xref\n0 {len(offsets)}\n'.encode())
    b.extend(b'0000000000 65535 f \n')
    for off in offsets[1:]:
        b.extend(f'{off:010d} 00000 n \n'.encode())
    b.extend(f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    if mode == 'nul-tail':
        b.extend(b'\x00' * 12)
    return bytes(b)


def main():
    cases = [('S0', 'control', True), ('S1', 'crc', False),
             ('S2', 'casefold', False), ('S3', 'symlink', False),
             ('S4', 'fake-pdf', False), ('S5', 'nul-tail', True)]
    results = []
    with tempfile.TemporaryDirectory(prefix='f001-supplement-318-') as d:
        epub, pdf = Path(d) / 'book.epub', Path(d) / 'book.pdf'
        for case, mode, expected in cases:
            epub.write_bytes(epub_bytes(mode))
            pdf.write_bytes(pdf_bytes(mode))
            before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (epub, pdf)]
            result = mod.check_package(epub, pdf)
            after = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (epub, pdf)]
            observed = result['supplement'] == 'PASS'
            ok = (observed == expected and before == after
                  and result['release'] == 'HOLD' and result['readiness'] == 'BLOCKED'
                  and result['publication_authorization'] == 'ABSENT'
                  and result['full_conformance_verified'] is False)
            results.append({'case': case, 'mode': mode, 'expected': 'PASS' if expected else 'FAIL',
                            'observed': result['supplement'], 'ok': ok,
                            'issues': result['issues'], 'unchanged': before == after})
    report = {'schema': 'f001-supplement-test/v1', 'planned': len(cases),
              'matched': sum(x['ok'] for x in results), 'cases': results}
    print(json.dumps(report, sort_keys=True, indent=2))
    if report['matched'] != len(cases):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
