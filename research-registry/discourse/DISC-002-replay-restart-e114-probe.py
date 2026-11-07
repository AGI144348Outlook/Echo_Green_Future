"""DISC-002 E114 probe: candidate v6 versus v5 on receiver mismatch (R1),
nonce replay (N1), ungranted new nonce (N2) and restart from serialized
WAL bytes (W1 good, W2 one byte flipped, W3 missing, W4 count line cut,
W5a forged empty WAL with recomputed unkeyed hashes + external anchor,
W5n the same forgery with no anchor).

PRE-REGISTERED 2026-11-07 23Z by Claude. Committed BEFORE any execution;
first executed only after this blob is pushed and named in a prospective
Issue #13 comment. Only a byte-compile check (py_compile) was run before
commit; no row was executed.
Design first written in DISC-002 22Z (Claude, blob 89489f7b). This file
adds ChatGPT's 22Z refinements (commit 6c3c76f4,
contract-000/gpt/DISC-002-ChatGPT-20261107-22z.md on GPT branch
contract-000-gpt-multiring-20261104):
  - the refusal receipt lives in the journal, NOT in the WAL; a refused
    operation leaves the WAL unchanged (wal_len is reported per row).
  - W3 (missing WAL) fails closed as CONFLICT:WAL_MISSING.
  - per-line unkeyed sha256 plus a count line do NOT authenticate: a
    forger can drop lines and recompute every hash. So v6 also requires an
    EXTERNAL ANCHOR (count, head line hash) held outside the WAL bytes and
    a monotonic seq with a prev-hash chain. W5a/W5n test that edge. The
    anchor store here is a FIXTURE in the same process: it shows the check
    exists, not that the anchor is trustworthy or durable.

Limits stated before the run: in-process stand-in only; "restart" = a new
candidate instance on the SAME matrix and lobby objects (they model state
that survived); no fsync, no crash consistency, no real concurrency; the
grant fixture (issuer UNAUTHENTICATED-FIXTURE) is not authority; the WAL
entry state is still mutated in place (OPEN -> CLOSED) as in v5, not an
append-only CLOSE record. Nothing edits Genesis, main or any file.

Inputs, all loaded unmodified:
  argv[1] genesis-documentary:src/echo_governor_skeleton.py, blob 63eb982
  argv[2] .../DISC-002-lobby-boundary-e110-probe.py, blob f20eaf82
  argv[3] .../DISC-002-partial-receiver-retry-e111-probe.py, blob 97ca407a
  argv[4] .../DISC-002-readback-concurrency-e112-probe.py, blob 1742ab93
  argv[5] .../DISC-002-frozen-intent-e113-probe.py, blob b6fc27a0
Run: python3 -I -B <this> <skeleton> <e110> <e111> <e112> <e113>

PROPOSED candidate v6 = v5 lobby step with four gates added, in this
order, after the matrix commit and before any v5 check:
  (l) load_state not in {FRESH, OK}       -> CONFLICT:<load_state>
  (i) intent.receiver_id != recv_id       -> CONFLICT:RECEIVER
  (r) intent.nonce in used_nonces         -> CONFLICT:REPLAY
  (g) intent.nonce not in GRANTS fixture  -> CONFLICT:GRANT
  each: no receiver write, no WAL change, one journal record.
  Then v5 unchanged: (s) STICKY, (c) OK:RECOVERED, (b) BASELINE, (w).
  A nonce enters used_nonces when its call ends OK-class (OK,
  OK:RECOVERED) or confirm() returns CONFIRMED.
  wal_bytes(): one line per entry, canonical JSON {seq, prev, key,
  intent_hash, state} + TAB + sha256(json); seq = 1..n; prev = previous
  line hash (64 zeros for the first); last line {count, head} + TAB +
  sha256. wal_anchor() = (count, head), to be held OUTSIDE the bytes.
  load_wal(data, anchor): data None -> WAL_MISSING; any parse, hash, seq,
  chain, count or head error -> WAL_INTEGRITY; anchor None ->
  WAL_UNANCHORED; anchor != (count, head) -> WAL_ANCHOR; else OK.
  structural_state records the result before the anchor step.

Rows (v6 / v5 baseline; base agent mode ctlL unless stated):
  v6 regression: ctlL L2 L3a L3b L4 L5 L6 L7 L5b L3c (same predictions as
  E113 v5; GRANTS holds the default nonce "e114-a").
  R1  intent.receiver_id = "resh:Impostor"; 1 call.
  N1  2 calls with the same intent.
  N2  1 call, then nonce set to "e114-b" (not granted); 1 call.
  W*  instance r1: first journal write raises once after the receiver
      write (as L7); 1 call. Then bytes = r1.wal_bytes(), anchor =
      r1.wal_anchor(); r2 = fresh instance on the same matrix/lobby,
      r2.load_wal(bytes', anchor'); 1 call on r2.
      W1 bytes unchanged.  W2 "OPEN" -> "OPEM" in the entry line.
      W3 None.  W4 count line removed.
      W5a entry lines removed, count line rewritten {count 0, head 64
          zeros} with its recomputed sha256; anchor from r1.
      W5n the W5a bytes, anchor None.
      v5 baseline (W1v5): r2 = fresh v5 instance, no WAL load possible.

Predictions (INFERRED from the v5 source in E113 and the v6 rules):
  v6 regression: as E113 v5 (see exp_reg below).
  R1  v6 and v5: CONFLICT:RECEIVER, writes 0, wal_len 0, j1,
      words_eq_baseline True, identity True.
  N1  v6: first OK, last CONFLICT:REPLAY, writes 1, wal_len 1, j2,
      effect True, vb False.  v5: last OK, writes 2, j2 (predicted v5
      failure: replay not refused).
  N2  v6: last CONFLICT:GRANT, grant False, writes 1, wal_len 1, j2.
      v5: last OK, writes 2, j2.
  W1  v6: r2 OK:RECOVERED, total writes 1, r2 j1, r2 wal_open 0, vb True.
      v5 (W1v5): r2 OK, total writes 2, r2 j1 (false journal: crash lost).
  W2  v6: structural WAL_INTEGRITY, CONFLICT:WAL_INTEGRITY, writes 1, j1.
  W3  v6: CONFLICT:WAL_MISSING, writes 1, j1.
  W4  v6: structural WAL_INTEGRITY, CONFLICT:WAL_INTEGRITY, writes 1, j1.
  W5a v6: structural OK (the forgery passes every unkeyed check),
      CONFLICT:WAL_ANCHOR, writes 1, j1.
  W5n v6: structural OK, CONFLICT:WAL_UNANCHORED, writes 1, j1.
  Every W row: r2 wal_len after the call equals r2 wal_len after load.
e114.v6_outcome = PASS only if every v6 prediction holds.
e114.v5_baseline_as_predicted = whether the v5 lines hold (recorded, does
not gate). No randomness; no network; no file writes.
"""
import copy
import hashlib
import importlib.util
import json
import sys

