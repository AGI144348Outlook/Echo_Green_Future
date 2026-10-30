"""Synthetic fixture tests only. No actual TAM source or EPUB reader validation."""
import hashlib
import importlib.util
import json
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

spec = importlib.util.spec_from_file_location('builder', Path(__file__).with_name('F-001-EPUB-DRAFT-BUILDER-457.py'))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
checks = []
def check(name, cond):
    checks.append((name, bool(cond)))
    if not cond: raise AssertionError(name)
with tempfile.TemporaryDirectory() as d:
    root = Path(d); source = root/'source'; source.mkdir(); output = root/'out'; output.mkdir()
    pins = {}
    for i, name in enumerate(b.PINS):
        data = ('Example & <demo> "'+str(i)+'"\n\nSecond paragraph').encode()
        (source/name).write_bytes(data)
        pins[name] = b.git_blob(data)
    first = b.build(source, output/'one.epub', pins)
    second = b.build(source, output/'two.epub', pins)
    check('eight sources', first['sources'] == 8)
    check('deterministic byte hashes', first['sha256'] == second['sha256'])
    check('HOLD not launch-ready', first['status']=='HOLD / NOT LAUNCH-READY' and not first['publication_authorized'])
    with zipfile.ZipFile(output/'one.epub') as z:
        names = z.namelist()
        check('mimetype first and stored', names[0]=='mimetype' and z.getinfo('mimetype').compress_type==zipfile.ZIP_STORED)
        check('mimetype exact', z.read('mimetype')==b'application/epub+zip')
        check('12 expected archive entries', len(names)==12)
        check('all XML parsable', all(ET.fromstring(z.read(n)) is not None for n in names if n.endswith(('.xhtml','.xml','.opf'))))
        x = z.read('OEBPS/chapter-01.xhtml')
        check('escaped content', b'&amp;' in x and b'&lt;demo&gt;' in x and b'<demo>' not in x)
        check('eight nav links', z.read('OEBPS/nav.xhtml').count(b'<li>')==8)
    try:
        b.build(source, output/'one.epub', pins)
        raise AssertionError('existing output accepted')
    except ValueError:
        check('refuses overwrite', True)
    (source/'Article 5').write_text('TAMPER', encoding='utf8')
    try:
        b.build(source, output/'tampered.epub', pins)
        raise AssertionError('tampered source accepted')
    except ValueError:
        check('rejects tampered source', not (output/'tampered.epub').exists())
    (source/'Article 5').unlink()
    try:
        b.build(source, output/'missing.epub', pins)
        raise AssertionError('missing source accepted')
    except FileNotFoundError:
        check('rejects missing source', not (output/'missing.epub').exists())
    try:
        b.build(source, source/'bad.epub', pins)
        raise AssertionError('inside source accepted')
    except ValueError:
        check('rejects output inside source', True)
    (source/'Article 5').write_bytes(b'Invalid XML: \x00')
    pins['Article 5'] = b.git_blob((source/'Article 5').read_bytes())
    try:
        b.build(source, output/'invalid-xml.epub', pins)
        raise AssertionError('invalid XML accepted')
    except ET.ParseError:
        check('invalid XML leaves no output', not (output/'invalid-xml.epub').exists())
    try:
        b.build(source, output/'wrongpins.epub', dict(list(pins.items())[:-1]))
        raise AssertionError('incomplete pin set accepted')
    except ValueError:
        check('rejects incomplete pins', True)
print(json.dumps({'passed':sum(ok for _,ok in checks),'total':len(checks),'cases':checks},indent=2))
