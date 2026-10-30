#!/usr/bin/env python3
"""F-001 HOLD-only readable EPUB draft successor; no editorial approval implied.

Requires the unchanged F-001-EPUB-DRAFT-BUILDER-457.py beside this file.
Preserves exact source bytes and pins through the original builder's read_pinned.
Each nonempty source line is rendered as its own paragraph, with no rewriting.
"""
import html
import importlib.util
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

OLD = Path(__file__).with_name('F-001-EPUB-DRAFT-BUILDER-457.py')
spec = importlib.util.spec_from_file_location('f001_original_builder_457', OLD)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
_original_write = base.write_entry


def chapter(name, content):
    lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    paragraphs = ''.join('<p>' + html.escape(line, quote=True) + '</p>'
                         for line in lines if line.strip())
    return ('<?xml version="1.0" encoding="utf-8"?>'
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">'
            '<head><title>' + html.escape(name, quote=True) + '</title></head>'
            '<body><main id="main"><h1>' + html.escape(name, quote=True) + '</h1>'
            + paragraphs + '</main></body></html>').encode('utf-8')


def write_entry(z, name, data, stored=False):
    if name == 'OEBPS/content.opf':
        old_root = b'<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">'
        new_root = b'<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" prefix="schema: http://schema.org/">'
        old_end = b'</dc:language>'
        metadata = (b'</dc:language><dc:description>UNREVIEWED research notebook draft; claims and citations not approved.</dc:description>'
                    b'<meta property="schema:accessMode">textual</meta>'
                    b'<meta property="schema:accessibilityFeature">tableOfContents</meta>')
        if data.count(old_root) != 1 or data.count(old_end) != 1:
            raise ValueError('unexpected original EPUB package template')
        data = data.replace(old_root, new_root).replace(old_end, metadata)
    return _original_write(z, name, data, stored)


base.chapter = chapter
base.write_entry = write_entry
PINS = base.PINS
read_pinned = base.read_pinned
git_blob = base.git_blob


def build(source_dir, output, pins=None):
    """Fixture pins allowed only to local callers, never the production CLI."""
    result = base.build(source_dir, output, pins)
    result['formatting'] = 'one XHTML paragraph per nonblank source line'
    result['editorial_overlay_applied'] = False
    result['accessibility_reader_validated'] = False
    return result


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: python -I F-001-EPUB-READABLE-BUILDER-459.py EXACT_TAM_SOURCE_DIR NEW_OUTPUT.epub')
    try:
        print(json.dumps(build(sys.argv[1], sys.argv[2]), sort_keys=True))
    except (OSError, ValueError, UnicodeError, ET.ParseError) as e:
        print('F-001 HOLD / BUILD REFUSED: ' + str(e), file=sys.stderr)
        sys.exit(2)
