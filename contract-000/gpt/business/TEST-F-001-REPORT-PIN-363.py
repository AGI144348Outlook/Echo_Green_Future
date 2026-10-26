#!/usr/bin/env python3
"""Synthetic Run 363 prospective Issue #56 suite. No real TAM stage or release."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("F-001-REPORT-PIN-363.py")
spec = importlib.util.spec_from_file_location("f001_pin363", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def valid():
    return {"base_g_per_unit": 13.7, "source_commit": checker.PIN_COMMIT,
            "files": {k: dict(v, rejected=[]) for k, v in checker.PINS.items()}}


class Tests(unittest.TestCase):
    def test_valid_synthetic(self):
        self.assertEqual(checker.validate(valid()), {"status":"HOLD","consistent":True,"errors":[]})

    def test_field_corruptions(self):
        changes = [
            lambda x: x.update(source_commit="wrong"),
            lambda x: x.update(base_g_per_unit=14),
            lambda x: x.update(extra=True),
            lambda x: x.pop("source_commit"),
            lambda x: x["files"]["A"].update(sha256="0" * 64),
            lambda x: x["files"]["B"].update(git_blob="0" * 40),
            lambda x: x["files"]["A"].update(rows=5),
            lambda x: x["files"]["A"].update(rows=True),
            lambda x: x["files"]["B"].update(rejected=["bad row"]),
            lambda x: x["files"].pop("B"),
            lambda x: x["files"]["A"].update(unexpected="bad"),
            lambda x: x.update(files=[]),
            lambda x: x.update(base_g_per_unit=True),
        ]
        for i, change in enumerate(changes):
            with self.subTest(case=i):
                fixture = copy.deepcopy(valid()); change(fixture)
                r = checker.validate(fixture)
                self.assertFalse(r["consistent"])
                self.assertEqual(r["status"], "HOLD")

    def test_strict_duplicate_top(self):
        raw = json.dumps(valid()).replace('"source_commit":', '"source_commit":"bad", "source_commit":')
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            checker.decode_strict(raw.encode())

    def test_strict_duplicate_nested(self):
        raw = json.dumps(valid()).replace('"rows": 6', '"rows": 7, "rows": 6')
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            checker.decode_strict(raw.encode())

    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            checker.decode_strict(b'{"base_g_per_unit":NaN}')

    def test_real_358_shape_rejected(self):
        # Historical Run 358 report shape lacks source_commit/git_blob; synthetic reproduction.
        older = valid(); older.pop("source_commit")
        for rec in older["files"].values(): rec.pop("git_blob")
        self.assertFalse(checker.validate(older)["consistent"])

    def test_bounded_path_and_cli(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td); good=d/"good.json"; good.write_text(json.dumps(valid()))
            result=checker.verify_path(good)
            self.assertTrue(result["consistent"])
            p=subprocess.run([sys.executable,"-I","-B",str(SCRIPT),str(good)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(p.stdout)["status"],"HOLD")
            symlink=d/"link.json"; symlink.symlink_to(good)
            self.assertFalse(checker.verify_path(symlink)["consistent"])
            oversized=d/"oversized.json"; oversized.write_bytes(b" "*(checker.MAX_REPORT_BYTES+1))
            self.assertFalse(checker.verify_path(oversized)["consistent"])
            self.assertFalse(checker.verify_path(d)["consistent"])
            self.assertFalse(checker.verify_path(d/"absent.json")["consistent"])
            duplicate=d/"duplicate.json"; duplicate.write_text(json.dumps(valid()).replace('"rows": 6','"rows": 7, "rows": 6'))
            self.assertFalse(checker.verify_path(duplicate)["consistent"])
            bad=subprocess.run([sys.executable,"-I","-B",str(SCRIPT),str(duplicate)],capture_output=True,text=True)
            self.assertEqual(bad.returncode,1)
            self.assertEqual(json.loads(bad.stdout)["status"],"HOLD")

if __name__ == "__main__":
    unittest.main(verbosity=2)
