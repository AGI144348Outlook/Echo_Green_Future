#!/usr/bin/env python3
"""F-001 HOLD-only supplemental editorial gate for claims marked 'cut'.

Usage: python3 -I -B F-001-CUT-DISPOSITION-GATE-415.py <claims.csv> <manuscript.md> [expected_rows]

This does NOT approve editorial claims or publication. It refuses an incomplete
claim ledger and detects a 'cut' source sentence still present in the draft.
Must run alongside original listing_check.py, source-pin verification, human
review and all other F-001 release gates. Does not modify either input.
"""
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

PROJECT = 'F-001'
STATUS = 'HOLD / NOT LAUNCH-READY'
HEADER = ['file', 'sentence_no', 'triggers', 'sentence', 'status']
DONE = {'claimed', 'inferred', 'test', 'cut', 'sourced'}
MAX_BYTES = 8 * 1024 * 1024
ZERO_WIDTH = dict.fromkeys(map(ord, '\u200b\u200c\u200d\u2060\ufeff'))


def normalized(text):
    return ' '.join(unicodedata.normalize('NFKC', text).translate(ZERO_WIDTH).split()).casefold()


def bounded_text(path):
    p = Path(path)
    if not p.is_file() or p.is_symlink() or p.stat().st_size > MAX_BYTES:
        raise ValueError('missing, symlink or oversized input: ' + p.name)
    data = p.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError('oversized input: ' + p.name)
    return data.decode('utf-8', 'strict')


def check(claims, manuscript, expected_rows=None):
    if expected_rows is not None and (type(expected_rows) is not int or expected_rows < 1):
        raise ValueError('expected_rows must be a positive integer')
    text = normalized(bounded_text(manuscript))
    csv.field_size_limit(MAX_BYTES)
    reader = csv.DictReader(bounded_text(claims).splitlines())
    if reader.fieldnames != HEADER:
        raise ValueError('unexpected or duplicate claim-ledger headers')
    rows = list(reader)
    if not rows:
        raise ValueError('claim ledger empty')
    if expected_rows is not None and len(rows) != expected_rows:
        raise ValueError('claim ledger row count differs from expected')
    seen = set()
    cuts = 0
    for index, row in enumerate(rows, 1):
        if None in row or any(row.get(key) is None for key in HEADER):
            raise ValueError('malformed claim-ledger row ' + str(index))
        source = row['file'].strip()
        number = row['sentence_no'].strip()
        sentence = normalized(row['sentence'])
        status = row['status'].strip().lower()
        if not source or not number.isdecimal() or int(number) < 1 or not sentence:
            raise ValueError('missing or invalid source identity at row ' + str(index))
        key = (source, int(number))
        if key in seen:
            raise ValueError('duplicate source sentence at row ' + str(index))
        seen.add(key)
        if status not in DONE:
            raise ValueError('unreviewed or invalid status at row ' + str(index))
        if status == 'cut':
            cuts += 1
            if sentence in text:
                raise ValueError('cut sentence still appears in manuscript at row ' + str(index))
    return {'audit': 'PASS', 'project': PROJECT, 'status': STATUS,
            'claim_rows': len(rows), 'cut_rows_absent': cuts,
            'editorial_approved': False, 'release_authorized': False,
            'scope': 'supplemental text-only cut check; not a release gate by itself'}


def main(argv):
    if len(argv) not in (3, 4):
        print(__doc__, file=sys.stderr)
        return 2
    try:
        expected = int(argv[3]) if len(argv) == 4 else None
        print(json.dumps(check(argv[1], argv[2], expected), sort_keys=True))
        return 0
    except (OSError, ValueError, UnicodeError, csv.Error) as exc:
        print(json.dumps({'audit': 'FAIL', 'project': PROJECT, 'status': STATUS,
                          'release_authorized': False, 'reason': str(exc)}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
