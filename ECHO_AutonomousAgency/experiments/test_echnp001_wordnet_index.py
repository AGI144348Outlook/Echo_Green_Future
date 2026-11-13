"""ECHNP-001 pre-registered definition-evidence tests; no source invention."""
import tempfile
import unittest
from pathlib import Path
from echnp001_wordnet_index import (WORD_RE, lexical_occurrences, definition_record,
     native_relations, build_index, verify_index)

class MockSynset:
    def __init__(self, name, definition, lemmas=None, relatives=None):
        self._name=name; self._definition=definition; self._lemmas=lemmas or [name.split(".")[0]]
        self._relatives=relatives or {}
    def name(self): return self._name
    def definition(self): return self._definition
    def lemma_names(self): return self._lemmas
    def pos(self): return "n"
    def hypernyms(self): return self._relatives.get("hypernyms", [])
    def part_meronyms(self): return self._relatives.get("part_meronyms", [])

class DictionaryIndexTests(unittest.TestCase):
    def test_every_word_including_prepositions(self):
        text = "A wheel of the cart is with an axle, and inside a frame."
        words = [v["surface"] for v in lexical_occurrences(text, "wheel.n.01")]
        self.assertEqual(words, ["A","wheel","of","the","cart","is","with","an","axle","and","inside","a","frame"])
        self.assertEqual(len(words),len(list(WORD_RE.finditer(text))))
    def test_definition_identity_and_order_preserved(self):
        s=MockSynset("wheel.n.01","one of two wheels; a wheel")
        entry=definition_record(s)
        self.assertEqual(entry["headword_sense_id"],"wn:wheel.n.01")
        o=list(lexical_occurrences(entry["definition"],s.name()))
        self.assertEqual(len(o),7)
        self.assertEqual([v["position"] for v in o],list(range(7)))
        self.assertEqual(len(set(v["id"] for v in o)),7)
        self.assertTrue(all(v["definition_id"]==entry["id"] for v in o))
    def test_no_automatic_hypernyms_from_prepositions(self):
        s=MockSynset("wheel.n.01","a wheel of a vehicle with an axle")
        self.assertEqual(list(native_relations(s)),[])
        self.assertIn("of",[o["surface"] for o in lexical_occurrences(s.definition(),s.name())])
    def test_native_wordnet_relation_only(self):
        t=MockSynset("component.n.01","a part of a larger thing")
        s=MockSynset("wheel.n.01","a circular component of a vehicle",relatives={"hypernyms":[t]})
        rel=list(native_relations(s))
        self.assertEqual(len(rel),1)
        self.assertEqual(rel[0]["relation_type"],"is_a")
        self.assertEqual(rel[0]["source_ref"],"wordnet:wheel.n.01#hypernyms")
    def test_cycles_and_shared_spelling_are_not_merged_as_senses(self):
        a=MockSynset("bank.n.01","bank by river")
        b=MockSynset("bank.n.02","bank of money")
        x=list(lexical_occurrences(a.definition(),a.name()))
        y=list(lexical_occurrences(b.definition(),b.name()))
        self.assertEqual(x[0]["lexeme_id"],y[0]["lexeme_id"])
        self.assertNotEqual(x[0]["id"],y[0]["id"])
    def test_persisted_reconciliation(self):
        a=MockSynset("wheel.n.01","a wheel of a vehicle with an axle")
        b=MockSynset("vehicle.n.01","a vehicle on a road",relatives={"hypernyms":[a]})
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            m=build_index(iter([a,b]),out)
            self.assertEqual(m["counts"]["definitions"],2)
            self.assertGreater(m["counts"]["function_word_occurrences"],0)
            self.assertTrue(verify_index(out))
            self.assertEqual(m["counts"]["native_relations"],1)

if __name__ == "__main__":
    unittest.main()
