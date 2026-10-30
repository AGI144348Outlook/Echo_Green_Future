#!/usr/bin/env python3
"""F-001 HOLD-only editorial register byte-fidelity gate (stdlib).

Pins the *entire* 82-row proposed editorial register to its reviewed Git
blob, not merely its identifiers and approval labels. This is not a digital
signature, a Timothy approval verifier, or a release gate. It NEVER approves
edits, applies replacements, or authorizes publication.

Production CLI has a fixed expected blob. The audit_bytes expected_blob
parameter exists only to permit offline synthetic-fixture regression tests;
callers who supply their own expected blob have NOT established trust.
"""
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

PROJECT = 'F-001'
REGISTER_BLOB = '300dfcf0ba9e9d236326d09b2a4b6c5467d3874c'
SOURCE_COMMIT = 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9'
MANUSCRIPT_BLOB = 'b015fab385b0baf68d88956cb86888b094a69ca2'
STATUS = 'HOLD / NOT LAUNCH-READY'
COPIES = {
 'Collective information#S293': 'Article 10#S3',
 'Collective information#S294': 'Article 10#S4',
 'Collective information#S295': 'Article 10#S5',
 'Collective information#S298': 'Article 10#S8',
 'Collective information#S150': 'Article 6#S1',
 'Collective information#S153': 'Article 6#S4',
 'Collective information#S161': 'Article 6#S12',
 'Collective information#S168': 'Article 6#S19',
 'Collective information#S172': 'Article 6#S23',
 'Collective information#S178': 'Article 6#S29',
}
COLUMNS = ('project', 'occurrence_id', 'proposal_section', 'short_text',
           'claude_proposed_state', 'same_text_as', 'editorial_approval',
           'publication_status', 'tam_source_commit', 'manuscript_git_blob')

class Refused(ValueError):
    pass


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def audit_bytes(raw, expected_blob=REGISTER_BLOB, expected_copies=COPIES):
    if not isinstance(raw, bytes) or not raw:
        raise Refused('nonempty bytes required')
    if not re.fullmatch('[0-9a-f]{40}', expected_blob):
        raise Refused('invalid trusted blob pin')
    actual = git_blob(raw)
    if actual != expected_blob:
        raise Refused('complete register blob differs from reviewed pin')
    try:
        s = raw.decode('utf-8', errors='strict')
    except UnicodeError as exc:
        raise Refused('invalid UTF-8') from exc
    if '\x00' in s or '\r' in s or s.startswith('\ufeff') or not s.endswith('\n'):
        raise Refused('noncanonical TSV bytes')
    rows = list(csv.reader(io.StringIO(s, newline=''), delimiter='\t',
                           quoting=csv.QUOTE_NONE, strict=True))
    if len(rows) != 83 or tuple(rows[0]) != COLUMNS:
        raise Refused('expected exact 82-row register and header')
    seen, copies = set(), {}
    for i, values in enumerate(rows[1:], 1):
        if len(values) != len(COLUMNS):
            raise Refused('malformed row %d' % i)
        d = dict(zip(COLUMNS, values))
        ident = d['occurrence_id']
        if (d['project'] != PROJECT or not re.fullmatch(r'.+#S[1-9][0-9]*', ident)
                or ident in seen):
            raise Refused('invalid or duplicate occurrence %d' % i)
        seen.add(ident)
        if (not re.fullmatch(r'§[0-9]+', d['proposal_section'])
                or not d['short_text'].strip() or not d['claude_proposed_state'].strip()):
            raise Refused('missing editorial evidence %d' % i)
        if (d['editorial_approval'] != 'PROPOSED_NOT_APPROVED'
                or d['publication_status'] != STATUS):
            raise Refused('approval or release status is not HOLD')
        if (d['tam_source_commit'] != SOURCE_COMMIT
                or d['manuscript_git_blob'] != MANUSCRIPT_BLOB):
            raise Refused('source provenance differs')
        if d['same_text_as']:
            copies[ident] = d['same_text_as']
    if (copies != expected_copies or len(copies) != 10
            or any(source not in seen or target == source
                   for target, source in copies.items())):
        raise Refused('exact-copy provenance incomplete')
    return {'project': PROJECT, 'status': STATUS, 'rows': 82,
            'proposed': 82, 'approved': 0, 'copies': 10,
            'git_blob': actual, 'sha256': hashlib.sha256(raw).hexdigest(),
            'publication_authorized': False, 'editorial_overlay_applied': False}


def main(argv):
    if len(argv) != 2:
        print('usage: python -I F-001-EDITORIAL-BYTE-GATE-460.py REGISTER.tsv', file=sys.stderr)
        return 2
    try:
        raw = Path(argv[1]).read_bytes()
        print(json.dumps(audit_bytes(raw), sort_keys=True))
        return 0
    except (OSError, Refused, csv.Error) as exc:
        print('F-001 HOLD / REGISTER REFUSED: ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv))
