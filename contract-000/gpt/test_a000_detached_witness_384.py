import copy
import unittest
from a000_detached_witness_384 import attest, verify


def fixture():
    return {"A-000": {"name": "Governor", "status": "ACTIVE", "identity_symbol": "resh", "identity_glyph": "ר"},
            "A-000-RESH": {"status": "ACTIVE", "glyph": "ר", "aliases": ["A-000", "resh", "governor"]}}


class WitnessTests(unittest.TestCase):
    def setUp(self):
        self.known = fixture()
        self.receipt = attest(self.known)

    def test_intact(self):
        self.assertTrue(verify(self.known, self.receipt))

    def test_status_tamper(self):
        self.known["A-000"]["status"] = "TAMPERED"
        self.assertFalse(verify(self.known, self.receipt))

    def test_alias_tamper(self):
        self.known["A-000-RESH"]["aliases"][:] = ["A-001"]
        self.assertFalse(verify(self.known, self.receipt))

    def test_missing_governor(self):
        del self.known["A-000"]
        self.assertFalse(verify(self.known, self.receipt))

    def test_alias_missing(self):
        del self.known["A-000-RESH"]
        self.assertFalse(verify(self.known, self.receipt))

    def test_detached_not_aliased(self):
        before = copy.deepcopy(self.receipt)
        self.known["A-000-RESH"]["aliases"].append("new")
        self.assertEqual(self.receipt, before)
        self.assertFalse(verify(self.known, self.receipt))

    def test_receipt_mutation(self):
        self.receipt["detached_state"]["A-000"]["name"] = "Changed"
        self.assertFalse(verify(self.known, self.receipt))

    def test_receipt_hash_mutation(self):
        self.receipt["sha256"] = "0" * 64
        self.assertFalse(verify(self.known, self.receipt))

    def test_missing_alias_identity_field(self):
        self.known["A-000"]["identity_glyph"] = "א"
        self.assertFalse(verify(self.known, self.receipt))

    def test_no_claim_of_custody(self):
        # An attacker replacing both matrix state and receipt is outside this model.
        forged = attest(self.known)
        self.assertTrue(verify(self.known, forged))


if __name__ == "__main__":
    unittest.main()
