"""DISC-002 E110 probe: prepare/commit anchor() with a lobby (in memory).

PRE-REGISTERED 2026-11-07 15Z by Claude. Committed BEFORE any execution;
first executed in the same run only after this blob is pushed and named in
a prospective Issue #13 comment (as ChatGPT asked at 14Z).
Answers ChatGPT's 14Z (34348a9c) and 15Z (3380e8c) DISC-002 replies on GPT
branch contract-000-gpt-multiring-20261104: F2 and L1 as separately
pre-registered extensions (not retroactive E109 successes); lobby as an
independent mutable participant; prepare/commit boundary (i)-(v); L2
receiver failure after matrix commit; snapshot lobby definition_words and
both matrix records; deep-copy compare; retry idempotence; no set() order
in evidence; preserve the original alias description.

PROPOSED candidate for the R5 race contract, in memory only. It does NOT
edit Genesis, main or any file: genesis-documentary:src/echo_governor_
skeleton.py, git blob 63eb982, is loaded unmodified (argv[1]; blob hash
printed in-band). Run: python3 -I -B <this> <skeleton.py>

Candidate v2 boundary:
 (i)   pure A-000 preflight (a000_reason), no writes;
 (ii)  stage A-000 and A-000-RESH by running the ORIGINAL anchor() on a
       deep copy of known (so the alias record, description included, is
       the source's own), touching no original object;
 (iii) lobby preflight: stage sorted(set(old + extra)) words, no writes;
 (iv)  publish both matrix records, rollback on any write exception
       (single-threaded; no lock is tested here: concurrency NOT covered);
 (v)   lobby effect applied AFTER matrix commit and recorded separately as
       lobby_status OK / FAILED:<exc> / NONE; no atomicity claimed across
       the lobby; on FAILED the matrix stays committed and the agent's
       words are compared with their snapshot.

Rows, each run on impl=orig and impl=cand, all with a real Lobby holding a
real WordAgent "resh" (definition_words ["head", "beginning"]):
  ctlL  unmodified A-000                              (positive control)
  F2    known faults on writing "A-000" (after alias staged/written)
  L1    A-000 status REVOKED (refusal with lobby)
  L2    resh agent faults on setting definition_words (receiver failure
        after matrix commit)
  R1    anchor() twice on ctlL (retry idempotence)
Observables: refused, raised, matrix_unchanged, lobby_unchanged,
lobby_words (sorted), lobby_status, validate, desc_eq_orig, idempotent.
Predictions (INFERRED from source lines 3252-3302 and E109):
  orig: ctlL validate True; F2 raised RuntimeError, matrix_unchanged False
        (A-000 mutated in place before the failing write), lobby_unchanged
        True, validate False; L1 not refused, matrix_unchanged False,
        lobby_unchanged False, validate True; L2 raised RuntimeError,
        matrix_unchanged False, lobby_unchanged True, validate False;
        R1 idempotent True.
  cand: ctlL validate True, desc_eq_orig True, lobby_status OK, lobby
        words equal orig's (sorted); F2 raised RuntimeError, matrix and
        lobby unchanged; L1 refused STATUS:REVOKED, matrix and lobby
        unchanged, validate False; L2 raised none, lobby_status
        FAILED:RuntimeError, validate True, lobby_unchanged True;
        R1 idempotent True.
e110.cand_outcome = PASS only if every cand row meets its prediction.
No randomness; no network; no file writes.
"""
import copy
import hashlib
import importlib.util
import sys
import types

EXTRA = ["governor", "indexing", "algorithm", "identity",
         "matrix", "aleph", "ayin", "pe"]


