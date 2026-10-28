#!/usr/bin/env python3
"""F-001 HOLD-only staged ledger merge; proposed, NOT production or tax certification.

Usage: python -I -B f001_ledger_stage_gate_425.py ORIGINAL_LEDGER_MERGE.py OLD.csv|- NEW.csv FINAL.csv
Runs only Git-blob-pinned original public merge source. No network, account, or real records.
Publishes FINAL only after all checks pass. FINAL is created without clobbering.
PRE: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/98
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from decimal import Decimal, InvalidOperation
from pathlib import Path

ORIGINAL_GIT_BLOB = '0f706be4229458ed20a25105ae18b58f90b93ff7'
FIELDS = ['date','fiscal_contract','kind','category','gross','fees','net',
          'asset_or_liability','share','source','source_ref','receipt_ref',
          'evidence','entered_by']


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def is_in_git_directory(directory):
    d = directory.resolve()
    return any((p / '.git').exists() for p in (d, *d.parents))


def verify_stage(staged, report):
    if not isinstance(report, dict):
        raise ValueError('child report not a JSON object')
    for key in ('conflicts', 'unkeyed_not_merged', 'net_missing'):
        if not isinstance(report.get(key), list) or report[key]:
            raise ValueError('child report flags ' + key)
    if not isinstance(report.get('appended'), int) or not isinstance(report.get('ledger_rows'), int):
        raise ValueError('child report lacks row counts')
    seen = set()
    total = Decimal(0)
    count = 0
    with staged.open(newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        if r.fieldnames != FIELDS:
            raise ValueError('staged CSV header mismatch')
        for row in r:
            count += 1
            ref = (row.get('source_ref') or '').strip()
            if not ref or ref in seen:
                raise ValueError('blank or repeated source_ref')
            seen.add(ref)
            try:
                net = Decimal(row['net'])
            except (InvalidOperation, TypeError, ValueError):
                raise ValueError('staged net not numeric') from None
            if not net.is_finite():
                raise ValueError('staged net not finite')
            total += net
    if count != report['ledger_rows'] + report['appended']:
        raise ValueError('staged row count mismatch')
    try:
        reported = Decimal(str(report['net_total']))
    except (KeyError, InvalidOperation, TypeError, ValueError):
        raise ValueError('child net_total invalid') from None
    if not reported.is_finite() or total != reported:
        raise ValueError('child total differs from staged rows')
    return count, str(total)


def run(original, old, new, final):
    final = Path(final).absolute()
    parent = final.parent
    if is_in_git_directory(parent):
        raise ValueError('final output is inside a git repository')
    if os.path.lexists(final):
        raise ValueError('final output already exists')
    raw = Path(original).read_bytes()
    if git_blob(raw) != ORIGINAL_GIT_BLOB:
        raise ValueError('unverified original merge script')
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.f001-stage-', dir=parent) as d:
        staged = Path(d) / 'candidate.csv'
        cmd = [sys.executable, '-I', '-B', str(Path(original).resolve()),
               str(old), str(new), str(staged)]
        child = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if child.returncode != 0:
            raise ValueError('original merge returned nonzero status')
        try:
            report = json.loads(child.stdout)
        except (json.JSONDecodeError, TypeError):
            raise ValueError('original merge returned invalid JSON') from None
        if not staged.is_file():
            raise ValueError('original merge produced no staged CSV')
        count, total = verify_stage(staged, report)
        # Exclusive hard link: never replaces an existing FINAL, even under a same-name race.
        os.link(staged, final, follow_symlinks=False)
        return {'status':'PREPARED_HOLD', 'rows':count,
                'source_git_blob':ORIGINAL_GIT_BLOB}


def main(argv):
    if len(argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        result = run(*argv)
    except (OSError, ValueError, subprocess.TimeoutExpired) as e:
        print(json.dumps({'status':'HOLD', 'reason':str(e)}))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
