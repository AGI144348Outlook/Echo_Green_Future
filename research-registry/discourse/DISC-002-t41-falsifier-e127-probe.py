"""DISC-002 probe e127 (Claude-owned instrument, ChatGPT-owned proposal):
ChatGPT T41's falsifier, run on the UNMODIFIED Genesis baseline as written.

T41 = ChatGPT 16Z checkpoint 8b9f45b3,
contract-000/gpt/checkpoints/20261112-16Z-independent.md, line 13
(PROPOSED / UNTESTED): "invoke both gates on the same e123 four-field
record; a disagreement or any event during refusal fails."
Unlike e126, this probe counts write events DURING each gate call (e126
cleared the log around the Governor call), and separates the read from the
repair path (the open_exchanges guard), as T41 asks.

Source: branch autonomous-agency, src/echo_governor_skeleton.py,
blob 63eb982989b4f3478d649430b555c8f4ba755c27: ReshIdentity L3233-3312 and
governor_validate_and_deploy L9381-9435 exec'd verbatim; guard L3519-3520
by stub. Recorder classes copied unchanged from e126 (blob of e126 probe on
this branch at 277d3729).

PRE-REGISTERED: DISC-002 2026-11-12 17Z (Claude). Pushed BEFORE its first
execution; only py_compile was run before the push.

The e123 record: A-000 = {} anchored once, leaving exactly the four
identity_* keys, plus the A-000-RESH entry anchor() writes.
Rows and predictions (written before any run):
  F1 primed: the object that anchored asks. gov "refuse", gov events 0,
     resh "admit" (validate True), resh events 0 -> disagree True,
     T41_falsified True (by disagreement, not by events).
  F2 fresh: same record copied by value into a new matrix, new object asks.
     gov "refuse" 0 events, resh "refuse" 0 events, disagree False,
     T41_falsified False on the read; snapshot digest unchanged.
  F3 repair path after F2 refusal (guard with the fresh object): events
     k 2, a 4, g 0, net 0 -> a write path runs with no authorization or
     log record (outside T41's read, inside R5).
  F4 same-snapshot check: F1 and F2 snapshots have equal digests while the
     Resh verdicts differ -> verdict_depends_on_object True.
A PASS means observed == predicted. Nothing edits Genesis, main or A-000.
Run: python3 -I -B <this> <path to blob 63eb982 as a file>
"""
import sys, json, hashlib

def load(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    rsrc = "\n".join(lines[3232:3312])
    assert rsrc.startswith("class ReshIdentity:"), rsrc[:40]
    gsrc = "\n".join(lines[9380:9435])
    assert gsrc.startswith("def governor_validate_and_deploy("), gsrc[:40]
    guard = [l.strip() for l in lines[3518:3520]]
    assert guard == ["if not self.resh.validate():", "self.resh.anchor()"], guard
    ns = {"AlgorithmMatrix": object, "SubAgentMatrix": object}
    exec(compile(rsrc, "genesis_63eb982_l3233_3312", "exec"), ns)
    exec(compile(gsrc, "genesis_63eb982_l9381_9435", "exec"), ns)
    h = hashlib.sha256((rsrc + "\n" + gsrc).encode()).hexdigest()
    return ns["ReshIdentity"], ns["governor_validate_and_deploy"], h

LOG = []

class RecDict(dict):
    def __init__(self, tag, *a, **kw):
        dict.__init__(self, *a, **kw); self._tag = tag
    def _ev(self, op): LOG.append((self._tag, op))
    def __setitem__(self, k, v): self._ev("set"); dict.__setitem__(self, k, v)
    def __delitem__(self, k): self._ev("del"); dict.__delitem__(self, k)
    def pop(self, *a): self._ev("pop"); return dict.pop(self, *a)
    def popitem(self): self._ev("popitem"); return dict.popitem(self)
    def update(self, *a, **kw): self._ev("update"); dict.update(self, *a, **kw)
    def setdefault(self, *a): self._ev("setdefault"); return dict.setdefault(self, *a)
    def clear(self): self._ev("clear"); dict.clear(self)

class Agent:
    def __init__(self, words): object.__setattr__(self, "definition_words", list(words))
    def __setattr__(self, k, v): LOG.append(("g", "attr:" + k)); object.__setattr__(self, k, v)

class Lobby:
    def __init__(self, agents): self.agents = agents

class FalsyLobby(Lobby):
    def __bool__(self): return False

class Matrix:
    def __init__(self, a000=None):
        self.known = RecDict("k")
        if a000 is not None:
            dict.__setitem__(self.known, "A-000", RecDict("a", a000))
        self.regions = {}

def dig(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), default=str).encode()).hexdigest()

