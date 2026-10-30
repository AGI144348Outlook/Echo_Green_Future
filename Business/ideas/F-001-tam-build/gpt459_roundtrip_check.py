# F-001 §159 (Claude, 2026-10-30 05Z): checks that each chapter of a GPT 459 EPUB has exactly one <p> per nonblank source line.
# Usage: python3 -I <this> <built.epub> <TAM-source-dir>
import sys, zipfile, re, json, html
from pathlib import Path
from xml.etree import ElementTree as ET
ep, src = sys.argv[1], Path(sys.argv[2])
z = zipfile.ZipFile(ep); NS='{http://www.w3.org/1999/xhtml}'
opf = z.read('OEBPS/content.opf').decode()
names = re.findall(r'<itemref idref="([^"]+)"', opf)
rows=[]; ok=0
chaps=[n for n in z.namelist() if n.endswith('.xhtml') and 'nav' not in n]
for n in sorted(chaps):
    root=ET.fromstring(z.read(n)); title=root.find(f'.//{NS}h1').text
    ps=[''.join(p.itertext()) for p in root.iter(f'{NS}p')]
    brs=len(list(root.iter(f'{NS}br')))
    s=(src/title).read_bytes().decode('utf-8').replace('\r\n','\n').replace('\r','\n')
    lines=[l for l in s.split('\n') if l.strip()]
    same = ps==lines
    heb=sum(1 for c in s if '֐'<=c<='׿')
    rows.append(dict(file=n,title=title,paragraphs=len(ps),nonblank_lines=len(lines),exact_roundtrip=same,br=brs,hebrew_chars=heb))
    ok+=same
print(json.dumps(dict(chapters=len(rows),roundtrip_exact=f"{ok}/{len(rows)}",rows=rows),ensure_ascii=False,indent=1))
