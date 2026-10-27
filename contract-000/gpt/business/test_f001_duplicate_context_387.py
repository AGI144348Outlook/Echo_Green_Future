"""Synthetic tests for HOLD-only context comparator; PRE https://github.com/AGI144348Outlook/Echo_Green_Future/issues/60"""
import tempfile
import unittest
from pathlib import Path
from f001_duplicate_context_387 import compare_pair, compare_sources, git_blob_sha, sentences

class ContextTests(unittest.TestCase):
    def test_identical_windows(self):
        r=compare_pair(["before.","claim.","after."],2,["before.","claim.","after."],2)
        self.assertTrue(r["raw_previous_equal"] and r["raw_next_equal"])
    def test_zero_width_previous_is_normalized(self):
        r=compare_pair(["I.","claim.","after."],2,["\u200bI.","claim.","after."],2)
        self.assertFalse(r["raw_previous_equal"]);self.assertTrue(r["normalized_previous_equal"])
    def test_zero_width_next_is_normalized(self):
        r=compare_pair(["before.","claim.","II."],2,["before.","claim.","\u200bII."],2)
        self.assertFalse(r["raw_next_equal"]);self.assertTrue(r["normalized_next_equal"])
    def test_real_next_word_change_not_hidden(self):
        r=compare_pair(["before.","claim.","next one."],2,["before.","claim.","next two."],2)
        self.assertFalse(r["normalized_next_equal"])
    def test_end_of_file_differs_from_continuation(self):
        r=compare_pair(["before.","claim."],2,["before.","claim.","continuation."],2)
        self.assertFalse(r["normalized_next_equal"]);self.assertFalse(r["left_has_next"]);self.assertTrue(r["right_has_next"])
    def test_claim_mismatch_rejected(self):
        with self.assertRaises(ValueError):compare_pair(["claim."],1,["other."],1)
    def test_index_out_of_bounds_rejected(self):
        with self.assertRaises(ValueError):compare_pair(["claim."],0,["claim."],1)
    def test_pinned_synthetic_source_accepted(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/"a";b=Path(t)/"b";a.write_text("before.\n\nclaim.");b.write_text("before.\n\nclaim.\n\ncontinuation.")
            r=compare_sources(t,{"a":git_blob_sha(a.read_bytes()),"b":git_blob_sha(b.read_bytes())},[("a",2,"b",2)])
            self.assertEqual(r["status"],"HOLD");self.assertFalse(r["pairs"][0]["normalized_next_equal"])
    def test_changed_source_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/"a";a.write_text("claim.");pin=git_blob_sha(a.read_bytes());a.write_text("tamper.")
            with self.assertRaises(ValueError):compare_sources(t,{"a":pin},[("a",1,"a",1)])
    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/"a";a.write_text("claim.");(Path(t)/"link").symlink_to(a)
            with self.assertRaises(ValueError):compare_sources(t,{"link":git_blob_sha(a.read_bytes())},[("link",1,"link",1)])
    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):compare_sources(t,{"../outside":"abc"},[])
    def test_splitter_keeps_numbered_sentence_positions(self):
        self.assertEqual(sentences("One. Two!\n\nThree?"),["One.","Two!","Three?"])

if __name__=="__main__":unittest.main()
