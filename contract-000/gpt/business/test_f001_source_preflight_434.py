import json
import tempfile
import unittest
from pathlib import Path
from f001_source_preflight_434 import FILES, PreflightError, preflight


class PreflightControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src = self.root / "source"
        self.src.mkdir()
        for name in FILES:
            (self.src / name).write_text("data " + name, encoding="utf-8")
        self.dest = self.root / "receipt.json"

    def test_eight_sources(self):
        self.assertEqual(preflight(self.src, self.dest)["source_count"], 8)

    def test_manifest_matches_content(self):
        m = preflight(self.src, self.dest)
        self.assertEqual(m, json.loads(self.dest.read_text()))
        self.assertEqual(len({x["sha256"] for x in m["files"]}), 8)

    def test_replay_deterministic(self):
        preflight(self.src, self.dest)
        other = self.root / "second.json"
        preflight(self.src, other)
        self.assertEqual(self.dest.read_bytes(), other.read_bytes())

    def test_mutation_changes_digest(self):
        before = preflight(self.src, self.dest)["files"][0]["sha256"]
        (self.src / FILES[0]).write_text("changed", encoding="utf-8")
        after = preflight(self.src, self.root / "other.json")["files"][0]["sha256"]
        self.assertNotEqual(before, after)

    def test_missing_fails_without_receipt(self):
        (self.src / FILES[1]).unlink()
        with self.assertRaises(PreflightError): preflight(self.src, self.dest)
        self.assertFalse(self.dest.exists())

    def test_empty_fails(self):
        (self.src / FILES[1]).write_bytes(b"")
        with self.assertRaises(PreflightError): preflight(self.src, self.dest)

    def test_invalid_utf8_fails(self):
        (self.src / FILES[1]).write_bytes(b"\xff")
        with self.assertRaises(PreflightError): preflight(self.src, self.dest)

    def test_source_symlink_fails(self):
        link = self.root / "src-link"
        link.symlink_to(self.src, target_is_directory=True)
        with self.assertRaises(PreflightError): preflight(link, self.dest)

    def test_file_symlink_fails(self):
        (self.src / FILES[0]).unlink()
        (self.src / FILES[0]).symlink_to(self.src / FILES[1])
        with self.assertRaises(PreflightError): preflight(self.src, self.dest)

    def test_directory_instead_of_file_fails(self):
        (self.src / FILES[0]).unlink()
        (self.src / FILES[0]).mkdir()
        with self.assertRaises(PreflightError): preflight(self.src, self.dest)

    def test_refuses_inside_source(self):
        with self.assertRaises(PreflightError): preflight(self.src, self.src / "receipt.json")

    def test_refuses_clobber(self):
        self.dest.write_text("DO NOT OVERWRITE")
        with self.assertRaises(PreflightError): preflight(self.src, self.dest)
        self.assertEqual(self.dest.read_text(), "DO NOT OVERWRITE")

    def test_missing_parent_fails(self):
        with self.assertRaises(PreflightError): preflight(self.src, self.root / "missing" / "out.json")

    def test_output_symlink_fails(self):
        self.dest.symlink_to(self.src / FILES[0])
        with self.assertRaises(PreflightError): preflight(self.src, self.dest)

    def test_size_cap_fails(self):
        from unittest.mock import patch
        with patch("f001_source_preflight_434.MAX_SOURCE_BYTES", 1):
            with self.assertRaises(PreflightError): preflight(self.src, self.dest)

    def test_source_unchanged(self):
        before = {name: (self.src / name).read_bytes() for name in FILES}
        preflight(self.src, self.dest)
        self.assertEqual(before, {name: (self.src / name).read_bytes() for name in FILES})

if __name__ == "__main__":
    unittest.main(verbosity=2)