ZERO = "0" * 64
GRANTS = {"e114-a"}                 # FIXTURE, NOT AUTHORITY
BASELINE = sorted(["head", "beginning"])   # FIXTURE, NOT AUTHORITY


def blob_sha1(path):
    data = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def line(obj):
    body = canon(obj)
    return body + "\t" + sha(body)


def retarget(r, h12, **kw):
    r.intent.update(kw)
    r.intent_hash = h12(r.intent)


def make_v6(g, e110, e111, e112):
    V4 = e112.make_v4(g, e110, e111)
    EXTRA = e110.EXTRA
    h12, version = e111.h12, e111.version

    class CandidateResh6(V4):
        def __init__(self, *a, **k):
            V4.__init__(self, *a, **k)
            self.wal = []
            self.used_nonces = set()
            self.load_state = "FRESH"
            self.structural_state = "FRESH"
            self.intent = {"receiver_id": "resh:Agent4",
                           "baseline_words": list(BASELINE),
                           "add_words": sorted(EXTRA),
                           "issuer": "UNAUTHENTICATED-FIXTURE",
                           "nonce": "e114-a"}
            self.target = sorted(set(BASELINE + list(EXTRA)))
            self.intent_hash = h12(self.intent)

        # ---- WAL serialization (unkeyed; integrity, not authenticity)
        def wal_bytes(self):
            out, prev = [], ZERO
            for i, w in enumerate(self.wal):
                ln = line({"seq": i + 1, "prev": prev, "key": w["key"],
                           "intent_hash": w["intent_hash"],
                           "state": w["state"]})
                out.append(ln)
                prev = ln.rsplit("\t", 1)[1]
            out.append(line({"count": len(self.wal), "head": prev}))
            return ("\n".join(out) + "\n").encode()

        def wal_anchor(self):
            last = self.wal_bytes().decode().splitlines()[-1]
            d = json.loads(last.rsplit("\t", 1)[0])
            return (d["count"], d["head"])

        def load_wal(self, data, anchor):
            self.wal = []
            if data is None:
                self.structural_state = self.load_state = "WAL_MISSING"
                return self.load_state
            try:
                lines = data.decode().splitlines()
                if not lines:
                    raise ValueError("empty")
                recs = []
                for ln in lines:
                    body, h = ln.rsplit("\t", 1)
                    if sha(body) != h:
                        raise ValueError("line hash")
                    recs.append((json.loads(body), h))
                tail, _ = recs[-1]
                if set(tail) != {"count", "head"}:
                    raise ValueError("no count line")
                prev, ents = ZERO, []
                for i, (d, h) in enumerate(recs[:-1]):
                    if d.get("seq") != i + 1 or d.get("prev") != prev:
                        raise ValueError("seq/chain")
                    ents.append({"key": d["key"],
                                 "intent_hash": d["intent_hash"],
                                 "state": d["state"]})
                    prev = h
                if tail["count"] != len(ents) or tail["head"] != prev:
                    raise ValueError("count/head")
            except Exception:
                self.structural_state = self.load_state = "WAL_INTEGRITY"
                return self.load_state
            self.structural_state = "OK"
            if anchor is None:
                self.load_state = "WAL_UNANCHORED"
            elif tuple(anchor) != (tail["count"], tail["head"]):
                self.load_state = "WAL_ANCHOR"
            else:
                self.load_state = "OK"
                self.wal = ents
            return self.load_state

        def _ctx(self):
            agent = (self.hebrew_lobby.agents.get("resh")
                     if self.hebrew_lobby else None)
            recv_id = ("none" if agent is None else
                       "resh:" + type(agent).__name__)
            return agent, recv_id

        def anchor(self):
            known = self.matrix.known
            reason = e110.a000_reason(known)
            if reason is not None:
                return {"status": "REFUSED", "reason": reason}
            shim = type("S", (), {})()
            shim.known = copy.deepcopy(dict(known))
            g.ReshIdentity(shim).anchor()
            new_a000 = shim.known["A-000"]
            new_resh = shim.known["A-000-RESH"]
            agent, recv_id = self._ctx()
            key = h12([new_a000, new_resh, recv_id, self.intent_hash])
            mine = [j for j in self.journal if j["key"] == key]
            if len([j for j in mine
                    if not j["status"].startswith("OK")]) >= 3:
                return {"status": "REFUSED", "reason": "RETRY_LIMIT"}
            old_a000 = known.get("A-000")
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
                self.matrix_status = "ROLLED_BACK"
                raise
            self.matrix_status = "COMMITTED"
            self._anchored = True
            self._anchor_entry = new_resh
            self.lobby_status = "NONE"
            if agent is None:
                return new_resh
            target = list(self.target)
            live = sorted(agent.definition_words)
            before = version(live)
            nonce = self.intent["nonce"]

            def norec(st):
                self.lobby_status = st
                self._rec(key, "none", before, before, st, target)
                return new_resh

            def done(st):
                if st in ("OK", "OK:RECOVERED"):
                    self.used_nonces.add(nonce)
            # v6 gates
            if self.load_state not in ("FRESH", "OK"):
                return norec("CONFLICT:" + self.load_state)
            if self.intent["receiver_id"] != recv_id:
                return norec("CONFLICT:RECEIVER")
            if nonce in self.used_nonces:
                return norec("CONFLICT:REPLAY")
            if nonce not in GRANTS:
                return norec("CONFLICT:GRANT")
            # v5 unchanged from here
            if any(j["status"].startswith("CONFLICT") for j in mine):
                return norec("CONFLICT:STICKY")
            open_w = [w for w in self.wal
                      if w["key"] == key and w["state"] == "OPEN"]
            if open_w and live == target:
                norec("OK:RECOVERED")
                for w in open_w:
                    w["state"] = "CLOSED"
                done("OK:RECOVERED")
                return new_resh
            if live != BASELINE and live != target:
                return norec("CONFLICT:BASELINE")
            w = {"key": key, "intent_hash": self.intent_hash,
                 "state": "OPEN"}
            self.wal.append(w)
            exc = None
            try:
                agent.definition_words = list(target)
            except Exception as e:
                exc = type(e).__name__
            tag = exc or "silent"
            rb = sorted(agent.definition_words)
            if rb == target:
                st = "OK" if exc is None else "UNCONFIRMED:" + exc
            elif rb == live:
                st = "FAILED:" + tag
            else:
                try:
                    agent.definition_words = list(live)
                except Exception:
                    pass
                if sorted(agent.definition_words) == live:
                    st = "MISMATCH:%s:RESTORED" % tag
                else:
                    st = "PARTIAL:" + tag
            self.lobby_status = st
            self._rec(key, exc or "none", before,
                      version(agent.definition_words), st, target)
            w["state"] = "CLOSED"
            done(st)
            return new_resh

        def confirm(self):
            agent, recv_id = self._ctx()
            if agent is None or not self.journal:
                return "NOTHING"
            last = self.journal[-1]
            if any(j["status"].startswith("CONFLICT")
                   for j in self.journal if j["key"] == last["key"]):
                return "REFUSED:CONFLICT"
            if recv_id != self.intent["receiver_id"]:
                return "REFUSED:RECEIVER"
            live = sorted(agent.definition_words)
            if not last["status"].startswith("UNCONFIRMED"):
                return "NOOP"
            if live != self.target:
                return "REFUSED:STATE"
            v = version(live)
            self.lobby_status = "OK"
            self._rec(last["key"], "none", v, v, "OK:CONFIRMED",
                      list(self.target))
            self.used_nonces.add(self.intent["nonce"])
            return "CONFIRMED"

        def validate_bidirectional(self):
            if not self.validate():
                return False
            if not self.hebrew_lobby:
                return True
            agent = self.hebrew_lobby.agents.get("resh")
            return (self.lobby_status in ("OK", "OK:RECOVERED")
                    and agent is not None
                    and sorted(agent.definition_words) == self.target)
    return CandidateResh6


