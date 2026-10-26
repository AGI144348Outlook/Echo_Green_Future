import csv
import hashlib
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from f001_claims_binding_377 import FILES, HEADER, check


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src, self.out = self.root / 'src', self.root / 'out'
        self.src.mkdir(); self.out.mkdir()
        for name in FILES:
            (self.src / name).write_text('Quiet narrative.', encoding='utf-8')
        (self.src / FILES[0]).write_text('This proves an accuracy of 90%.', encoding='utf-8')
        (self.src / FILES[1]).write_text('The result is exactly 1.', encoding='utf-8')
        self.rows = [dict(zip(HEADER, [FILES[0], '1', 'certainty;percent;accuracy',
                                      'This proves an accuracy of 90%.', 'claimed'])),
                     dict(zip(HEADER, [FILES[1], '1', 'superlative',
                                       'The result is exactly 1.', 'inferred']))]
        self.write_csv()
        self.report = {
            'source_files': {name: hashlib.sha256((self.src / name).read_bytes()).hexdigest() for name in FILES},
            'per_file': {name: (1 if name in FILES[:2] else 0) for name in FILES},
            'per_trigger': {'certainty': 1, 'percent': 1, 'accuracy': 1, 'superlative': 1},
            'rows': 2,
        }
        self.write_report()

    def write_csv(self):
        with (self.out / 'claims.csv').open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=HEADER); w.writeheader(); w.writerows(self.rows)

    def write_report(self):
        (self.out / 'claims-report.json').write_text(json.dumps(self.report), encoding='utf-8')

    def assert_rejects(self):
        r = check(self.src, self.out)
        self.assertFalse(r['structurally_reviewable'], r)
        self.assertFalse(r['release_authorized'])
        self.assertEqual(r['status'], 'HOLD')

    def test_pristine_structural_only(self):
        r = check(self.src, self.out)
        self.assertTrue(r['structurally_reviewable'], r)
        self.assertEqual(r['candidate_count'], 2)
        self.assertFalse(r['release_authorized'])
        self.assertEqual(r['status'], 'HOLD')

    def test_source_edit(self):
        (self.src / FILES[0]).write_text('This proves accuracy of 91%.'); self.assert_rejects()

    def test_missing_claim_row(self):
        self.rows.pop(); self.write_csv(); self.assert_rejects()

    def test_modified_claim_sentence(self):
        self.rows[0]['sentence'] = 'Fabricated.'; self.write_csv(); self.assert_rejects()

    def test_duplicate_row(self):
        self.rows.append(dict(self.rows[1])); self.write_csv(); self.assert_rejects()

    def test_invalid_status(self):
        self.rows[0]['status'] = 'certified'; self.write_csv(); self.assert_rejects()

    def test_open_status(self):
        self.rows[0]['status'] = ''; self.write_csv(); self.assert_rejects()

    def test_bad_report_hash(self):
        self.report['source_files'][FILES[0]] = '0' * 64; self.write_report(); self.assert_rejects()

    def test_bad_report_counts(self):
        self.report['per_trigger']['accuracy'] = 0; self.write_report(); self.assert_rejects()

    def test_missing_source(self):
        (self.src / FILES[-1]).unlink(); self.assert_rejects()

    def test_source_symlink(self):
        (self.src / FILES[-1]).unlink(); (self.src / FILES[-1]).symlink_to(self.src / FILES[0]); self.assert_rejects()

    def test_csv_symlink(self):
        (self.out / 'claims.csv').unlink(); (self.out / 'claims.csv').symlink_to(self.src / FILES[0]); self.assert_rejects()

    def test_reordered_claim_rows(self):
        self.rows.reverse(); self.write_csv(); self.assert_rejects()

    def test_cut_status_is_not_release_authorization(self):
        self.rows[0]['status'] = 'cut'; self.write_csv()
        r = check(self.src, self.out)
        self.assertTrue(r['structurally_reviewable'])
        self.assertFalse(r['release_authorized'])


if __name__ == '__main__':
    unittest.main()
