"""Deterministic development boot protocol; process-local governance, not a security sandbox."""
from copy import deepcopy
import hashlib
import json

STANDARD = tuple("אבגדהוזחטיכלמנסעפצקרשת")
EXTENDED = ("ם", "ן", "ף", "ץ", "ך")
TARGET = "invariant_alg_001"
GOVERNOR = "governor_indexing_alg"

class AlgorithmMatrixRuntime:
    def __init__(self):
        self.primary = {"matrix_id": "algorithm_matrix_primary", "status": "LOCKED",
                        "active_slots": 1, "matrix_data": [
                            {"slot_index": [0, 0], "algorithm_id": TARGET,
                             "type": "INVARIANT_TARGET", "executable": False}],
                        "governor_context": {"governor_id": GOVERNOR,
                            "permission_scope": ["matrix_data[0][0]"],
                            "validation_condition": "IDENTITY_MATCH",
                            "unlock_target": "algorithm_matrix_primary"}}
        self.permit = False
        self.sub_matrices = {}
        self.infrastructure_locked = False
        self.verifier_instantiated = False
        self.verified = False
        self.storage_unlocked = False
        self.digest = None
        self.audit = []

    def _require(self, condition, reason):
        if not condition:
            self.verified = False
            self.storage_unlocked = False
            self.audit.append({"event": "DENIED", "reason": reason})
            raise PermissionError(reason)

    def _actor(self, actor):
        self._require(actor == GOVERNOR, "Governor identity mismatch")

    def _digest(self):
        layout = {key: {k: v for k, v in value.items() if k != "storage"}
                  for key, value in self.sub_matrices.items()}
        return hashlib.sha256(json.dumps(layout, sort_keys=True,
                                          ensure_ascii=False).encode()).hexdigest()

    def alg_001(self, actor=GOVERNOR, target=TARGET, slot=(0, 0)):
        self._actor(actor)
        self._require(target == TARGET and slot == (0, 0), "Invariant identity or scope mismatch")
        self._require(self.primary["matrix_data"] == [
            {"slot_index": [0, 0], "algorithm_id": TARGET,
             "type": "INVARIANT_TARGET", "executable": False}], "Invariant slot modified")
        self.primary["status"] = "UNLOCKED"
        self.audit.append({"event": "alg_001", "status": "UNLOCKED"})

    def alg_003(self, actor=GOVERNOR):
        self._actor(actor)
        self._require(self.primary["status"] == "UNLOCKED", "Primary matrix locked")
        self.permit = True
        self.audit.append({"event": "alg_003", "granted_to": actor})

    def alg_004(self, actor=GOVERNOR):
        self._actor(actor)
        self._require(self.primary["status"] == "UNLOCKED" and self.permit,
                      "Creation permission absent")
        self._require(not self.sub_matrices, "Infrastructure already instantiated")
        for group, glyphs in (("standard", STANDARD), ("extended", EXTENDED)):
            for index, glyph in enumerate(glyphs):
                self.sub_matrices[f"{group}:{index}"] = {
                    "glyph": glyph, "group": group, "index": index, "storage": {}}
        self.infrastructure_locked = True
        self.digest = self._digest()
        self.verifier_instantiated = True
        self.audit.append({"event": "alg_004", "count": 27, "status": "LOCKED"})

    def alg_005(self, actor=GOVERNOR):
        self._actor(actor)
        expected = {(group, i, glyph) for group, glyphs in
                    (("standard", STANDARD), ("extended", EXTENDED))
                    for i, glyph in enumerate(glyphs)}
        actual = {(v["group"], v["index"], v["glyph"]) for v in self.sub_matrices.values()}
        self._require(self.verifier_instantiated and self.infrastructure_locked
                      and len(self.sub_matrices) == 27 and actual == expected
                      and self._digest() == self.digest, "Infrastructure verification failed")
        self.verified = True
        self.audit.append({"event": "alg_005", "verified": True})
        return True

    def alg_002(self):
        try:
            valid = (self.primary["status"] == "UNLOCKED" and self.permit
                     and self.verifier_instantiated and self.infrastructure_locked
                     and self.verified and len(self.sub_matrices) == 27
                     and self._digest() == self.digest)
        except (KeyError, TypeError):
            valid = False
        if not valid:
            self.verified = False
            self.storage_unlocked = False
        return bool(valid)

    def alg_006(self, actor=GOVERNOR):
        self._actor(actor)
        self._require(self.alg_002(), "Storage key unavailable before verification")
        self.storage_unlocked = True
        self.audit.append({"event": "alg_006", "storage_unlocked": True})

    def storage(self, matrix_id, actor=GOVERNOR):
        self._actor(actor)
        self._require(self.alg_002() and self.storage_unlocked, "Storage locked")
        return deepcopy(self.sub_matrices[matrix_id]["storage"])

    def snapshot(self):
        valid = self.alg_002()
        return deepcopy({"primary": self.primary, "system_state": {
            "primary_matrix_unlocked": self.primary["status"] == "UNLOCKED",
            "alg_002_status": valid, "storage_unlocked": self.storage_unlocked},
            "sub_matrices": self.sub_matrices, "audit": self.audit})

    def run_boot_handshake(self):
        if self.storage_unlocked and self.alg_002():
            return self.snapshot()
        self.alg_001()
        self.alg_003()
        self.alg_004()
        self.alg_005()
        self.alg_006()
        return self.snapshot()
