"""Unified lineage and audit record for ECHO Homework.

Records study events without storing third-party image bytes or live image URLs.
The resulting snapshot can be frozen before Classroom examination.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json


@dataclass(frozen=True)
class HomeworkEvent:
    sequence: int
    action: str
    concept: str
    source: str
    parent: str | None = None
    detail_hash: str | None = None


class HomeworkAudit:
    def __init__(self):
        self.events = []
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.frozen = False

    @staticmethod
    def _hash_detail(detail):
        if detail is None:
            return None
        canonical = json.dumps(detail, sort_keys=True, default=str)
        return sha256(canonical.encode("utf-8")).hexdigest()

    def record(self, action, concept, source, parent=None, detail=None):
        if self.frozen:
            raise RuntimeError("Homework audit is frozen")
        event = HomeworkEvent(
            sequence=len(self.events) + 1,
            action=action,
            concept=concept.lower(),
            source=source,
            parent=parent.lower() if parent else None,
            detail_hash=self._hash_detail(detail),
        )
        self.events.append(event)
        return event

    def record_seed(self, word):
        return self.record("instantiate", word, "seed")

    def record_definition(self, word, definition, candidates):
        return self.record(
            "definition",
            word,
            "GF WordNet",
            detail={"definition": definition, "candidates": sorted(candidates)},
        )

    def record_instantiation(self, word, parent, source="definition"):
        return self.record("instantiate", word, source, parent=parent)

    def record_visual_exposure(self, word, source, references):
        return self.record(
            "visual_exposure",
            word,
            source,
            detail={"reference_hashes": [
                sha256(str(ref).encode("utf-8")).hexdigest()
                for ref in references
            ]},
        )

    def freeze(self, governor_snapshot=None):
        if self.frozen:
            return self.snapshot(governor_snapshot)
        self.frozen = True
        return self.snapshot(governor_snapshot)

    def snapshot(self, governor_snapshot=None):
        payload = {
            "started_at": self.started_at,
            "frozen": self.frozen,
            "events": [asdict(event) for event in self.events],
            "governor": governor_snapshot,
        }
        canonical = json.dumps(payload, sort_keys=True, default=str)
        payload["audit_sha256"] = sha256(canonical.encode("utf-8")).hexdigest()
        return payload
