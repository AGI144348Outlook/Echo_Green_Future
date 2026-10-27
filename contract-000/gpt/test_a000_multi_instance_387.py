"""Isolated source-transcribed ReshIdentity lifecycle characterization, Genesis blob 63eb982.
PRE-TEST: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/60
Not a complete Genesis runtime, Governor implementation, or frozen test.
"""
import unittest

class ReshIdentity:
    """Methods transcribed from genesis-documentary/src/echo_governor_skeleton.py:3233-3305."""
    def __init__(self, matrix, hebrew_lobby=None):
        self.matrix = matrix
        self.hebrew_lobby = hebrew_lobby
        self._anchored = False
        self._anchor_entry = None

    def anchor(self):
        a000 = self.matrix.known.get("A-000", {})
        a000["identity_symbol"] = "resh"
        a000["identity_glyph"] = "ר"
        a000["identity_letter"] = "resh"
        a000["identity_meaning"] = "head beginning leader identity"
        self.matrix.known["A-000"] = a000
        self.matrix.known["A-000-RESH"] = {
            "name": "Resh — Governor Identity Anchor",
            "status": "ACTIVE",
            "type": "IDENTITY-LETTER",
            "glyph": "ר",
            "aliases": ["A-000", "resh", "governor"],
            "description": (
                "The Governor and Resh are one and the same — "
                "Resh is head, beginning, identity; the Governor "
                "reads Resh when it reads itself in the matrix. "
                "Identity validation (IDENTIFY→VALIDATE→OPEN) "
                "runs through this entry."),
            "perception_operator": "ayin",
            "expression_operator": "pe",
        }
        if self.hebrew_lobby:
            resh_agent = self.hebrew_lobby.agents.get("resh")
            if resh_agent:
                resh_agent.definition_words = list(set(
                    resh_agent.definition_words +
                    ["governor", "indexing", "algorithm", "identity",
                     "matrix", "aleph", "ayin", "pe"]))
        self._anchored = True
        self._anchor_entry = self.matrix.known["A-000-RESH"]
        return self._anchor_entry

    def validate(self):
        return (self._anchored
                and "A-000-RESH" in self.matrix.known
                and self.matrix.known.get("A-000", {}).get("identity_symbol") == "resh")

class MatrixStub:
    def __init__(self):
        self.known={"A-000":{"name":"Governor","status":"ACTIVE"}}

class MultiInstanceTests(unittest.TestCase):
    def setUp(self):
        self.m=MatrixStub()
        self.a=ReshIdentity(self.m)
        self.b=ReshIdentity(self.m)
    def test_initial_both_unanchored(self):
        self.assertFalse(self.a.validate());self.assertFalse(self.b.validate())
    def test_first_instance_true_second_false_on_same_matrix(self):
        self.a.anchor();self.assertTrue(self.a.validate());self.assertFalse(self.b.validate())
    def test_second_anchor_allows_both(self):
        self.a.anchor();self.b.anchor();self.assertTrue(self.a.validate());self.assertTrue(self.b.validate())
    def test_second_anchor_replaces_alias_record(self):
        old=self.a.anchor();self.b.anchor();self.assertIsNot(old,self.m.known["A-000-RESH"])
    def test_first_anchor_reference_stale_after_second_anchor(self):
        self.a.anchor();self.b.anchor();self.assertIsNot(self.a._anchor_entry,self.m.known["A-000-RESH"])
    def test_first_instance_still_validates_after_alias_replacement(self):
        self.a.anchor();self.b.anchor();self.m.known["A-000-RESH"]={"unexpected":"replacement"};self.assertTrue(self.a.validate())
    def test_deleted_alias_fails_both(self):
        self.a.anchor();self.b.anchor();del self.m.known["A-000-RESH"];self.assertFalse(self.a.validate());self.assertFalse(self.b.validate())
    def test_reinsert_any_alias_restores_both_without_reanchor(self):
        self.a.anchor();self.b.anchor();del self.m.known["A-000-RESH"];self.m.known["A-000-RESH"]=None;self.assertTrue(self.a.validate());self.assertTrue(self.b.validate())

if __name__ == "__main__":unittest.main()
