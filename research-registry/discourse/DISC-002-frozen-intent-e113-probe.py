"""DISC-002 E113 probe: FROZEN-INTENT candidate v5 versus v4 on pre-stage
contamination (L6), crash after receiver write before journal (L7), third
call after CONFLICT (L5b) and read-only confirm() after a raised write (L3c).

PRE-REGISTERED 2026-11-07 20Z by Claude. Committed BEFORE any execution;
first executed only after this blob is pushed and named in a prospective
Issue #13 comment.
Cases and predictions were first written in DISC-002 19Z (Claude, blob
04b5da03, (nnnnn)). This file adds ChatGPT's 20Z refinements (commit
b54a8736, contract-000/gpt/DISC-002-ChatGPT-20261107-20z.md on GPT branch
contract-000-gpt-multiring-20261104):
  - the first-call baseline here is a TECHNICAL FIXTURE, NOT AN AUTHORITY:
    the receiver's construction words in this probe, issuer
    "UNAUTHENTICATED-FIXTURE". Nothing here proves who authorized it.
  - L7 uses a write-ahead intent record (self.wal) written BEFORE the
    receiver write; it is still in memory, so it proves nothing about
    completeness after a real restart.
  - L3c confirm() compares an immutable target and the receiver id, with
    no open CONFLICT and no mutation (write counter must stay unchanged).

PROPOSED candidate v5 for the R5 race contract, in memory only. It does NOT
edit Genesis, main or any file. Inputs, all loaded unmodified:
  argv[1] genesis-documentary:src/echo_governor_skeleton.py, blob 63eb982
  argv[2] .../DISC-002-lobby-boundary-e110-probe.py, blob f20eaf82
  argv[3] .../DISC-002-partial-receiver-retry-e111-probe.py, blob 97ca407a
  argv[4] .../DISC-002-readback-concurrency-e112-probe.py, blob 1742ab93
Run: python3 -I -B <this> <skeleton> <e110> <e111> <e112>

Candidate v5 = v4 matrix step unchanged; lobby step replaced:
  intent = {receiver_id, baseline_words, add_words=EXTRA, issuer, nonce},
  target = sorted(set(baseline + add)), intent_hash = h12(intent).
  Order of checks, after the matrix commit:
   (i)  intent.receiver_id != recv_id         -> CONFLICT:RECEIVER, no write
   (s)  any CONFLICT* record for this key     -> CONFLICT:STICKY, no write
   (c)  an OPEN wal entry for this key and live == target
                                              -> OK:RECOVERED, no write
   (b)  live != baseline and live != target   -> CONFLICT:BASELINE, no write
   (w)  wal OPEN; write target; readback classified exactly as v4
        (OK / UNCONFIRMED / FAILED / MISMATCH:..:RESTORED / PARTIAL);
        journal record; wal CLOSED.
  Retry bound: 3 records for a key whose status does not start with "OK"
  -> REFUSED:RETRY_LIMIT, nothing written.
  confirm(): read-only. Promotes the last UNCONFIRMED:* to OK (record
  status OK:CONFIRMED) only when live == target, receiver id matches and
  no CONFLICT* record exists; else returns the reason and changes nothing.
  validate_bidirectional() = validate() and lobby_status in
  {OK, OK:RECOVERED} and live == target.
  SEMANTIC CHANGE (ooooo): v5 replaces from intent instead of merging the
  live receiver. That is a design decision for Timothy, not a fix.

Rows: v5 on ctlL L2 L3a L3b L4 L5 (E112 regression) and L6 L7 L5b L3c;
      v4 on L6 L7 L5b (baseline for the new cases).
  L6  a word "planted" is added to the receiver BEFORE the first call; 1 call
  L7  plain receiver; the first journal write (_rec) raises once, after the
      receiver write; 2 calls
  L5b as L5 (first write raises, foreign word added before call 2); 3 calls
  L3c as L3a (writes, then raises once); 1 call, then confirm()

Predictions (INFERRED from the v4 source in E112 and the v5 rules above):
  v5: ctlL OK vb True j1. L2 FAILED:RuntimeError vb False j1.
      L3a first UNCONFIRMED:RuntimeError, last OK, vb True, j2.
      L3b first UNCONFIRMED:RuntimeError, last UNCONFIRMED:RuntimeError,
          refused_last RETRY_LIMIT, j3, vb False.
      L4 MISMATCH:silent:RESTORED, vb False, j1.
      L5 first FAILED:RuntimeError, last CONFLICT:BASELINE, has_foreign
          True, vb False, j2.
      L6 CONFLICT:BASELINE, writes 0, has_planted True, vb False, j1.
      L7 first-call raised:RuntimeError; last OK:RECOVERED; writes 1;
          wal_open 0; vb True; j1.
      L5b last CONFLICT:STICKY, has_foreign True, vb False, j3.
      L3c after confirm: lobby OK, confirm_writes 0, j2, vb True.
  v4: L6 OK, has_planted True, vb True (the 19Z hazard).
      L7 last OK, writes 2, j1 (first write unrecorded).
      L5b last OK, has_foreign True, vb True (foreign word adopted).
e113.v5_outcome = PASS only if every v5 prediction holds.
e113.v4_baseline_as_predicted = whether the three v4 lines hold (recorded,
does not gate). No randomness; no network; no file writes.
"""
import copy
import hashlib
import importlib.util
import sys


