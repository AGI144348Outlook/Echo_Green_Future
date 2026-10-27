import copy
import unittest
from f001_occurrence_evidence_gate_392 import check

H = 'a' * 64

def fixture():
    q = {'project':'F-001','card_count':3,'cards':[
        {'id':'Article 6#S29','source_file':'Article 6','source_blob_sha':'b'*40,'full_sentence':'Duplicate claim.'},
        {'id':'Collective information#S178','source_file':'Collective information','source_blob_sha':'c'*40,'full_sentence':'Duplicate claim.'},
        {'id':'README.md#S24','source_file':'README.md','source_blob_sha':'d'*40,'full_sentence':'Another claim.'}
    ]}
    d = {'project':'F-001','decisions':[
        {'occurrence_id':'Article 6#S29','action':'retain_sourced','reviewer':'reviewer A','editorial_note':'source checked','rights':'cleared','rights_basis':'signed review','evidence_refs':['e1']},
        {'occurrence_id':'Collective information#S178','action':'cut','reviewer':'reviewer B','editorial_note':'remove duplicate'},
        {'occurrence_id':'README.md#S24','action':'qualify','reviewer':'reviewer C','editorial_note':'qualify claim','rights':'cleared','rights_basis':'rights record','replacement_text':'A hypothesis to test.'}
    ],'evidence':[{'id':'e1','occurrence_id':'Article 6#S29','reference':'source1','locator':'p.12','reviewed_by':'reviewer A'}],
    'artifact_receipts':[{'occurrence_id':'Collective information#S178','format':fmt,'absent':True,'artifact_sha256':H} for fmt in ('epub','pdf')]}
    return q,d

class GateTests(unittest.TestCase):
    def test_complete_schema_still_hold(self):
        q,d=fixture();r=check(q,d);self.assertTrue(r['schema_complete']);self.assertEqual(r['release_status'],'HOLD');self.assertFalse(r['release_authorized'])
    def test_partial_queue_is_hold(self):
        q,d=fixture();d['decisions'].pop();r=check(q,d);self.assertFalse(r['schema_complete']);self.assertEqual(r['pending_occurrences'],1)
    def test_sourced_without_reference_fails(self):
        q,d=fixture();d['decisions'][0]['evidence_refs']=[];self.assertIn('lacks evidence',str(check(q,d)['errors']))
    def test_cross_occurrence_reference_fails(self):
        q,d=fixture();d['evidence'][0]['occurrence_id']='Collective information#S178';self.assertIn('not independently occurrence-bound',str(check(q,d)['errors']))
    def test_duplicate_decision_fails(self):
        q,d=fixture();d['decisions'].append(copy.deepcopy(d['decisions'][0]));self.assertIn('duplicate decision',str(check(q,d)['errors']))
    def test_duplicate_sentence_distinct_occurrences(self):
        q,d=fixture();d['decisions']=[d['decisions'][0],d['decisions'][2]];r=check(q,d);self.assertEqual(r['pending_occurrences'],1);self.assertFalse(r['schema_complete'])
    def test_cut_missing_pdf_fails(self):
        q,d=fixture();d['artifact_receipts']=[d['artifact_receipts'][0]];self.assertIn('pdf cut-absence',str(check(q,d)['errors']))
    def test_cut_bad_hash_fails(self):
        q,d=fixture();d['artifact_receipts'][1]['artifact_sha256']='fake';self.assertIn('pdf cut-absence',str(check(q,d)['errors']))
    def test_unknown_card_fails(self):
        q,d=fixture();d['decisions'][0]['occurrence_id']='not-real';self.assertIn('unknown occurrence',str(check(q,d)['errors']))
    def test_missing_rights_fails(self):
        q,d=fixture();d['decisions'][0]['rights']='unknown';self.assertIn('rights clearance',str(check(q,d)['errors']))
    def test_qualify_needs_replacement(self):
        q,d=fixture();d['decisions'][2].pop('replacement_text');self.assertIn('qualifying text missing',str(check(q,d)['errors']))
    def test_forged_release_flag_still_hold(self):
        q,d=fixture();d['release_authorized']=True;d['status']='LAUNCH';r=check(q,d);self.assertEqual(r['release_status'],'HOLD');self.assertFalse(r['release_authorized'])
    def test_bad_queue_count_fails(self):
        q,d=fixture();q['card_count']=45;self.assertIn('queue card count',str(check(q,d)['errors']))
    def test_duplicate_evidence_id_fails(self):
        q,d=fixture();d['evidence'].append(copy.deepcopy(d['evidence'][0]));self.assertIn('duplicate evidence',str(check(q,d)['errors']))

if __name__=='__main__':unittest.main()
