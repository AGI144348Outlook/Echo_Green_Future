"""Mirror comprehension audit.

Audits what ECHO can reconstruct about an instantiated Lobby word without
granting new dictionary access. Scores are structural diagnostics, not claims
of human-like understanding.
"""

from dataclasses import dataclass, asdict
from hashlib import sha256
import json


@dataclass
class ComprehensionRecord:
    word: str
    recall: float
    relations: float
    coherence: float
    transfer: float
    contradictions: int = 0

    @property
    def score(self):
        # Transfer/coherence matter more than simple recall.
        raw = (
            0.15 * self.recall +
            0.30 * self.relations +
            0.30 * self.coherence +
            0.25 * self.transfer
        )
        return max(0.0, min(1.0, raw - min(self.contradictions, 3) * 0.10))

    @property
    def state(self):
        s = self.score
        if s >= 0.85: return "transferred"
        if s >= 0.70: return "coherent"
        if s >= 0.50: return "connected"
        if s > 0.0: return "encountered"
        return "unresolved"


class MirrorComprehensionAudit:
    def __init__(self, governor):
        self.governor = governor
        self.records = {}

    def audit(self, word, *, recall, relations, coherence, transfer,
              contradictions=0):
        word = self.governor.require_lobby(word)
        vals = [recall, relations, coherence, transfer]
        if any(v < 0 or v > 1 for v in vals):
            raise ValueError("comprehension signals must be between 0 and 1")
        record = ComprehensionRecord(
            word, recall, relations, coherence, transfer, contradictions
        )
        self.records[word] = record
        return record

    def weak_words(self, threshold=0.70):
        return sorted(
            (r for r in self.records.values() if r.score < threshold),
            key=lambda r: (r.score, r.word),
        )

    def coverage(self, threshold=0.70):
        lobby = self.governor.lobby
        if not lobby:
            return 1.0
        passed = sum(
            1 for w in lobby
            if w in self.records and self.records[w].score >= threshold
        )
        return passed / len(lobby)

    def next_action(self, threshold=0.70, coverage_target=0.90):
        weak = self.weak_words(threshold)
        if weak:
            return {"action": "repair", "word": weak[0].word,
                    "reason": "weak comprehension"}
        if self.coverage(threshold) < coverage_target:
            unaudited = sorted(set(self.governor.lobby) - set(self.records))
            return {"action": "audit", "word": unaudited[0] if unaudited else None,
                    "reason": "insufficient audited coverage"}
        return {"action": "expand", "word": None,
                "reason": "current vocabulary is sufficiently coherent"}

    def snapshot(self):
        body = {
            "coverage_0_70": self.coverage(),
            "records": {w: {**asdict(r), "score": r.score, "state": r.state}
                        for w, r in sorted(self.records.items())},
        }
        encoded = json.dumps(body, sort_keys=True).encode()
        body["sha256"] = sha256(encoded).hexdigest()
        return body
