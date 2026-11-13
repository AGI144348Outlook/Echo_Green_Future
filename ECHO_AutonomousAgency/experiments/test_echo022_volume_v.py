import json
import unittest
from pathlib import Path
from echo022_volume_v_study import source_pages
from echo022_score import assess

class LessonIntegrity(unittest.TestCase):
    def test_all_six_source_manifests_and_page_ids(self):
        p=Path(__file__).with_name("echo022_volume_v_lessons.json")
        pages,refs,digest=source_pages(p)
        self.assertEqual({x["source_id"] for x in refs},{f"volume-v:{i}" for i in range(32,38)})
        self.assertEqual(len(pages),12)
        self.assertEqual(len(digest),64)
        self.assertTrue(all(x["hash"] for x in pages))
    def test_questions_have_no_answer_keys(self):
        p=Path(__file__).with_name("echo022_holdout_questions.json")
        items=json.loads(p.read_text())["questions"]
        self.assertGreaterEqual(len(items),12)
        self.assertTrue(all(set(q)=={"id","strand","question","passage"} for q in items))
    def test_source_fragment_is_not_scored_as_inference(self):
        r=assess([{"id":"q","strand":"test","raw_answer":"Not proof of authorization",
          "reason":"source_retrieval_fragment","source_refs":["volume-v:32:p1"]}],"after")
        self.assertEqual(r["retrieval_only"],1)
        self.assertEqual(r["independent_inference_attested"],0)
if __name__=="__main__":unittest.main()
