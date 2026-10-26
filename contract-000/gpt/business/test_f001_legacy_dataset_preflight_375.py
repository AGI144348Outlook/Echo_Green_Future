"""Isolated synthetic tests only; no shared code or real TAM datasets executed."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from f001_legacy_dataset_preflight_375 import SCHEMA, inspect


def fixture(root):
    root = Path(root)
    report = {"files": {}}
    for key, (name, header, count) in SCHEMA.items():
        report["files"][key] = {"rows": count, "rejected": []}
        with (root / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows([["x"] * len(header) for _ in range(count)])
    (root / "dataset-check.json").write_text(json.dumps(report), encoding="utf-8")
    return report


class ReviewGate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.report = fixture(self.root)

    def write_report(self):
        (self.root / "dataset-check.json").write_text(json.dumps(self.report), encoding="utf-8")

    def test_valid_fixture_is_review_only(self):
        self.assertEqual(inspect(self.root), [])

    def test_partial_a_report_fails(self):
        self.report["files"]["A"]["rows"] = 1
        self.write_report()
        self.assertTrue(inspect(self.root))

    def test_rejected_rows_fails(self):
        self.report["files"]["B"]["rejected"] = [{"line": 4}]
        self.write_report()
        self.assertTrue(inspect(self.root))

    def test_stale_header_only_csv_fails(self):
        (self.root / "dataset-a.csv").write_text(",".join(SCHEMA["A"][1]) + "\n", encoding="utf-8")
        self.assertTrue(inspect(self.root))

    def test_missing_csv_fails(self):
        (self.root / "dataset-b.csv").unlink()
        self.assertTrue(inspect(self.root))

    def test_wrong_header_fails(self):
        p = self.root / "dataset-b.csv"
        p.write_text(p.read_text().replace("ratio,mass_g", "other,mass_g", 1))
        self.assertTrue(inspect(self.root))

    def test_zero_row_refusal_fails(self):
        self.report["not_written_zero_rows"] = ["dataset-a.csv"]
        self.write_report()
        self.assertTrue(inspect(self.root))

    def test_boolean_report_count_fails(self):
        self.report["files"]["A"]["rows"] = True
        self.write_report()
        self.assertTrue(inspect(self.root))

    def test_symlinked_csv_fails(self):
        p = self.root / "dataset-b.csv"
        target = self.root / "target.csv"
        p.rename(target)
        p.symlink_to(target)
        self.assertTrue(inspect(self.root))

    def test_malformed_report_fails(self):
        (self.root / "dataset-check.json").write_text("not json")
        self.assertTrue(inspect(self.root))


if __name__ == "__main__":
    unittest.main()
