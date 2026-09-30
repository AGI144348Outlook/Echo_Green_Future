"""Sense-aware readings of |P1| ::|word|:: |P2| (needs WordNet; CPython for now).

Each analogy is pinned to the word senses that make it true (the sense pair with
the shortest is-a path), and a single-word middle must work in one sense throughout.
"""
from functools import lru_cache
from nltk.corpus import wordnet as wn

ROOTISH = 2        # categories this close to the top (entity, abstraction...) say almost nothing


@lru_cache(maxsize=None)
def ancestors(ss_name):
    """{ancestor synset name: steps up} for one synset."""
    out = {}
    for path in wn.synset(ss_name).hypernym_paths():
        for i, a in enumerate(reversed(path)):
            if i and (a.name() not in out or i < out[a.name()]): out[a.name()] = i
    return out


def pair_senses(a, b):
    best = None
    for sa in wn.synsets(a, "n"):
        for sb in wn.synsets(b, "n"):
            for x, y, typ in ((sa, sb, "is_a"), (sb, sa, "includes")):
                d = ancestors(x.name()).get(y.name())
                if d and (best is None or d < best[2]): best = (sa.name(), sb.name(), d, typ)
    return best


@lru_cache(maxsize=None)
def pin(emel):
    """a:b::c:d -> the four pinned senses, or None if the pinning is inconsistent."""
    a, b, c, d = emel.replace("::", ":").split(":")
    p, q = pair_senses(a, b), pair_senses(c, d)
    if not p or not q or p[2:] != q[2:]: return None
    return {"terms": (a, b, c, d), "senses": (p[0], p[1], q[0], q[1]), "type": p[3], "depth": p[2]}


def x_senses(word):
    return [s.name() for s in wn.synsets(word, "n")]


def common(P1, word, P2):
    """word's sense is a lowest category over all eight pinned senses."""
    S = P1["senses"] + P2["senses"]
    for sx in x_senses(word):
        if wn.synset(sx).min_depth() <= ROOTISH: continue
        if all(sx == s or sx in ancestors(s) for s in S):
            lower = set.intersection(*(set(ancestors(s)) | {s} for s in S)) - {sx}
            if not any(sx in ancestors(l) for l in lower):          # nothing more specific covers all eight
                return {"sense": sx, "steps_down_to_terms": round(sum(ancestors(s).get(sx, 0) for s in S) / 8, 2)}
    return None


def pivot(P1, word, P2):
    """P1 lies under word, word lies under P2's general terms, and the two gaps are equal."""
    for sx in x_senses(word):
        if wn.synset(sx).min_depth() <= ROOTISH: continue
        if not all(sx in ancestors(s) for s in P1["senses"]): continue
        g1 = sum(ancestors(s)[sx] for s in P1["senses"]) / 4
        above = [ancestors(sx)[s] for s in P2["senses"] if s in ancestors(sx)]
        if len(above) >= 2:
            g2 = sum(above) / len(above)
            if abs(g1 - g2) <= 0.5:
                return {"sense": sx, "gap_below": g1, "gap_above": g2}
    return None


def hinge(P1, word, P2):
    """word is a term of both analogies, pinned to the same sense in each."""
    s1 = {t: s for t, s in zip(P1["terms"], P1["senses"])}
    s2 = {t: s for t, s in zip(P2["terms"], P2["senses"])}
    if word in s1 and word in s2 and s1[word] == s2[word]:
        role = lambda P: "lower" if P["terms"].index(word) in (0, 2) else "upper"
        return {"sense": s1[word], "roles": (role(P1), role(P2))}
    return None
