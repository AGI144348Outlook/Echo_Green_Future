#!/usr/bin/env python3
"""Run430 SOURCE-TRANSCRIBED bounded WordAgent/Lobby identity-guard fixture.
Relevant methods transcribed from genesis-documentary:src/echo_governor_skeleton.py
Git blob 63eb982989b4f3478d649430b555c8f4ba755c27.
NOT the complete Genesis runtime, a frozen race test or identity compromise.
"""
import re

class WordAgent:
    def __init__(self, word, definition_words):
        self.word = word
        self.definition_words = definition_words
        self.identity_confirmed = False
        self.ties = set()

    def confirm_identity(self):
        if not self.identity_confirmed:
            self.identity_confirmed = bool(self.word)
        return self.identity_confirmed

    def words_referenced_in_definitions(self):
        found = set()
        for token in re.findall(r"[a-z\']+", " ".join(self.definition_words).lower()):
            if token and token != self.word.lower() and len(token) > 1:
                found.add(token)
        return found

class Lobby:
    def __init__(self):
        self.agents = {}
        self.ties = {}

    def add_tie(self, w1, w2, strength=1):
        key = tuple(sorted([w1, w2]))
        self.ties[key] = self.ties.get(key, 0) + strength
        a1, a2 = self.agents.get(w1), self.agents.get(w2)
        if a1: a1.ties.add(w2)
        if a2: a2.ties.add(w1)

    def run_orientation(self):
        if not all(a.identity_confirmed for a in self.agents.values()):
            unconfirmed = [w for w, a in self.agents.items() if not a.identity_confirmed]
            raise RuntimeError(
                f"Orientation blocked: {len(unconfirmed)} agents have "
                f"not confirmed identity. First: {unconfirmed[:3]}")
        discovered = {
            word: agent.words_referenced_in_definitions()
            for word, agent in self.agents.items()
        }
        for word, referenced_words in discovered.items():
            for other_word in referenced_words:
                if other_word in self.agents and other_word != word:
                    self.add_tie(word, other_word, strength=1)
        return len(self.ties)

def main():
    n = 0
    def check(condition, label):
        nonlocal n
        assert condition, label
        n += 1

    a = WordAgent("resh", ["aleph"])
    b = WordAgent("aleph", [])
    lobby = Lobby()
    lobby.agents = {"resh": a, "aleph": b}
    check(a.confirm_identity() is True, "baseline resh confirms")
    check(b.confirm_identity() is True, "baseline aleph confirms")
    check(lobby.run_orientation() == 1, "baseline edge")
    check(lobby.ties[("aleph", "resh")] == 1, "baseline weight")
    a.word = ""
    check(a.confirm_identity() is True, "blank mutated word remains confirmed")
    check(lobby.run_orientation() == 1, "blank word passes cached guard")
    check(lobby.ties[("aleph", "resh")] == 2, "blank word still adds weight")
    a.word = "not-resh"
    check(lobby.run_orientation() == 1, "map key and agent word mismatch passes")
    check(lobby.ties[("aleph", "resh")] == 3, "old map key still drives edge")
    a.identity_confirmed = False
    try:
        lobby.run_orientation()
    except RuntimeError as exc:
        check("Orientation blocked" in str(exc), "explicit revocation blocks")
    else:
        raise AssertionError("expected guard failure")
    print(f"{n}/{n} bounded source-transcribed Python assertions PASS")

if __name__ == "__main__":
    main()
