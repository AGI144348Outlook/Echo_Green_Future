"""Isolated source-transcribed characterization; not the complete Genesis runtime."""
import unittest

class MatrixStub:
    def __init__(self):
        self.known = {'A-000': {'name':'Governor','status':'ACTIVE','identity_symbol':'resh'},
                      'A-000-RESH': {'glyph':'ר'}}
    def record(self, entry_id: str, entry: dict):
        self.known[entry_id] = entry

class ProposedGuard:
    def __init__(self, matrix): self.matrix=matrix
    def record(self, entry_id, entry):
        if entry_id in ('A-000','A-000-RESH'):
            raise PermissionError('identity slot requires explicit reviewed write')
        self.matrix.record(entry_id,entry)

class RecordGuardTests(unittest.TestCase):
    def test_original_allows_a000_replacement(self):
        m=MatrixStub();m.record('A-000',{'name':'Other'});self.assertEqual(m.known['A-000']['name'],'Other')
    def test_original_allows_alias_replacement(self):
        m=MatrixStub();m.record('A-000-RESH',None);self.assertIsNone(m.known['A-000-RESH'])
    def test_original_allows_other_algorithms(self):
        m=MatrixStub();m.record('A-111',{'name':'Other'});self.assertIn('A-111',m.known)
    def test_guard_rejects_a000(self):
        m=MatrixStub();g=ProposedGuard(m)
        with self.assertRaises(PermissionError):g.record('A-000',{})
        self.assertEqual(m.known['A-000']['name'],'Governor')
    def test_guard_rejects_alias(self):
        m=MatrixStub();g=ProposedGuard(m)
        with self.assertRaises(PermissionError):g.record('A-000-RESH',None)
    def test_guard_allows_other_ids(self):
        m=MatrixStub();g=ProposedGuard(m);g.record('A-111',{'name':'Other'});self.assertIn('A-111',m.known)
    def test_direct_dictionary_write_bypasses_wrapper(self):
        m=MatrixStub();g=ProposedGuard(m);m.known['A-000']={'name':'Unreviewed'}
        self.assertEqual(m.known['A-000']['name'],'Unreviewed')

if __name__=='__main__':unittest.main()
