"""The Governor as an index over any matrix: IDENTIFY -> VALIDATE -> OPEN, plus gated STORE / DELETE.

Both front ends (EMEL text and Python-native subscripts) compile to the same tree:
  ('prop', [slot x4])   slot = ('ent', term) | ('cmp', '<'|'>'|'=', term, term)
  ('chain', [part, ...]) consecutive triples are continued proportions P1 : x :: x : P2
  ('term', term)        a bare middle word or variable
  term = ('var', name) | ('word', text)

A matrix adapter supplies: entries, key(text) -> entry, order(entry) -> number or None,
rel(a, b) -> relation value or None, and `algebra`: how relation values combine
('diff' additive integers, 'xor' flips, 'typed' (kind, spectrum depth)).
"""
import itertools, random


class Matrix:
    def __init__(self, name, entries, key, order=None, rel=None, algebra="diff", label=str):
        self.name, self.entries, self.key, self.order, self.rel = name, entries, key, order, rel
        self.algebra, self.label = algebra, label
        self.ordered = order is not None


def variables(n, acc=None):
    acc = [] if acc is None else acc
    if isinstance(n, tuple):
        if n[0] == "var" and n[1] not in acc: acc.append(n[1])
        for x in n[1:]: variables(x, acc)
    elif isinstance(n, list):
        for x in n: variables(x, acc)
    return acc


def walk(n):
    yield n
    if isinstance(n, tuple):
        for x in n[1:]: yield from walk(x)
    elif isinstance(n, list):
        for x in n: yield from walk(x)


class Governor:
    def __init__(self, matrix, notebook=None):
        self.m = matrix
        self.notebook = notebook if notebook is not None else {}     # retained candidates, never canonical

    # ---- IDENTIFY -------------------------------------------------------------------
    def identify(self, node):
        words = [x[1] for x in walk(node) if isinstance(x, tuple) and x[0] == "word"]
        missing = [w for w in words if self.m.key(w) is None]
        return {"status": "PASS" if not missing else "FAIL", "variables": variables(node), "unresolved": missing}

    # ---- VALIDATE -------------------------------------------------------------------
    def validate(self, node):
        errs = []
        for x in walk(node):
            if isinstance(x, tuple) and x[0] == "prop":
                kinds = {s[0] for s in x[1]}
                if len(kinds) > 1: errs.append("a proportion mixes entries and booleans")
                if "cmp" in kinds and not self.m.ordered: errs.append(f"{self.m.name} has no order, so < > = are undefined")
                if "ent" in kinds and self.m.rel is None: errs.append(f"{self.m.name} has no relation for a:b")
        return {"status": "FAIL" if errs else "PASS", "errors": sorted(set(errs))}

    # ---- evaluation ------------------------------------------------------------------
    def _val(self, t, env): return env[t[1]] if t[0] == "var" else self.m.key(t[1])

    def _slot(self, s, env):
        if s[0] == "ent": return self._val(s[1], env)
        a, b = self._val(s[2], env), self._val(s[3], env)
        if a is None or b is None: return None
        oa, ob = self.m.order(a), self.m.order(b)
        if oa is None or ob is None: return None
        return {"<": oa < ob, ">": oa > ob, "=": oa == ob}[s[1]]

    def sig(self, node, env):
        """What a bounded operand expresses; None when it fails."""
        if node[0] == "prop":
            v = [self._slot(s, env) for s in node[1]]
            if any(x is None for x in v): return None
            if isinstance(v[0], bool):
                return ("xor", v[0] ^ v[1]) if (v[0] ^ v[1]) == (v[2] ^ v[3]) else None
            r1, r2 = self.m.rel(v[0], v[1]), self.m.rel(v[2], v[3])
            if r1 is None or r1 != r2: return None
            return (self.m.algebra, r1)
        if node[0] == "chain":
            sigs = [self.sig(p, env) for p in node[1]]
            if any(s is None for s in sigs): return None
            ok = all(self._continued(a, b, c) for a, b, c in zip(sigs, sigs[1:], sigs[2:]))
            return ("nested", ok, sigs[0], sigs[-1])
        if node[0] == "term":
            return ("term", self._val(node[1], env))

    def _step(self, s1, a, b, s2):
        """The step from s1 to a equals the step from b to s2."""
        kinds = {s1[0], a[0], b[0], s2[0]}
        if len(kinds) != 1: return False
        k = s1[0]
        if k == "xor" or (k == "diff" and self.m.algebra == "xor"): return (s1[1] ^ a[1]) == (b[1] ^ s2[1])
        if k == "diff": return a[1] - s1[1] == s2[1] - b[1]
        if k == "typed": return s1[1][0] == a[1][0] == b[1][0] == s2[1][0] and a[1][1] - s1[1][1] == s2[1][1] - b[1][1]
        return False

    def _continued(self, s1, sx, s2):
        if sx[0] == "nested": return sx[1] and self._step(s1, sx[2], sx[3], s2)
        if sx[0] == "term": return s1 == s2      # a bare middle has no reading, so it constrains nothing
        return self._step(s1, sx, sx, s2)

    def holds(self, node, env):
        s = self.sig(node, env)
        if node[0] == "chain": return bool(s) and s[1]
        return s is not None

    # ---- OPEN ------------------------------------------------------------------------
    def open(self, node, limit=250000, sample=None):
        idf, vl = self.identify(node), self.validate(node)
        if idf["status"] == "FAIL" or vl["status"] == "FAIL":
            return {"status": "CLOSED", "identify": idf, "validate": vl}
        vs = variables(node)
        if not vs:
            return {"status": "OPEN", "holds": self.holds(node, {})}
        space = len(self.m.entries) ** len(vs)
        if space <= limit:
            envs = (dict(zip(vs, combo)) for combo in itertools.product(self.m.entries, repeat=len(vs)))
            mode = "exhaustive"
        else:
            rnd = random.Random(sample or 144)
            envs = ({v: rnd.choice(self.m.entries) for v in vs} for _ in range(limit))
            mode = f"sampled {limit} of {space}"
        hits = [{v: self.m.label(e[v]) for v in vs} for e in envs if self.holds(node, e)]
        return {"status": "OPEN", "mode": mode, "matches": len(hits), "bindings": hits[:12]}

    # ---- STORE / DELETE: writing is gated; saving is not validation ------------------------
    def store(self, node, note=""):
        if variables(node): return {"status": "REJECTED", "reason": "cannot store a pattern with unknowns"}
        vl = self.validate(node)
        if vl["status"] == "FAIL": return {"status": "REJECTED", "reason": vl["errors"]}
        if not self.holds(node, {}): return {"status": "REJECTED", "reason": f"does not hold in {self.m.name}"}
        key = repr(node)
        self.notebook[key] = {"node": node, "matrix": self.m.name, "status": "retained candidate (unvalidated)", "note": note}
        return {"status": "RETAINED", "key": key}

    def delete(self, node):
        return {"status": "DELETED" if self.notebook.pop(repr(node), None) else "NOT FOUND"}


