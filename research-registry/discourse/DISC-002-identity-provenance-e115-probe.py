"""DISC-002 E115 probe (part a+b): A-000 semantic identity integrity (a) and
authorization provenance (b), candidate v7 versus the unmodified skeleton.

PRE-REGISTERED 2026-11-08 04Z by Claude. Committed BEFORE any execution;
first executed only after this blob is pushed and named in a prospective
Issue #13 comment. Only a byte-compile check (py_compile) was run before
commit; no row was executed.

Design: DISC-002 02Z (Claude, blob 0ef6ad3e); row-to-property mapping
accepted by ChatGPT 03Z (commit f7653f02,
contract-000/gpt/DISC-002-ChatGPT-20261108-03z.md on GPT branch
contract-000-gpt-multiring-20261104), incl. P3 under (a). Each row reports
ONE property, never a combined pass. Claude's 01Z A-D check (blob
11586b42) was exploratory; the baseline rows below must reproduce it.

SCOPE OF THIS FILE: properties (a) and (b) only. Property (c) restart
recovery (N3 replay after restart with the used-nonce set inside the
anchored WAL envelope, a corrupt-envelope row, and the E114 W1-W5 and
grant/receiver/nonce regression rows) is NOT in this file. It is deferred
to a separate pre-registered E115c, because it builds on the E114 v6 code.
So whatever this file prints, the candidate can at most be reported as
"integrity + provenance (partial); NOT write-protected" (R5 rule, 02Z).

Limits stated before the run: in-process stand-ins; the grant token set
GRANTS is a FIXTURE (issuer UNAUTHENTICATED-FIXTURE), not authority; the
bound hash store is in the same process (not an external anchor); sha256
over canonical JSON is a digest, not authentication. Nothing edits Genesis,
main or any file. Timothy's issuer, revocation, receiver binding and
merge-vs-replace remain open.

Input, loaded unmodified:
  argv[1] directory holding genesis-documentary:src/echo_governor_skeleton.py
          blob 63eb982 (file name echo_governor_skeleton.py)
Run: python3 -I -B <this> <dir>
(P3 child processes run with -B -s -P and env {PYTHONHASHSEED: n} only,
because -I would ignore PYTHONHASHSEED.)

PROPOSED candidate v7 (stand-in, never applied to Genesis):
  GuardedKnown(dict): PROTECTED = {"A-000", "A-000-RESH"}. Any write to a
    protected key via __setitem__, update, setdefault, __delitem__, pop,
    popitem, clear or |= raises PermissionError("CONFLICT:GRANT") unless
    inside `with known.granted(token)` with token in GRANTS. Unknown token
    -> PermissionError on entering. freeze=True stores protected values
    as MappingProxyType copies (in-place change refused); freeze=False
    stores plain dicts (in-place change possible, detected on validate).
  anchor_v7(known, token): copy-on-write version of ReshIdentity.anchor
    (same fields as skeleton l. 3255-3279, copied, written under grant);
    returns BOUND = {a000: H(A-000), resh: H(A-000-RESH)}, held outside
    the mapping. H = sha256(canonical JSON, sorted keys).
  validate_v7(known, bound) -> (bool, reason), checks in order:
    bound None -> UNANCHORED; A-000 missing or not a mapping -> MISSING;
    A-000 lacks name or status -> FIELDS; identity_symbol != resh ->
    SYMBOL; A-000-RESH missing or not a mapping -> RESH_MISSING;
    H(A-000) != bound.a000 -> A000_HASH; H(A-000-RESH) != bound.resh ->
    RESH_HASH; else OK.
  Falsifier candidate "record-only": AlgorithmMatrix subclass whose
    record() refuses protected keys without grant; .known stays a dict.

Rows and predictions (INFERRED from skeleton 63eb982 and the v7 rules):
 (a) integrity
  ctlA  real AlgorithmMatrix, anchor, validate.
        base True; v7 (True, OK).
  V1    known = {} (A-000 absent), anchor, validate.
        base True (wrongly accepted); v7 (False, FIELDS).
  V2    anchor, then A-000-RESH := "x" (v7: under grant, to isolate (a)).
        base True (wrongly accepted); v7 (False, RESH_MISSING).
  V3    anchor, then A-000 := {"identity_symbol": "resh"} (v7: grant).
        base True (wrongly accepted); v7 (False, FIELDS).
  V4    anchor, then A-000 := anchored A-000 copy with name changed
        (all fields present, symbol resh) (v7: grant).
        base True; v7 (False, A000_HASH).
  P2a   anchor, then known["A-000"]["status"] = "RETIRED" in place.
        base: change applied, validate True; v7 freeze: refused
        (TypeError), status unchanged, (True, OK).
  P2n   as P2a with v7 freeze=False: change applied, (False, A000_HASH).
  P3    resh agent definition_words after skeleton anchor() with a stub
        lobby, in child processes PYTHONHASHSEED=1,2,3; sha256 of the
        JSON list. base: not all three equal (INFERRED: list(set(...)) of
        10 strings; equality would mean "not falsified", not "stable");
        candidate (sorted list): all three equal.
 (b) provenance (all v7 freeze=True unless stated; no grant unless stated)
  P1m   known["A-000"] = {...}            -> CONFLICT:GRANT, unchanged.
  P1u   known.update({"A-000": {...}})    -> CONFLICT:GRANT, unchanged.
  P1d   del known["A-000"]                -> CONFLICT:GRANT, present.
  P1p   known.pop("A-000-RESH")           -> CONFLICT:GRANT, present.
  P1x   granted("not-a-grant")            -> CONFLICT:GRANT on entry.
  P1g   granted("e115-g"), known["A-000"] = {...}  -> OK, changed.
  P1n   non-protected key "A-999" without grant -> OK (guard is scoped).
  P1r   record-only falsifier: direct am.known["A-000"] = {...} -> OK,
        changed (WRONGLY accepted); am.record("A-000", ...) ->
        CONFLICT:GRANT.
  P1s   unmodified skeleton ReshIdentity.anchor() on GuardedKnown
        freeze=False, no grant: the final write is refused
        (CONFLICT:GRANT) but the nested A-000 dict was already mutated in
        place: leak True (identity_symbol present). With freeze=True:
        refused by TypeError before any write, leak False.
  SITES count of `.known[...] =` assignment lines in the skeleton
        (SOURCE-OBSERVED 00Z: 9). Reported, not a pass condition.

Outcome lines: e115.a_outcome = PASS iff every (a) row matches its
prediction for v7; e115.b_outcome likewise for (b); e115.base_as_predicted
for the baseline columns; e115.c_outcome = DEFERRED(E115c).
"""
import sys, os, json, hashlib, types, contextlib, subprocess, re

