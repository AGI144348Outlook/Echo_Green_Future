"""Test 003: identity-preserving, replaceable glyph profile assignments with real A-000 bridge.
The card registry is an experimental adapter; AlgorithmMatrix itself is not modified.
"""
import copy
import unittest
from echo_canvas_bridge import EchoCanvasBridge

class IndexCards:
    def __init__(self, matrix):
        self.matrix = matrix
        self.glyphs = {}
        self.cards = {}
        self.active = {}
        self.history = []
    def glyph(self, identity, source):
        if identity in self.glyphs: raise ValueError("duplicate glyph")
        self.glyphs[identity] = copy.deepcopy(source)
    def card(self, name, profile):
        if name in self.cards: raise ValueError("duplicate card")
        self.cards[name] = copy.deepcopy(profile)
    def assign(self, glyph, context, card):
        if glyph not in self.glyphs or card not in self.cards:
            raise ValueError("unknown glyph or card")
        key = (glyph, context)
        previous = self.active.get(key)
        self.active[key] = card
        self.history.append({"glyph":glyph,"context":context,"previous":previous,"current":card})
    def profile(self, glyph, context):
        return copy.deepcopy(self.cards[self.active[(glyph,context)]])

class Test003(unittest.TestCase):
    def setUp(self):
        self.bridge = EchoCanvasBridge()
        self.matrix = self.bridge.matrix
        self.cards = IndexCards(self.matrix)
        self.cards.glyph("glyph:aleph", {"symbol":"א","identity":"aleph"})
        self.cards.glyph("glyph:resh", {"symbol":"ר","identity":"resh"})
    def test_real_matrix_reference_and_identity(self):
        before = copy.deepcopy(self.cards.glyphs["glyph:aleph"])
        self.cards.card("cart",{"frame":"cartesian","xyz":[0,0,0]})
        self.cards.card("ray",{"frame":"nve-ray","radius":1})
        self.cards.assign("glyph:aleph","lvt","cart")
        self.cards.assign("glyph:aleph","lvt","ray")
        self.assertIs(self.cards.matrix,self.matrix)
        self.assertIs(self.bridge.matrix,self.matrix)
        self.assertEqual(self.cards.glyphs["glyph:aleph"],before)
        self.assertEqual(self.cards.history[-1]["previous"],"cart")
        self.assertEqual(self.cards.profile("glyph:aleph","lvt")["frame"],"nve-ray")
    def test_matrix_indexing_survives_card_reassignment(self):
        self.bridge.register("glyph:aleph","glyph","Aleph","aleph identity anchor")
        self.cards.card("a",{"element":"H"})
        self.cards.card("b",{"element":"He"})
        self.cards.assign("glyph:aleph","science","a")
        before = self.matrix.documents_seen
        self.cards.assign("glyph:aleph","science","b")
        self.assertEqual(self.matrix.documents_seen,before)
        self.assertEqual(self.bridge.query('{ entity(id: "glyph:aleph") { id label } }')["data"]["entity"]["id"],"glyph:aleph")
        self.assertEqual(self.cards.cards["a"]["element"],"H")
    def test_context_isolation_and_no_implicit_execution(self):
        self.cards.card("scientific",{"element":"H"})
        self.cards.card("operator",{"operation":"MOVE","executable":False})
        self.cards.assign("glyph:resh","science","scientific")
        self.cards.assign("glyph:resh","operation","operator")
        self.assertEqual(self.cards.profile("glyph:resh","science")["element"],"H")
        self.assertFalse(self.cards.profile("glyph:resh","operation")["executable"])
    def test_rejected_assignment_is_atomic(self):
        self.cards.card("valid",{"frame":"cartesian"})
        self.cards.assign("glyph:aleph","lvt","valid")
        history = copy.deepcopy(self.cards.history)
        active = copy.deepcopy(self.cards.active)
        with self.assertRaises(ValueError): self.cards.assign("glyph:aleph","lvt","missing")
        self.assertEqual(self.cards.history,history)
        self.assertEqual(self.cards.active,active)
    def test_overlay_is_not_implicitly_enabled(self):
        self.cards.card("ray",{"frame":"nve-ray"})
        self.cards.assign("glyph:aleph","lvt","ray")
        self.assertFalse(self.bridge.plasticity.enabled)
        self.assertEqual(self.bridge.plasticity.snapshot()["links"],[])

if __name__=="__main__":
    unittest.main(verbosity=2)
