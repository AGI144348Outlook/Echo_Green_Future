import unittest

from static_python_flow_outline import TargetNotFound, outline_source


SOURCE = """
SIDE_EFFECT = dangerous()

def choose(x):
    \"\"\"Ignored docstring.\"\"\"
    if x:
        left(x)
    else:
        right(x)
    return finish(x)

class Worker:
    async def run(self, items):
        for item in items:
            await handle(item)
"""


class StaticPythonFlowOutlineTests(unittest.TestCase):
    def test_parses_without_executing_module_source(self):
        outline = outline_source(SOURCE, "choose")
        self.assertEqual(outline.target, "choose")
        self.assertNotIn("dangerous", " ".join(node.detail for node in outline.nodes))

    def test_branch_arms_and_following_statement_are_explicit(self):
        outline = outline_source(SOURCE, "choose")
        labels = [edge.label for edge in outline.edges]
        self.assertIn("true", labels)
        self.assertIn("false", labels)
        self.assertIn("next", labels)

    def test_direct_async_class_method_is_supported(self):
        outline = outline_source(SOURCE, "run", class_name="Worker")
        self.assertEqual(outline.target, "Worker.run")
        self.assertTrue(any(node.kind == "loop" for node in outline.nodes))

    def test_result_is_deterministic_and_serializable(self):
        first = outline_source(SOURCE, "choose").as_dict()
        second = outline_source(SOURCE, "choose").as_dict()
        self.assertEqual(first, second)
        self.assertEqual([node["id"] for node in first["nodes"]], list(range(len(first["nodes"]))))

    def test_node_limit_is_strict_and_reports_truncation(self):
        outline = outline_source(SOURCE, "choose", max_nodes=2)
        self.assertEqual(len(outline.nodes), 2)
        self.assertTrue(outline.truncated)

    def test_missing_target_and_invalid_limits_fail_explicitly(self):
        with self.assertRaises(TargetNotFound):
            outline_source(SOURCE, "missing")
        with self.assertRaises(ValueError):
            outline_source(SOURCE, "choose", max_nodes=0)

    def test_syntax_error_is_not_hidden(self):
        with self.assertRaises(SyntaxError):
            outline_source("def broken(:", "broken")


if __name__ == "__main__":
    unittest.main()
