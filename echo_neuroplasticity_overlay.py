"""Experimental, opt-in neuroplasticity overlay for the Genesis Algorithm Matrix.

This module does not alter AlgorithmMatrix implementation or claim biological learning.
Candidate mechanisms: A1-a (hard resource cap), B1-a (count + recency),
C2-b (residency cap), E1-a (dormancy), F6-a (identity-preserving refinement).
"""
from dataclasses import dataclass, field

@dataclass
class PlasticLink:
    a: str
    b: str
    traversals: int = 0
    last_used: int = 0
    strength: float = 0.5
    status: str = "active"
    revisions: list = field(default_factory=list)

class NeuroplasticityOverlay:
    def __init__(self, matrix, enabled=False, max_links=1000, max_traversals_per_tick=100):
        self.matrix = matrix  # identity-preserving reference, not a replacement
        self.enabled = enabled
        self.max_links = max_links
        self.max_traversals_per_tick = max_traversals_per_tick
        self.links = {}
        self.tick = 0
        self.used_this_tick = 0
        self.audit = []

    def next_tick(self):
        self.tick += 1
        self.used_this_tick = 0

    def traverse(self, a, b, successful=None):
        if not self.enabled:
            return {"applied": False, "reason": "overlay_disabled"}
        if not isinstance(a, str) or not isinstance(b, str) or not a or not b:
            raise ValueError("link endpoints must be nonempty strings")
        key = (a, b)
        if key not in self.links and len(self.links) >= self.max_links:
            return {"applied": False, "reason": "link_budget"}
        if self.used_this_tick >= self.max_traversals_per_tick:
            return {"applied": False, "reason": "tick_budget"}
        link = self.links.setdefault(key, PlasticLink(a, b))
        if link.status != "active":
            return {"applied": False, "reason": "dormant"}
        link.traversals += 1
        link.last_used = self.tick
        self.used_this_tick += 1
        if successful is not None:
            old = link.strength
            link.strength = max(0.0, min(1.0, old + (0.05 if successful else -0.05)))
            link.revisions.append({"tick": self.tick, "from": old, "to": link.strength})
        self.audit.append({"tick": self.tick, "event": "traverse", "a": a, "b": b})
        return {"applied": True, "traversals": link.traversals, "strength": link.strength}

    def dormant(self, a, b):
        link = self.links[(a, b)]
        link.status = "dormant"
        self.audit.append({"tick": self.tick, "event": "dormant", "a": a, "b": b})

    def reactivate(self, a, b):
        link = self.links[(a, b)]
        link.status = "active"
        self.audit.append({"tick": self.tick, "event": "reactivate", "a": a, "b": b})

    def snapshot(self):
        return {"enabled": self.enabled, "tick": self.tick,
                "matrix_identity_preserved": self.matrix is not None,
                "links": [{"a": v.a, "b": v.b, "traversals": v.traversals,
                           "strength": v.strength, "status": v.status,
                           "revisions": list(v.revisions)}
                          for v in self.links.values()],
                "audit": list(self.audit)}
