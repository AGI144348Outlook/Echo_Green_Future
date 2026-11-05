"""Gematria-based numeric affinity candidate for Echo's inert 3^3 glyph graph.
DRAFT ONLY: no tests executed. Pre-test: issue #267.
Affinity is a design prior, NOT a measured causal influence.
"""
from dataclasses import dataclass
from math import gcd

VALUES = {
    "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7,
    "ח": 8, "ט": 9, "י": 10, "כ": 20, "ל": 30, "מ": 40,
    "נ": 50, "ס": 60, "ע": 70, "פ": 80, "צ": 90, "ק": 100,
    "ר": 200, "ש": 300, "ת": 400,
    "ך": 20, "ם": 40, "ן": 50, "ף": 80, "ץ": 90,
}
GLYPHS = tuple("אבגדהוזחטיכלמנסעפצקרשתךםןףץ")

@dataclass(frozen=True)
class NumericAffinity:
    source: str
    target: str
    source_value: int
    target_value: int
    harmonic: int
    gcd_ratio: float

def numeric_affinity(a: str, b: str) -> NumericAffinity:
    """Compute a symmetric harmonic divisor prior; do not claim causation."""
    x, y = VALUES[a], VALUES[b]
    low, high = min(x, y), max(x, y)
    return NumericAffinity(a, b, x, y, int(high % low == 0),
                           gcd(x, y) / high)

def cube_addresses():
    """27 fixed unique slots; values are separate from address and identity."""
    return {(i // 9, (i // 3) % 3, i % 3): glyph
            for i, glyph in enumerate(GLYPHS)}

def numeric_prior(a: str, b: str) -> float:
    """Binary divisor harmonic, with gcd ratio as tie-break (not causal)."""
    z = numeric_affinity(a, b)
    return z.harmonic + 0.01 * z.gcd_ratio

def causal_delta(run_model, state, source: str, target: str):
    """Intervention API sketch; caller must supply frozen deterministic model.
    Return baseline vs source-ablated target outcome; not used until tests.
    """
    base = run_model(state, disabled_source=None)
    ablated = run_model(state, disabled_source=source)
    return base[target] - ablated[target]
