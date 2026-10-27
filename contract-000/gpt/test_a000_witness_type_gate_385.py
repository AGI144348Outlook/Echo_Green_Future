#!/usr/bin/env python3
"""Run385 isolated candidate tests; pre-registered in Issue #13."""
import copy
import hashlib
import unittest
from a000_detached_witness_384 import attest, canonical, verify
from a000_witness_type_gate_385 import verify_strict


def fixture():
    return {
        "A-000": {"name": "Governor", "status": "ACTIVE", "identity_symbol": "resh", "identity_glyph": "ר", "iteration": 1, "confidence": 1, "nested": {"ready": 1}},
        "A-000-RESH": {"glyph": "ר", "status": "ACTIVE", "aliases": ["A-000", "resh", "governor"]}
    }


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.known = fixture()
        self.receipt = attest(self.known)

    def test_intact(self):
        self.assertTrue(verify(self.known, self.receipt))
        self.assertTrue(verify_strict(self.known, self.receipt))

    def test_bool_integer_confusion(self):
        self.known["A-000"]["iteration"] = True
        self.assertTrue(verify(self.known, self.receipt), "v1 must exhibit the type confusion")
        self.assertFalse(verify_strict(self.known, self.receipt))

    def test_integer_float_confusion(self):
        self.known["A-000"]["confidence"] = 1.0
        self.assertTrue(verify(self.known, self.receipt))
        self.assertFalse(verify_strict(self.known, self.receipt))

    def test_nested_type_confusion(self):
        self.known["A-000"]["nested"]["ready"] = True
        self.assertTrue(verify(self.known, self.receipt))
        self.assertFalse(verify_strict(self.known, self.receipt))

    def test_string_tamper(self):
        self.known["A-000-RESH"]["aliases"].append("other")
        self.assertFalse(verify_strict(self.known, self.receipt))

    def test_receipt_state_tamper(self):
        self.receipt["detached_state"]["A-000"]["iteration"] = 2
        self.assertFalse(verify_strict(self.known, self.receipt))

    def test_bad_digest(self):
        self.receipt["sha256"] = "0" * 64
        self.assertFalse(verify_strict(self.known, self.receipt))

    def test_malformed_receipt(self):
        self.assertFalse(verify_strict(self.known, {"schema": "a000-pair-candidate/v1", "detached_state": {}}))
        self.assertFalse(verify_strict(self.known, None))

    def test_missing_alias(self):
        del self.known["A-000-RESH"]
        self.assertFalse(verify_strict(self.known, self.receipt))

    def test_coordinated_reissue_still_accepted(self):
        self.known["A-000"]["iteration"] = 2
        replacement = attest(self.known)
        self.assertTrue(verify_strict(self.known, replacement), "custody remains unproven")


if __name__ == "__main__":
    unittest.main()
