import ast, inspect, json as _j, importlib, textwrap
def _first(doc):
    if not doc: return ""
    s = inspect.cleandoc(doc).split("\n\n")[0].replace("\n", " ").replace("``", "")
    return s[:240]
def _short(n, k=56):
    s = ast.unparse(n).split("\n")[0]
    return s if len(s) <= k else s[:k-3] + "..."
def _calls(n):
    out = []
    for c in ast.walk(n):
        if isinstance(c, ast.Call):
            try: out.append(ast.unparse(c.func))
            except Exception: pass
    return sorted(set(out))[:6]
def _flow(fn, cap=48):
    try: src = textwrap.dedent(inspect.getsource(fn))
    except Exception: return None
    return _flow_node(ast.parse(src).body[0], cap)
_GEN_TREE = None
def gen_flow(cls, meth, cap=48):
    global _GEN_TREE
    if _GEN_TREE is None:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore"); _GEN_TREE = ast.parse(GENESIS_SRC)
    return flow_from_source(_GEN_TREE, cls, meth, cap)
def flow_from_source(src, cls, meth, cap=48):
    t = src if isinstance(src, ast.AST) else ast.parse(src)
    for n in t.body:
        if cls and isinstance(n, ast.ClassDef) and n.name == cls:
            for m in n.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and m.name == meth:
                    return _j.dumps(_flow_node(m, cap))
        if not cls and isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == meth:
            return _j.dumps(_flow_node(n, cap))
    return "null"
def _flow_node(f, cap=48):
    nodes, links, st = [], [], {"y": 0}
    def add(kind, name, text, x):
        nodes.append({"kind": kind, "name": name, "text": text, "x": x, "y": st["y"]}); st["y"] += 1
        return len(nodes) - 1
    def link(a, b, lab):
        if a is not None and b is not None: links.append([a, b, lab])
    def block(stmts, x, prev, lab):
        for s in stmts:
            if len(nodes) >= cap: return prev
            if isinstance(s, ast.Expr) and isinstance(getattr(s, "value", None), ast.Constant) and isinstance(s.value.value, str):
                continue   # docstring
            if isinstance(s, ast.If):
                g = add("gate", "if " + _short(s.test, 40), "condition: " + ast.unparse(s.test), x); link(prev, g, lab)
                block(s.body, x + 1, g, "=T")
                if s.orelse: block(s.orelse, x + 1, g, "=F")
                prev, lab = g, "next"
            elif isinstance(s, (ast.For, ast.AsyncFor)):
                g = add("gate", "for " + _short(s.target, 16) + " in " + _short(s.iter, 28), "loop over: " + ast.unparse(s.iter), x); link(prev, g, lab)
                block(s.body, x + 1, g, "=T each"); prev, lab = g, "done"
            elif isinstance(s, ast.While):
                g = add("gate", "while " + _short(s.test, 40), "loop while: " + ast.unparse(s.test), x); link(prev, g, lab)
                block(s.body, x + 1, g, "=T"); prev, lab = g, "=F"
            elif isinstance(s, ast.Try):
                n = add("node", "try", "does: attempts the block below; errors go to the except gates", x); link(prev, n, lab)
                block(s.body, x + 1, n, "")
                for h in s.handlers:
                    hg = add("gate", "except " + (_short(h.type, 30) if h.type else "any error"), "catches: " + (ast.unparse(h.type) if h.type else "any error"), x + 1)
                    link(n, hg, "error"); block(h.body, x + 2, hg, "")
                prev, lab = n, "next"
            elif isinstance(s, ast.Return):
                n = add("node", "return " + (_short(s.value, 40) if s.value else ""), "gives: " + (ast.unparse(s.value) if s.value else "None"), x); link(prev, n, lab); prev, lab = n, ""
            elif isinstance(s, ast.Raise):
                n = add("node", "raise " + (_short(s.exc, 40) if s.exc else ""), "does: raises an error: " + (ast.unparse(s.exc) if s.exc else "re-raise"), x); link(prev, n, lab); prev, lab = n, ""
            else:
                cs = _calls(s)
                n = add("node", _short(s, 44), "does: " + ast.unparse(s)[:400] + ("\ncalls: " + ", ".join(cs) if cs else ""), x); link(prev, n, lab); prev, lab = n, ""
        return prev
    start = add("node", f.name + "(…)", "needs: " + ast.unparse(f.args), 0)
    block(f.body, 0, start, "")
    return {"nodes": nodes, "links": links, "truncated": len(nodes) >= cap}
def map_module(name):
    m = importlib.import_module(name)
    names = list(getattr(m, "__all__", None) or [n for n in dir(m) if not n.startswith("_")])
    out = {"name": name, "doc": _first(m.__doc__), "items": []}
    for n in names:
        o = getattr(m, n, None)
        kind = "module" if inspect.ismodule(o) else "class" if inspect.isclass(o) else "function" if callable(o) else "constant"
        sig = ""
        if kind in ("function", "class"):
            try: sig = str(inspect.signature(o))
            except Exception: sig = "(…)"
        it = {"name": n, "kind": kind, "sig": sig, "doc": _first(o.__doc__) if kind != "constant" else repr(o)[:80], "flow": None, "methods": []}
        if kind == "function": it["flow"] = _flow(o)
        if kind == "class": it["methods"] = [k for k, v in vars(o).items() if callable(v) and not k.startswith("_")][:30]
        out["items"].append(it)
    return _j.dumps(out)
