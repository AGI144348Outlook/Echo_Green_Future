"""Synthetic controls only. No TAM text or real-source scanner execution."""
import json
import tempfile
import unittest
from pathlib import Path
from f001_git_pin_gate_435 import FILES, PinError, REPO, SCHEMA, git_blob_sha1, verify

class PinControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root / "untrusted"
        self.src.mkdir()
        for name in FILES:
            (self.src / name).write_text("synthetic " + name, encoding="utf-8")
        self.pins = self.root / "pins.json"
        self.out = self.root / "receipt.json"
        self.payload = {"schema": SCHEMA, "repository": REPO, "ref": "a" * 40,
                        "files": [{"name": n, "git_blob_sha1": git_blob_sha1((self.src / n).read_bytes())} for n in FILES]}
        self.write_pins()

    def write_pins(self):
        self.pins.write_text(json.dumps(self.payload), encoding="utf-8")

    def assert_rejected(self):
        with self.assertRaises(PinError):
            verify(self.src, self.pins, self.out)
        self.assertFalse(self.out.exists())

    def test_positive_eight(self):
        receipt = verify(self.src, self.pins, self.out)
        self.assertEqual(receipt["source_count"], 8)
        self.assertEqual(receipt["status"], "HOLD_SOURCE_PIN_MATCH_NOT_EDITORIAL_APPROVAL")
        self.assertEqual(receipt, json.loads(self.out.read_text()))

    def test_git_blob_formula(self):
        self.assertEqual(git_blob_sha1(b"test\n"), "9daeafb9864cf43055ae93beb0afd6c7d144bfa4")

    def test_deterministic_receipt(self):
        verify(self.src, self.pins, self.out)
        other = self.root / "other.json"
        verify(self.src, self.pins, other)
        self.assertEqual(self.out.read_bytes(), other.read_bytes())

    def test_mutated_source_rejected(self):
        (self.src / FILES[0]).write_text("modified", encoding="utf-8")
        self.assert_rejected()

    def test_missing_source_rejected(self):
        (self.src / FILES[1]).unlink()
        self.assert_rejected()

    def test_empty_source_rejected(self):
        (self.src / FILES[1]).write_bytes(b"")
        self.assert_rejected()

    def test_invalid_utf8_rejected(self):
        (self.src / FILES[1]).write_bytes(b"\xff")
        self.assert_rejected()

    def test_symlink_source_rejected(self):
        (self.src / FILES[0]).unlink()
        (self.src / FILES[0]).symlink_to(self.src / FILES[1])
        self.assert_rejected()

    def test_missing_pin_rejected(self):
        self.payload["files"].pop()
        self.write_pins()
        self.assert_rejected()

    def test_duplicate_pin_rejected(self):
        self.payload["files"][0] = self.payload["files"][1].copy()
        self.write_pins()
        self.assert_rejected()

    def test_unexpected_pin_rejected(self):
        self.payload["files"][0]["name"] = "unlisted.txt"
        self.write_pins()
        self.assert_rejected()

    def test_wrong_pin_rejected(self):
        self.payload["files"][0]["git_blob_sha1"] = "0" * 40
        self.write_pins()
        self.assert_rejected()

    def test_bad_commit_ref_rejected(self):
        self.payload["ref"] = "main"
        self.write_pins()
        self.assert_rejected()

    def test_duplicate_json_key_rejected(self):
        raw = self.pins.read_text()
        self.pins.write_text(raw.replace('"schema":', '"schema": "bad", "schema":', 1))
        self.assert_rejected()

    def test_manifest_inside_source_rejected(self):
        inner = self.src / "pins.json"
        inner.write_text(self.pins.read_text())
        with self.assertRaises(PinError): verify(self.src, inner, self.out)

    def test_output_inside_source_rejected(self):
        with self.assertRaises(PinError): verify(self.src, self.pins, self.src / "receipt.json")

    def test_clobber_rejected(self):
        self.out.write_text("keep")
        with self.assertRaises(PinError): verify(self.src, self.pins, self.out)
        self.assertEqual(self.out.read_text(), "keep")

    def test_missing_pin_file_rejected(self):
        self.pins.unlink()
        self.assert_rejected()

    def test_source_bytes_unchanged(self):
        before = {n: (self.src / n).read_bytes() for n in FILES}
        verify(self.src, self.pins, self.out)
        self.assertEqual(before, {n: (self.src / n).read_bytes() for n in FILES})

if __name__ == "__main__":
    unittest.main(verbosity=2)
