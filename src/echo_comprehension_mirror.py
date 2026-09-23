"""Mirror self-comprehension audit for ECHO Homework.

The source is closed while ECHO produces its reconstruction. The reconstruction
is committed before reference evidence is supplied. The audit measures recall,
semantic relation overlap, internal coherence, and transfer separately.
"""

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
import re


def _terms(text):
    return {w.lower() for w in re.findall(r"[A-Za-z]+", text or "") if len(w) > 2}


@dataclass
class ComprehensionAudit:
    word: str
    reconstruction_hash: str
    recall: float
    relational: float
    coherence: float
    transfer: float
    state: str

    def snapshot(self):
        return asdict(self)


class ComprehensionMirror:
    STATES = ("encountered", "connected", "coherent", "transferred")

    @staticmethod
    def commit(word, reconstruction, relations=None, transfer=None):
        payload = {
            "word": word.lower(),
            "reconstruction": reconstruction,
            "relations": sorted(relations or []),
            "transfer": transfer or "",
        }
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return payload, sha256(raw.encode()).hexdigest()

    @staticmethod
    def audit(committed, commitment, reference_definition,
              reference_relations=None, coherence_checks=None,
              transfer_check=None):
        raw = json.dumps(committed, sort_keys=True, ensure_ascii=False)
        if sha256(raw.encode()).hexdigest() != commitment:
            raise ValueError("reconstruction changed after commitment")

        produced = _terms(committed["reconstruction"])
        expected = _terms(reference_definition)
        recall = len(produced & expected) / max(1, len(expected))

        got_rel = {x.lower() for x in committed.get("relations", [])}
        ref_rel = {x.lower() for x in (reference_relations or [])}
        relational = len(got_rel & ref_rel) / max(1, len(ref_rel))

        checks = list(coherence_checks or [])
        coherence = sum(bool(x) for x in checks) / max(1, len(checks)) if checks else 0.0
        transfer = 1.0 if transfer_check is True else 0.0

        # State is deliberately categorical; numeric components remain visible.
        if transfer >= 1.0 and coherence >= 0.75 and relational >= 0.5:
            state = "transferred"
        elif coherence >= 0.75 and relational >= 0.5:
            state = "coherent"
        elif relational > 0:
            state = "connected"
        else:
            state = "encountered"

        return ComprehensionAudit(
            word=committed["word"],
            reconstruction_hash=commitment,
            recall=round(recall, 4),
            relational=round(relational, 4),
            coherence=round(coherence, 4),
            transfer=round(transfer, 4),
            state=state,
        )
