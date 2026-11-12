"""ECHO-020 protocol and exam isolation checks; pre-test Issue #448."""
import json
import unittest
from pathlib import Path
from echo020_grade1_study import EchoSchool, words
from echo020_grade1_score import contains_exact_alias

HERE=Path(__file__).resolve().parent
class GradeOneProtocolTests(unittest.TestCase):
 def test_source_catalog_is_real_first_grade_material(self):
  data=json.loads((HERE/"echo020_grade1_source_manifest.json").read_text())
  self.assertGreaterEqual(len(data["sources"]),8)
  self.assertEqual({x["strand"] for x in data["sources"]},
   {"reading","language","math","science","social_studies"})
  for source in data["sources"]:
   self.assertTrue(source["url"].startswith("https://www.coreknowledge.org/"))
   self.assertTrue(source["type"] in {"pdf","html"})
 def test_exam_frozen_cross_subject_and_heldout(self):
  data=json.loads((HERE/"echo020_grade1_heldout_exam.json").read_text())
  self.assertEqual(len(data["questions"]),35)
  self.assertEqual(len({q["id"] for q in data["questions"]}),35)
  for strand in data["strands"]:
   self.assertEqual(sum(q["strand"]==strand for q in data["questions"]),7)
  self.assertTrue(all(q.get("acceptable") for q in data["questions"]))
 def test_answer_key_is_not_in_study_source(self):
  code=(HERE/"echo020_grade1_study.py").read_text()
  self.assertNotIn("echo020_grade1_heldout_exam.json",code)
  self.assertIn('if any("acceptable" in x',code)
  self.assertNotIn("OpenAI",code)
 def test_strict_math_matching_and_no_guess_scoring(self):
  self.assertTrue(contains_exact_alias("15",["15"])[0])
  self.assertFalse(contains_exact_alias("150",["15"])[0])
  self.assertFalse(contains_exact_alias("",["15"])[0])
 def test_curriculum_agent_has_no_preloaded_answers(self):
  a=EchoSchool(None,[])
  # No source materials read, no learned operator or lesson cards.
  self.assertEqual(a.cards,{})
  self.assertEqual(a.links,{})
  self.assertEqual(a.sentences,[])
  self.assertEqual(sum(x["n"] for x in a.policy.values()),0)
if __name__=="__main__":unittest.main()
