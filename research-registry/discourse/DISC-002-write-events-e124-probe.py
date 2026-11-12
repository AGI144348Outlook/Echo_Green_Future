"""DISC-002 probe e124 (event-level write witness for T38 / T39): how many
write EVENTS do the UNMODIFIED Genesis identity paths make, as opposed to the
net-change digest used in e123 and e125?

Source: branch autonomous-agency, src/echo_governor_skeleton.py,
blob 63eb982989b4f3478d649430b555c8f4ba755c27.
  - class ReshIdentity, lines 3233-3312, exec'd verbatim (anchor, validate).
  - governor_validate_and_deploy(), lines 9381-9435, exec'd verbatim.
  - the open_exchanges() guard, lines 3519-3520, applied by a stub (as e123).

PRE-REGISTERED: DISC-002 2026-11-12 15Z (Claude). Committed and pushed
BEFORE its first execution in the same run; only py_compile was run before
the push. Nothing is changed after seeing results.

Instrument: matrix.known and the seeded A-000 entry are dict subclasses that
log every mutating call (__setitem__, __delitem__, pop, popitem, update,
setdefault, clear), even when the value written equals the old value. A
stand-in resh agent logs every attribute assignment after construction.
Counters: k = events on matrix.known, a = events on the A-000 entry object
that was seeded (a dict created later by known.get("A-000", {}) is a plain
dict and is NOT instrumented: stated limit), g = events on the agent.
net = 1 if the JSON digest of matrix.known changed, else 0 (e125's measure).
Writes to the ReshIdentity object's own attributes are not counted.

Rows and predictions (written before any run):
  E1 anchor() on seeded {name, status ACTIVE}, no lobby.
     Predict k 2, a 4, g 0, net 1.
  E2 anchor() again on the E1 state, no lobby.
     Predict k 2, a 4, g 0, net 0   (the net digest misses 6 events).
  E3 anchor() on seeded state with stand-in lobby, agent resh with
     definition_words ["head", "beginning"].
     Predict k 2, a 4, g 1, net 1.
  E4 ReshIdentity.validate() on the E1 state.
     Predict k 0, a 0, g 0, net 0.
  E5 governor_validate_and_deploy on the E1 state (identity passes, stops at
     "tool belt empty"). Predict k 0, a 0, g 0, net 0.
  E6 governor_validate_and_deploy on the e123 T36c-a state (A-000 made by
     the guard, 4 identity_* keys): a REFUSAL.
     Predict k 0, a 0, g 0, net 0.
  E7 guard on an empty matrix (A-000 absent).
     Predict k 2, a 0 (uninstrumented plain dict), g 0, net 1.
  E8 guard on the E1 state (validate True, so no anchor()).
     Predict k 0, a 0, g 0, net 0.
A row PASS means observation == prediction. E5/E6/E8 PASS would mean those
paths made zero recorded write events in this harness; E2 PASS would mean a
net-change measure undercounts writes. Neither shows protection.

Nothing here edits Genesis, main, A-000 or any file.
Run: python3 -I -B <this> <path to blob 63eb982 as a file>
"""
import sys, json, hashlib

def load(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    rsrc = "\n".join(lines[3232:3312])            # l. 3233-3312
    assert rsrc.startswith("class ReshIdentity:"), rsrc[:40]
    gsrc = "\n".join(lines[9380:9435])            # l. 9381-9435
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
        dict.__init__(self, *a, **kw)
        self._tag = tag
    def _ev(self, op):
        LOG.append((self._tag, op))
    def __setitem__(self, k, v):
        self._ev("set"); dict.__setitem__(self, k, v)
    def __delitem__(self, k):
        self._ev("del"); dict.__delitem__(self, k)
    def pop(self, *a):
        self._ev("pop"); return dict.pop(self, *a)
    def popitem(self):
        self._ev("popitem"); return dict.popitem(self)
    def update(self, *a, **kw):
        self._ev("update"); dict.update(self, *a, **kw)
    def setdefault(self, *a):
        self._ev("setdefault"); return dict.setdefault(self, *a)
    def clear(self):
        self._ev("clear"); dict.clear(self)

class Agent:
    def __init__(self, words):
        object.__setattr__(self, "definition_words", list(words))
    def __setattr__(self, k, v):
        LOG.append(("g", "attr:" + k)); object.__setattr__(self, k, v)

class Lobby:
    def __init__(self, agents):
        self.agents = agents

class Matrix:
    def __init__(self, a000=None):
        self.known = RecDict("k")
        if a000 is not None:
            dict.__setitem__(self.known, "A-000", RecDict("a", a000))
        self.regions = {}

def dig(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), default=str).encode()).hexdigest()

def guard(r):
    if not r.validate():
        r.anchor()

def measure(name, m, fn, pred):
    before = dig(m.known)
    LOG.clear()
    res = fn()
    obs = {"k": sum(1 for t, _ in LOG if t == "k"),
           "a": sum(1 for t, _ in LOG if t == "a"),
           "g": sum(1 for t, _ in LOG if t == "g"),
           "net": 0 if dig(m.known) == before else 1}
    LOG.clear()
    extra = {}
    if isinstance(res, dict) and "reason" in res:
        extra["reason"] = res["reason"]
    if isinstance(res, bool):
        extra["returned"] = res
    ok = all(obs[x] == v for x, v in pred.items())
    return {"row": name, "pass": ok, "obs": obs, "pred": pred, **extra}

def main(path):
    R, G, h = load(path)
    GOV = {"name": "Governor", "status": "ACTIVE"}
    out = []
    m1 = Matrix(GOV); r1 = R(m1)
    out.append(measure("E1", m1, r1.anchor, {"k": 2, "a": 4, "g": 0, "net": 1}))
    out.append(measure("E2", m1, r1.anchor, {"k": 2, "a": 4, "g": 0, "net": 0}))
    m3 = Matrix(GOV)
    r3 = R(m3, Lobby({"resh": Agent(["head", "beginning"])}))
    out.append(measure("E3", m3, r3.anchor, {"k": 2, "a": 4, "g": 1, "net": 1}))
    out.append(measure("E4", m1, r1.validate, {"k": 0, "a": 0, "g": 0, "net": 0}))
    out.append(measure("E5", m1, lambda: G(m1), {"k": 0, "a": 0, "g": 0, "net": 0}))
    m6 = Matrix(); r6 = R(m6); guard(r6)
    out.append(measure("E6", m6, lambda: G(m6), {"k": 0, "a": 0, "g": 0, "net": 0}))
    m7 = Matrix(); r7 = R(m7)
    out.append(measure("E7", m7, lambda: guard(r7), {"k": 2, "a": 0, "g": 0, "net": 1}))
    out.append(measure("E8", m1, lambda: guard(r1), {"k": 0, "a": 0, "g": 0, "net": 0}))
    print(json.dumps({"probe": "e124", "falsifier": "T38/T39 zero-write-events instrument",
                      "src_sha256_l3233_3312_l9381_9435": h,
                      "python": sys.version.split()[0], "rows": out,
                      "summary": f"{sum(x['pass'] for x in out)}/{len(out)} as predicted"},
                     indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
