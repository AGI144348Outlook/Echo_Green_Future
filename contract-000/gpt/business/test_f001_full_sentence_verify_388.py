"""Synthetic verifier controls only. PRE-TEST Issue #61; no actual TAM local replay."""
import copy, tempfile, unittest
from pathlib import Path
from f001_full_sentence_verify_388 import git_blob_sha, verify

class FullSentenceTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(); self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name); self.name='sample.txt'; self.text='One sentence. Two sentences.'
        (self.root/self.name).write_text(self.text,encoding='utf-8')
        self.pin=git_blob_sha(self.text.encode()); self.pins={self.name:self.pin}
        self.queue={'status':'HOLD','release_authorized':False,'card_count':1,'source_counts':{self.name:1},'unique_normalized_sentence_count':1,'duplicate_group_count':0,'cards':[{'id':self.name+'#S1','source_file':self.name,'source_blob_sha':self.pin,'sentence_no':1,'excerpt':'One sentence.','full_sentence':'One sentence.','previous_sentence':None,'next_sentence':'Two sentences.','was_truncated':False,'review_status':'UNREVIEWED','editorial_disposition':None,'evidence_reference':None,'rights_clearance':None}]}
    def check(self,q=None): return verify(self.queue if q is None else q,self.root,self.pins,1)
    def test_intact(self): self.assertEqual(self.check(),[])
    def test_mutated_source(self): (self.root/self.name).write_text('Other sentence.');self.assertTrue(self.check())
    def test_missing_source(self): (self.root/self.name).unlink();self.assertTrue(self.check())
    def test_symlink_source(self): (self.root/self.name).unlink();(self.root/self.name).symlink_to('/etc/hosts');self.assertTrue(self.check())
    def test_wrong_full_text(self): q=copy.deepcopy(self.queue);q['cards'][0]['full_sentence']='X';self.assertTrue(self.check(q))
    def test_wrong_context(self): q=copy.deepcopy(self.queue);q['cards'][0]['next_sentence']='X';self.assertTrue(self.check(q))
    def test_unauthorized_release(self): q=copy.deepcopy(self.queue);q['release_authorized']=True;self.assertTrue(self.check(q))
    def test_editorial_approval(self): q=copy.deepcopy(self.queue);q['cards'][0]['review_status']='APPROVED';self.assertTrue(self.check(q))
    def test_truncated_preview_binding(self): q=copy.deepcopy(self.queue);q['cards'][0]['excerpt']='One';q['cards'][0]['was_truncated']=True;self.assertEqual(self.check(q),[])
    def test_truncated_preview_wrong_flag(self): q=copy.deepcopy(self.queue);q['cards'][0]['excerpt']='One';self.assertTrue(self.check(q))

if __name__=='__main__': unittest.main()
