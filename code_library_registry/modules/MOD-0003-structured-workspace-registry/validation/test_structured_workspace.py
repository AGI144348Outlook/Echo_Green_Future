import json
from pathlib import Path
import tempfile
import unittest

from structured_workspace import StructuredWorkspace


class Provider:
    def lookup(self, key, *, limit):
        return [{"key": key, "rank": n} for n in range(min(limit, 2))]


class Ids:
    def __init__(self):
        self.value = 0

    def __call__(self):
        self.value += 1
        return f"fixed{self.value:03d}"


class StructuredWorkspaceTests(unittest.TestCase):
    def workspace(self, root):
        return StructuredWorkspace(
            provider=Provider(), root=root, id_factory=Ids(),
            clock=lambda: "2026-10-03T00:00:00+00:00",
        )

    def test_create_link_bind_and_detached_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(tmp)
            collection = workspace.create_collection("demo", "test")
            left = workspace.add_item(collection, {"value": 1})
            right = workspace.add_provider_item(collection, "echo", selection=1)
            workspace.add_relation(collection, left, right, "supports", evidence={"n": 1})
            workspace.bind_index("entry", collection, label="demo")
            snapshot = workspace.snapshot(collection)
            snapshot["items"][left]["payload"]["value"] = 99
            self.assertEqual(workspace.snapshot(collection)["items"][left]["payload"]["value"], 1)
            self.assertEqual(len(snapshot["relations"]), 1)
            self.assertEqual(len(snapshot["indexes"]), 1)

    def test_duplicate_and_missing_references_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(tmp)
            collection = workspace.create_collection("demo", collection_id="safe")
            workspace.add_item(collection, 1, item_id="same")
            with self.assertRaises(ValueError):
                workspace.add_item(collection, 2, item_id="same")
            with self.assertRaises(KeyError):
                workspace.add_relation(collection, "same", "missing", "link")
            with self.assertRaises(KeyError):
                workspace.bind_index("key", "missing")

    def test_provider_contract_and_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            no_provider = StructuredWorkspace(root=tmp)
            collection = no_provider.create_collection("demo")
            with self.assertRaises(RuntimeError):
                no_provider.add_provider_item(collection, "echo")

            workspace = self.workspace(tmp)
            collection = workspace.create_collection("demo")
            with self.assertRaises(IndexError):
                workspace.add_provider_item(collection, "echo", selection=8)
            with self.assertRaises(ValueError):
                workspace.add_provider_item(collection, "echo", limit=0)

    def test_safe_ids_and_atomic_json_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(tmp)
            with self.assertRaises(ValueError):
                workspace.create_collection("bad", collection_id="../escape")
            collection = workspace.create_collection("demo", collection_id="safe-id")
            workspace.add_item(collection, {"ok": True}, item_id="item-1")
            saved = workspace.save(collection)
            self.assertEqual(saved, Path(tmp) / "safe-id.json")
            self.assertTrue(json.loads(saved.read_text(encoding="utf-8"))["items"])
            self.assertEqual(list(Path(tmp).glob("*.tmp")), [])

    def test_unserializable_payload_does_not_replace_prior_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(tmp)
            collection = workspace.create_collection("demo", collection_id="safe")
            workspace.add_item(collection, {"version": 1}, item_id="old")
            saved = workspace.save(collection)
            prior = saved.read_bytes()
            workspace.add_item(collection, {"bad": object()}, item_id="bad")
            with self.assertRaises(TypeError):
                workspace.save(collection)
            self.assertEqual(saved.read_bytes(), prior)


if __name__ == "__main__":
    unittest.main()

