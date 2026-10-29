"""Deterministic polymathematical index-card pit → swarm demonstration (not AI)."""
from dataclasses import dataclass
from hashlib import sha256
import json

GLYPHS = tuple("אבגדהוזחטיכךלמםנןסעפףצץקרשת")
OPS = frozenset(("identity", "compose", "compare", "route"))

def digest(obj):
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(raw.encode("utf-8")).hexdigest()[:16]

@dataclass(frozen=True)
class Card:
    glyph: str
    meanings: tuple
    mathematics: tuple
    operations: tuple
    source: str

    @property
    def fingerprint(self):
        return digest((self.glyph, self.meanings, self.mathematics, self.operations, self.source))

@dataclass(frozen=True)
class Agent:
    identity: str
    origin: str
    glyph: str
    card_fingerprint: str

class Pit:
    def __init__(self):
        self.positions = {(x, y, z): None for z in range(3) for y in range(3) for x in range(3)}
        self.events = []
        self.released = False

    def load(self, position, card):
        if self.released or position not in self.positions or self.positions[position] is not None:
            raise ValueError("unavailable loading position")
        if card.glyph not in GLYPHS or any(v.glyph == card.glyph for v in self.positions.values() if v):
            raise ValueError("duplicate or unknown glyph")
        if not card.operations or not set(card.operations).issubset(OPS) or not card.source:
            raise ValueError("invalid operations/provenance")
        self.positions[position] = card
        self.events.append(("load", position, card.glyph, card.fingerprint))

    def release(self):
        if self.released or {c.glyph for c in self.positions.values() if c} != set(GLYPHS):
            raise ValueError("incomplete/already released")
        self.released = True
        agents = {}
        for position, card in self.positions.items():
            identity = "ALG-" + digest(("Alg-000", card.glyph, card.fingerprint))
            agents[identity] = Agent(identity, "Alg-000", card.glyph, card.fingerprint)
            self.events.append(("instantiate", position, identity, card.fingerprint))
        return Swarm(agents, list(self.events))

class Swarm:
    def __init__(self, agents, events):
        self.agents = agents
        self.events = events
        self.candidates = {}

    def message(self, sender, target, payload):
        if sender not in self.agents or target not in self.agents or not isinstance(payload, str):
            raise ValueError("invalid message")
        record = ("message", sender, target, payload)
        self.events.append(record)
        return record

    def compose(self, sender, target, operator="compose"):
        if sender not in self.agents or target not in self.agents or operator not in OPS:
            raise ValueError("invalid composition")
        left, right = self.agents[sender], self.agents[target]
        candidate = {"origin": "Alg-000", "parents": [left.identity, right.identity],
                     "card_provenance": [left.card_fingerprint, right.card_fingerprint],
                     "operator": operator}
        identity = "CAND-" + digest(candidate)
        self.candidates[identity] = candidate
        self.events.append(("compose", identity, sender, target, operator))
        return identity

    def transcript(self):
        return json.dumps(self.events, ensure_ascii=False, separators=(",", ":"))

def demo():
    pit = Pit()
    for position, glyph in zip(pit.positions, GLYPHS):
        pit.load(position, Card(glyph, ("symbol:" + glyph,), ("graph", "algebra"),
                                ("identity", "compose"), "synthetic-demo-v1"))
    swarm = pit.release()
    first, second = list(swarm.agents)[:2]
    swarm.message(first, second, "neighbor-probe")
    candidate = swarm.compose(first, second)
    return pit, swarm, candidate

if __name__ == "__main__":
    pit, swarm, candidate = demo()
    print(json.dumps({"fixed_nodes": len(pit.positions), "agents": len(swarm.agents),
                      "candidate": candidate, "events": len(swarm.events),
                      "log_digest": sha256(swarm.transcript().encode()).hexdigest()}, indent=2))
