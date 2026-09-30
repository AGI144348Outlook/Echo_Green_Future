"""The indexing formula as a query language over any matrix.

    formula := bounded ( '::' bounded )*            consecutive triples are continued proportions
    bounded := '|' '{' ( formula | prop ) '}' '|' | '|' prop '|' | '|' term '|'
    prop    := slot ':' slot '::' slot ':' slot
    slot    := '(' inner ')' | inner          inner := term ( ('<' | '>' | '=') term )?
    term    := '?' | single-letter variable | word

A slot is either an ENTRY (a word or variable) or a BOOLEAN (a comparison between two).
A proportion holds when:  entries  rel(s1,s2) == rel(s3,s4)   (rel supplied by the matrix)
                          booleans (s1 XOR s2) == (s3 XOR s4)  (the same change)
|P1| :: |x| :: |P2| holds when P1 : x :: x : P2 on their signatures.
Mixing entries and booleans inside one proportion fails VALIDATE.
"""
import re

TOK = re.compile(r"\s*(::|:|\||\{|\}|\(|\)|<|>|=|\?|[^\s:|{}()<>=?]+)")


class PatternError(Exception): pass


def tokenize(s):
    out, i = [], 0
    s = s.strip()
    while i < len(s):
        m = TOK.match(s, i)
        if not m or m.end() == i: raise PatternError(f"bad symbol at {i}: {s[i]!r}")
        out.append(m.group(1)); i = m.end()
    return out


class P:
    def __init__(self, toks): self.t, self.i, self.anon = toks, 0, 0
    def peek(self, k=0): return self.t[self.i + k] if self.i + k < len(self.t) else None
    def take(self, v=None):
        tk = self.peek()
        if tk is None or (v and tk != v): raise PatternError(f"expected {v}, found {tk}")
        self.i += 1; return tk

    def formula(self):
        parts = [self.bounded()]
        while self.peek() == "::":
            self.take("::"); parts.append(self.bounded())
        return parts[0] if len(parts) == 1 else ("chain", parts)

    def bounded(self):
        self.take("|")
        if self.peek() == "{":
            self.take("{")
            node = self.formula() if self.peek() == "|" else self.prop()
            self.take("}")
        else:
            save = self.i
            try:
                node = self.prop()
            except PatternError:
                self.i = save; node = ("term", self.term())
        self.take("|")
        return node

    def prop(self):
        s = [self.slot()]; self.take(":"); s.append(self.slot()); self.take("::")
        s.append(self.slot()); self.take(":"); s.append(self.slot())
        return ("prop", s)

    def slot(self):
        if self.peek() == "(":
            self.take("("); x = self.inner(); self.take(")"); return x
        return self.inner()

    def inner(self):
        a = self.term()
        if self.peek() in ("<", ">", "="):
            op = self.take(); b = self.term(); return ("cmp", op, a, b)
        return ("ent", a)

    def term(self):
        tk = self.take()
        if tk == "?":
            self.anon += 1; return ("var", f"?{self.anon}")
        if tk in (":", "::", "|", "{", "}", "(", ")", "<", ">", "="): raise PatternError(f"expected a term, found {tk}")
        if re.fullmatch(r"[a-hx]", tk): return ("var", tk)         # the notation's placeholders a..h and x
        return ("word", tk.lower())


def parse(s):
    p = P(tokenize(s)); f = p.formula()
    if p.peek() is not None: raise PatternError(f"unexpected {p.peek()}")
    return f


def _unused_variables(n, acc=None):
    acc = [] if acc is None else acc
    if isinstance(n, tuple):
        if n[0] == "var" and n[1] not in acc: acc.append(n[1])
        for x in n[1:]: variables(x, acc)
    elif isinstance(n, list):
        for x in n: variables(x, acc)
    return acc


from .gov_index import variables  # noqa: E402  (shared with the Python-native front end)


class _LegacyGovernor:
    """Superseded by gov_index.Governor; kept so experiment E9 still runs unchanged."""

    def __init__(self, matrix):
        self.m = matrix

    def identify(self, node):
        words = [x[1] for x in _walk(node) if isinstance(x, tuple) and x[0] == "word"]
        missing = [w for w in words if self.m.key(w) is None]
        return {"variables": variables(node), "words": words, "unresolved": missing,
                "status": "PASS" if not missing else "FAIL"}

    def validate(self, node):
        errs = []
        for x in _walk(node):
            if isinstance(x, tuple) and x[0] == "prop":
                kinds = {s[0] for s in x[1]}
                if len(kinds) > 1: errs.append("a proportion mixes entries and booleans")
                if "cmp" in kinds and not self.m.ordered: errs.append(f"{self.m.name} has no order, so < and > are undefined")
                if "ent" in kinds and self.m.rel is None: errs.append(f"{self.m.name} has no relation for a:b")
        return {"status": "FAIL" if errs else "PASS", "errors": sorted(set(errs))}

    # --- evaluation under one assignment -------------------------------------------
    def val(self, t, env):
        return env[t[1]] if t[0] == "var" else self.m.key(t[1])

    def slot(self, s, env):
        if s[0] == "ent": return self.val(s[1], env)
        a, b = self.m.order(self.val(s[2], env)), self.m.order(self.val(s[3], env))
        if a is None or b is None: return None
        return {"<": a < b, ">": a > b, "=": a == b}[s[1]]

    def sig(self, node, env):
        """Signature of a bounded operand: the relation a proportion expresses (or None if it fails)."""
        if node[0] == "prop":
            v = [self.slot(s, env) for s in node[1]]
            if any(x is None for x in v): return None
            if isinstance(v[0], bool):
                return ("xor", v[0] ^ v[1]) if (v[0] ^ v[1]) == (v[2] ^ v[3]) else None
            r1, r2 = self.m.rel(v[0], v[1]), self.m.rel(v[2], v[3])
            return r1 if r1 is not None and r1 == r2 else None
        if node[0] == "chain":
            return ("chain", self.holds(node, env))
        if node[0] == "term":
            return ("term", self.val(node[1], env))

    def holds(self, node, env):
        if node[0] != "chain":
            return self.sig(node, env) is not None
        parts = node[1]
        sigs = [self.sig(p, env) for p in parts]
        if any(s is None for s in sigs): return False
        for s1, sx, s2 in zip(sigs, sigs[1:], sigs[2:]):
            if not self.m.continued(s1, sx, s2): return False
        return True

    def open(self, node, domain_sample):
        """Every assignment (from the given iterable) under which the formula holds."""
        vs = variables(node)
        return [env for env in domain_sample(vs) if self.holds(node, env)]


def _walk(n):
    yield n
    if isinstance(n, tuple):
        for x in n[1:]: yield from _walk(x)
    elif isinstance(n, list):
        for x in n: yield from _walk(x)