GRANTS = {"e115-g"}
PROTECTED = {"A-000", "A-000-RESH"}


def H(v):
    return hashlib.sha256(json.dumps(plain(v), sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def plain(v):
    if isinstance(v, (dict, types.MappingProxyType)):
        return {k: plain(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [plain(x) for x in v]
    return v


class GuardedKnown(dict):
    def __init__(self, init=(), freeze=True):
        super().__init__()
        self._freeze = freeze
        self._grant = None
        for k, v in dict(init).items():
            dict.__setitem__(self, k, self._wrap(k, v))

    def _wrap(self, k, v):
        if self._freeze and k in PROTECTED and isinstance(v, dict):
            return types.MappingProxyType(dict(v))
        return v

    def _check(self, k):
        if k in PROTECTED and self._grant not in GRANTS:
            raise PermissionError("CONFLICT:GRANT")

    @contextlib.contextmanager
    def granted(self, token):
        if token not in GRANTS:
            raise PermissionError("CONFLICT:GRANT")
        prev, self._grant = self._grant, token
        try:
            yield self
        finally:
            self._grant = prev

    def __setitem__(self, k, v):
        self._check(k); dict.__setitem__(self, k, self._wrap(k, v))

    def __delitem__(self, k):
        self._check(k); dict.__delitem__(self, k)

    def update(self, *a, **kw):
        d = dict(*a, **kw)
        for k in d: self._check(k)
        for k, v in d.items(): dict.__setitem__(self, k, self._wrap(k, v))

    def __ior__(self, other):
        self.update(other); return self

    def setdefault(self, k, v=None):
        if k not in self: self[k] = v
        return dict.__getitem__(self, k)

    def pop(self, k, *d):
        if k in self: self._check(k)
        return dict.pop(self, k, *d)

    def popitem(self):
        if self: self._check(next(reversed(self)))
        return dict.popitem(self)

    def clear(self):
        for k in list(self): self._check(k)
        dict.clear(self)


def anchor_v7(known, token):
    a000 = dict(known.get("A-000", {}))
    a000.update(identity_symbol="resh", identity_glyph="ר", identity_letter="resh",
                identity_meaning="head beginning leader identity")
    resh = {"name": "Resh — Governor Identity Anchor", "status": "ACTIVE",
            "glyph": "ר", "aliases": ["A-000", "resh", "governor"],
            "perception_operator": "ayin", "expression_operator": "pe"}
    with known.granted(token):
        known["A-000"] = a000
        known["A-000-RESH"] = resh
    return {"a000": H(known["A-000"]), "resh": H(known["A-000-RESH"])}


def validate_v7(known, bound):
    if bound is None: return (False, "UNANCHORED")
    a = known.get("A-000")
    if not isinstance(a, (dict, types.MappingProxyType)): return (False, "MISSING")
    if "name" not in a or "status" not in a: return (False, "FIELDS")
    if a.get("identity_symbol") != "resh": return (False, "SYMBOL")
    r = known.get("A-000-RESH")
    if not isinstance(r, (dict, types.MappingProxyType)): return (False, "RESH_MISSING")
    if H(a) != bound["a000"]: return (False, "A000_HASH")
    if H(r) != bound["resh"]: return (False, "RESH_HASH")
    return (True, "OK")


class M:
    pass


def attempt(fn):
    try:
        fn(); return "OK"
    except PermissionError as e:
        return str(e)
    except TypeError as e:
        return "TypeError"


def p3_child(skel_dir, mode):
    sys.path.insert(0, skel_dir)
    import echo_governor_skeleton as g
    ag = types.SimpleNamespace(definition_words=["resh", "head"])
    lobby = types.SimpleNamespace(agents={"resh": ag})
    r = g.ReshIdentity(g.AlgorithmMatrix(), lobby); r.anchor()
    words = ag.definition_words if mode == "base" else sorted(ag.definition_words)
    print(hashlib.sha256(json.dumps(words).encode()).hexdigest())


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--p3-child":
        return p3_child(sys.argv[2], sys.argv[3])
    skel_dir = sys.argv[1]
    sp = os.path.join(skel_dir, "echo_governor_skeleton.py")
    data = open(sp, "rb").read()
    print("input.skeleton_blob=", hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest())
    sys.path.insert(0, skel_dir)
    import echo_governor_skeleton as g
    out = {}

    def row(name, base, v7, exp_base, exp_v7, prop):
        mb = (exp_base is None) or (base == exp_base)
        mv = v7 == exp_v7
        out[name] = (prop, mb, mv)
        print(f"e115.{name}.prop={prop} base={base!r} exp_base={exp_base!r} match_base={mb}")
        print(f"e115.{name}.v7={v7!r} exp_v7={exp_v7!r} match_v7={mv}")

    def base_anchor(init):
        m = M(); m.known = dict(init) if init is not None else g.AlgorithmMatrix().known
        r = g.ReshIdentity(m); r.anchor(); return m, r

    def v7_anchor(init, freeze=True):
        k = GuardedKnown(g.AlgorithmMatrix().known if init is None else init, freeze=freeze)
        return k, anchor_v7(k, "e115-g")

    # (a) integrity
    m, r = base_anchor(None); k, b = v7_anchor(None)
    row("ctlA", r.validate(), validate_v7(k, b), True, (True, "OK"), "a")
    m, r = base_anchor({}); k, b = v7_anchor({})
    row("V1", r.validate(), validate_v7(k, b), True, (False, "FIELDS"), "a")
    m, r = base_anchor(None); m.known["A-000-RESH"] = "x"
    k, b = v7_anchor(None)
    with k.granted("e115-g"): k["A-000-RESH"] = "x"
    row("V2", r.validate(), validate_v7(k, b), True, (False, "RESH_MISSING"), "a")
    m, r = base_anchor(None); m.known["A-000"] = {"identity_symbol": "resh"}
    k, b = v7_anchor(None)
    with k.granted("e115-g"): k["A-000"] = {"identity_symbol": "resh"}
    row("V3", r.validate(), validate_v7(k, b), True, (False, "FIELDS"), "a")
    m, r = base_anchor(None); c = dict(m.known["A-000"]); c["name"] = "Impostor"; m.known["A-000"] = c
    k, b = v7_anchor(None); c = dict(k["A-000"]); c["name"] = "Impostor"
    with k.granted("e115-g"): k["A-000"] = c
    row("V4", r.validate(), validate_v7(k, b), True, (False, "A000_HASH"), "a")

    def p2(freeze):
        k, b = v7_anchor(None, freeze)
        def f(): k["A-000"]["status"] = "RETIRED"
        st = attempt(f)
        return (st, k["A-000"]["status"], validate_v7(k, b))
    m, r = base_anchor(None)
    def fb(): m.known["A-000"]["status"] = "RETIRED"
    bst = (attempt(fb), m.known["A-000"]["status"], r.validate())
    row("P2a", bst, p2(True), ("OK", "RETIRED", True), ("TypeError", "ACTIVE", (True, "OK")), "a")
    row("P2n", bst, p2(False), ("OK", "RETIRED", True), ("OK", "RETIRED", (False, "A000_HASH")), "a")

    def child(seed, mode):
        p = subprocess.run([sys.executable, "-B", "-s", "-P", os.path.abspath(__file__), "--p3-child",
                            skel_dir, mode], env={"PYTHONHASHSEED": str(seed)},
                           capture_output=True, text=True)
        return (p.stdout.strip().splitlines() or ["ERR:" + p.stderr.strip()[-200:]])[-1]
    hb = [child(s, "base") for s in (1, 2, 3)]
    hc = [child(s, "sorted") for s in (1, 2, 3)]
    print("e115.P3.base_hashes=", [h[:12] for h in hb])
    print("e115.P3.cand_hashes=", [h[:12] for h in hc])
    row("P3", len(set(hb)) == 1, len(set(hc)) == 1, False, True, "a")

    # (b) provenance
    new = {"name": "Other", "status": "ACTIVE"}
    k, b = v7_anchor(None); h0 = H(k["A-000"])
    row("P1m", None, (attempt(lambda: k.__setitem__("A-000", new)), H(k["A-000"]) == h0),
        None, ("CONFLICT:GRANT", True), "b")
    row("P1u", None, (attempt(lambda: k.update({"A-000": new})), H(k["A-000"]) == h0),
        None, ("CONFLICT:GRANT", True), "b")
    row("P1d", None, (attempt(lambda: k.__delitem__("A-000")), "A-000" in k),
        None, ("CONFLICT:GRANT", True), "b")
    row("P1p", None, (attempt(lambda: k.pop("A-000-RESH")), "A-000-RESH" in k),
        None, ("CONFLICT:GRANT", True), "b")
    def fx():
        with k.granted("not-a-grant"): k["A-000"] = new
    row("P1x", None, (attempt(fx), H(k["A-000"]) == h0), None, ("CONFLICT:GRANT", True), "b")
    k2, _ = v7_anchor(None)
    def fg():
        with k2.granted("e115-g"): k2["A-000"] = new
    row("P1g", None, (attempt(fg), k2["A-000"]["name"]), None, ("OK", "Other"), "b")
    row("P1n", None, (attempt(lambda: k.__setitem__("A-999", {"name": "x"})),), None, ("OK",), "b")

    class RecordOnly(g.AlgorithmMatrix):
        def record(self, entry_id, entry):
            if entry_id in PROTECTED: raise PermissionError("CONFLICT:GRANT")
            super().record(entry_id, entry)
    am = RecordOnly()
    direct = attempt(lambda: am.known.__setitem__("A-000", dict(new)))
    changed = am.known["A-000"]["name"] == "Other"
    viarec = attempt(lambda: am.record("A-000", {"name": "Third", "status": "ACTIVE"}))
    row("P1r", None, (direct, changed, viarec), None, ("OK", True, "CONFLICT:GRANT"), "b")

    def p1s(freeze):
        m = M(); m.known = GuardedKnown(g.AlgorithmMatrix().known, freeze=freeze)
        st = attempt(lambda: g.ReshIdentity(m).anchor())
        return (st, "identity_symbol" in m.known["A-000"])
    row("P1s_nofreeze", None, p1s(False), None, ("CONFLICT:GRANT", True), "b")
    row("P1s_freeze", None, p1s(True), None, ("TypeError", False), "b")

    sites = [i + 1 for i, l in enumerate(data.decode("utf-8").splitlines())
             if re.search(r"\.known\[[^\]]+\]\s*=(?!=)", l)]
    print("e115.SITES.count=", len(sites), "lines=", sites)

    a = all(v[2] for v in out.values() if v[0] == "a")
    bb = all(v[2] for v in out.values() if v[0] == "b")
    print("e115.a_outcome=", "PASS" if a else "FAIL",
          "misses=", [n for n, v in out.items() if v[0] == "a" and not v[2]] or "-")
    print("e115.b_outcome=", "PASS" if bb else "FAIL",
          "misses=", [n for n, v in out.items() if v[0] == "b" and not v[2]] or "-")
    print("e115.base_as_predicted=", all(v[1] for v in out.values()),
          "misses=", [n for n, v in out.items() if not v[1]] or "-")
    print("e115.c_outcome= DEFERRED(E115c)")
    print("e115.r5_label=", "integrity+provenance(partial); NOT write-protected" if a and bb
          else "candidate fails (a) or (b)")


if __name__ == "__main__":
    main()
