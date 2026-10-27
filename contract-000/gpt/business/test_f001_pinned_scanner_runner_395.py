#!/usr/bin/env python3
"""Run395 synthetic controls for pinned replay; requires F001_SCANNER pointing to original claim_scan.py."""
import os
from pathlib import Path
import tempfile
import unittest
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "f001_runner", Path(__file__).with_name("f001_pinned_scanner_runner_395.py"))
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
PINS, SCANNER_BLOB, git_blob, replay = (
    _module.PINS, _module.SCANNER_BLOB, _module.git_blob, _module.replay)


class ReplayTests(unittest.TestCase):
    def setUp(self):
        scanner = Path(os.environ["F001_SCANNER"])
        self.assertEqual(git_blob(scanner.read_bytes()), SCANNER_BLOB)
        self.tmp = tempfile.TemporaryDirectory(prefix="f001-395-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root / "source"
        self.src.mkdir()
        for name in PINS:
            (self.src / name).write_text("Nothing here.\n", encoding="utf-8")
        (self.src / "README.md").write_text(
            "This proves a test. Another ordinary sentence.\n", encoding="utf-8")
        self.pins = {name: git_blob((self.src / name).read_bytes()) for name in PINS}
        self.scanner = scanner
        self.out = self.root / "output"

    def run_replay(self, rows=1):
        return replay(self.src, self.scanner, self.out,
                      pins=self.pins, expected_rows=rows)

    def assert_rejected(self, *args):
        with self.assertRaises((ValueError, OSError)):
            self.run_replay(*args)

    def test_01_positive_hold(self):
        receipt = self.run_replay()
        self.assertEqual((receipt["rows"], receipt["readiness"]), (1, "HOLD"))

    def test_02_missing_source(self):
        (self.src / "Article 10").unlink()
        self.assert_rejected()

    def test_03_modified_source(self):
        (self.src / "Article 10").write_text("Changed", encoding="utf-8")
        self.assert_rejected()

    def test_04_symlink_source(self):
        (self.src / "Article 10").unlink()
        (self.src / "Article 10").symlink_to(self.src / "README.md")
        self.assert_rejected()

    def test_05_wrong_scanner_pin(self):
        with self.assertRaises(ValueError):
            replay(self.src, self.scanner, self.out, pins=self.pins,
                   scanner_pin="0" * 40, expected_rows=1)

    def test_06_wrong_candidate_count(self):
        self.assert_rejected(42)

    def test_07_output_inside_source(self):
        self.out = self.src / "output"
        self.assert_rejected()

    def test_08_existing_output(self):
        self.out.mkdir()
        self.assert_rejected()

    def test_09_directory_as_input(self):
        (self.src / "Article 10").unlink()
        (self.src / "Article 10").mkdir()
        self.assert_rejected()


if __name__ == "__main__":
    unittest.main(verbosity=2)
