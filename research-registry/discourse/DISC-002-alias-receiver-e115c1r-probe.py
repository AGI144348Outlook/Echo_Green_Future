"""DISC-002 E115c-1 probe: alias paths (a: D1, D2, P1s-atomic) and
cross-receiver binding (b: X0-X3), candidate v8 versus the unmodified
skeleton and the E115 v7 shallow freeze.

REVISION r of E115c-1 (blob 55045825, commit 59ae4d29). That blob was
executed twice at 06Z (byte-identical partial stdout sha256 fa0a045b...4c68) and ABORTED with rc 1 after 3 rows: its v7s D2
row called ref.__setitem__(...), and a MappingProxyType has no such
attribute (AttributeError, not caught), so the harness, not the candidate,
failed. The only change here: v7s/v8 D2 now uses item assignment
(operator.setitem), which raises TypeError on a mappingproxy as the
prediction assumed. Rows and predictions are otherwise byte-for-byte the
same. Partial output of the aborted run (3 rows, all "match") is recorded
in DISC-002 06Z and does not count toward any outcome.

PRE-REGISTERED 2026-11-08 06Z by Claude. Committed BEFORE any execution;
first executed only after this blob is pushed and named in a prospective
Issue #13 comment. Only a byte-compile check (py_compile) was run before
commit; no row was executed.

Design: DISC-002 05Z (Claude, rdr 3174bb2a, blob b8c48312): D1/D2 from
the alias paths at skeleton l. 3271 (nested "aliases" list) and l. 3293
(ReshIdentity._anchor_entry), P1s moved under (a) as an atomicity row
(ChatGPT 05Z c5bf06a3), X1/X2 from ChatGPT 04Z b5c74354 cross-receiver
falsifier. Each row reports ONE property, never a combined pass.

SCOPE: this is part 1 of E115c. Property (c) restart recovery (N3 used
nonce replayed after restart with the used-nonce set inside the anchored
WAL envelope; C1 flipped byte; C2 missing envelope; C3 truncated WAL tail;
C4 refusal-receipt isolation) and the E114 W1-W5 regression rows build on
the E114 v6 code and are NOT in this file; they stay DEFERRED to E115c-2.
So whatever this file prints, no candidate can be reported as
"write-protected"; at most "integrity + provenance (partial)".

Limits stated before the run: in-process stand-ins; GRANTS is a FIXTURE
(not authority); the bound-hash store is in the same process; sha256 over
canonical JSON is a digest, not authentication. Nothing edits Genesis,
main or any file. Timothy's issuer/revocation/receiver tie/merge-vs-replace
remain open.

Input, loaded unmodified: argv[1] = directory holding
  genesis-documentary:src/echo_governor_skeleton.py blob 63eb982.
Run: python3 -I -B <this> <dir>

Candidates:
  v7s (shallow, as E115 v7 freeze=True): protected values stored as
    MappingProxyType(dict(v)); nested lists stay plain lists.
  v8 (PROPOSED, never applied to Genesis): protected values stored as
    canonical JSON bytes; every read (__getitem__, get) returns a fresh
    deep copy; writes to protected keys need `with known.granted(tok)`
    else PermissionError("CONFLICT:GRANT").
  Receipt v8: R = H({key, def_hash: H(definition), ser: SER, src: SRC}).
    verify_v8(R, key, definition, ser, src) recomputes; reason DEF_HASH /
    SER_VER / SRC / OK. Name-only verifier (E114-style receiver id):
    accepts iff key and identity_symbol markers match.

Rows and predictions (INFERRED from skeleton 63eb982 and the rules above):
 (a)
  D1  after anchor, r._anchor_entry["aliases"].append("x").
      base: stored aliases changed, validate True (wrongly accepted).
      v7s: append goes through the proxy's nested list -> stored changed,
           hash check (False, RESH_HASH).  [05Z INFERRED claim, now tested]
      v8 : copy changed only; stored unchanged; (True, OK).
  D2  after anchor, r._anchor_entry["status"] = "RETIRED".
      base: stored changed, validate True (wrongly accepted).
      v7s: TypeError, stored unchanged, (True, OK).
      v8 : copy changed only; stored unchanged; (True, OK).
  P1s skeleton ReshIdentity.anchor() on the guarded mapping, no grant.
      v7 unfrozen (E115 regression): refused, leak True.
      v8: refused (CONFLICT:GRANT), leak False (get() returned a copy).
  V4r regression: under grant A-000 := anchored copy with name changed.
      v8 (False, A000_HASH).
  P2r regression: known["A-000"]["status"] = "RETIRED" in place.
      v8: copy only; stored unchanged; (True, OK).
 (b)
  X0  receipt for definition D, verify against D, same ser/src.
      name-only True; v8 (True, OK).   [control]
  X1  verify against D' = D with description changed (same key, same
      identity markers). name-only True (wrongly accepted); v8 DEF_HASH.
  X2  same D, ser "e115c-v2" instead of "e115c-v1".
      name-only True (wrongly accepted); v8 SER_VER.
  X3  same D, src commit "0000000" instead of "63eb982".
      name-only True (wrongly accepted); v8 SRC.

Outcome lines: e115c1.a_outcome = PASS iff every (a) row matches its v8
prediction; e115c1.b_outcome likewise for (b); e115c1.base_as_predicted
for base / v7s / name-only columns; e115c1.c_outcome = DEFERRED(E115c-2).
"""
import sys, json, hashlib, types, contextlib, operator

