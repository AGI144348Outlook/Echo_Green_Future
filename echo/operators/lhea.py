"""LHEA - the 22 letter operators as primitive transformation types.

Glyphs and values come from the kernel's HEBREW_LETTER_INDEX. The operation
names are the table in the Unified Spec (Layer 0). decompose() is the same
Latin-phoneme mapping A-174 uses, so results agree with the RIE runs.
"""
from ..kernel import HEBREW_LETTER_INDEX

LETTER_ORDER = ["aleph", "bet", "gimel", "dalet", "he", "vav", "zayin", "het",
                "tet", "yod", "kaf", "lamed", "mem", "nun", "samekh", "ayin",
                "pe", "tsadi", "qof", "resh", "shin", "tav"]

OPERATION = {
    "aleph": "INITIALIZE", "bet": "CONTAIN", "gimel": "TRAVERSE", "dalet": "FILTER",
    "he": "REVEAL", "vav": "CONNECT", "zayin": "TIMESTAMP", "het": "BOUND",
    "tet": "COIL", "yod": "SEED", "kaf": "CAPACITY", "lamed": "DIRECT",
    "mem": "FLOW", "nun": "INDIVIDUATE", "samekh": "CYCLE", "ayin": "PERCEIVE",
    "pe": "EXPRESS", "tsadi": "HUNT", "qof": "SCAN_PERIPHERY", "resh": "GOVERN",
    "shin": "TRANSFORM", "tav": "SEAL",
}

PHONEME_MAP = {
    "sh": "shin", "ts": "tsadi", "th": "tav", "kh": "het", "ch": "het",
    "a": "aleph", "b": "bet", "v": "vav", "g": "gimel", "d": "dalet", "h": "he",
    "z": "zayin", "t": "tet", "y": "yod", "k": "kaf", "l": "lamed", "m": "mem",
    "n": "nun", "s": "samekh", "e": "he", "p": "pe", "f": "pe", "q": "qof",
    "r": "resh", "i": "yod", "o": "ayin", "u": "vav",
}


def decompose(word):
    """Latin-script word -> LHEA letter names. Digraphs first; adjacent repeats collapse."""
    w = (word or "").lower().split()[0] if (word or "").strip() else ""
    out, i = [], 0
    while i < len(w):
        two = w[i:i + 2]
        if len(two) == 2 and two in PHONEME_MAP:
            out.append(PHONEME_MAP[two]); i += 2; continue
        if w[i] in PHONEME_MAP:
            out.append(PHONEME_MAP[w[i]])
        i += 1
    dedup = []
    for letter in out:
        if not dedup or dedup[-1] != letter:
            dedup.append(letter)
    return dedup


def gematria(letters):
    return sum(HEBREW_LETTER_INDEX.get(l, {}).get("val", 0) for l in letters)


def glyphs(letters):
    return "".join(HEBREW_LETTER_INDEX.get(l, {}).get("glyph", "?") for l in letters)


def operations(letters):
    return [OPERATION.get(l, "?") for l in letters]


def profile(word):
    """Everything the Canvas and inspector show about a word's LHEA structure."""
    letters = decompose(word)
    return {
        "letters": letters,
        "glyphs": glyphs(letters),
        "gematria": gematria(letters),
        "lhea": " \u2192 ".join(operations(letters)),
    }


def equilibrium(w1, w2):
    """A-152 style balance point: the highest-value letter two words share, or None."""
    shared = set(decompose(w1)) & set(decompose(w2))
    if not shared:
        return None
    best = max(shared, key=lambda l: HEBREW_LETTER_INDEX.get(l, {}).get("val", 0))
    d = HEBREW_LETTER_INDEX.get(best, {})
    return {"letter": best, "glyph": d.get("glyph", "?"), "value": d.get("val", 0),
            "operation": OPERATION.get(best, "?"), "shared": sorted(shared)}
