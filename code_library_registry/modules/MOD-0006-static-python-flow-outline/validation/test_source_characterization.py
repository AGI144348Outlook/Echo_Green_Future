import ast
import json
import unittest

import libmap


SOURCE = """
def choose(x):
    if x:
        left()
    else:
        right()
    finish()
"""


class SourceCharacterizationTests(unittest.TestCase):
    def test_missing_target_returns_json_null_string(self):
        self.assertEqual(libmap.flow_from_source(SOURCE, None, "absent"), "null")

    def test_branch_is_an_outline_without_join_edges(self):
        result = json.loads(libmap.flow_from_source(ast.parse(SOURCE), None, "choose"))
        gate = next(i for i, node in enumerate(result["nodes"]) if node["kind"] == "gate")
        finish = next(i for i, node in enumerate(result["nodes"]) if node["name"].startswith("finish"))
        self.assertIn([gate, finish, "next"], result["links"])
        self.assertFalse(any(edge[1] == finish and edge[0] != gate for edge in result["links"]))


if __name__ == "__main__":
    unittest.main()
