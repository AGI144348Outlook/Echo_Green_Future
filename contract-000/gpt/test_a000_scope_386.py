import copy, unittest
from a000_detached_witness_384 import attest
from a000_witness_type_gate_385 import verify_strict

class Scope(unittest.TestCase):
    def setUp(self):
        self.known={"A-000":{"name":"Governor","status":"ACTIVE","identity_symbol":"resh","identity_glyph":"ר","identity_letter":"resh"},"A-000-RESH":{"name":"Resh — Governor Identity Anchor","status":"ACTIVE","glyph":"ר","aliases":["A-000","resh","governor"]}}
        self.receipt=attest(self.known)
    def test_intact(self): self.assertTrue(verify_strict(self.known,self.receipt))
    def test_unrelated_index_growth(self):
        self.known['A-777']={'name':'new document'}
        self.assertTrue(verify_strict(self.known,self.receipt))
    def test_a000_metadata_added(self):
        self.known['A-000']['display_note']='nonidentity annotation'
        self.assertFalse(verify_strict(self.known,self.receipt))
    def test_resh_metadata_added(self):
        self.known['A-000-RESH']['last_checked']='2026-10-26'
        self.assertFalse(verify_strict(self.known,self.receipt))
    def test_identity_mutation(self):
        self.known['A-000']['identity_glyph']='ש'
        self.assertFalse(verify_strict(self.known,self.receipt))
    def test_recovery_after_metadata_reversion(self):
        self.known['A-000']['display_note']='nonidentity annotation'
        self.assertFalse(verify_strict(self.known,self.receipt))
        del self.known['A-000']['display_note']
        self.assertTrue(verify_strict(self.known,self.receipt))
    def test_type_mutation(self):
        self.known['A-000']['identity_letter']=True
        self.assertFalse(verify_strict(self.known,self.receipt))

if __name__=='__main__': unittest.main()
