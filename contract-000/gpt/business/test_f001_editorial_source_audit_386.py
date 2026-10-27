import copy
import tempfile
import unittest
from pathlib import Path
from f001_editorial_source_audit_386 import audit, git_blob

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.raw = b'First exact claim.\n\nSecond long claim with more content.'
        (self.root/'Article A').write_bytes(self.raw)
        (self.root/'Article B').write_bytes(self.raw)
        sha = git_blob(self.raw)
        self.q = {'project':'F-001','status':'HOLD','release_authorized':False,'card_count':3,'unreviewed_count':3,
                  'cards':[{'id':'A#S1','source_file':'Article A','source_blob_sha':sha,'sentence_no':1,'excerpt':'First exact claim.','review_status':'UNREVIEWED'},
                           {'id':'A#S2','source_file':'Article A','source_blob_sha':sha,'sentence_no':2,'excerpt':'Second long claim','review_status':'UNREVIEWED'},
                           {'id':'B#S1','source_file':'Article B','source_blob_sha':sha,'sentence_no':1,'excerpt':'First exact claim.','review_status':'UNREVIEWED'}]}
    def test_intact(self):
        r=audit(self.q,self.root)
        self.assertTrue(r['verified']); self.assertEqual(r['cards_verified'],3)
        self.assertEqual(r['truncated_preview_cards'],1)
        self.assertEqual(r['duplicate_groups'],[['A#S1','B#S1']])
        self.assertEqual(r['unique_full_sentences'],2)
    def test_tampered_blob(self):
        (self.root/'Article A').write_text('changed')
        self.assertFalse(audit(self.q,self.root)['verified'])
    def test_wrong_excerpt(self):
        self.q['cards'][1]['excerpt']='not from source'
        self.assertFalse(audit(self.q,self.root)['verified'])
    def test_missing_source(self):
        (self.root/'Article B').unlink()
        self.assertFalse(audit(self.q,self.root)['verified'])
    def test_symlink(self):
        (self.root/'Article B').unlink(); (self.root/'Article B').symlink_to('Article A')
        self.assertFalse(audit(self.q,self.root)['verified'])
    def test_duplicate_card_id(self):
        self.q['cards'][2]['id']='A#S1'
        self.assertFalse(audit(self.q,self.root)['verified'])
    def test_release_flag(self):
        self.q['release_authorized']=True
        self.assertFalse(audit(self.q,self.root)['verified'])
    def test_unauthorized_review_status(self):
        self.q['cards'][0]['review_status']='APPROVED'
        self.assertFalse(audit(self.q,self.root)['verified'])
    def test_invalid_sentence_number(self):
        self.q['cards'][0]['sentence_no']=999
        self.assertFalse(audit(self.q,self.root)['verified'])
    def test_path_traversal(self):
        self.q['cards'][0]['source_file']='../Article A'
        self.assertFalse(audit(self.q,self.root)['verified'])

if __name__ == '__main__': unittest.main()
