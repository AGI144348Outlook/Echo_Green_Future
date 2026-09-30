"""A-177 part 2: the analogical proportion a:b::c:d and its eight forms.

For number proportions (a/b = c/d, i.e. a*d = b*c) exactly eight arrangements stay
true: the ones that keep the extremes {a,d} and the means {b,c} as pairs. They form
the symmetry group of a square (dihedral group of order 8), and every one of them is
built from flips. Classical names: symmetry (c:d::a:b), invertendo (b:a::d:c) and
alternando (a:c::b:d).

A proportion `holds` under a relation R when R(a,b) == R(c,d) and is defined.
"""

FORM_NAMES = {
    "abcd": "identity  a:b::c:d",
    "cdab": "symmetry  c:d::a:b",
    "badc": "invertendo  b:a::d:c",
    "dcba": "inversion of both  d:c::b:a",
    "acbd": "alternando  a:c::b:d",
    "cadb": "c:a::d:b",
    "bdac": "b:d::a:c",
    "dbca": "d:b::c:a",
}


def forms(a, b, c, d):
    v = {"a": a, "b": b, "c": c, "d": d}
    return {k: (v[k[0]], v[k[1]], v[k[2]], v[k[3]]) for k in FORM_NAMES}


def holds(rel, a, b, c, d):
    r1, r2 = rel(a, b), rel(c, d)
    return r1 is not None and r1 == r2


def closure_report(rel, quad):
    """Which of the eight forms still hold for this quadruple under this relation."""
    return {k: holds(rel, *q) for k, q in forms(*quad).items()}


def solve(rel, candidates, a, b, c):
    """a:b::c:? -> every d among candidates with rel(c, d) == rel(a, b)."""
    target = rel(a, b)
    if target is None:
        return []
    return [d for d in candidates if rel(c, d) == target]
