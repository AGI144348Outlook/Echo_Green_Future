"""Isolated source-grounded exploratory tests. PRE #61; not frozen RC-R5."""
import copy
import unittest
from a000_identity_core_388 import anchored_fixture, source_validate, validate_candidate

class IdentityCoreScopeTests(unittest.TestCase):
    def setUp(self):
        self.m = anchored_fixture()

    def test_valid_anchored(self):
        self.assertTrue(source_validate(self.m, True)); self.assertTrue(validate_candidate(self.m, True))
    def test_instance_not_anchored(self):
        self.assertFalse(source_validate(self.m, False)); self.assertFalse(validate_candidate(self.m, False))
    def test_missing_alias(self):
        del self.m['A-000-RESH']; self.assertFalse(source_validate(self.m, True)); self.assertFalse(validate_candidate(self.m, True))
    def test_alias_none_false_accept(self):
        self.m['A-000-RESH'] = None; self.assertTrue(source_validate(self.m, True)); self.assertFalse(validate_candidate(self.m, True))
    def test_alias_foreign_dict_false_accept(self):
        self.m['A-000-RESH'] = {'unexpected':'other'}; self.assertTrue(source_validate(self.m, True)); self.assertFalse(validate_candidate(self.m, True))
    def test_identity_glyph_mutation_false_accept(self):
        self.m['A-000']['identity_glyph']='X'; self.assertTrue(source_validate(self.m, True)); self.assertFalse(validate_candidate(self.m, True))
    def test_identity_letter_mutation_false_accept(self):
        self.m['A-000']['identity_letter']='other'; self.assertTrue(source_validate(self.m, True)); self.assertFalse(validate_candidate(self.m, True))
    def test_identity_meaning_mutation_false_accept(self):
        self.m['A-000']['identity_meaning']='other'; self.assertTrue(source_validate(self.m, True)); self.assertFalse(validate_candidate(self.m, True))
    def test_alias_type_mutation_false_accept(self):
        self.m['A-000-RESH']['type']='OTHER'; self.assertTrue(source_validate(self.m, True)); self.assertFalse(validate_candidate(self.m, True))
    def test_alias_list_mutation_false_accept(self):
        self.m['A-000-RESH']['aliases']=['A-000']; self.assertTrue(source_validate(self.m, True)); self.assertFalse(validate_candidate(self.m, True))
    def test_unrelated_a000_metadata_is_permitted(self):
        self.m['A-000']['runtime_counter']=77; self.assertTrue(source_validate(self.m, True)); self.assertTrue(validate_candidate(self.m, True))
    def test_unrelated_alias_metadata_is_permitted(self):
        self.m['A-000-RESH']['annotation']={'changed':True}; self.assertTrue(source_validate(self.m, True)); self.assertTrue(validate_candidate(self.m, True))
    def test_original_fields_unchanged(self):
        original=copy.deepcopy(self.m); self.assertTrue(validate_candidate(original, True)); self.assertEqual(original,self.m)
    def test_bool_flag_must_be_bool(self):
        self.assertTrue(source_validate(self.m, 1)); self.assertFalse(validate_candidate(self.m, 1))

if __name__=='__main__': unittest.main()