# ---- matrix adapters that work offline (Pyodide) -------------------------------------------
def glyph_matrix():
    from .lexicon import GLYPHS
    from ..kernel import HEBREW_LETTER_INDEX
    from ..operators.lhea import LETTER_ORDER
    G = list(GLYPHS.values())
    val = {v["glyph"]: v["val"] for v in HEBREW_LETTER_INDEX.values()}
    name = {HEBREW_LETTER_INDEX[n]["glyph"]: n for n in LETTER_ORDER}
    def key(w):
        return GLYPHS.get(w) or next((r for r in G if r["operation"].lower() == w.lower() or name.get(r["glyph"]) == w.lower()), None)
    return Matrix("Hebrew Glyph Registry", G, key, lambda e: val.get(e["glyph"]), lambda a, b: b["ordinal"] - a["ordinal"],
                  "diff", label=lambda e: e["glyph"])


def hexagram_matrix():
    return Matrix("I Ching hexagrams", list(range(64)), lambda w: int(w) if str(w).isdigit() and int(w) < 64 else None,
                  lambda e: e, lambda a, b: a ^ b, "xor", label=lambda e: format(e, "06b"))


def registry_matrix(registry):
    def rel(a, b):
        d = registry.ancestors(a).get(b)
        if d: return ("is_a", d)
        d = registry.ancestors(b).get(a)
        if d: return ("includes", d)
        return None
    return Matrix("ECHO Registry", registry.all_words(), lambda w: registry.key(w.replace("_", " ")) if registry.has(w.replace("_", " ")) else None,
                  lambda e: len(registry.chain(e)), rel, "typed")
