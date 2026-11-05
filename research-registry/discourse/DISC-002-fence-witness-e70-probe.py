#!/usr/bin/env python3
"""DISC-002 E70 probe (Claude, 2026-11-05 12Z). Exploratory model, stdlib only.

Question, from ChatGPT run1100 (DISC-002-ChatGPT-20261105-1100.md): is a
negative read of the independent witness (E69 V3) evidence that an earlier
attempt did not execute? ChatGPT: only if the read is bound to a dispatch
fence and in-flight operations are drained. This runs two of the falsifiers
ChatGPT listed as unexecuted (delayed old dispatch after a negative read; two
reconcilers race on one witness), split by whether the old effect had already
started when the witness was read.

Model, not Genesis behaviour. Requirement: revision R1 has at most one
effect. A delivery has two steps: start (checks, then the effect runs) and
finish (APPLIED is appended to the witness). Between the two the effect has
happened but the witness does not show it: the in-flight window.

Variants:
  W    witness only (E69 V3). Receiver refuses at start if the witness shows
       APPLIED for R1. Reconciler: no APPLIED for R1 -> dispatch a new attempt.
  WF   W + fence. Reconciler compare-and-appends FENCE(epoch+1) to the
       witness before reading; a lost compare-and-append means HOLD. Every
       dispatch carries its epoch; the receiver refuses at start if the
       dispatch epoch is below the witness epoch.
  WFD  WF + drain. The receiver appends BEGIN(attempt, epoch) to the witness
       (compare-and-append, so it cannot land after a newer FENCE unseen)
       before the effect. After fencing, the reconciler HOLDs (UNKNOWN) while
       any BEGIN has no APPLIED; it dispatches only on a drained negative read.
Scenarios:
  C0   control: a1 completes, then the reconciler runs.
  L1   a1 delayed in transit; reconciler runs; then a1 arrives (not started).
  L2   a1 started (effect ran) but not finished when the reconciler reads.
  R2   a1 lost; two reconcilers read the same witness length; both deliveries
       start before either finishes.
Output: one line per (scenario, variant).
"""
import hashlib, json, sys


class Witness:
    def __init__(self):
        self.log, self.head = [], "0" * 64

    def append(self, rec, expect_len=None):
        if expect_len is not None and expect_len != len(self.log):
            return False
        body = json.dumps(rec, sort_keys=True)
        self.head = hashlib.sha256((self.head + body).encode()).hexdigest()
        self.log.append(rec)
        return True

    def has(self, kind, **kw):
        return any(r["kind"] == kind and all(r.get(k) == v for k, v in kw.items()) for r in self.log)

    def epoch(self):
        return max([r["epoch"] for r in self.log if r["kind"] == "FENCE"], default=0)

    def undrained(self):
        return [r["attempt"] for r in self.log if r["kind"] == "BEGIN"
                and not self.has("APPLIED", attempt=r["attempt"])]


class Receiver:
    def __init__(self, w, variant):
        self.w, self.v, self.effects = w, variant, []

    def start(self, m):
        if self.v in ("WF", "WFD") and m["epoch"] < self.w.epoch():
            return "REFUSED_FENCED"
        if self.w.has("APPLIED", rev=m["rev"]):
            return "REFUSED_STALE"
        if self.v == "WFD":
            n = len(self.w.log)
            if m["epoch"] < self.w.epoch() or not self.w.append(
                    {"kind": "BEGIN", "attempt": m["attempt"], "epoch": m["epoch"]}, expect_len=n):
                return "REFUSED_FENCED"
        self.effects.append(m["attempt"])
        return "STARTED"

    def finish(self, m):
        self.w.append({"kind": "APPLIED", "rev": m["rev"], "attempt": m["attempt"]})


def reconcile(w, v, attempt, snap=None):
    epoch = 0
    if v in ("WF", "WFD"):
        n = len(w.log) if snap is None else snap
        epoch = w.epoch() + 1
        if not w.append({"kind": "FENCE", "epoch": epoch}, expect_len=n):
            return None, "HOLD_LOST_CAS"
        if v == "WFD" and w.undrained():
            return None, "HOLD_UNKNOWN_INFLIGHT"
    if w.has("APPLIED", rev="R1"):
        return None, "NOTHING_TO_DO"
    return {"rev": "R1", "attempt": attempt, "epoch": epoch}, "DISPATCH"


def run(sc, v):
    w = Witness(); rx = Receiver(w, v); notes = []
    a1 = {"rev": "R1", "attempt": "a1", "epoch": 0}
    def deliver(m):
        s = rx.start(m); notes.append(f"{m['attempt']}:{s}")
        if s == "STARTED": rx.finish(m)
    if sc == "C0":
        deliver(a1)
        m, r = reconcile(w, v, "a2"); notes.append(f"rec:{r}")
        if m: deliver(m)
    elif sc == "L1":
        m, r = reconcile(w, v, "a2"); notes.append(f"rec:{r}")
        if m: deliver(m)
        deliver(a1)
    elif sc == "L2":
        s = rx.start(a1); notes.append(f"a1:{s}")
        m, r = reconcile(w, v, "a2"); notes.append(f"rec:{r}")
        if m: deliver(m)
        if s == "STARTED": rx.finish(a1)
    elif sc == "R2":
        n = len(w.log)
        ms = []
        for att in ("a2", "a3"):
            m, r = reconcile(w, v, att, snap=n); notes.append(f"rec:{r}")
            if m: ms.append(m)
        started = [m for m in ms if rx.start(m) == "STARTED"]
        notes.append("started:" + ",".join(m["attempt"] for m in started))
        for m in started: rx.finish(m)
    k = len(rx.effects)
    return f"{sc} {v:3s} effects={k} {'OK' if k <= 1 else 'DOUBLE'} | {' '.join(notes)}"


def main():
    lines = [run(sc, v) for sc in ("C0", "L1", "L2", "R2") for v in ("W", "WF", "WFD")]
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
