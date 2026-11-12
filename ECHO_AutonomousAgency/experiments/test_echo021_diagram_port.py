import unittest
from echo021_diagram_port import emit_from_echo_answer

class EchoDiagramPortTests(unittest.TestCase):
    def emit(self, answer, question="What relation do these things have?"):
        return emit_from_echo_answer(
            run_id="echo-experimental-run",
            stimulus_id="question-01",
            title="Echo output inspection",
            prompt=question,
            echo_answer=answer,
        )

    def test_unanswered_question_remains_abstained(self):
        t=self.emit({"raw_answer":None,"reason":"no_evidence_path","source_refs":[]})
        self.assertEqual(t["status"],"abstained")
        self.assertEqual(t["nodes"],[])
        self.assertEqual(t["relations"],[])
        self.assertIsNone(t["utterance"])

    def test_retrieval_must_be_marked_retrieval_not_causal_reasoning(self):
        original="The air is warm during the summer."
        t=self.emit({"raw_answer":original,"reason":"source_retrieval_fragment",
             "source_refs":["reader:page-4"]},question="Why is it warm?")
        self.assertEqual(t["utterance"],original)
        self.assertEqual(t["relations"][0]["predicate"],"retrieved_text_for")
        self.assertEqual(t["relations"][0]["source_refs"],["reader:page-4","stimulus:question-01"])
        self.assertNotIn("causes",str(t["relations"]))

    def test_existing_echo_math_is_expressed_but_not_recomputed(self):
        t=self.emit({"raw_answer":"7","reason":"observed_math_operator",
             "source_refs":["curriculum:math:observed_subtraction"]},question="12 - 5 = ?")
        self.assertEqual(t["status"],"expressed")
        self.assertEqual([n["quantity"] for n in t["nodes"]],[12,5,7])
        self.assertEqual(len(t["relations"]),2)
        self.assertTrue(all(e["predicate"]=="reported_subtraction" for e in t["relations"]))

    def test_wrong_answer_is_preserved_unfixed(self):
        t=self.emit({"raw_answer":"13","reason":"observed_math_operator",
             "source_refs":["curriculum:math:observed_subtraction"]},question="12 - 5 = ?")
        self.assertEqual(t["nodes"][-1]["quantity"],13)

    def test_prompt_numbers_alone_do_not_create_a_solution(self):
        t=self.emit({"raw_answer":"there are some objects","reason":"source_retrieval_fragment",
              "source_refs":["reading:page-2"]},question="8 + 7 = ?")
        self.assertFalse(any("quantity" in n for n in t["nodes"]))
        self.assertFalse(any(e["predicate"]=="reported_addition" for e in t["relations"]))

    def test_unsupported_response_is_not_promoted_to_proof(self):
        t=self.emit({"raw_answer":"maybe","reason":"insufficient_evidence",
              "source_refs":[]})
        self.assertEqual(t["status"],"partial")
        self.assertEqual(t["relations"],[])
        self.assertEqual(t["nodes"],[])

    def test_cannot_fake_agent_run_provenance(self):
        with self.assertRaises(ValueError):
            emit_from_echo_answer(run_id="",stimulus_id="1",prompt="?",echo_answer={},title="Test")

if __name__=="__main__":
    unittest.main()
