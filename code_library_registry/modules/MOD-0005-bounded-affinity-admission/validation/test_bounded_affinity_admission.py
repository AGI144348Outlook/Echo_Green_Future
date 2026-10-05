import unittest

from bounded_affinity_admission import BoundedAffinityAdmission, WeightedTieLedger


def table_score(table):
    return lambda left, right: table.get((left, right), table.get((right, left), 0.0))


class WeightedTieLedgerTests(unittest.TestCase):
    def test_undirected_weights_events_and_snapshot_are_unambiguous(self):
        ledger = WeightedTieLedger()
        ledger.record("beta", "alpha", 0.25)
        ledger.record("alpha", "beta", 0.50)

        self.assertEqual(ledger.event_count, 2)
        self.assertEqual(ledger.activation_count("alpha"), 2)
        self.assertEqual(ledger.strongest(), ((('alpha', 'beta'), 0.75),))
        self.assertEqual(
            ledger.snapshot()["ties"],
            [{"left": "alpha", "right": "beta", "weight": 0.75}],
        )

    def test_invalid_or_ambiguous_ties_are_rejected(self):
        ledger = WeightedTieLedger(key=lambda item: item[0])
        with self.assertRaises(ValueError):
            ledger.record("same", "same", 0.5)
        with self.assertRaises(ValueError):
            ledger.record("alpha", "atom", 0.5)
        with self.assertRaises(ValueError):
            WeightedTieLedger().record("a", "b", 1.1)


class BoundedAffinityAdmissionTests(unittest.TestCase):
    def test_thresholds_capacity_and_neighbor_ties(self):
        score = table_score(
            {
                ("mid", "base"): 0.5,
                ("high", "base"): 0.95,
                ("low", "base"): 0.01,
                ("other", "base"): 0.4,
            }
        )
        flow = BoundedAffinityAdmission(
            ["base"], per_cycle=1, min_score=0.1, max_score=0.9, neighbor_min_score=0.2
        )
        flow.enqueue(["high", "low", "mid", "other"])
        ledger = WeightedTieLedger()

        result = flow.run_cycle(ledger, score)

        self.assertEqual([d.item for d in result.accepted], ["mid"])
        self.assertEqual(
            [(d.item, d.reason) for d in result.rejected],
            [("high", "above_maximum"), ("low", "below_minimum")],
        )
        self.assertEqual(flow.queue, ("other",))
        self.assertEqual(flow.population, ("base", "mid"))
        self.assertEqual(ledger.event_count, 1)

    def test_considered_rejections_do_not_starve_later_candidates(self):
        flow = BoundedAffinityAdmission(["base"], per_cycle=1, scan_multiplier=2)
        flow.enqueue(["base", "base", "later"])
        ledger = WeightedTieLedger()
        score = lambda left, right: 0.5

        first = flow.run_cycle(ledger, score)
        second = flow.run_cycle(ledger, score)

        self.assertEqual(first.queue_remaining, 1)
        self.assertEqual([d.item for d in second.accepted], ["later"])

    def test_scoring_failure_leaves_cycle_state_uncommitted(self):
        flow = BoundedAffinityAdmission(["base"])
        flow.enqueue(["candidate"])
        ledger = WeightedTieLedger()

        def fail(left, right):
            raise RuntimeError("scorer unavailable")

        with self.assertRaisesRegex(RuntimeError, "scorer unavailable"):
            flow.run_cycle(ledger, fail)

        self.assertEqual(flow.population, ("base",))
        self.assertEqual(flow.queue, ("candidate",))
        self.assertEqual(ledger.event_count, 0)

    def test_deterministic_sampling_and_tie_order(self):
        scores = table_score(
            {
                ("candidate", "alpha"): 0.4,
                ("candidate", "beta"): 0.8,
                ("candidate", "zeta"): 0.6,
            }
        )
        flow = BoundedAffinityAdmission(
            ["zeta", "beta", "alpha"],
            admission_sample_limit=2,
            neighbor_sample_limit=3,
            max_neighbors=2,
            neighbor_min_score=0.1,
        )
        flow.enqueue(["candidate"])

        result = flow.run_cycle(WeightedTieLedger(), scores)

        decision = result.accepted[0]
        self.assertEqual(decision.score, 0.8)
        self.assertEqual(decision.neighbors, (("beta", 0.8), ("zeta", 0.6)))

    def test_configuration_and_score_ranges_are_validated(self):
        with self.assertRaises(ValueError):
            BoundedAffinityAdmission([], per_cycle=0)
        with self.assertRaises(ValueError):
            BoundedAffinityAdmission([], min_score=0.8, max_score=0.2)

        flow = BoundedAffinityAdmission(["base"])
        flow.enqueue(["candidate"])
        with self.assertRaises(ValueError):
            flow.run_cycle(WeightedTieLedger(), lambda left, right: float("nan"))


if __name__ == "__main__":
    unittest.main()
