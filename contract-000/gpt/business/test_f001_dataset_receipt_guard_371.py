import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import f001_dataset_receipt_guard_371 as guard

ROOT = Path(__file__).parent
A = list(guard.SOURCE)[0]
B = list(guard.SOURCE)[1]


class DatasetGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.src = self.base / "src"
        self.out = self.base / "out"
        shutil.copytree(ROOT / "tam-source", self.src)
        self.build()

    def build(self):
        result = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "rebuild_datasets.py"),
                                 str(self.src), str(self.out)], capture_output=True, text=True)
        return result

    def assert_hold(self):
        with self.assertRaises(guard.HoldGateError):
            guard.verify(self.src, self.out)

    def test_exact_pinned_positive_review_only(self):
        result = guard.verify(self.src, self.out)
        self.assertEqual(result["status"], "VERIFIED_FOR_REVIEW")
        self.assertFalse(result["release_authorized"])
        self.assertEqual(result["rows"], {"A": 6, "B": 8})

    def test_source_A_tamper(self):
        with (self.src / A).open("a") as f: f.write("X")
        self.assert_hold()

    def test_source_B_tamper(self):
        with (self.src / B).open("a") as f: f.write("X")
        self.assert_hold()

    def test_output_A_tamper(self):
        with (self.out / "dataset-a.csv").open("a") as f: f.write("X")
        self.assert_hold()

    def test_output_B_tamper(self):
        with (self.out / "dataset-b.csv").open("a") as f: f.write("X")
        self.assert_hold()

    def test_report_tamper(self):
        with (self.out / "dataset-check.json").open("a") as f: f.write(" ")
        self.assert_hold()

    def test_missing_output(self):
        (self.out / "dataset-b.csv").unlink()
        self.assert_hold()

    def test_symlink_output(self):
        p = self.out / "dataset-a.csv"
        dest = self.base / "safe-copy.csv"
        p.rename(dest)
        p.symlink_to(dest)
        self.assert_hold()

    def test_symlink_source(self):
        p = self.src / A
        dest = self.base / "safe-copy.txt"
        p.rename(dest)
        p.symlink_to(dest)
        self.assert_hold()

    def test_corrupt_A_row_builder_succeeds_but_guard_holds(self):
        p = self.src / A
        p.write_text(p.read_text().replace("Silver Droplet 3.42g", "Silver Droplet CORRUPTED"))
        proc = self.build()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads((self.out / "dataset-check.json").read_text())
        self.assertEqual(report["files"]["A"]["rows"], 5)
        self.assertEqual(len(report["files"]["A"]["rejected"]), 1)
        self.assert_hold()

    def test_corrupt_B_row_builder_succeeds_but_guard_holds(self):
        p = self.src / B
        p.write_text(p.read_text().replace("8 6.85g", "8 CORRUPTED"))
        proc = self.build()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads((self.out / "dataset-check.json").read_text())
        self.assertEqual(report["files"]["B"]["rows"], 7)
        self.assertEqual(len(report["files"]["B"]["rejected"]), 1)
        self.assert_hold()

    def test_missing_valid_A_row_builder_succeeds_but_guard_holds(self):
        p = self.src / A
        p.write_text("\n".join(x for x in p.read_text().split("\n") if not x.startswith("Small Scrap")))
        proc = self.build()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads((self.out / "dataset-check.json").read_text())
        self.assertEqual(report["files"]["A"]["rows"], 5)
        self.assertEqual(report["files"]["A"]["rejected"], [])
        self.assert_hold()

    def test_missing_source(self):
        (self.src / B).unlink()
        self.assert_hold()

    def test_oversize_output(self):
        (self.out / "dataset-a.csv").write_bytes(b"X" * 1000001)
        self.assert_hold()

    def test_cli_positive(self):
        proc = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "f001_dataset_receipt_guard_371.py"), str(self.src), str(self.out)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertFalse(json.loads(proc.stdout)["release_authorized"])

    def test_cli_negative(self):
        (self.out / "dataset-a.csv").unlink()
        proc = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "f001_dataset_receipt_guard_371.py"), str(self.src), str(self.out)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("HOLD", proc.stderr)


if __name__ == "__main__":
    unittest.main()
