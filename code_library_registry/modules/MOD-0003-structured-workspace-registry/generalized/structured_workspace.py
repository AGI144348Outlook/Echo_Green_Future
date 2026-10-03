"""Small, provider-optional workspace for structured items and relations."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Callable, Mapping, Protocol, Sequence
import uuid


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class LookupProvider(Protocol):
    def lookup(self, key: str, *, limit: int) -> Sequence[Any]: ...


@dataclass
class Item:
    id: str
    payload: Any
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Relation:
    source: str
    target: str
    relation_type: str
    evidence: Any = None


@dataclass
class Collection:
    id: str
    name: str
    purpose: str = ""
    items: dict[str, Item] = field(default_factory=dict)
    relations: list[Relation] = field(default_factory=list)
    created_at: str = ""


@dataclass
class IndexBinding:
    id: str
    key: str
    collection_id: str
    label: str
    relation_type: str


class StructuredWorkspace:
    """Maintain collections, items, relations and external index bindings.

    The object is process-local. Returned snapshots are detached copies.
    Persistence uses a same-directory temporary file and ``os.replace`` so a
    completed save is atomic on filesystems that support atomic replacement.
    """

    def __init__(
        self,
        *,
        provider: LookupProvider | None = None,
        root: str | Path = "workspace",
        id_factory: Callable[[], str] | None = None,
        clock: Callable[[], str] | None = None,
    ) -> None:
        self.provider = provider
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._id_factory = id_factory or (lambda: uuid.uuid4().hex)
        self._clock = clock or (lambda: datetime.now(timezone.utc).isoformat())
        self._collections: dict[str, Collection] = {}
        self._indexes: list[IndexBinding] = []

    def create_collection(
        self,
        name: str,
        purpose: str = "",
        *,
        collection_id: str | None = None,
    ) -> str:
        identifier = collection_id or self._new_id("COL")
        self._validate_id(identifier, "collection_id")
        if identifier in self._collections:
            raise ValueError("collection id already exists")
        self._collections[identifier] = Collection(
            identifier, str(name), str(purpose), created_at=self._clock()
        )
        return identifier

    def add_item(
        self,
        collection_id: str,
        payload: Any,
        *,
        source: str = "caller",
        metadata: Mapping[str, Any] | None = None,
        item_id: str | None = None,
    ) -> str:
        collection = self._collection(collection_id)
        identifier = item_id or self._new_id("ITEM")
        self._validate_id(identifier, "item_id")
        if identifier in collection.items:
            raise ValueError("item id already exists")
        if metadata is not None and not isinstance(metadata, Mapping):
            raise TypeError("metadata must be a mapping")
        collection.items[identifier] = Item(
            identifier,
            deepcopy(payload),
            str(source),
            deepcopy(dict(metadata or {})),
        )
        return identifier

    def add_provider_item(
        self,
        collection_id: str,
        key: str,
        *,
        selection: int = 0,
        limit: int = 8,
    ) -> str:
        if self.provider is None:
            raise RuntimeError("no lookup provider attached")
        if limit <= 0:
            raise ValueError("limit must be positive")
        results = tuple(self.provider.lookup(str(key), limit=limit))
        if not results:
            payload = {"key": str(key), "result": None}
        else:
            if not 0 <= selection < len(results):
                raise IndexError("selection outside available results")
            payload = {"key": str(key), "result": deepcopy(results[selection])}
        return self.add_item(collection_id, payload, source="provider")

    def add_relation(
        self,
        collection_id: str,
        source_item: str,
        target_item: str,
        relation_type: str,
        *,
        evidence: Any = None,
    ) -> int:
        collection = self._collection(collection_id)
        if source_item not in collection.items or target_item not in collection.items:
            raise KeyError("both relation endpoints must exist")
        if not str(relation_type):
            raise ValueError("relation_type must not be empty")
        collection.relations.append(
            Relation(source_item, target_item, str(relation_type), deepcopy(evidence))
        )
        return len(collection.relations) - 1

    def bind_index(
        self,
        key: str,
        collection_id: str,
        *,
        label: str = "",
        relation_type: str = "index",
        binding_id: str | None = None,
    ) -> str:
        self._collection(collection_id)
        identifier = binding_id or self._new_id("IDX")
        self._validate_id(identifier, "binding_id")
        if any(binding.id == identifier for binding in self._indexes):
            raise ValueError("binding id already exists")
        self._indexes.append(IndexBinding(
            identifier, str(key), collection_id, str(label), str(relation_type)
        ))
        return identifier

    def snapshot(self, collection_id: str) -> dict[str, Any]:
        collection = self._collection(collection_id)
        data = asdict(collection)
        data["indexes"] = [
            asdict(binding)
            for binding in self._indexes
            if binding.collection_id == collection_id
        ]
        return deepcopy(data)

    def save(self, collection_id: str) -> Path:
        self._validate_id(collection_id, "collection_id")
        document = json.dumps(
            self.snapshot(collection_id), ensure_ascii=False, indent=2
        ) + "\n"
        target = self.root / f"{collection_id}.json"
        descriptor, temporary = tempfile.mkstemp(
            prefix=f".{collection_id}.", suffix=".tmp", dir=self.root
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(document)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
        except Exception:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
        return target

    def _collection(self, collection_id: str) -> Collection:
        try:
            return self._collections[collection_id]
        except KeyError as exc:
            raise KeyError("collection does not exist") from exc

    def _new_id(self, prefix: str) -> str:
        return f"{prefix}-{self._id_factory()[:16]}"

    @staticmethod
    def _validate_id(identifier: str, field_name: str) -> None:
        if not isinstance(identifier, str) or not _SAFE_ID.fullmatch(identifier):
            raise ValueError(f"{field_name} is not a safe identifier")