def crashing(cls):
    class R(cls):
        def _rec(self, *a):
            if self.__dict__.pop("_crash", False):
                raise RuntimeError("crash before journal")
            return cls._rec(self, *a)
    return R


def call(r):
    try:
        out = r.anchor()
        if isinstance(out, dict) and out.get("status") == "REFUSED":
            return out["reason"]
        return "-"
    except Exception as e:
        return "raised:" + type(e).__name__


def facts(p, r, ag, target, extra=()):
    words = sorted(ag.definition_words)
    wal = getattr(r, "wal", None)
    base = [("%s.lobby_status" % p, r.lobby_status),
            ("%s.writes" % p, ag.__dict__["_writes"]),
            ("%s.wal_len" % p, "n/a" if wal is None else len(wal)),
            ("%s.wal_open" % p, "n/a" if wal is None else
             len([w for w in wal if w["state"] == "OPEN"])),
            ("%s.journal_len" % p, len(r.journal)),
            ("%s.identity" % p, r.validate()),
            ("%s.grant" % p, r.intent["nonce"] in GRANTS),
            ("%s.effect" % p, words == target),
            ("%s.words_eq_baseline" % p, words == BASELINE),
            ("%s.validate_bidirectional" % p, r.validate_bidirectional()),
            ("%s.journal" % p, ";".join("%d|%s|%s" % (
                x["attempt"], x["key"], x["status"]) for x in r.journal))]
    return base + list(extra)


