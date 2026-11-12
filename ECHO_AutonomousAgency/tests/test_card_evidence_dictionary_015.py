"""Algorithmic Echo card/evidence/dictionary experiment — see pre-test Issue #435."""
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ECHO_AutonomousAgency" / "src"))
from card_evidence_dictionary_015 import (PAIR_CASES, EvidenceDictionary,
                                          baseline, load_dictionary, run_comparison)


class EvidenceDictionaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dictionary = load_dictionary()

    def test_input_is_frozen_source_dictionary(self):
        self.assertEqual(len(self.dictionary), 22)
        self.assertIn("being", self.dictionary)
        self.assertIn("entity", self.dictionary)

    def test_same_wordnet_synset_has_pinned_evidence_witnesses(self):
        with EvidenceDictionary(self.dictionary) as model:
            out = model.relate("being", "existence")
            self.assertEqual(out["decision"], "supported_provisional")
            self.assertEqual(out["reason"], "exact recorded synset")
            self.assertEqual(len(out["witnesses"]), 2)
            self.assertTrue(all(w["source_card"]["revision"] == 1 for w in out["witnesses"]))
            self.assertTrue(out["not_empirical_truth"])

    def test_universal_root_does_not_make_every_word_related(self):
        self.assertEqual(baseline(self.dictionary, "entity", "relation")["decision"],
                         "associated")
        with EvidenceDictionary(self.dictionary) as model:
            self.assertEqual(model.relate("entity", "relation")["decision"], "abstain")

    def test_missing_evidence_path_requires_abstention(self):
        with EvidenceDictionary(self.dictionary) as model:
            original = model.relate("being", "existence")
            self.assertEqual(original["decision"], "supported_provisional")
            first_edge = model.graph["being"][0]
            out = model.relate("being", "existence", omit_edges={
                ("being", first_edge["from"], first_edge["to"])})
            self.assertEqual(out["decision"], "abstain")
            self.assertEqual(out["reason"], "incomplete evidence path")

    def test_stale_reference_and_homograph_cannot_make_evidence(self):
        with EvidenceDictionary(self.dictionary) as model:
            refs = dict(model.refs)
            refs["being"] = {"id": refs["being"]["id"], "revision": 99}
            self.assertEqual(model.relate("being", "existence", card_refs=refs)["decision"],
                             "abstain")
            out = model.relate("condition", "state")
            self.assertEqual(out["decision"], "abstain")

    def test_new_terms_are_candidates_not_automatic_lobby_admissions(self):
        with EvidenceDictionary(self.dictionary) as model:
            candidates = model.candidate_words()
            self.assertGreater(len(candidates), 0)
            self.assertNotIn("entity", candidates)  # already in seed
            out = model.relate("being", "existence")
            self.assertEqual(out["vocabulary_admitted"], 0)

    def test_comparison_is_not_claimed_as_new_learning(self):
        report = run_comparison(self.dictionary)
        self.assertEqual(report["comparison_pairs"], len(PAIR_CASES))
        self.assertGreater(report["baseline_associations"], 0)
        self.assertGreater(report["treatment_provisional_supports"], 0)
        self.assertLess(report["treatment_provisional_supports"], report["baseline_associations"])
        self.assertEqual(report["source_witness_coverage_of_supported"], 1.0)
        self.assertEqual(report["vocabulary_actually_admitted"], 0)
        self.assertTrue(all(c["treatment"]["decision"] != "verified_truth"
                            for c in report["cases"]))


if __name__ == "__main__":
    unittest.main()