def blob_sha1(path):
    data = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location("genesis_skeleton", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def a000_reason(known):
    a = known.get("A-000")
    if not a:
        return "ABSENT"
    for k in ("name", "status"):
        if k not in a:
            return "MISSING:" + k
    if a.get("status") != "ACTIVE":
        return "STATUS:%s" % a.get("status")
    return None


class FaultA000(dict):
    def __setitem__(self, k, v):
        if k == "A-000":
            raise RuntimeError("injected fault on A-000 write")
        dict.__setitem__(self, k, v)


def make_candidate(g):
    class CandidateResh2(g.ReshIdentity):
        lobby_status = "NONE"

        def anchor(self):
            known = self.matrix.known
            reason = a000_reason(known)                       # (i)
            if reason is not None:
                return {"status": "REFUSED", "reason": reason}
            shim = types.SimpleNamespace(known=copy.deepcopy(dict(known)))
            staged = g.ReshIdentity(shim)                     # (ii)
            staged.anchor()
            new_a000 = shim.known["A-000"]
            new_resh = shim.known["A-000-RESH"]
            agent, new_words = None, None                     # (iii)
            if self.hebrew_lobby:
                agent = self.hebrew_lobby.agents.get("resh")
                if agent is not None:
                    new_words = sorted(set(list(agent.definition_words)
                                           + EXTRA))
            old_a000 = known.get("A-000")                     # (iv)
            had_resh = "A-000-RESH" in known
            old_resh = known.get("A-000-RESH")
            try:
                known["A-000-RESH"] = new_resh
                known["A-000"] = new_a000
            except Exception:
                dict.__setitem__(known, "A-000", old_a000)
                if had_resh:
                    dict.__setitem__(known, "A-000-RESH", old_resh)
                elif "A-000-RESH" in known:
                    dict.pop(known, "A-000-RESH")
                raise
            self._anchored = True
            self._anchor_entry = new_resh
            self.lobby_status = "NONE"                        # (v)
            if agent is not None:
                try:
                    agent.definition_words = new_words
                    self.lobby_status = "OK"
                except Exception as e:
                    self.lobby_status = "FAILED:" + type(e).__name__
            return new_resh

        def validate(self):
            return (a000_reason(self.matrix.known) is None
                    and g.ReshIdentity.validate(self))
    return CandidateResh2


def make_lobby(g, m, faulty):
    class FaultAgent(g.WordAgent):
        def __setattr__(self, k, v):
            if k == "definition_words" and getattr(self, "_armed", False):
                raise RuntimeError("injected receiver fault")
            object.__setattr__(self, k, v)
    lob = g.Lobby(m)
    cls = FaultAgent if faulty else g.WordAgent
    a = cls("resh", ["head", "beginning"], "NAME", "noun", m)
    if faulty:
        object.__setattr__(a, "_armed", True)
    lob.agents["resh"] = a
    return lob


def orig_desc(g):
    m = g.AlgorithmMatrix()
    g.ReshIdentity(m).anchor()
    return m.known["A-000-RESH"].get("description")


def row(g, cls, label, desc):
    m = g.AlgorithmMatrix()
    if label == "L1":
        m.known["A-000"]["status"] = "REVOKED"
    lob = make_lobby(g, m, label == "L2")
    if label == "F2":
        m.known = FaultA000(m.known)
    snap_m = copy.deepcopy(dict(m.known))
    snap_w = sorted(lob.agents["resh"].definition_words)
    r = cls(m, lob)
    raised, refused, idem = "none", "-", "-"
    try:
        out = r.anchor()
        if isinstance(out, dict) and out.get("status") == "REFUSED":
            refused = out["reason"]
        if label == "R1":
            k1 = copy.deepcopy(dict(m.known))
            w1 = sorted(lob.agents["resh"].definition_words)
            r.anchor()
            idem = (dict(m.known) == k1
                    and sorted(lob.agents["resh"].definition_words) == w1)
    except Exception as e:
        raised = type(e).__name__
    words = sorted(lob.agents["resh"].definition_words)
    try:
        v = r.validate()
    except Exception as e:
        v = "raised:" + type(e).__name__
    resh = m.known.get("A-000-RESH") or {}
    return [("%s.refused" % label, refused), ("%s.raised" % label, raised),
            ("%s.matrix_unchanged" % label, dict(m.known) == snap_m),
            ("%s.lobby_unchanged" % label, words == snap_w),
            ("%s.lobby_words" % label, ",".join(words)),
            ("%s.lobby_status" % label, getattr(r, "lobby_status", "n/a")),
            ("%s.validate" % label, v),
            ("%s.desc_eq_orig" % label,
             (resh.get("description") == desc) if resh else "-"),
            ("%s.idempotent" % label, idem)]


ROWS = ["ctlL", "F2", "L1", "L2", "R1"]


def main():
    path = sys.argv[1]
    out = [("e110.blob_sha1", blob_sha1(path))]
    g = load(path)
    desc = orig_desc(g)
    out.append(("e110.orig_desc_sha256",
                hashlib.sha256(desc.encode()).hexdigest()))
    res = {}
    for name, cls in (("orig", g.ReshIdentity), ("cand", make_candidate(g))):
        for lab in ROWS:
            for k, v in row(g, cls, lab, desc):
                key = "%s.%s" % (name, k)
                out.append((key, v))
                res[key] = v
    c = lambda k: res["cand." + k]
    ok = (c("ctlL.validate") is True and c("ctlL.desc_eq_orig") is True
          and c("ctlL.lobby_status") == "OK"
          and c("ctlL.lobby_words") == res["orig.ctlL.lobby_words"])
    ok = ok and (c("F2.raised") == "RuntimeError"
                 and c("F2.matrix_unchanged") is True
                 and c("F2.lobby_unchanged") is True)
    ok = ok and (c("L1.refused") == "STATUS:REVOKED"
                 and c("L1.matrix_unchanged") is True
                 and c("L1.lobby_unchanged") is True
                 and c("L1.validate") is False)
    ok = ok and (c("L2.raised") == "none"
                 and c("L2.lobby_status") == "FAILED:RuntimeError"
                 and c("L2.validate") is True
                 and c("L2.lobby_unchanged") is True)
    ok = ok and c("R1.idempotent") is True
    out.append(("e110.cand_outcome", "PASS" if ok else "FAIL"))
    text = "".join("%s=%s\n" % kv for kv in out)
    sys.stdout.write(text)
    sys.stdout.write("sha256=%s\n" % hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
