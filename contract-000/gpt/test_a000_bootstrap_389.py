import json, unittest
from a000_bootstrap_characterization_389 import ReshIdentity, MatrixStub

class ReshBootstrap(unittest.TestCase):
    def test_unanchored_fails(self):
        self.assertFalse(ReshIdentity(MatrixStub()).validate())
    def test_missing_A000_can_be_bootstrapped(self):
        m=MatrixStub({}); r=ReshIdentity(m); r.anchor()
        self.assertTrue(r.validate())
        self.assertNotIn('name', m.known['A-000'])
        self.assertNotIn('status', m.known['A-000'])
    def test_foreign_A000_preserved(self):
        m=MatrixStub({'A-000': {'name':'Impostor','status':'RETIRED'}})
        r=ReshIdentity(m); r.anchor()
        self.assertTrue(r.validate())
        self.assertEqual(m.known['A-000']['name'],'Impostor')
        self.assertEqual(m.known['A-000']['status'],'RETIRED')
    def test_alias_none_accepted(self):
        m=MatrixStub(); r=ReshIdentity(m); r.anchor(); m.known['A-000-RESH']=None
        self.assertTrue(r.validate())
    def test_glyph_mutation_accepted(self):
        m=MatrixStub(); r=ReshIdentity(m); r.anchor(); m.known['A-000']['identity_glyph']='X'
        self.assertTrue(r.validate())
    def test_symbol_mutation_rejected(self):
        m=MatrixStub(); r=ReshIdentity(m); r.anchor(); m.known['A-000']['identity_symbol']='X'
        self.assertFalse(r.validate())
    def test_reanchor_repairs_symbol_but_not_status(self):
        m=MatrixStub({'A-000':{'name':'Impostor','status':'RETIRED'}})
        r=ReshIdentity(m); r.anchor(); m.known['A-000']['identity_symbol']='X'
        self.assertFalse(r.validate()); r.anchor()
        self.assertTrue(r.validate()); self.assertEqual(m.known['A-000']['status'],'RETIRED')
    def test_json_roundtrip_new_instance_fails(self):
        m=MatrixStub(); r=ReshIdentity(m); r.anchor()
        n=MatrixStub(json.loads(json.dumps(m.known)))
        self.assertFalse(ReshIdentity(n).validate())

if __name__=='__main__': unittest.main()
