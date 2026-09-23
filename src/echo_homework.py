"""ECHO constrained homework governor.

Lobby membership is permission to study.
Unknown words discovered in permitted definitions become candidates,
not automatic Lobby members.
"""

import re

WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")


class HomeworkGovernor:
    def __init__(self, seeds, max_turns=100, max_new_words_per_turn=5):
        self.lobby = {w.lower() for w in seeds}
        self.candidates = set()
        self.max_turns = max_turns
        self.max_new_words_per_turn = max_new_words_per_turn
        self.turn = 0
        self.lineage = {w: {"source": "seed", "parent": None} for w in self.lobby}

    def _spend_turn(self):
        if self.turn >= self.max_turns:
            raise RuntimeError("Homework study budget exhausted")
        self.turn += 1

    def require_lobby(self, word):
        word = word.lower()
        if word not in self.lobby:
            raise PermissionError(f"{word} is not instantiated in the Lobby")
        return word

    def discover_from_definition(self, word, definition):
        parent = self.require_lobby(word)
        self._spend_turn()
        found = {w.lower() for w in WORD.findall(definition)}
        found -= self.lobby
        found.discard(parent)
        self.candidates.update(found)
        return sorted(found)

    def instantiate(self, words, parent):
        parent = self.require_lobby(parent)
        self._spend_turn()
        chosen = []
        for raw in words:
            word = raw.lower()
            if len(chosen) >= self.max_new_words_per_turn:
                break
            if word not in self.candidates:
                raise PermissionError(f"{word} was not discovered during permitted study")
            self.candidates.remove(word)
            self.lobby.add(word)
            self.lineage[word] = {"source": "definition", "parent": parent}
            chosen.append(word)
        return chosen

    def snapshot(self):
        return {
            "turn": self.turn,
            "lobby": sorted(self.lobby),
            "candidates": sorted(self.candidates),
            "lineage": self.lineage,
        }
