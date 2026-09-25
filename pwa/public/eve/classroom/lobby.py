"""ECHO Classroom Lobby — Lesson 000 substrate.

Identity + vocabulary neighbors only. The vocabulary is deliberately
systems-oriented rather than anthropocentric. No taxonomy, semantic clusters,
POS index, or organizational answer is supplied.
"""
from dataclasses import dataclass, field
from typing import Dict

SEED_VOCABULARY = (
    # identity / distinction
    "identity", "entity", "state", "difference", "same", "other", "boundary", "context",
    # structure / environment
    "environment", "system", "structure", "matrix", "index", "node", "edge", "cell",
    "coordinate", "position", "axis", "anchor", "region", "layer", "network", "field",
    # relation / causality
    "relation", "connection", "constraint", "condition", "cause", "effect", "event", "transition",
    "input", "output", "source", "target", "path", "sequence", "cycle", "feedback",
    # information / knowledge
    "information", "signal", "data", "pattern", "value", "meaning", "reference", "memory",
    "known", "unknown", "uncertain", "inference", "question", "answer", "error", "noise",
    # operation / agency
    "operation", "algorithm", "process", "action", "change", "create", "connect", "separate",
    "select", "compare", "validate", "compose", "transform", "organize", "express", "perceive",
    # quantity / logic
    "one", "many", "none", "part", "whole", "true", "false", "possible",
    # time / persistence
    "before", "after", "present", "history", "persist", "repeat", "begin", "complete",
)

@dataclass(frozen=True)
class VocabularyNeighbor:
    word: str
    status: str = "neighbor"
    organization: str = "unassigned"

@dataclass
class EchoLobby:
    identity: str = "ECHO"
    neighbors: Dict[str, VocabularyNeighbor] = field(default_factory=dict)
    indexes: Dict[str, dict] = field(default_factory=dict)
    lesson: str = "L000"

    def instantiate_seed_neighbors(self) -> None:
        for word in SEED_VOCABULARY:
            self.neighbors.setdefault(word, VocabularyNeighbor(word=word))

    def snapshot(self) -> dict:
        return {
            "identity": self.identity,
            "lesson": self.lesson,
            "neighbor_count": len(self.neighbors),
            "neighbors": list(self.neighbors),
            "indexes": list(self.indexes),
            "organization_state": "UNORGANIZED" if not self.indexes else "ORGANIZED",
        }

ECHO_LOBBY = EchoLobby()
ECHO_LOBBY.instantiate_seed_neighbors()
