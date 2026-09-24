"""Inert EVE substrate — no Governor is instantiated here.

Environmental invariants:
- Addressability is structurally distinct from occupancy.
- The environment begins with no occupied NVE cells.
- Runtime capability does not imply active agency.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

Coordinate = Tuple[int, int, int]


@dataclass
class InertEVE:
    """Minimal structural substrate for later Matrix/NVE development."""

    occupancy: Dict[Coordinate, Any] = field(default_factory=dict)

    def is_occupied(self, coordinate: Coordinate) -> bool:
        return coordinate in self.occupancy

    def snapshot(self) -> dict:
        return {
            "environment": "EVE",
            "state": "VOID",
            "occupied": len(self.occupancy),
            "governor": None,
        }


EVE = InertEVE()