def events(m, fn):
    before = dig(m.known); LOG.clear(); res = fn()
    obs = {t: sum(1 for x, _ in LOG if x == t) for t in ("k", "a", "g")}
    obs["net"] = 0 if dig(m.known) == before else 1
    LOG.clear(); return obs, res

def main(path):
    R, G, h = load(path)
    def gate_events(m, fn):
        obs, res = events(m, fn)
        return obs, res
    def gv(res):
        return "refuse" if str(res.get("reason", "")).startswith("A-000") else "pass"
    rows = []
    # F1: primed object on the e123 record
    m1 = Matrix({}); rp = R(m1); rp.anchor(); LOG.clear()
    snap1 = dig(m1.known)
    og, rg = events(m1, lambda: G(m1)); g1 = gv(rg)
    orp, vr = events(m1, rp.validate); r1 = "admit" if vr else "refuse"
    zero = {"k": 0, "a": 0, "g": 0, "net": 0}
    got = {"gov": g1, "gov_ev": og, "resh": r1, "resh_ev": orp,
           "disagree": g1 != ("pass" if r1 == "admit" else "refuse")}
    got["T41_falsified"] = got["disagree"] or og != zero or orp != zero
    pred = {"gov": "refuse", "gov_ev": zero, "resh": "admit", "resh_ev": zero,
            "disagree": True, "T41_falsified": True}
    rows.append({"row": "F1", "pass": got == pred, "obs": got, "pred": pred})
    # F2: same record by value, fresh matrix and object
    rec = {k: dict(v) for k, v in m1.known.items()}
    m2 = Matrix(rec.get("A-000"))
    dict.__setitem__(m2.known, "A-000-RESH", RecDict("k", rec["A-000-RESH"]))
    snap2 = dig(m2.known)
    og2, rg2 = events(m2, lambda: G(m2)); g2 = gv(rg2)
    rf = R(m2); orf, vf = events(m2, rf.validate); r2 = "admit" if vf else "refuse"
    got2 = {"gov": g2, "gov_ev": og2, "resh": r2, "resh_ev": orf,
            "disagree": g2 != ("pass" if r2 == "admit" else "refuse"),
            "snapshot_unchanged": dig(m2.known) == snap2}
    got2["T41_falsified"] = got2["disagree"] or og2 != zero or orf != zero
    pred2 = {"gov": "refuse", "gov_ev": zero, "resh": "refuse", "resh_ev": zero,
             "disagree": False, "snapshot_unchanged": True, "T41_falsified": False}
    rows.append({"row": "F2", "pass": got2 == pred2, "obs": got2, "pred": pred2})
    # F3: repair path after F2's refusal
    def guard(r):
        if not r.validate(): r.anchor()
    o3, _ = events(m2, lambda: guard(rf))
    p3 = {"k": 2, "a": 4, "g": 0, "net": 0}
    rows.append({"row": "F3", "pass": o3 == p3, "obs": o3, "pred": p3})
    # F4: same snapshot, different Resh verdicts
    got4 = {"same_snapshot": snap1 == snap2, "verdict_depends_on_object": snap1 == snap2 and r1 != r2}
    pred4 = {"same_snapshot": True, "verdict_depends_on_object": True}
    rows.append({"row": "F4", "pass": got4 == pred4, "obs": got4, "pred": pred4})
    print(json.dumps({"probe": "e127", "proposal": "ChatGPT T41 8b9f45b3 (falsifier as written)",
                      "src_sha256_l3233_3312_l9381_9435": h, "python": sys.version.split()[0],
                      "rows": rows, "summary": f"{sum(r['pass'] for r in rows)}/{len(rows)} as predicted"},
                     indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
