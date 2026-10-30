#!/usr/bin/env python3
"""F-001 deterministic, HOLD-only EPUB3 draft builder (GPT Run457).

This preserves exact eight public TAM source files as escaped text, not a
historical fact-check, Markdown renderer, rights review or release approval.
Production CLI always enforces source Git blob pins. The optional pins argument
is for isolated synthetic fixtures and must not be exposed as a CLI flag.
"""
import hashlib
import html
import json
import os
import stat
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

PINS = {
    'README.md': '213bcfaf560dcc54fbb7ae79fad932e86b660357',
    'Article 1 Hacksilber': '237bd3335abdcc0f0465817dffe01ad6eaa86055',
    'Article 2 Water Weight Computes': 'ec657c3fa0f70da9686fb1ae52983d28f77c6c4c',
    'The Color Dyed and Dental Records': 'b525ad60ab37cb2d72ea43c40ba687b0fe2a348d',
    'Article 5': 'c8c1bf617c0d81389f6c2408ed975131695857ff',
    'Article 6': '662d745f0b9b41236d1053cdbaa9351f7c020dd0',
    'Article 10': 'e82be564872f636662652d34dcb8d3437559f84f',
    'Collective information': '710ad3cd4feeae7bafa329d7437a78df4c40cfa8',
}
MAX_BYTES = 5 * 1024 * 1024
STAMP = (1980, 1, 1, 0, 0, 0)
TITLE = 'F-001 TAM Protocol — UNREVIEWED WORKING DRAFT'


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def read_pinned(root, pins):
    if not root.is_dir() or root.is_symlink() or len(pins) != 8 or set(pins) != set(PINS):
        raise ValueError('exactly eight pinned TAM source names required')
    result = []
    for name, expected in pins.items():
        path = root / name
        flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
        fd = os.open(path, flags)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                raise ValueError('source is not a regular bounded file: ' + name)
            with os.fdopen(os.dup(fd), 'rb') as handle:
                data = handle.read(MAX_BYTES + 1)
        finally:
            os.close(fd)
        if len(data) > MAX_BYTES or git_blob(data) != expected:
            raise ValueError('source Git blob mismatch: ' + name)
        result.append((name, data.decode('utf-8', errors='strict')))
    return result


def chapter(name, content):
    paragraphs = content.replace('\r\n', '\n').replace('\r', '\n').split('\n\n')
    body = '\n'.join('<p>' + '<br/>'.join(html.escape(line, quote=True)
                    for line in block.split('\n')) + '</p>' for block in paragraphs if block.strip())
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="en"><head><title>'
            + html.escape(name) + '</title></head><body><h1>' + html.escape(name)
            + '</h1>' + body + '</body></html>').encode('utf-8')


def write_entry(z, name, data, stored=False):
    item = zipfile.ZipInfo(name, STAMP)
    item.compress_type = zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
    item.create_system = 3
    item.external_attr = 0o100644 << 16
    z.writestr(item, data)


def build(source_dir, output, pins=None):
    source_dir, output = Path(source_dir).absolute(), Path(output).absolute()
    if output.exists() or not output.parent.is_dir():
        raise ValueError('output must be a new file in an existing directory')
    if source_dir.resolve() == output.parent.resolve() or source_dir.resolve() in output.parent.resolve().parents:
        raise ValueError('output must be outside source tree')
    sources = read_pinned(source_dir, PINS if pins is None else pins)
    digest = hashlib.sha256(b'\n'.join(name.encode() + b'\0' + text.encode()
                                    for name, text in sources)).hexdigest()
    navlinks = ''.join(f'<li><a href="chapter-{i:02d}.xhtml">{html.escape(name)}</a></li>'
                       for i, (name, _) in enumerate(sources, 1))
    nav = ('<?xml version="1.0" encoding="utf-8"?>'
           '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">'
           '<head><title>Contents</title></head><body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>'
           + navlinks + '</ol></nav></body></html>').encode()
    items = '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
    items += ''.join(f'<item id="c{i}" href="chapter-{i:02d}.xhtml" media-type="application/xhtml+xml"/>'
                     for i in range(1, len(sources) + 1))
    spine = ''.join(f'<itemref idref="c{i}"/>' for i in range(1, len(sources) + 1))
    opf = ('<?xml version="1.0" encoding="utf-8"?>'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">'
           '<dc:identifier id="uid">urn:sha256:' + digest + '</dc:identifier><dc:title>' + html.escape(TITLE)
           + '</dc:title><dc:language>en</dc:language>'
           '<meta property="dcterms:modified">2026-10-29T00:00:00Z</meta></metadata>'
           '<manifest>' + items + '</manifest><spine>' + spine + '</spine></package>').encode()
    container = (b'<?xml version="1.0" encoding="utf-8"?>'
                 b'<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 b'<rootfiles><rootfile full-path="OEBPS/content.opf" '
                 b'media-type="application/oebps-package+xml"/></rootfiles></container>')
    try:
        with zipfile.ZipFile(output, 'x') as z:
            write_entry(z, 'mimetype', b'application/epub+zip', stored=True)
            write_entry(z, 'META-INF/container.xml', container)
            write_entry(z, 'OEBPS/content.opf', opf)
            write_entry(z, 'OEBPS/nav.xhtml', nav)
            for i, (name, content) in enumerate(sources, 1):
                write_entry(z, f'OEBPS/chapter-{i:02d}.xhtml', chapter(name, content))
        with zipfile.ZipFile(output) as z:
            for name in z.namelist():
                if name.endswith(('.xhtml', '.opf', '.xml')):
                    ET.fromstring(z.read(name))
    except BaseException:
        output.unlink(missing_ok=True)
        raise
    return {'project': 'F-001', 'status': 'HOLD / NOT LAUNCH-READY',
            'sources': len(sources), 'bytes': output.stat().st_size,
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'publication_authorized': False, 'reader_validated': False,
            'source_commit': 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9'}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: python -I F-001-EPUB-DRAFT-BUILDER-457.py EXACT_TAM_SOURCE_DIR NEW_OUTPUT.epub')
    try:
        print(json.dumps(build(sys.argv[1], sys.argv[2]), sort_keys=True))
    except (OSError, ValueError, UnicodeError, zipfile.BadZipFile, ET.ParseError) as e:
        print('F-001 HOLD / BUILD REFUSED: ' + str(e), file=sys.stderr)
        sys.exit(2)
