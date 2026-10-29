#!/usr/bin/env python3
"""Run432 synthetic EPUB metadata gate controls; never use production files."""
import io
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import importlib.util
spec = importlib.util.spec_from_file_location("gate432", Path(__file__).with_name("f001_a11y_metadata_gate_432.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
inspect, main = mod.inspect, mod.main

MIME=b'application/epub+zip'
CONTAINER=b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf"/></rootfiles></container>'
OPF=b'<package xmlns="http://www.idpf.org/2007/opf"><metadata><meta property="schema:accessibilityFeature">tableOfContents</meta><meta property="schema:accessibilityFeature">alternativeText</meta></metadata></package>'

def epub(path, opf=OPF, container=CONTAINER, extra=(), mimetype=MIME, first=True):
    with zipfile.ZipFile(path, 'w') as z:
        entries=[('mimetype',mimetype,zipfile.ZIP_STORED),('META-INF/container.xml',container,zipfile.ZIP_DEFLATED),('OEBPS/content.opf',opf,zipfile.ZIP_DEFLATED)]
        if not first: entries=[entries[1],entries[0],entries[2]]
        for n,b,method in entries+list(extra):
            z.writestr(n,b,compress_type=method)

cases=[]
with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'book.epub'
    epub(p); cases.append(('valid_two_distinct_features',inspect(p)['ok'],True))
    epub(p,opf=OPF.replace(b'alternativeText',b'tableOfContents')); cases.append(('duplicate_feature',inspect(p)['ok'],False))
    epub(p,opf=b'<package><metadata/></package>'); cases.append(('no_a11y',inspect(p)['ok'],False))
    epub(p,opf=b'<package>'); cases.append(('malformed_opf',inspect(p)['ok'],False))
    epub(p,container=b'<container/>'); cases.append(('no_rootfile',inspect(p)['ok'],False))
    epub(p,container=CONTAINER.replace(b'OEBPS/content.opf',b'../escape.opf')); cases.append(('traversal',inspect(p)['ok'],False))
    epub(p,extra=[('OEBPS/extra.opf',b'<package/>',zipfile.ZIP_DEFLATED)]); cases.append(('two_opfs',inspect(p)['ok'],False))
    epub(p,mimetype=b'not-epub'); cases.append(('bad_mimetype',inspect(p)['ok'],False))
    epub(p,first=False); cases.append(('mimetype_not_first',inspect(p)['ok'],False))
    p.write_bytes(b'not zip'); cases.append(('invalid_zip',inspect(p)['ok'],False))
    cases.append(('missing_file',inspect(Path(d)/'absent.epub')['ok'],False))
    link=Path(d)/'link.epub'; link.symlink_to(p); cases.append(('symlink',inspect(link)['ok'],False))
    epub(p,container=b'<container>'); cases.append(('malformed_container',inspect(p)['ok'],False))
    epub(p); cases.append(('cli_valid_exit',main(['gate',str(p)]),0))
    epub(p,opf=b'<package/>'); cases.append(('cli_invalid_exit',main(['gate',str(p)]),1))
    for name,got,want in cases:
        assert got==want,(name,got,want)
    print(f'PASS {len(cases)}/{len(cases)} F-001 synthetic metadata gate controls')
