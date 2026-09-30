"""A-174 RecursiveInvariantExtractor, as a Notebook experimental operator.

X_{n+1} = K(X_n, I_n(X_n))

This version addresses the audit on the algebra branch:
- Two fixed-point conditions are reported separately and never conflated:
    strict_involution_fixed : I(x) == x          (the sequence maps to itself)
    letter_set_fixed        : set(I(x)) == set(x) (only the letter set does)
  For sequence reversal the letter set is ALWAYS preserved, so
  letter_set_fixed is trivially true there; the strict condition is the
  informative one (it holds only for palindromic sequences).
- The complex-phase / gematria reading is labelled a hypothesis.
- Results are returned as a trace for a Notebook temporary matrix. Nothing
  here writes to a Registry or the VGM.
"""
import math
from .lhea import decompose, gematria, glyphs, operations, LETTER_ORDER


def I_seq(letters):
    return list(reversed(letters))


def K_letters(x, ix):
    return {
        "invariant_gematria": gematria(x),
        "gematria_preserved": gematria(x) == gematria(ix),
        "invariant_letter_set": sorted(set(x) & set(ix)),
        "forward_ops": operations(x),
        "reversed_ops": operations(ix),
        "strict_involution_fixed": x == ix,
        "letter_set_fixed": set(x) == set(ix),
        "involution_check": I_seq(ix) == x,
    }


def phase_hypothesis(letters):
    """HYPOTHESIS, not an established result: word as R*e^(i*theta).

    R = gematria, theta = sum(index/22 * 2*pi). When the index sum is a
    multiple of 22, theta = 2*pi*k and the imaginary part vanishes.
    """
    idx = [LETTER_ORDER.index(l) for l in letters if l in LETTER_ORDER]
    theta = sum(i / 22 * 2 * math.pi for i in idx)
    R = gematria(letters)
    return {"status": "hypothesis", "R": R, "theta": round(theta, 4),
            "index_sum": sum(idx), "real": round(R * math.cos(theta), 3),
            "imag": round(R * math.sin(theta), 3),
            "on_real_axis": sum(idx) % 22 == 0}


def probe(word):
    """One RIE step on a word's LHEA sequence, returned as a trace row."""
    x = decompose(word)
    ix = I_seq(x)
    k = K_letters(x, ix)
    return {
        "operator": "A-174/I_seq",
        "thing": word,
        "sequence": glyphs(x),
        "inverted": glyphs(ix),
        **k,
        "phase": phase_hypothesis(x),
        "note": ("Sequence reversal always preserves gematria and the letter set; "
                 "strict_involution_fixed is the meaningful fixed-point test."),
    }
