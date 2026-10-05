import importlib.util
import pathlib
import unittest


SOURCE = pathlib.Path(__file__).parents[1] / "original" / "echo_hourglass.py"
SPEC = importlib.util.spec_from_file_location("echo_hourglass_source", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SourceCharacterizationTests(unittest.TestCase):
    def test_tie_economy_is_undirected_and_counts_endpoint_activations(self):
        economy = MODULE.TieEconomy()
        economy.trade("beta", "alpha", 0.25)
        economy.trade("alpha", "beta", 0.50)

        self.assertEqual(economy.ledger, {("alpha", "beta"): 0.75})
        self.assertEqual(economy.wealth("alpha"), 2)
        self.assertEqual(economy.export()["total_trades"], 4)

    def test_rejected_front_candidates_remain_in_source_queue(self):
        governor = MODULE.HourglassGovernor(["known"], flow_rate=1)
        governor.fill_dictionary(["known", "known", "known", "later"])
        economy = MODULE.TieEconomy()

        governor.one_cycle(economy, {}, {})

        self.assertEqual(governor.top_chamber, ["known", "known", "known", "later"])
        self.assertEqual(governor.cycles_run, 1)


if __name__ == "__main__":
    unittest.main()
