#!/usr/bin/env python3
"""F-001 HOLD-only proposed EPUB cut-claim presence audit; NOT a release gate.

Reads a synthetic or review EPUB and a claim CSV; never edits either. This checks
only whether a row marked 'cut' still appears verbatim (after conservative
Unicode/whitespace normalization) in EPUB XHTML. It cannot prove absence in a
PDF, paraphrase, image, or rewritten sentence; editorial approval is separate.
"""
import csv
import re
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

MAX_ENTRIES = 1000
MAX_TOTAL_BYTES = 20_000_000
MAX_MEMBER_BYTES = 4_000_000


def normalize(s):
    s = unicodedata.normalize('NFKC', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Cf')
    return re.sub(r'\s+', ' ', s).strip().casefold()


def inspect(claims_csv, epub):
    with Path(claims_csv).open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not {'sentence', 'status'} <= set(rows[0]):
        return False, ['missing or invalid claim ledger']
    if any(not (r.get('status') or '').strip() for r in rows):
        return False, ['open editorial status remains']
    cut = [(i, (r.get('sentence') or '').strip()) for i, r in enumerate(rows, 1)
           if (r.get('status') or '').strip().lower() == 'cut']
    if any(not sentence for _, sentence in cut):
        return False, ['empty cut sentence cannot be checked']
    findings = []
    try:
        with zipfile.ZipFile(epub) as z:
            infos = z.infolist()
            if len(infos) > MAX_ENTRIES or sum(i.file_size for i in infos) > MAX_TOTAL_BYTES:
                return False, ['EPUB exceeds bounded ZIP limits']
            if any(i.file_size > MAX_MEMBER_BYTES for i in infos):
                return False, ['EPUB contains oversized member']
            if any(i.filename.startswith('/') or '..' in i.filename.split('/') or
                   ((i.external_attr >> 16) & 0o170000) == 0o120000 for i in infos):
                return False, ['EPUB has unsafe member path or symlink']
            xhtml = [i for i in infos if i.filename.lower().endswith(('.xhtml', '.html'))]
            if not xhtml:
                return False, ['EPUB has no XHTML text to audit']
            text = []
            for item in xhtml:
                root = ET.fromstring(z.read(item))
                text.append(normalize(''.join(root.itertext())))
    except (OSError, zipfile.BadZipFile, ET.ParseError, RuntimeError, ValueError) as exc:
        return False, [f'EPUB could not be safely inspected: {type(exc).__name__}']
    for row, sentence in cut:
        if normalize(sentence) in text[0] or any(normalize(sentence) in t for t in text[1:]):
            findings.append(f'row {row}: CUT claim still appears in EPUB XHTML')
    if findings:
        return False, findings
    return True, [f'no exact normalized cut-text match in {len(xhtml)} XHTML files; PDF/paraphrase NOT checked']


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: f001_cut_presence_gate_390.py claims.csv book.epub')
    ok, findings = inspect(sys.argv[1], sys.argv[2])
    for item in findings:
        print(('PASS ' if ok else 'HOLD ') + item)
    sys.exit(0 if ok else 1)
