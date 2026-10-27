import unittest
from collections import Counter
from a000_lobby_anchor_probe_392 import ReshIdentity, StubMatrix, StubLobby

class AnchorTests(unittest.TestCase):
    def test_anchor_without_lobby_validates(self):
        r=ReshIdentity(StubMatrix());self.assertFalse(r.validate());r.anchor();self.assertTrue(r.validate())
    def test_duplicate_occurrences_collapsed(self):
        m=StubMatrix();l=StubLobby(['governor','governor','novel','novel']);r=ReshIdentity(m,l);r.anchor();self.assertEqual(Counter(l.agents['resh'].definition_words)['novel'],1);self.assertTrue(r.validate())
    def test_original_unique_membership_preserved(self):
        l=StubLobby(['novel','other']);r=ReshIdentity(StubMatrix(),l);r.anchor();self.assertTrue({'novel','other','governor','pe'}.issubset(set(l.agents['resh'].definition_words)))
    def test_second_anchor_does_not_restore_multiplicity(self):
        l=StubLobby(['novel','novel']);r=ReshIdentity(StubMatrix(),l);r.anchor();r.anchor();self.assertEqual(l.agents['resh'].definition_words.count('novel'),1)
    def test_validation_ignores_lobby_loss(self):
        l=StubLobby(['novel','novel']);r=ReshIdentity(StubMatrix(),l);r.anchor();l.agents['resh'].definition_words.clear();self.assertTrue(r.validate())
    def test_no_resh_agent_does_not_fail(self):
        l=StubLobby([]);l.agents={};r=ReshIdentity(StubMatrix(),l);r.anchor();self.assertTrue(r.validate())
    def test_identity_symbol_tamper_fails(self):
        m=StubMatrix();r=ReshIdentity(m,StubLobby([]));r.anchor();m.known['A-000']['identity_symbol']='x';self.assertFalse(r.validate())
    def test_alias_value_tamper_passes(self):
        m=StubMatrix();r=ReshIdentity(m,StubLobby([]));r.anchor();m.known['A-000-RESH']=None;self.assertTrue(r.validate())

if __name__=='__main__':unittest.main()
