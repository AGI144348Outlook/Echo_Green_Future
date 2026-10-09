"""Standard-library verification for configuration_lab.py; run from this directory."""
import random
import unittest
from configuration_lab import (
    ALPHABET, ENTITIES, MOVES, TestedSet, apply_move, configuration,
    judge_b, judge_b_independent, run_arm, verify_config
)

PIN = "code-library-registry:PINNED-COMMIT-REPLACE-BEFORE-REAL-TRIAL"


class ConfigurationLabTests(unittest.TestCase):
    def test_240_ordered_pairs(self):
        c = configuration(registry_ref=PIN)
        self.assertEqual(len(c["relations"]), 240)
        self.assertTrue(verify_config(c))

    def test_canonical_independent_of_insertion_order(self):
        c = configuration(registry_ref=PIN)
        rel = dict(c["relations"])
        reversed_rel = dict(reversed(list(rel.items())))
        d = configuration(reversed_rel, registry_ref=PIN)
        self.assertEqual(c["config_id"], d["config_id"])

    def test_tamper_detected(self):
        c = configuration(registry_ref=PIN)
        c["relations"][0][1] = ">"
        with self.assertRaises(ValueError):
            verify_config(c)

    def test_registry_ref_is_part_of_identity(self):
        a = configuration(registry_ref=PIN)
        b = configuration(registry_ref=PIN + "-different")
        self.assertNotEqual(a["config_id"], b["config_id"])

    def test_duplicate_tracking(self):
        c = configuration(registry_ref=PIN)
        s = TestedSet()
        self.assertTrue(s.add(c))
        self.assertFalse(s.add(c))
        self.assertEqual(s.dump(), TestedSet.load(s.dump()).dump())

    def test_judge_agreement_for_open_and_equal(self):
        c = configuration(registry_ref=PIN)
        binding = ENTITIES[:4]
        self.assertEqual(judge_b(c, binding)["token"],
                         judge_b_independent(c, binding))
        rel = dict(c["relations"])
        for i in range(4):
            rel[f"{binding[i]}|{binding[(i+1)%4]}"] = "<"
        d = configuration(rel, registry_ref=PIN)
        self.assertEqual(judge_b(d, binding)["token"], "=")
        self.assertEqual(judge_b_independent(d, binding), "=")
        rel[f"{binding[0]}|{binding[1]}"] = ">"
        e = configuration(rel, registry_ref=PIN)
        self.assertEqual(judge_b(e, binding)["token"], "0")
        self.assertEqual(judge_b_independent(e, binding), "0")

    def test_candidate_moves_never_mutate_parent(self):
        c = configuration(registry_ref=PIN)
        before = c["config_id"]
        next_c = apply_move(c, "י", random.Random(1))
        self.assertTrue(verify_config(next_c))
        self.assertEqual(c["config_id"], before)
        self.assertNotEqual(next_c["config_id"], before)
        self.assertEqual(set(MOVES), set("וזטסמקת י".replace(" ", "")))

    def test_seed_reproducibility_and_budgets(self):
        for arm in ("random", "sparse", "adaptive"):
            a = run_arm(arm=arm, seed=21, budget=25, registry_ref=PIN)
            b = run_arm(arm=arm, seed=21, budget=25, registry_ref=PIN)
            self.assertEqual(a, b)
            self.assertLessEqual(a["tested_new"], 25)
            self.assertEqual(a["tested_new"], len(a["history"]))
            self.assertFalse(a["semantic_conclusion"])

    def test_no_unpinned_registry(self):
        with self.assertRaises(ValueError):
            configuration(registry_ref="unverified")


if __name__ == "__main__":
    unittest.main()
