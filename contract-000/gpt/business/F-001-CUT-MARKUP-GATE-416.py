#!/usr/bin/env python3
"""F-001 HOLD-only supplemental cut-disposition audit with markup projection.

Usage: python3 -I -B F-001-CUT-MARKUP-GATE-416.py <claims.csv> <manuscript.md> [expected_rows]

Checks that a human-marked 'cut' sentence is absent from both literal manuscript
text and a *bounded approximation* of rendered Markdown/inline HTML. This is
not a Markdown/EPUB renderer and cannot certify every rephrasing or layout.
Always run with the original source-pinned scanner, editorial verification,
listing checker and final EPUB/PDF checks. Never grants release approval.
"""
import csv
import html
from html.parser import HTMLParser
import json
import re
import stat
import sys
import unicodedata
from pathlib import Path

PROJECT = 'F-001'
HOLD = 'HOLD / NOT LAUNCH-READY'
HEADER = ['file', 'sentence_no', 'triggers', 'sentence', 'status']
DONE = {'claimed', 'inferred', 'test', 'cut', 'sourced'}
MAX_BYTES = 8 * 1024 * 1024
ZERO_WIDTH = dict.fromkeys(map(ord, '\u200b\u200c\u200d\u2060\ufeff'))


def normalized(text):
    return ' '.join(unicodedata.normalize('NFKC', text).translate(ZERO_WIDTH).split()).casefold()


def bounded_text(path):
    p = Path(path)
    st = p.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_BYTES:
        raise ValueError('missing, nonregular or oversized input: ' + p.name)
    raw = p.read_bytes()
    if len(raw) > MAX_BYTES or p.lstat().st_size != st.st_size:
        raise ValueError('changed or oversized input: ' + p.name)
    return raw.decode('utf-8', 'strict')


class TextProjection(HTMLParser):
    BLOCK = {'p', 'div', 'br', 'li', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'blockquote', 'section'}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCK: self.parts.append(' ')
    def handle_endtag(self, tag):
        if tag in self.BLOCK: self.parts.append(' ')
    def handle_data(self, data):
        self.parts.append(data)
    def handle_entityref(self, name):
        self.parts.append(html.unescape('&' + name + ';'))
    def handle_charref(self, name):
        self.parts.append(html.unescape('&#' + name + ';'))


def markup_projection(text):
    # Conservative inline Markdown approximation: label text remains, URL is
    # omitted, formatting markers disappear. This does NOT parse all Markdown.
    text = re.sub(r'!?\[([^\]]*)\]\([^\n)]*\)', r'\1', text)
    text = re.sub(r'(?m)^\s{0,3}#{1,6}\s+', '', text)
    text = re.sub(r'(?m)^\s*>\s?', '', text)
    text = re.sub(r'[*_~`]', '', text)
    parser = TextProjection()
    parser.feed(text)
    parser.close()
    return normalized(html.unescape(''.join(parser.parts)))


def check(claims, manuscript, expected_rows=None):
    if expected_rows is not None and (type(expected_rows) is not int or expected_rows < 1):
        raise ValueError('expected_rows must be a positive integer')
    source = bounded_text(manuscript)
    literal = normalized(source)
    projected = markup_projection(source)
    csv.field_size_limit(MAX_BYTES)
    reader = csv.DictReader(bounded_text(claims).splitlines())
    if reader.fieldnames != HEADER:
        raise ValueError('unexpected or duplicate claim-ledger headers')
    rows = list(reader)
    if not rows or (expected_rows is not None and len(rows) != expected_rows):
        raise ValueError('empty or mismatched claim ledger')
    seen, cuts = set(), 0
    for i, row in enumerate(rows, 1):
        if None in row or any(row.get(k) is None for k in HEADER):
            raise ValueError('malformed row ' + str(i))
        key = (row['file'].strip(), row['sentence_no'].strip())
        if not key[0] or not key[1].isdecimal() or int(key[1]) < 1 or not normalized(row['sentence']):
            raise ValueError('invalid source identity at row ' + str(i))
        key = (key[0], int(key[1]))
        if key in seen: raise ValueError('duplicate source identity at row ' + str(i))
        seen.add(key)
        status = row['status'].strip().lower()
        if status not in DONE: raise ValueError('unreviewed or invalid status at row ' + str(i))
        if status == 'cut':
            cuts += 1
            sentence = normalized(row['sentence'])
            if sentence in literal or sentence in projected:
                raise ValueError('cut claim remains in manuscript or markup projection at row ' + str(i))
    return {'audit': 'PASS', 'project': PROJECT, 'status': HOLD,
            'claim_rows': len(rows), 'cut_rows_absent_in_projection': cuts,
            'markup_projection_checked': True, 'editorial_approved': False,
            'release_authorized': False,
            'scope': 'supplemental Markdown/inline-HTML approximation only; no EPUB render or paraphrase certification'}


def main(args):
    if len(args) not in (3, 4):
        print(__doc__, file=sys.stderr)
        return 2
    try:
        expected = int(args[3]) if len(args) == 4 else None
        print(json.dumps(check(args[1], args[2], expected), sort_keys=True))
        return 0
    except (OSError, ValueError, UnicodeError, csv.Error) as exc:
        print(json.dumps({'audit': 'FAIL', 'project': PROJECT, 'status': HOLD,
                          'release_authorized': False, 'reason': str(exc)}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
