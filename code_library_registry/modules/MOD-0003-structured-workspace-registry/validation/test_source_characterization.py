import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SOURCE = Path(__file__).parents[1] / "original" / "echo_matrix_dictionary.py"
SPEC = importlib.util.spec_from_file_location("echo_matrix_dictionary", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Provider:
    def senses(self, word, limit=8):
        return [{"word": word, "rank": n} for n in range(min(limit, 2))]


class SourceCharacterizationTests(unittest.TestCase):
    def test_source_create_link_index_and_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = MODULE.MatrixDictionary(Provider(), workspace=tmp)
            matrix = workspace.new_matrix("demo", "characterization")
            left = workspace.add_cell(matrix, {"value": 1}, cell_id="left")
            right = workspace.add_dictionary_cell(matrix, "echo", sense_index=1)
            workspace.relate(matrix, left, right, "supports", evidence="fixture")
            workspace.index_glyph("key", matrix, label="demo")
            saved = Path(workspace.save(matrix))
            data = json.loads(saved.read_text(encoding="utf-8"))
            self.assertEqual(data["id"], matrix)
            self.assertEqual(len(data["cells"]), 2)
            self.assertEqual(len(data["relations"]), 1)
            self.assertEqual(len(data["indexes"]), 1)

    def test_source_rejects_duplicate_cell_and_bad_sense(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = MODULE.MatrixDictionary(Provider(), workspace=tmp)
            matrix = workspace.new_matrix("demo")
            workspace.add_cell(matrix, 1, cell_id="same")
            with self.assertRaises(ValueError):
                workspace.add_cell(matrix, 2, cell_id="same")
            with self.assertRaises(IndexError):
                workspace.add_dictionary_cell(matrix, "echo", sense_index=9)


if __name__ == "__main__":
    unittest.main()

