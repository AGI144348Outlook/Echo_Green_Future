import unittest

from bounded_composition_search import BoundedCompositionSearch, replay


OPS = (
    ("double", lambda x: x * 2),
    ("increment", lambda x: x + 1),
)


class BoundedCompositionSearchTests(unittest.TestCase):
    def test_finds_shortest_replayable_path(self):
        search = BoundedCompositionSearch(OPS, admit_state=lambda x: -1000 < x < 1000)
        result = search.find(3, lambda x: x == 11, max_depth=5)
        self.assertTrue(result.found)
        self.assertEqual(replay(3, result.path, OPS), 11)
        self.assertEqual(len(result.path), 4)

    def test_zero_length_solution(self):
        result = BoundedCompositionSearch(OPS).find(3, lambda x: x == 3, max_depth=0)
        self.assertEqual(result.path, ())
        self.assertEqual(result.reason, "initial-state-is-goal")

    def test_depth_limit_fails_closed(self):
        result = BoundedCompositionSearch(OPS).find(3, lambda x: x == 11, max_depth=3)
        self.assertFalse(result.found)
        self.assertEqual(result.reason, "depth-limit")

    def test_state_admission_rejects_outcomes(self):
        search = BoundedCompositionSearch(OPS, admit_state=lambda x: x <= 5)
        result = search.find(3, lambda x: x == 11, max_depth=5)
        self.assertFalse(result.found)
        self.assertTrue(any(e.status == "rejected-state" for e in result.events))

    def test_expansion_limit_is_enforced(self):
        result = BoundedCompositionSearch(OPS).find(
            3, lambda x: x == 999, max_depth=10, max_expansions=2
        )
        self.assertFalse(result.found)
        self.assertEqual(result.reason, "expansion-limit")
        self.assertEqual(result.expansions, 2)

    def test_operation_error_is_recorded_and_skipped(self):
        operations = (("bad", lambda _x: 1 / 0), ("increment", lambda x: x + 1))
        result = BoundedCompositionSearch(operations).find(1, lambda x: x == 2, max_depth=1)
        self.assertTrue(result.found)
        self.assertEqual(result.path, ("increment",))
        self.assertEqual(result.events[0].status, "operation-error")

    def test_duplicate_operation_names_are_rejected(self):
        with self.assertRaises(ValueError):
            BoundedCompositionSearch((("same", lambda x: x), ("same", lambda x: x)))


if __name__ == "__main__":
    unittest.main()

