#!/usr/bin/env python3
"""HOLD-only reproduction of the exact pinned F-001 listing checker.

Run: python3 -I -B test_listing_replay_391.py path/to/listing_check.py
Pre-test: Echo_Green_Future issue #64. Synthetic fixtures only; no release.
"""
import csv
import hashlib
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

EXPECTED_GIT_BLOB = 'adc3123c303168650e03270701cd3123afe0ce28'
SENTENCE = 'Synthetic assertion: the lunar river is blue.'
LISTING = 'Research notebook: EPUB and CSV files. Each claim is marked.\n'


def git_blob_sha(raw):
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def fixture(root, status='cut', include_claims=True, include_epub=True,
            include_csv=True, text=LISTING, epub_body=SENTENCE):
    root.mkdir(parents=True, exist_ok=True)
    listing = root / 'listing.md'
    listing.write_text(text, encoding='utf-8')
    out = root / 'out'
    out.mkdir()
    if include_claims:
        with (out / 'claims.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['file', 'sentence_no', 'triggers', 'sentence', 'status'])
            writer.writeheader()
            writer.writerow({'file': 'synthetic', 'sentence_no': 1, 'triggers': 'certainty',
                             'sentence': SENTENCE, 'status': status})
    if include_csv:
        (out / 'dataset.csv').write_text('value\n1\n', encoding='utf-8')
    if include_epub:
        with zipfile.ZipFile(out / 'synthetic.epub', 'w') as z:
            z.writestr('mimetype', 'application/epub+zip')
            z.writestr('OEBPS/chapter.xhtml', '<html xmlns="http://www.w3.org/1999/xhtml"><body><p>' + epub_body + '</p></body></html>')
    return listing, out


def run_case(script, name, expected, **kw):
    with tempfile.TemporaryDirectory(prefix='f001-run391-') as td:
        listing, out = fixture(Path(td) / name, **kw)
        p = subprocess.run([sys.executable, '-I', '-B', str(script), str(listing), str(out)],
                           capture_output=True, text=True, timeout=10)
        actual = 'PASS' if p.returncode == 0 else 'FAIL'
        assert actual == expected, f'{name}: expected {expected}, got {actual}; stdout={p.stdout}; stderr={p.stderr}'
        print(f'{name}: expected={expected} actual={actual} rc={p.returncode}; ' +
              ' | '.join(x for x in p.stdout.splitlines() if x.startswith('FAIL')))


def main():
    script = Path(sys.argv[1]).resolve()
    raw = script.read_bytes()
    sha = git_blob_sha(raw)
    assert sha == EXPECTED_GIT_BLOB, f'wrong source: {sha}'
    print(f'ORIGINAL source pin verified: {sha}, bytes={len(raw)}')
    cases = [
        ('cut_claim_still_in_epub', 'PASS', dict(status='cut')),
        ('sourced_claim_without_citation', 'PASS', dict(status='sourced')),
        ('claimed_claim_no_evidence', 'PASS', dict(status='claimed')),
        ('open_claim', 'FAIL', dict(status='')),
        ('missing_claims_csv', 'FAIL', dict(include_claims=False)),
        ('missing_epub', 'FAIL', dict(include_epub=False)),
        ('missing_dataset_csv', 'FAIL', dict(include_csv=False)),
        ('forbidden_accuracy', 'FAIL', dict(text='Research notebook EPUB and CSV. 99.9% accuracy.')),
        ('cut_absent_from_epub', 'PASS', dict(status='cut', epub_body='This is unrelated.')),
    ]
    for name, expected, kw in cases:
        run_case(script, name, expected, **kw)
    print(f'PASS: {len(cases)}/{len(cases)} expected outcomes; source pin exact; synthetic fixtures only.')


if __name__ == '__main__':
    main()