def blob_sha1(path):
    data = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BASELINE = sorted(["head", "beginning"])   # FIXTURE, NOT AUTHORITY


def make_v5(g, e110, e111, e112):
    V4 = e112.make_v4(g, e110, e111)
    EXTRA = e110.EXTRA
    h12, version = e111.h12, e111.version

    class CandidateResh5(V4):
        def __init__(self, *a, **k):
            V4.__init__(self, *a, **k)
            self.wal = []
            self.intent = {"receiver_id": "resh:Agent4",
                           "baseline_words": list(BASELINE),
                           "add_words": sorted(EXTRA),
                           "issuer": "UNAUTHENTICATED-FIXTURE",
                           "nonce": "e113-fixed"}
            self.target = sorted(set(BASELINE + list(EXTRA)))
            self.intent_hash = h12(self.intent)

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

            def norec(st):
                self.lobby_status = st
                self._rec(key, "none", before, before, st, target)
                return new_resh
            if self.intent["receiver_id"] != recv_id:
                return norec("CONFLICT:RECEIVER")
            if any(j["status"].startswith("CONFLICT") for j in mine):
                return norec("CONFLICT:STICKY")
            open_w = [w for w in self.wal
                      if w["key"] == key and w["state"] == "OPEN"]
            if open_w and live == target:
                norec("OK:RECOVERED")
                for w in open_w:
                    w["state"] = "CLOSED"
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
    return CandidateResh5


BASE_MODE = {"L6": "ctlL", "L7": "ctlL", "L5b": "L5", "L3c": "L3a"}
CALLS = {"ctlL": 1, "L2": 1, "L3a": 2, "L3b": 4, "L4": 1, "L5": 2,
         "L6": 1, "L7": 2, "L5b": 3, "L3c": 1}


def counted(a):
    base = type(a)

    class Counted(base):
        def __setattr__(self, k, v):
            if k == "definition_words":
                self.__dict__["_writes"] = self.__dict__.get("_writes", 0) + 1
            base.__setattr__(self, k, v)
    a.__class__ = Counted
    Counted.__name__ = base.__name__
    a.__dict__["_writes"] = 0
    return a


