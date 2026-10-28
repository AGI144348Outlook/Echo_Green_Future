#!/usr/bin/env python3
"""Prospectively registered synthetic tests for F-001 cut-disposition gate."""
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('cut_gate', HERE / 'F-001-CUT-DISPOSITION-GATE-415.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

BASE = [{'file': 'Article 1', 'sentence_no': '1', 'triggers': 'certainty',
         'sentence': 'A source claim that should be cut.', 'status': 'cut'}]


def fixture(root, rows=BASE, text='A source claim that should be cut.', header=None):
    claims, manuscript = root / 'claims.csv', root / 'tam-draft.md'
    with claims.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header or gate.HEADER)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    manuscript.write_text(text, encoding='utf-8')
    return claims, manuscript


def expect_failure(claims, manuscript, **kwargs):
    try:
        gate.check(claims, manuscript, **kwargs)
    except ValueError:
        return True
    return False


def main():
    results = {}
    with tempfile.TemporaryDirectory(prefix='f001-cut415-') as td:
        root = Path(td)
        c, m = fixture(root)
        # Original byte-for-byte pinned listing checker: status 'cut' passes
        listing = root / 'listing.md'
        listing.write_text('A speculative reconstruction.', encoding='utf-8')
        original = subprocess.run([sys.executable, '-I', '-B', str(HERE / 'F-001-LISTING-CHECK-PINNED-415.py'),
                                   str(listing), str(root)], capture_output=True, text=True)
        results['original_listing_accepts_unapplied_cut'] = original.returncode == 0 and 'FAIL' not in original.stdout
        results['new_gate_rejects_unapplied_cut'] = expect_failure(c, m)
        c, m = fixture(root, text='The draft now contains a different claim.')
        results['cut_absent_positive'] = gate.check(c, m)['cut_rows_absent'] == 1
        c, m = fixture(root, rows=[{**BASE[0], 'status': 'sourced'}], text='A source claim that should be cut.')
        results['sourced_present_positive_no_approval'] = gate.check(c, m)['release_authorized'] is False
        c, m = fixture(root, rows=[{**BASE[0], 'status': ''}], text='No claim.')
        results['blank_status_rejected'] = expect_failure(c, m)
        c, m = fixture(root, rows=[{**BASE[0], 'status': 'approved'}], text='No claim.')
        results['unknown_status_rejected'] = expect_failure(c, m)
        c, m = fixture(root, rows=BASE * 2, text='No claim.')
        results['duplicate_source_id_rejected'] = expect_failure(c, m)
        c, m = fixture(root, rows=[], text='No claim.')
        results['empty_ledger_rejected'] = expect_failure(c, m)
        c, m = fixture(root, rows=[{**BASE[0], 'sentence_no': 'not-a-number'}], text='No claim.')
        results['bad_sentence_number_rejected'] = expect_failure(c, m)
        c, m = fixture(root, rows=[{**BASE[0], 'sentence': ''}], text='No claim.')
        results['empty_sentence_rejected'] = expect_failure(c, m)
        c, m = fixture(root, text='A source\n claim that should be cut.')
        results['whitespace_normalized_cut_rejected'] = expect_failure(c, m)
        c, m = fixture(root, text='A source\u200b claim that should be cut.')
        results['zero_width_normalized_cut_rejected'] = expect_failure(c, m)
        c, m = fixture(root, text='No claim.')
        results['row_count_mismatch_rejected'] = expect_failure(c, m, expected_rows=2)
        results['row_count_match_positive'] = gate.check(c, m, expected_rows=1)['audit'] == 'PASS'
        c, m = fixture(root, text='No claim.')
        c.unlink()
        results['missing_ledger_rejected'] = expect_failure(c, m)
        c, m = fixture(root, text='No claim.')
        m.unlink()
        results['missing_manuscript_rejected'] = expect_failure(c, m)
    print(json.dumps({'passed': sum(results.values()), 'total': len(results),
                      'checks': results}, indent=2))
    if not all(results.values()):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
