import unittest
from prototype import Card, GLYPHS, Pit, demo

class GlyphPitTests(unittest.TestCase):
    def test_27_glyphs(self):
        self.assertEqual((27, 27), (len(GLYPHS), len(set(GLYPHS))))
    def test_27_positions(self):
        self.assertEqual(27, len(Pit().positions))
    def test_incomplete_release_refused(self):
        with self.assertRaises(ValueError): Pit().release()
    def test_duplicate_glyph_refused(self):
        pit = Pit()
        card = Card("א", ("a",), ("graph",), ("identity",), "source")
        pit.load((0,0,0), card)
        with self.assertRaises(ValueError): pit.load((1,0,0), card)
    def test_invalid_operator_refused(self):
        with self.assertRaises(ValueError):
            Pit().load((0,0,0), Card("א", (), (), ("exec",), "source"))
    def test_missing_provenance_refused(self):
        with self.assertRaises(ValueError):
            Pit().load((0,0,0), Card("א", (), (), ("identity",), ""))
    def test_release(self):
        pit, swarm, _ = demo()
        self.assertTrue(pit.released)
        self.assertEqual(27, len(swarm.agents))
    def test_unique_agent_id(self):
        _, swarm, _ = demo()
        self.assertEqual(27, len(set(swarm.agents)))
    def test_origin(self):
        _, swarm, _ = demo()
        self.assertTrue(all(a.origin == "Alg-000" for a in swarm.agents.values()))
    def test_reload_refused(self):
        pit, _, _ = demo()
        with self.assertRaises(ValueError):
            pit.load((0,0,0), Card("א", (), (), ("identity",), "source"))
    def test_message_recorded(self):
        _, swarm, _ = demo()
        self.assertEqual("message", swarm.events[-2][0])
    def test_unknown_target_refused(self):
        _, swarm, _ = demo()
        with self.assertRaises(ValueError):
            swarm.message(next(iter(swarm.agents)), "missing", "hello")
    def test_candidate_logged(self):
        _, swarm, candidate = demo()
        self.assertIn(candidate, swarm.candidates)
        self.assertEqual("compose", swarm.events[-1][0])
    def test_candidate_provenance(self):
        _, swarm, candidate = demo()
        self.assertEqual(2, len(swarm.candidates[candidate]["card_provenance"]))
    def test_deterministic_replay(self):
        _, a, x = demo()
        _, b, y = demo()
        self.assertEqual((x, a.transcript()), (y, b.transcript()))
    def test_agent_not_cartesian_bound(self):
        _, swarm, _ = demo()
        self.assertTrue(all(not hasattr(a, "position") for a in swarm.agents.values()))

if __name__ == "__main__":
    unittest.main(verbosity=2)
