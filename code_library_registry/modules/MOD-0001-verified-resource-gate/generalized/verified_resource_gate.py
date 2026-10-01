"""Deterministic staged gate for constructing and exposing a fixed resource layout.

This is process-local governance, not authentication or a security sandbox.
"""
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json


@dataclass(frozen=True)
class ResourceSpec:
    key: str
    kind: str
    ordinal: int


class VerifiedResourceGate:
    def __init__(self, *, actor_id, target_id, resources):
        resources = tuple(resources)
        keys = [r.key for r in resources]
        if not actor_id or not target_id:
            raise ValueError("actor_id and target_id are required")
        if len(keys) != len(set(keys)):
            raise ValueError("resource keys must be unique")
        self.actor_id = actor_id
        self.target_id = target_id
        self._expected = resources
        self.target_unlocked = False
        self.creation_permitted = False
        self.resources = {}
        self.layout_locked = False
        self.verified = False
        self.storage_unlocked = False
        self._layout_digest = None
        self.audit = []

    def _deny(self, reason):
        self.verified = False
        self.storage_unlocked = False
        self.audit.append({"event": "DENIED", "reason": reason})
        raise PermissionError(reason)

    def _require(self, condition, reason):
        if not condition:
            self._deny(reason)

    def _actor(self, actor):
        self._require(actor == self.actor_id, "actor identity mismatch")

    def _layout(self):
        return {
            key: {field: value for field, value in record.items() if field != "storage"}
            for key, record in self.resources.items()
        }

    def _digest(self):
        encoded = json.dumps(self._layout(), sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    def authorize_target(self, *, actor, target_id):
        self._actor(actor)
        self._require(target_id == self.target_id, "target identity mismatch")
        self.target_unlocked = True
        self.audit.append({"event": "target_authorized", "target_id": target_id})

    def grant_creation(self, *, actor):
        self._actor(actor)
        self._require(self.target_unlocked, "target locked")
        self.creation_permitted = True
        self.audit.append({"event": "creation_granted", "actor": actor})

    def instantiate(self, *, actor):
        self._actor(actor)
        self._require(self.target_unlocked and self.creation_permitted, "creation permission absent")
        self._require(not self.resources, "resources already instantiated")
        self.resources = {
            item.key: {
                "kind": item.kind,
                "ordinal": item.ordinal,
                "storage": {},
            }
            for item in self._expected
        }
        self.layout_locked = True
        self._layout_digest = self._digest()
        self.audit.append({"event": "resources_instantiated", "count": len(self.resources)})

    def validate(self):
        expected = {
            item.key: {"kind": item.kind, "ordinal": item.ordinal}
            for item in self._expected
        }
        try:
            valid = (
                self.target_unlocked
                and self.creation_permitted
                and self.layout_locked
                and self._layout() == expected
                and self._digest() == self._layout_digest
            )
        except (KeyError, TypeError, ValueError):
            valid = False
        if not valid:
            self.verified = False
            self.storage_unlocked = False
        return bool(valid)

    def verify(self, *, actor):
        self._actor(actor)
        self._require(self.validate(), "resource verification failed")
        self.verified = True
        self.audit.append({"event": "resources_verified", "verified": True})
        return True

    def unlock_storage(self, *, actor):
        self._actor(actor)
        self._require(self.verified and self.validate(), "storage unavailable before verification")
        self.storage_unlocked = True
        self.audit.append({"event": "storage_unlocked"})

    def read_storage(self, key, *, actor):
        self._actor(actor)
        self._require(self.verified and self.validate() and self.storage_unlocked, "storage locked")
        self._require(key in self.resources, "unknown resource")
        return deepcopy(self.resources[key]["storage"])

    def snapshot(self):
        valid = self.verified and self.validate()
        return deepcopy({
            "state": {
                "target_unlocked": self.target_unlocked,
                "creation_permitted": self.creation_permitted,
                "layout_locked": self.layout_locked,
                "verified": bool(valid),
                "storage_unlocked": self.storage_unlocked,
            },
            "resources": self.resources,
            "audit": self.audit,
        })

    def run(self):
        if self.verified and self.storage_unlocked and self.validate():
            return self.snapshot()
        self.authorize_target(actor=self.actor_id, target_id=self.target_id)
        self.grant_creation(actor=self.actor_id)
        self.instantiate(actor=self.actor_id)
        self.verify(actor=self.actor_id)
        self.unlock_storage(actor=self.actor_id)
        return self.snapshot()
