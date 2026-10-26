import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from f001_hold_gate_367 import verify, HoldError

class HoldGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        artifacts = []
        for name, kind in [('book.epub','epub'), ('book.pdf','pdf'), ('data.csv','csv')]:
            p = self.root / name
            p.write_bytes((kind+'-synthetic-only').encode())
            artifacts.append({'path':name,'kind':kind,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        self.data = {'project_id':'F-001','mode':'HOLD',
            'approval':{'publication_authorized':False},
            'source':{'repository':'The-TAM-protocol','commit':'a'*40,
                      'rights_evidence':'synthetic human reference','rights_reviewer':'synthetic reviewer'},
            'editorial':{'reviewer':'synthetic reviewer','claims':[{'id':'C1','status':'sourced','evidence':'synthetic reference'}]},
            'package':{'identifier':'urn:uuid:00000000-0000-4000-8000-000000000001','artifacts':artifacts}}
        self.receipt = self.root/'receipt.json'
    def check(self, data=None):
        self.receipt.write_text(json.dumps(self.data if data is None else data))
        return verify(self.receipt, self.root)
    def test_complete_stays_hold(self):
        self.assertTrue(self.check().startswith('HOLD:'))
    def test_missing_rights(self):
        del self.data['source']['rights_evidence']
        with self.assertRaises(HoldError): self.check()
    def test_missing_artifact(self):
        (self.root/'book.epub').unlink()
        with self.assertRaises(HoldError): self.check()
    def test_tampered_artifact(self):
        (self.root/'book.pdf').write_bytes(b'changed')
        with self.assertRaises(HoldError): self.check()
    def test_unreviewed_claim(self):
        self.data['editorial']['claims'][0]['status']='open'
        with self.assertRaises(HoldError): self.check()
    def test_release_requested(self):
        self.data['approval']['publication_authorized']=True
        with self.assertRaises(HoldError): self.check()
    def test_path_traversal(self):
        self.data['package']['artifacts'][0]['path']='../book.epub'
        with self.assertRaises(HoldError): self.check()
    def test_symlink(self):
        (self.root/'book.epub').unlink()
        (self.root/'book.epub').symlink_to(self.root/'book.pdf')
        with self.assertRaises(HoldError): self.check()
    def test_duplicate_json_key(self):
        self.receipt.write_text('{"project_id":"F-001","project_id":"X"}')
        with self.assertRaises(HoldError): verify(self.receipt,self.root)
    def test_malformed_json(self):
        self.receipt.write_text('{')
        with self.assertRaises(HoldError): verify(self.receipt,self.root)
    def test_nonfinite_json(self):
        self.receipt.write_text('{"n":NaN}')
        with self.assertRaises(HoldError): verify(self.receipt,self.root)
    def test_duplicate_claim(self):
        self.data['editorial']['claims'].append(copy.deepcopy(self.data['editorial']['claims'][0]))
        with self.assertRaises(HoldError): self.check()
    def test_wrong_extension(self):
        self.data['package']['artifacts'][0]['path']='book.pdf'
        with self.assertRaises(HoldError): self.check()
    def test_oversized_receipt(self):
        self.receipt.write_bytes(b' '* (1024*1024+1))
        with self.assertRaises(HoldError): verify(self.receipt,self.root)

if __name__=='__main__': unittest.main(verbosity=2)
