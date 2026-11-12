"""Pre-registered ECHO-017 full WordNet scope / safety tests (Issue #438)."""
import tempfile
import unittest
from pathlib import Path
from echo017_full_wordnet_study import Study, ALLOWED_SYSTEMS, ALLOWED_TOOLS, wn


class FullWordNetStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.st = Study()

    def test_full_lexical_corpus_not_22_word_fixture(self):
        self.assertGreater(len(self.st.full_lemmas), 100000)
        self.assertGreater(self.st.full_synsets, 100000)
        self.assertIn("dog", self.st.lemma_set)
        self.assertIn("transcendence", self.st.lemma_set)

    def test_only_three_authorized_systems_discoverable(self):
        discovered = self.st.mcp_request(
            {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})["result"]["tools"]
        self.assertEqual({x["name"] for x in discovered}, ALLOWED_TOOLS)
        self.assertEqual(ALLOWED_SYSTEMS, {"dictionary", "catalog", "evidence"})
        self.assertEqual({x["name"].split(".")[0] for x in discovered}, ALLOWED_SYSTEMS)
        self.assertTrue(any("Use it for gaining additional meaning" in x["description"]
                            for x in discovered))

    def test_source_senses_not_arbitrarily_limited(self):
        result = self.st.mcp_request({"jsonrpc": "2.0", "id": 2,
              "method": "tools/call", "params": {"name": "dictionary.lexical_senses",
                 "arguments": {"word": "set"}}})
        self.assertFalse(result["result"]["isError"])
        import json
        details = json.loads(result["result"]["content"][0]["text"])
        self.assertGreater(details["synsets"], 8)
        self.assertEqual(details["synsets"], len(wn.synsets("set")))

    def test_source_backed_proposal_and_unrelated_tool_denial(self):
        self.st._study_senses("dog")
        out = self.st._perform("evidence.edge.propose", {"word": "dog"})
        self.assertEqual(out["outcome"], "provisional_edge")
        edge = self.st.edges[out["edge_id"]]
        self.assertEqual(edge["evidence_state"], "proposed")
        self.assertTrue(edge["source_ref"].startswith("Princeton WordNet:"))
        denied = self.st.mcp_request({"jsonrpc": "2.0", "id": 3,
          "method": "tools/call", "params": {"name": "shell.run",
             "arguments": {"command": "echo test"}}})
        self.assertEqual(denied["error"]["code"], -32602)

    def test_no_action_pacing_and_active_time_budget(self):
        st = Study()
        with tempfile.TemporaryDirectory() as temp:
            result = st.run(seconds=0.25, outdir=temp)
            self.assertGreaterEqual(result["elapsed_active_wall_seconds"], 0.25)
            self.assertTrue(result["no_artificial_pacing"])
            self.assertGreater(result["action_count"], 0)
            self.assertEqual(result["wordnet_total_synsets_available"], st.full_synsets)
            self.assertEqual(result["allowed_systems"], ["catalog", "dictionary", "evidence"])
            self.assertEqual(result["mcp_transport"], "in-process JSON-RPC tool API, not deployed MCP-over-HTTP")
            self.assertTrue((Path(temp) / "echo017_full_wordnet_summary.json").exists())


if __name__ == "__main__":
    unittest.main()
