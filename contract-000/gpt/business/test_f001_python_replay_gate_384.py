#!/usr/bin/env python3
"""Synthetic regression for HOLD-only F-001 scanner replay; no real TAM source checkout."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import f001_python_replay_gate_384 as gate

SCANNER = Path(os.environ["F001_SCANNER_PATH"]).resolve()  # Git blob 31f3dcf; from library-shared


class ReplayGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.src = self.base / "source"
        self.src.mkdir()
        self.out = self.base / "out"
        self.pins = {}
        for name in gate.PINS:
            p = self.src / name
            p.write_text("This result is proven.\n", encoding="utf-8")
            self.pins[name] = gate.blob_sha(p.read_bytes())
        inv = {"project": "F-001", "status": "HOLD", "release_authorized": False,
               "baseline_candidates": 8, "supplemental_unflagged_candidates": 1,
               "combined_review_queue": 9,
               "sources": [{"file": k, "blob_sha": v} for k, v in self.pins.items()],
               "baseline": [{"file": k, "sentence_no": 1, "triggers": ["certainty"],
                             "excerpt": "This result is proven."} for k in self.pins],
               "supplemental": [{"file": "README.md", "sentence_no": 2}]}
        self.inventory = self.base / "inventory.json"
        self.inventory.write_text(json.dumps(inv), encoding="utf-8")
        self.pin_patch = patch.object(gate, "PINS", self.pins)
        self.inv_patch = patch.object(gate, "INVENTORY_PIN", gate.blob_sha(self.inventory.read_bytes()))
        self.pin_patch.start()
        self.inv_patch.start()
        self.addCleanup(self.pin_patch.stop)
        self.addCleanup(self.inv_patch.stop)

    def replay(self):
        return gate.run(self.src, SCANNER, self.inventory.resolve(), self.out)

    def test_valid_synthetic_original_scanner(self):
        r = self.replay()
        self.assertEqual(r["baseline_replayed"], 8)
        self.assertEqual(r["supplemental_not_scanned"], 1)
        self.assertEqual(r["status"], "HOLD")
        self.assertEqual(r["editorial_reviewed"], 0)
        self.assertFalse(r["publication_authorized"])

    def test_missing_source(self):
        (self.src / "Article 5").unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            self.replay()

    def test_tampered_source(self):
        (self.src / "Article 5").write_text("This result is unproven.")
        with self.assertRaisesRegex(ValueError, "blob mismatch"):
            self.replay()

    def test_symlink_source(self):
        p = self.src / "Article 5"
        data = p.read_bytes()
        p.unlink()
        target = self.base / "outside"
        target.write_bytes(data)
        p.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.replay()

    def test_output_inside_source(self):
        self.out = self.src / "output"
        with self.assertRaisesRegex(ValueError, "inside source"):
            self.replay()

    def test_output_existing(self):
        self.out.mkdir()
        with self.assertRaisesRegex(ValueError, "new, absent"):
            self.replay()

    def test_inventory_changed_without_repin(self):
        x = json.loads(self.inventory.read_text())
        x["baseline"][0]["excerpt"] = "forged"
        self.inventory.write_text(json.dumps(x))
        with self.assertRaisesRegex(ValueError, "blob mismatch"):
            self.replay()

    def test_inventory_repin_detects_bad_excerpt(self):
        x = json.loads(self.inventory.read_text())
        x["baseline"][0]["excerpt"] = "forged"
        self.inventory.write_text(json.dumps(x))
        with patch.object(gate, "INVENTORY_PIN", gate.blob_sha(self.inventory.read_bytes())):
            with self.assertRaisesRegex(ValueError, "content or status differs"):
                self.replay()

    def test_inventory_release_flag(self):
        x = json.loads(self.inventory.read_text())
        x["release_authorized"] = True
        self.inventory.write_text(json.dumps(x))
        with patch.object(gate, "INVENTORY_PIN", gate.blob_sha(self.inventory.read_bytes())):
            with self.assertRaisesRegex(ValueError, "HOLD"):
                self.replay()

    def test_scanner_tamper(self):
        p = self.base / "scanner.py"
        p.write_bytes(SCANNER.read_bytes() + b"\n# change\n")
        with self.assertRaisesRegex(ValueError, "blob mismatch"):
            gate.run(self.src, p.resolve(), self.inventory.resolve(), self.out)

    def test_inventory_wrong_source_pin(self):
        x = json.loads(self.inventory.read_text())
        x["sources"][0]["blob_sha"] = "0" * 40
        self.inventory.write_text(json.dumps(x))
        with patch.object(gate, "INVENTORY_PIN", gate.blob_sha(self.inventory.read_bytes())):
            with self.assertRaisesRegex(ValueError, "inventory pin mismatch"):
                self.replay()


if __name__ == "__main__":
    unittest.main()