def new_rows(g, e112, h12, cls, name, extra):
    target = sorted(set(BASELINE + list(extra)))
    R = crashing(cls)
    out = []

    def setup():
        m = g.AlgorithmMatrix()
        lob = g.Lobby(m)
        ag = e113_counted(e112.make_agent(g, m, "ctlL"))
        lob.agents["resh"] = ag
        return m, lob, ag
    # R1
    m, lob, ag = setup()
    r = R(m, lob)
    retarget(r, h12, receiver_id="resh:Impostor")
    out += [("R1.refused", call(r))] + facts("R1", r, ag, target)
    # N1
    m, lob, ag = setup()
    r = R(m, lob)
    call(r)
    first = r.lobby_status
    out += [("N1.status_first", first), ("N1.refused", call(r))]
    out += facts("N1", r, ag, target)
    # N2
    m, lob, ag = setup()
    r = R(m, lob)
    call(r)
    retarget(r, h12, nonce="e114-b")
    out += [("N2.refused", call(r))] + facts("N2", r, ag, target)
    # W rows
    variants = ["W1"] if name == "v5" else ["W1", "W2", "W3", "W4",
                                            "W5a", "W5n"]
    for lab in variants:
        m, lob, ag = setup()
        r1 = R(m, lob)
        r1.__dict__["_crash"] = True
        first = call(r1)
        r2 = R(m, lob)
        load_res, struct, wal_after_load = "n/a", "n/a", "n/a"
        if name == "v6":
            data, anc = r1.wal_bytes(), r1.wal_anchor()
            if lab == "W2":
                data = data.replace(b'"OPEN"', b'"OPEM"', 1)
            elif lab == "W3":
                data = None
            elif lab == "W4":
                data = b"\n".join(data.split(b"\n")[:-2]) + b"\n"
            elif lab in ("W5a", "W5n"):
                data = (line({"count": 0, "head": ZERO}) + "\n").encode()
                if lab == "W5n":
                    anc = None
            load_res = r2.load_wal(data, anc)
            struct = r2.structural_state
            wal_after_load = len(r2.wal)
        out += [("%s.r1_call" % lab, first), ("%s.load" % lab, load_res),
                ("%s.structural" % lab, struct),
                ("%s.wal_len_after_load" % lab, wal_after_load),
                ("%s.refused" % lab, call(r2))]
        out += facts(lab, r2, ag, target)
    return out