def row(g, e112, cls, label, extra):
    class R(cls):
        def _rec(self, *a):
            if self.__dict__.pop("_crash", False):
                raise RuntimeError("crash before journal")
            return cls._rec(self, *a)
    m = g.AlgorithmMatrix()
    lob = g.Lobby(m)
    ag = counted(e112.make_agent(g, m, BASE_MODE.get(label, label)))
    lob.agents["resh"] = ag
    target = sorted(set(BASELINE + list(extra)))
    r = R(m, lob)
    if label == "L6":
        object.__setattr__(ag, "definition_words",
                           sorted(ag.definition_words) + ["planted"])
    if label == "L7":
        r.__dict__["_crash"] = True
    first, last_refused, first_out = None, "-", "-"
    for i in range(CALLS[label]):
        if label in ("L5", "L5b") and i == 1:
            object.__setattr__(ag, "definition_words",
                               sorted(ag.definition_words) + ["foreign"])
        last_refused = "-"
        try:
            out = r.anchor()
            if isinstance(out, dict) and out.get("status") == "REFUSED":
                last_refused = out["reason"]
        except Exception as e:
            last_refused = "raised:" + type(e).__name__
        if i == 0:
            first = getattr(r, "lobby_status", "n/a")
            first_out = last_refused
    writes_before_confirm = ag.__dict__["_writes"]
    conf = "-"
    if label == "L3c" and hasattr(r, "confirm"):
        conf = r.confirm()
    words = sorted(ag.definition_words)
    j = r.journal
    jtxt = ";".join("%d|%s|%s|%s>%s|%s" % (
        x["attempt"], x["key"], x["failure"], x["recv_before"],
        x["recv_after"], x["status"]) for x in j)
    wal = getattr(r, "wal", None)
    return [("%s.status_first" % label, first),
            ("%s.first_call" % label, first_out),
            ("%s.lobby_status" % label, r.lobby_status),
            ("%s.refused_last" % label, last_refused),
            ("%s.confirm" % label, conf),
            ("%s.confirm_writes" % label,
             ag.__dict__["_writes"] - writes_before_confirm),
            ("%s.writes" % label, ag.__dict__["_writes"]),
            ("%s.words_eq_target" % label, words == target),
            ("%s.has_foreign" % label, "foreign" in words),
            ("%s.has_planted" % label, "planted" in words),
            ("%s.validate" % label, r.validate()),
            ("%s.validate_bidirectional" % label,
             r.validate_bidirectional()),
            ("%s.journal_len" % label, len(j)),
            ("%s.wal_open" % label,
             "n/a" if wal is None else
             len([w for w in wal if w["state"] == "OPEN"])),
            ("%s.journal" % label, jtxt)]


def main():
    sk, p110, p111, p112 = sys.argv[1:5]
    out = [("e113.skeleton_blob_sha1", blob_sha1(sk)),
           ("e113.e110_blob_sha1", blob_sha1(p110)),
           ("e113.e111_blob_sha1", blob_sha1(p111)),
           ("e113.e112_blob_sha1", blob_sha1(p112))]
    g = load(sk, "genesis_skeleton")
    e110 = load(p110, "e110_probe")
    e111 = load(p111, "e111_probe")
    e112 = load(p112, "e112_probe")
    res = {}
    plan = (("v5", make_v5(g, e110, e111, e112),
             ("ctlL", "L2", "L3a", "L3b", "L4", "L5",
              "L6", "L7", "L5b", "L3c")),
            ("v4", e112.make_v4(g, e110, e111), ("L6", "L7", "L5b")))
    for name, cls, labs in plan:
        for lab in labs:
            for k, v in row(g, e112, cls, lab, e110.EXTRA):
                key = "%s.%s" % (name, k)
                out.append((key, v))
                res[key] = v
    c = lambda k: res["v5." + k]
    T, F = True, False
    exp5 = [
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
    misses5 = [k for k, v in exp5 if c(k) != v]
    b = lambda k: res["v4." + k]
    exp4 = [("L6.lobby_status", "OK"), ("L6.has_planted", T),
            ("L6.validate_bidirectional", T),
            ("L7.lobby_status", "OK"), ("L7.writes", 2),
            ("L7.journal_len", 1),
            ("L5b.lobby_status", "OK"), ("L5b.has_foreign", T),
            ("L5b.validate_bidirectional", T)]
    misses4 = [k for k, v in exp4 if b(k) != v]
    out.append(("e113.v5_misses", ",".join(misses5) or "-"))
    out.append(("e113.v4_misses", ",".join(misses4) or "-"))
    out.append(("e113.v5_outcome", "PASS" if not misses5 else "FAIL"))
    out.append(("e113.v4_baseline_as_predicted", not misses4))
    text = "".join("%s=%s\n" % kv for kv in out)
    sys.stdout.write(text)
    sys.stdout.write("sha256=%s\n" % hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
