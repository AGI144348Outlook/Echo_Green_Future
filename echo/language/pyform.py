"""Python-native front end: the formula written as Python subscripts, parsed by Python itself.

    G[a:b, c:d]                              a:b::c:d          (Python's slice holds a pair)
    G[(a<b):(c>d), (e<d):(f>g)]              boolean proportion
    G[P[a:b, c:d], x, P[e:f, g:h]]           |P1| :: |x| :: |P2|   (P builds a proportion without running it)
    G[P[..], P[P[..], x, P[..]], P[..]]      nesting
    G[...] = note                            STORE: retain as a candidate (gated, never canonical)
    del G[...]                               DELETE: retract a retained candidate

Single letters a..h and x are variables, `_` is an anonymous slot, other names are words
(Hebrew letters are legal Python names). G's __getitem__ is the Governor: IDENTIFY -> VALIDATE -> OPEN.

compile_py() never runs code: it walks Python's own syntax tree after a whitelist check.
GovernorView gives the same forms at runtime inside Python code.
"""
import ast

VARS = set("abcdefghx")
ALLOWED = (ast.Expression, ast.Module, ast.Expr, ast.Subscript, ast.Slice, ast.Tuple, ast.Name, ast.Load,
           ast.Compare, ast.Lt, ast.Gt, ast.Eq, ast.Constant, ast.Assign, ast.Store, ast.Delete, ast.Del)
OPS = {ast.Lt: "<", ast.Gt: ">", ast.Eq: "="}


class FormError(Exception):
    pass


def check(tree):
    for n in ast.walk(tree):
        if not isinstance(n, ALLOWED):
            raise FormError(f"not allowed in a formula: {type(n).__name__}")
        if isinstance(n, ast.Name) and n.id.startswith("__"):
            raise FormError("dunder names are not allowed")
        if isinstance(n, ast.Compare) and len(n.ops) != 1:
            raise FormError("one comparison per slot (a<b), not chains like a<b<c")


class _Compiler:
    def __init__(self): self.anon = 0

    def term(self, n):
        if isinstance(n, ast.Name):
            if n.id == "_":
                self.anon += 1; return ("var", f"?{self.anon}")
            return ("var", n.id) if n.id in VARS else ("word", n.id.lower())
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, str)):
            return ("word", str(n.value).lower())
        raise FormError(f"expected a word or variable, found {type(n).__name__}")

    def slot(self, n):
        if isinstance(n, ast.Compare):
            return ("cmp", OPS[type(n.ops[0])], self.term(n.left), self.term(n.comparators[0]))
        return ("ent", self.term(n))

    def key(self, n):
        """The inside of G[...] or P[...]."""
        elts = n.elts if isinstance(n, ast.Tuple) else [n]
        if len(elts) == 2 and all(isinstance(e, ast.Slice) and e.step is None for e in elts):
            (s1, s2) = elts
            return ("prop", [self.slot(s1.lower), self.slot(s1.upper), self.slot(s2.lower), self.slot(s2.upper)])
        if len(elts) >= 3:
            return ("chain", [self.operand(e) for e in elts])
        raise FormError("expected a:b, c:d (a proportion) or P1, x, P2 (a chain)")

    def operand(self, n):
        if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "P":
            return self.key(n.slice)
        return ("term", self.term(n))


def compile_py(src):
    """Source text -> (action, tree). action is OPEN, STORE or DELETE."""
    tree = ast.parse(src.strip())
    check(tree)
    if len(tree.body) != 1: raise FormError("one formula at a time")
    stmt, c = tree.body[0], _Compiler()
    def target(sub):
        if not (isinstance(sub, ast.Subscript) and isinstance(sub.value, ast.Name) and sub.value.id == "G"):
            raise FormError("the formula must be written as G[...]")
        return c.key(sub.slice)
    if isinstance(stmt, ast.Expr): return "OPEN", target(stmt.value)
    if isinstance(stmt, ast.Assign):
        note = stmt.value.value if isinstance(stmt.value, ast.Constant) else ""
        return "STORE", target(stmt.targets[0]), note
    if isinstance(stmt, ast.Delete): return "DELETE", target(stmt.targets[0])
    raise FormError("expected G[...], G[...] = note, or del G[...]")


def run_py(src, governor):
    action, *rest = compile_py(src)
    if action == "OPEN": return governor.open(rest[0])
    if action == "STORE": return governor.store(rest[0], note=rest[1])
    return governor.delete(rest[0])


# ---- runtime form: the same syntax used directly inside Python code ------------------------
class Sym:
    def __init__(self, term): self.term = term
    def __lt__(self, o): return Cmp("<", self, o)
    def __gt__(self, o): return Cmp(">", self, o)
    def __eq__(self, o): return Cmp("=", self, o)
    __hash__ = object.__hash__


class Cmp:
    def __init__(self, op, a, b): self.op, self.a, self.b = op, a, b
    def __bool__(self): raise FormError("a comparison slot is a formula node, not a Python truth value")


def _slot(v):
    if isinstance(v, Cmp): return ("cmp", v.op, _t(v.a), _t(v.b))
    return ("ent", _t(v))


def _t(v):
    if isinstance(v, Sym): return v.term
    return ("word", str(v).lower())


def _key(k):
    elts = k if isinstance(k, tuple) else (k,)
    if len(elts) == 2 and all(isinstance(e, slice) and e.step is None for e in elts):
        return ("prop", [_slot(elts[0].start), _slot(elts[0].stop), _slot(elts[1].start), _slot(elts[1].stop)])
    if len(elts) >= 3:
        return ("chain", [e.node if isinstance(e, Built) else ("term", _t(e)) for e in elts])
    raise FormError("expected a:b, c:d or P1, x, P2")


class Built:
    def __init__(self, node): self.node = node


class _PBuilder:
    def __getitem__(self, k): return Built(_key(k))


class GovernorView:
    """G[...] reads (OPEN), G[...] = note stores a candidate, del G[...] retracts one."""
    def __init__(self, governor): self.g = governor
    def __getitem__(self, k): return self.g.open(_key(k))
    def __setitem__(self, k, note): self.last = self.g.store(_key(k), note=str(note))
    def __delitem__(self, k): self.last = self.g.delete(_key(k))


def namespace(governor):
    """Names for Notebook cells: variables, anonymous slots, P, G, and any other name as a word."""
    class Names(dict):
        def __missing__(self, name):
            if name == "_": return Sym(("var", "?"))
            return Sym(("var", name) if name in VARS else ("word", name.lower()))
    ns = Names(P=_PBuilder(), G=GovernorView(governor))
    return ns
