import unittest
from echo_canvas_bridge import EchoCanvasBridge

class Integration002(unittest.TestCase):
    def test_baseline_unchanged_and_overlay_opt_in(self):
        b = EchoCanvasBridge()
        matrix = b.matrix
        b.register("node-a", "registry", "A", "indexing reference")
        self.assertIs(b.plasticity.matrix, matrix)
        self.assertFalse(b.plasticity.traverse("node-a", "node-b")["applied"])
        self.assertEqual(b.plasticity.snapshot()["links"], [])
        b.enable_plasticity()
        self.assertTrue(b.plasticity.traverse("node-a", "node-b", True)["applied"])
        self.assertIs(b.matrix, matrix)
        self.assertEqual(b.query('{ entity(id: "node-a") { id } }')["data"]["entity"]["id"], "node-a")

    def test_resource_budget_and_dormancy(self):
        b = EchoCanvasBridge()
        p = b.plasticity
        p.enabled = True
        p.max_links = 1
        p.max_traversals_per_tick = 2
        self.assertTrue(p.traverse("a", "b")["applied"])
        self.assertEqual(p.traverse("a", "c")["reason"], "link_budget")
        self.assertTrue(p.traverse("a", "b")["applied"])
        self.assertEqual(p.traverse("a", "b")["reason"], "tick_budget")
        p.next_tick()
        p.dormant("a", "b")
        self.assertEqual(p.traverse("a", "b")["reason"], "dormant")
        p.reactivate("a", "b")
        self.assertTrue(p.traverse("a", "b")["applied"])

    def test_recess_replay_and_identity(self):
        b = EchoCanvasBridge()
        b.recess_operation({"op": "PRESENTIATE", "id": "entity", "word": "entity", "x": 600, "y": 316, "r": 30})
        b.recess_operation({"op": "PRESENTIATE", "id": "cast", "word": "cast", "x": 700, "y": 724, "r": 30})
        b.recess_operation({"op": "MOVE", "id": "cast", "x": 610, "y": 340})
        b.recess_operation({"op": "ROTATE", "id": "cast", "theta": 1.5})
        b.recess_operation({"op": "ALIGN", "a": "entity", "b": "cast", "kind": "shared_segment"})
        b.recess_operation({"op": "SET_GROUP", "group": 1, "members": ["entity", "cast"]})
        s = b.stats()["recess"]
        self.assertEqual(s["nodes"]["cast"]["x"], 610)
        self.assertEqual(s["nodes"]["cast"]["theta"], 1.5)
        self.assertEqual(s["groups"]["1"], ["entity", "cast"])
        self.assertEqual(s["operations"], 6)
        with self.assertRaises(ValueError):
            b.recess_operation({"op": "PRESENTIATE", "id": "cast"})

    def test_recess_rejects_invalid_operations(self):
        b = EchoCanvasBridge()
        with self.assertRaises(ValueError):
            b.recess_operation({"op": "EXECUTE_PYTHON", "code": "pass"})
        with self.assertRaises(ValueError):
            b.recess_operation({"op": "MOVE", "id": "unknown", "x": 2})

if __name__ == "__main__":
    unittest.main()
