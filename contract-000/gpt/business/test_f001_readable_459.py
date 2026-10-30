"""Prospectively documented synthetic tests only; not EPUBCheck or real TAM QA."""
import importlib.util
import json
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

spec = importlib.util.spec_from_file_location('readable', Path(__file__).with_name('F-001-EPUB-READABLE-BUILDER-459.py'))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
checks = []
def check(label, condition):
    checks.append([label, bool(condition)])
    if not condition:
        raise AssertionError(label)

with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    src = root/'src'; src.mkdir()
    out = root/'out'; out.mkdir()
    pins = {}
    fixture = 'Header & <test>\nSecond line with café and שלום\n\nThird line\n'
    for i, name in enumerate(b.PINS):
        data = (fixture + str(i) + '\n').encode('utf-8')
        (src/name).write_bytes(data)
        pins[name] = b.git_blob(data)
    first = b.build(src, out/'first.epub', pins)
    second = b.build(src, out/'second.epub', pins)
    check('eight sources', first['sources'] == 8)
    check('deterministic archive', first['sha256'] == second['sha256'])
    check('HOLD and no approval', first['status'] == 'HOLD / NOT LAUNCH-READY' and first['publication_authorized'] is False)
    check('no editorial overlay', first['editorial_overlay_applied'] is False)
    check('reader QA not claimed', first['reader_validated'] is False and first['accessibility_reader_validated'] is False)
    with zipfile.ZipFile(out/'first.epub') as z:
        names = z.namelist()
        check('12 entries', len(names) == 12)
        check('mimetype first uncompressed', names[0] == 'mimetype' and z.getinfo('mimetype').compress_type == zipfile.ZIP_STORED)
        check('mimetype bytes', z.read('mimetype') == b'application/epub+zip')
        check('XML parses', all(ET.fromstring(z.read(n)) is not None for n in names if n.endswith(('.xml', '.xhtml', '.opf'))))
        x = ET.fromstring(z.read('OEBPS/chapter-01.xhtml'))
        ns = {'x': 'http://www.w3.org/1999/xhtml'}
        ps = x.findall('.//x:main/x:p', ns)
        check('four nonblank source lines, four paragraphs', len(ps) == 4)  # Header, second, third, 0
        expected = [line for line in (fixture + '0\n').splitlines() if line.strip()]
        check('exact visible text line roundtrip', [p.text for p in ps] == expected)
        check('escaped special XML', b'&amp;' in z.read('OEBPS/chapter-01.xhtml') and b'&lt;test&gt;' in z.read('OEBPS/chapter-01.xhtml'))
        check('main landmark', x.find('.//x:main', ns) is not None)
        check('chapter language', x.attrib.get('{http://www.w3.org/XML/1998/namespace}lang') == 'en')
        opf = z.read('OEBPS/content.opf')
        check('textual accessMode', b'schema:accessMode' in opf and b'textual' in opf)
        check('TOC access feature', b'schema:accessibilityFeature' in opf and b'tableOfContents' in opf)
        check('draft warning', b'UNREVIEWED research notebook' in opf)
        check('eight nav links', z.read('OEBPS/nav.xhtml').count(b'<li>') == 8)
        check('eight spine refs', opf.count(b'<itemref') == 8)
    try:
        b.build(src, out/'first.epub', pins)
        raise AssertionError('overwrite accepted')
    except ValueError:
        check('overwrite refused', True)
    (src/'Article 5').write_bytes(b'tampered')
    try:
        b.build(src, out/'tampered.epub', pins)
        raise AssertionError('tampered accepted')
    except ValueError:
        check('tampered refused with no artifact', not (out/'tampered.epub').exists())
    (src/'Article 5').unlink()
    try:
        b.build(src, out/'missing.epub', pins)
        raise AssertionError('missing accepted')
    except FileNotFoundError:
        check('missing refused with no artifact', not (out/'missing.epub').exists())
    (src/'Article 5').write_bytes(b'bad \x00 xml')
    pins['Article 5'] = b.git_blob((src/'Article 5').read_bytes())
    try:
        b.build(src, out/'invalid.epub', pins)
        raise AssertionError('invalid XML accepted')
    except ET.ParseError:
        check('invalid XML cleaned', not (out/'invalid.epub').exists())
    try:
        b.build(src, out/'wrongpins.epub', dict(list(pins.items())[:-1]))
        raise AssertionError('incomplete pins accepted')
    except ValueError:
        check('incomplete pins refused', True)

print(json.dumps({'passed':sum(x[1] for x in checks), 'total':len(checks), 'cases':checks},ensure_ascii=False,indent=2))
