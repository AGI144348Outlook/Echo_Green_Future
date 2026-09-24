"""ECHO Classroom Lobby — Lesson 000 substrate.

This module instantiates identity + vocabulary neighbors only.
It deliberately supplies no semantic index, taxonomy, clustering, or answer
to the organization assignment. ECHO must devise those later.
"""
from dataclasses import dataclass, field
from typing import Dict, List

SEED_VOCABULARY = (
    "I", "you", "we", "this", "that", "who", "what", "not",
    "all", "many", "one", "two", "person", "water", "fire",
    "earth", "eat", "drink", "see", "hear",
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
