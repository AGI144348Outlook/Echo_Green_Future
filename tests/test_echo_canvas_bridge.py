import unittest
from echo_canvas_bridge import EchoCanvasBridge

class BridgeTests(unittest.TestCase):
    def test_register_query_and_index(self):
        b=EchoCanvasBridge()
        result=b.register("julian","character","Julian","Citadel Nexus")
        self.assertTrue(result["indexed"])
        self.assertEqual(b.stats()["entities"],1)
        self.assertEqual(b.query('{ entity(id: "julian") { id kind label } }'),{"data":{"entity":{"id":"julian","kind":"character","label":"Julian"}}})
    def test_missing_entity(self):
        b=EchoCanvasBridge()
        self.assertEqual(b.query('{ entity(id: "absent") { id } }'),{"data":{"entity":None}})
    def test_reject_unknown_field(self):
        b=EchoCanvasBridge()
        with self.assertRaises(ValueError): b.query('{ entity(id: "x") { password } }')
    def test_reject_unsupported_mutation(self):
        b=EchoCanvasBridge()
        with self.assertRaises(ValueError): b.query('mutation { deleteEverything }')
    def test_reject_empty_id(self):
        b=EchoCanvasBridge()
        with self.assertRaises(ValueError): b.register("","x","x","text")

if __name__=="__main__": unittest.main()