GRANTS = {"e115c-g"}
PROTECTED = {"A-000", "A-000-RESH"}
SER, SRC = "e115c-v1", "63eb982"


def plain(v):
    if isinstance(v, (dict, types.MappingProxyType)):
        return {k: plain(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [plain(x) for x in v]
    return v


def C(v):
    return json.dumps(plain(v), sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode()


def H(v):
    return hashlib.sha256(C(v)).hexdigest()


class Guard(dict):
    """Shared grant logic. mode 'v7u' (plain), 'v7s' (shallow proxy), 'v8' (bytes)."""
    def __init__(self, init, mode):
        super().__init__()
        self.mode, self._tok = mode, None
        for k, v in dict(init).items():
            dict.__setitem__(self, k, self._wrap(k, v))

    def _wrap(self, k, v):
        if k not in PROTECTED:
            return v
        if self.mode == "v7s":
            return types.MappingProxyType(dict(v))
        if self.mode == "v8":
            return C(v)
        return v

    def _out(self, k, v):
        if k in PROTECTED and self.mode == "v8":
            return json.loads(v.decode())
        return v

    def __getitem__(self, k):
        return self._out(k, dict.__getitem__(self, k))

    def get(self, k, d=None):
        return self[k] if k in self else d

    def raw(self, k):
        return plain(self[k]) if self.mode != "v8" else json.loads(dict.__getitem__(self, k).decode())

    @contextlib.contextmanager
    def granted(self, tok):
        if tok not in GRANTS:
            raise PermissionError("CONFLICT:GRANT")
        self._tok = tok
        try:
            yield self
        finally:
            self._tok = None

    def __setitem__(self, k, v):
        if k in PROTECTED and self._tok is None:
            raise PermissionError("CONFLICT:GRANT")
        dict.__setitem__(self, k, self._wrap(k, v))


def attempt(fn):
    try:
        fn(); return "ok"
    except PermissionError as e:
        return str(e)
    except TypeError:
        return "TypeError"


def anchor_cow(known, tok):
    a = dict(plain(known.get("A-000", {})))
    a.update({"identity_symbol": "resh", "identity_glyph": "ר",
              "identity_letter": "resh",
              "identity_meaning": "head beginning leader identity"})
    resh = {"name": "Resh — Governor Identity Anchor", "status": "ACTIVE",
            "type": "IDENTITY-LETTER", "glyph": "ר",
            "aliases": ["A-000", "resh", "governor"],
            "description": "copied from skeleton l. 3268-3279 (text not hashed against Genesis)",
            "perception_operator": "ayin", "expression_operator": "pe"}
    with known.granted(tok):
        known["A-000"] = a
        known["A-000-RESH"] = resh
    return {"a000": H(known.raw("A-000")), "resh": H(known.raw("A-000-RESH"))}


def validate(known, bound):
    a = known.get("A-000")
    if not isinstance(a, (dict, types.MappingProxyType)):
        return (False, "MISSING")
    if "name" not in a or "status" not in a:
        return (False, "FIELDS")
    if a.get("identity_symbol") != "resh":
        return (False, "SYMBOL")
    if not isinstance(known.get("A-000-RESH"), (dict, types.MappingProxyType)):
        return (False, "RESH_MISSING")
    if H(known.raw("A-000")) != bound["a000"]:
        return (False, "A000_HASH")
    if H(known.raw("A-000-RESH")) != bound["resh"]:
        return (False, "RESH_HASH")
    return (True, "OK")


def receipt(key, d, ser, src):
    return H({"key": key, "def_hash": H(d), "ser": ser, "src": src})


def verify_v8_reason(r, issued, key, d, ser, src):
    """Acceptance is r == receipt(key, d, ser, src) only. `issued` is used
    ONLY to name the reason (swap one field back at a time); a real
    verifier would not hold it."""
    if r == receipt(key, d, ser, src):
        return "OK"
    d0, ser0, src0 = issued
    if r == receipt(key, d0, ser, src):
        return "DEF_HASH"
    if r == receipt(key, d, ser0, src):
        return "SER_VER"
    if r == receipt(key, d, ser, src0):
        return "SRC"
    return "MISMATCH"


def name_only(key, d):
    return key == "A-000-RESH" and "resh" in d.get("aliases", [])


def main():
    sys.path.insert(0, sys.argv[1])
    import echo_governor_skeleton as g
    res, ok_a, ok_b, ok_base = [], True, True, True

    def out(row, prop, got, exp, col):
        nonlocal ok_a, ok_b, ok_base
        m = (got == exp)
        print(f"{row}\t{prop}\t{col}\tgot={got}\texp={exp}\t{'match' if m else 'MISS'}")
        if not m:
            if col in ("v8",):
                if prop == "a": ok_a = False
                else: ok_b = False
            else:
                ok_base = False

    class M:
        pass

    # ---- base (unmodified skeleton) D1 / D2
    for row, fn in (("D1", lambda r: r._anchor_entry["aliases"].append("x")),
                    ("D2", lambda r: r._anchor_entry.__setitem__("status", "RETIRED"))):
        m = M(); m.known = g.AlgorithmMatrix().known
        r = g.ReshIdentity(m); r.anchor()
        before = H(m.known["A-000-RESH"]); fn(r)
        changed = H(m.known["A-000-RESH"]) != before
        out(row, "a", (changed, r.validate()), (True, True), "base")

    # ---- v7s and v8 D1 / D2: anchor (COW, grant), then skeleton-style retained reference
    for mode in ("v7s", "v8"):
        for row in ("D1", "D2"):
            k = Guard(g.AlgorithmMatrix().known, mode)
            bound = anchor_cow(k, "e115c-g")
            ref = k["A-000-RESH"]          # what l. 3293 would retain
            before = H(k.raw("A-000-RESH"))
            if row == "D1":
                st = attempt(lambda: ref["aliases"].append("x"))
            else:
                st = attempt(lambda: operator.setitem(ref, "status", "RETIRED"))
            changed = H(k.raw("A-000-RESH")) != before
            v = validate(k, bound)
            if mode == "v7s":
                exp = (("ok", True, (False, "RESH_HASH")) if row == "D1"
                       else ("TypeError", False, (True, "OK")))
            else:
                exp = ("ok", False, (True, "OK"))
            out(row, "a", (st, changed, v), exp, mode)

    # ---- P1s atomicity: unmodified skeleton anchor() on guarded mapping, no grant
    for mode, exp in (("v7u", ("CONFLICT:GRANT", True)), ("v8", ("CONFLICT:GRANT", False))):
        m = M(); m.known = Guard(g.AlgorithmMatrix().known, mode)
        st = attempt(lambda: g.ReshIdentity(m).anchor())
        leak = "identity_symbol" in m.known.raw("A-000")
        out("P1s", "a", (st, leak), exp, mode)

    # ---- V4r / P2r regression on v8
    k = Guard(g.AlgorithmMatrix().known, "v8"); bound = anchor_cow(k, "e115c-g")
    a = k["A-000"]; a["name"] = "changed"
    with k.granted("e115c-g"):
        k["A-000"] = a
    out("V4r", "a", validate(k, bound), (False, "A000_HASH"), "v8")
    k = Guard(g.AlgorithmMatrix().known, "v8"); bound = anchor_cow(k, "e115c-g")
    st = attempt(lambda: k["A-000"].__setitem__("status", "RETIRED"))
    out("P2r", "a", (st, k.raw("A-000")["status"], validate(k, bound)),
        ("ok", k.raw("A-000")["status"], (True, "OK")), "v8")
    out("P2r.status", "a", k.raw("A-000")["status"] != "RETIRED", True, "v8")

    # ---- (b) cross-receiver
    k = Guard(g.AlgorithmMatrix().known, "v8"); anchor_cow(k, "e115c-g")
    D = k.raw("A-000-RESH")
    D2_ = dict(D); D2_["description"] = D["description"] + " (other receiver)"
    R = receipt("A-000-RESH", D, SER, SRC)
    issued = (D, SER, SRC)
    rows = (("X0", D, SER, SRC, True, "OK"),
            ("X1", D2_, SER, SRC, True, "DEF_HASH"),
            ("X2", D, "e115c-v2", SRC, True, "SER_VER"),
            ("X3", D, SER, "0000000", True, "SRC"))
    for row, d, ser, src, exp_n, exp_v in rows:
        out(row, "b", name_only("A-000-RESH", d), exp_n, "name-only")
        out(row, "b", verify_v8_reason(R, issued, "A-000-RESH", d, ser, src), exp_v, "v8")

    print(f"e115c1.a_outcome={'PASS' if ok_a else 'FAIL'}")
    print(f"e115c1.b_outcome={'PASS' if ok_b else 'FAIL'}")
    print(f"e115c1.base_as_predicted={ok_base}")
    print("e115c1.c_outcome=DEFERRED(E115c-2)")


if __name__ == "__main__":
    main()