def e113_counted(a):
    return E113.counted(a)


E113 = None


def main():
    global E113
    sk, p110, p111, p112, p113 = sys.argv[1:6]
    out = [("e114.skeleton_blob_sha1", blob_sha1(sk)),
           ("e114.e110_blob_sha1", blob_sha1(p110)),
           ("e114.e111_blob_sha1", blob_sha1(p111)),
           ("e114.e112_blob_sha1", blob_sha1(p112)),
           ("e114.e113_blob_sha1", blob_sha1(p113))]
    g = load(sk, "genesis_skeleton")
    e110 = load(p110, "e110_probe")
    e111 = load(p111, "e111_probe")
    e112 = load(p112, "e112_probe")
    E113 = load(p113, "e113_probe")
    h12 = e111.h12
    v6 = make_v6(g, e110, e111, e112)
    v5 = E113.make_v5(g, e110, e111, e112)
    res = {}
    for lab in ("ctlL", "L2", "L3a", "L3b", "L4", "L5",
                "L6", "L7", "L5b", "L3c"):
        for k, v in E113.row(g, e112, v6, lab, e110.EXTRA):
            out.append(("v6." + k, v))
            res["v6." + k] = v
    for name, cls in (("v6", v6), ("v5", v5)):
        for k, v in new_rows(g, e112, h12, cls, name, e110.EXTRA):
            out.append(("%s.%s" % (name, k), v))
            res["%s.%s" % (name, k)] = v
    T, F = True, False
    exp_reg = [
        ("ctlL.lobby_status", "OK"), ("ctlL.validate_bidirectional", T),
        ("ctlL.journal_len", 1),
        ("L2.lobby_status", "FAILED:RuntimeError"),
        ("L2.validate_bidirectional", F), ("L2.journal_len", 1),
        ("L3a.status_first", "UNCONFIRMED:RuntimeError"),
        ("L3a.lobby_status", "OK"), ("L3a.validate_bidirectional", T),
        ("L3a.journal_len", 2),
        ("L3b.status_first", "UNCONFIRMED:RuntimeError"),
        ("L3b.lobby_status", "UNCONFIRMED:RuntimeError"),
        ("L3b.refused_last", "RETRY_LIMIT"), ("L3b.journal_len", 3),
        ("L3b.validate_bidirectional", F),
        ("L4.lobby_status", "MISMATCH:silent:RESTORED"),
        ("L4.validate_bidirectional", F), ("L4.journal_len", 1),
        ("L5.status_first", "FAILED:RuntimeError"),
        ("L5.lobby_status", "CONFLICT:BASELINE"), ("L5.has_foreign", T),
        ("L5.validate_bidirectional", F), ("L5.journal_len", 2),
        ("L6.lobby_status", "CONFLICT:BASELINE"), ("L6.writes", 0),
        ("L6.has_planted", T), ("L6.validate_bidirectional", F),
        ("L6.journal_len", 1),
        ("L7.first_call", "raised:RuntimeError"),
        ("L7.lobby_status", "OK:RECOVERED"), ("L7.writes", 1),
        ("L7.wal_open", 0), ("L7.validate_bidirectional", T),
        ("L7.journal_len", 1),
        ("L5b.lobby_status", "CONFLICT:STICKY"), ("L5b.has_foreign", T),
        ("L5b.validate_bidirectional", F), ("L5b.journal_len", 3),
        ("L3c.lobby_status", "OK"), ("L3c.confirm", "CONFIRMED"),
        ("L3c.confirm_writes", 0), ("L3c.journal_len", 2),
        ("L3c.validate_bidirectional", T)]
    exp6 = exp_reg + [
        ("R1.lobby_status", "CONFLICT:RECEIVER"), ("R1.writes", 0),
        ("R1.wal_len", 0), ("R1.journal_len", 1),
        ("R1.words_eq_baseline", T), ("R1.identity", T),
        ("N1.status_first", "OK"), ("N1.lobby_status", "CONFLICT:REPLAY"),
        ("N1.writes", 1), ("N1.wal_len", 1), ("N1.journal_len", 2),
        ("N1.effect", T), ("N1.validate_bidirectional", F),
        ("N2.lobby_status", "CONFLICT:GRANT"), ("N2.grant", F),
        ("N2.writes", 1), ("N2.wal_len", 1), ("N2.journal_len", 2),
        ("W1.r1_call", "raised:RuntimeError"), ("W1.load", "OK"),
        ("W1.lobby_status", "OK:RECOVERED"), ("W1.writes", 1),
        ("W1.journal_len", 1), ("W1.wal_open", 0),
        ("W1.validate_bidirectional", T),
        ("W2.structural", "WAL_INTEGRITY"),
        ("W2.lobby_status", "CONFLICT:WAL_INTEGRITY"), ("W2.writes", 1),
        ("W2.journal_len", 1),
        ("W3.lobby_status", "CONFLICT:WAL_MISSING"), ("W3.writes", 1),
        ("W3.journal_len", 1),
        ("W4.structural", "WAL_INTEGRITY"),
        ("W4.lobby_status", "CONFLICT:WAL_INTEGRITY"), ("W4.writes", 1),
        ("W4.journal_len", 1),
        ("W5a.structural", "OK"),
        ("W5a.lobby_status", "CONFLICT:WAL_ANCHOR"), ("W5a.writes", 1),
        ("W5a.journal_len", 1),
        ("W5n.structural", "OK"),
        ("W5n.lobby_status", "CONFLICT:WAL_UNANCHORED"),
        ("W5n.writes", 1), ("W5n.journal_len", 1)]
    for lab in ("W1", "W2", "W3", "W4", "W5a", "W5n"):
        exp6.append(("%s.wal_len" % lab,
                     res.get("v6.%s.wal_len_after_load" % lab)))
    misses6 = [k for k, v in exp6 if res.get("v6." + k) != v]
    exp5 = [("R1.lobby_status", "CONFLICT:RECEIVER"), ("R1.writes", 0),
            ("R1.wal_len", 0), ("R1.journal_len", 1),
            ("N1.lobby_status", "OK"), ("N1.writes", 2),
            ("N1.journal_len", 2),
            ("N2.lobby_status", "OK"), ("N2.writes", 2),
            ("N2.journal_len", 2),
            ("W1.lobby_status", "OK"), ("W1.writes", 2),
            ("W1.journal_len", 1)]
    misses5 = [k for k, v in exp5 if res.get("v5." + k) != v]
    out.append(("e114.v6_misses", ",".join(misses6) or "-"))
    out.append(("e114.v5_misses", ",".join(misses5) or "-"))
    out.append(("e114.v6_outcome", "PASS" if not misses6 else "FAIL"))
    out.append(("e114.v5_baseline_as_predicted", not misses5))
    text = "".join("%s=%s\n" % kv for kv in out)
    sys.stdout.write(text)
    sys.stdout.write("sha256=%s\n" % hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
