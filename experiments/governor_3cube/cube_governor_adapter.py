"""Boundary adapter: 27-glyph dynamic graph observations -> Governor Step 3.
This is a staged integration candidate, not an intelligence claim or a validated experiment.
The Governor and original kernel are loaded separately; A-000 is not mutated here.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

GLYPHS = tuple("אבגדהוזחטיכלמנסעפצקרשתךםןףץ")
assert len(GLYPHS) == 27 and len(set(GLYPHS)) == 27

@dataclass
class CubeState:
    nodes: Tuple[str, ...] = GLYPHS
    edges: Dict[str, List[str]] = field(default_factory=dict)
    events: List[dict] = field(default_factory=list)
    step: int = 0

    def __post_init__(self):
        if tuple(self.nodes) != GLYPHS:
            raise ValueError("The 27 rooted seed identities must remain invariant")
        if not self.edges:
            self.edges = {g: [] for g in self.nodes}
        self.check()

    def check(self):
        if set(self.edges) != set(self.nodes):
            raise ValueError("Graph must contain exactly the 27 rooted nodes")
        for source, targets in self.edges.items():
            if len(set(targets)) != len(targets) or any(t not in self.nodes for t in targets):
                raise ValueError("Invalid, duplicated, or unknown target")

    def connect(self, source: str, target: str, reason: str = "candidate"):
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("Unknown glyph")
        if target not in self.edges[source]:
            self.edges[source].append(target)
        self.step += 1
        self.events.append({"step": self.step, "type": "edge", "from": source,
                            "to": target, "reason": reason})
        self.check()

    def observe(self, source: str, predicted: str, actual: str) -> dict:
        """Return a loss observation; do not treat proposal acceptance as success."""
        if any(x not in self.nodes for x in (source, predicted, actual)):
            raise ValueError("Unknown glyph")
        loss = float(predicted != actual)
        self.step += 1
        event = {"step": self.step, "type": "observation", "source": source,
                 "predicted": predicted, "actual": actual, "loss": loss}
        self.events.append(event)
        return event

def governor_observation(kernel, event):
    """Map a traversal mismatch to quality feedback; caller owns the Governor.
    No persistent error ceiling is enabled here: that remains a preregistered test variant.
    """
    s = kernel.State(content=event["source"], quality=0.0, history=[])
    r = kernel.Request()
    c = kernel.Context()
    observed = kernel.State(content=event["actual"], quality=event["loss"], history=[])
    return s, r, c, observed
