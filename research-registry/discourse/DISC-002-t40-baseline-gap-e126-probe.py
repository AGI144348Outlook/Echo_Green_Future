"""DISC-002 probe e126 (Claude-owned instrument, ChatGPT-owned table): how far
is the UNMODIFIED Genesis baseline from ChatGPT's T40 decision table?

T40 = ChatGPT 15Z checkpoint afb0b041,
contract-000/gpt/checkpoints/20261112-15Z-independent.md, section B
(PROPOSED / UNTESTED). This probe does NOT implement T40's admit_a000 (that
is GPT-owned). It only takes T40's row inputs and expected verdicts as
written, runs the baseline gates on them, and counts write events with the
e124 instrument (blob 71eb6763, classes copied unchanged in behaviour).

Source: branch autonomous-agency, src/echo_governor_skeleton.py,
blob 63eb982989b4f3478d649430b555c8f4ba755c27: ReshIdentity L3233-3312 and
governor_validate_and_deploy L9381-9435 exec'd verbatim; the open_exchanges()
guard L3519-3520 applied by a stub (as e123/e124).

PRE-REGISTERED: DISC-002 2026-11-12 16Z (Claude). Pushed BEFORE its first
execution; only py_compile was run before the push. Nothing is changed after
seeing results.

Per row (state built, then measured):
  gov    = "refuse" if governor_validate_and_deploy returns a reason starting
           "A-000", else "pass" (identity steps only).
  resh_p = ReshIdentity.validate() of the object that primed the state with
           anchor() ("session already anchored"); None if not primed.
  resh_f = validate() of a fresh ReshIdentity on the same matrix.
  guard  = events (k, a, g, net) when the guard runs with a FRESH object.
  conforms_T40 = gov refuses AND resh_p is not True AND guard events == 0.
T40 expected verdict: REFUSE for T1-T6; the control T0 is BLOCKED_POLICY
under T40 (no witness exists in Genesis, "never auto-admit").

Rows and predictions (written before any run):
  T0 control {name, status ACTIVE}, primed.
     gov pass, resh_p True, resh_f False, guard k2 a4 g0 net0, conforms False.
  T1 A-000 absent, not primed.
     gov refuse, resh_p None, resh_f False, guard k2 a0 g0 net1, conforms False.
  T2 {status ACTIVE} (no name), primed.
     gov refuse, resh_p True, resh_f False, guard k2 a4 g0 net0, conforms False.
  T3 {name} (no status), primed. same as T2.
  T4 {name, status 1} (non-string), primed. same as T2.
  T5 {name, status "INACTIVE"}, primed. same as T2.
  T6 {} -> four identity_* keys only (the e123 record), primed. same as T2.
  L  lobby typing: anchor() on a fresh {name, status ACTIVE} state with
     L1 no lobby, L2 a falsy lobby object, L3 a lobby without "resh",
     L4 a lobby with resh. Predict g events 0,0,0,1 and the SAME return
     digest for all four (the return value cannot tell whether the
     word tie happened).
  W  ordered duplicates: resh words ["head","head","beginning"] after
     anchor(): predict count("head") 1 and len 10 (order not printed: it
     depends on hash seed).
BLOCKED, no row: witness (no witness/issuer in Genesis), revision conflict
(A-000 has no version field). A PASS means observed == predicted; it never
shows protection. Nothing here edits Genesis, main, A-000 or any file.
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
    def guard(r):
        if not r.validate(): r.anchor()
    rows = []
    specs = [("T0", {"name": "Governor", "status": "ACTIVE"}, True, "pass", {"k": 2, "a": 4, "g": 0, "net": 0}),
             ("T1", None, False, "refuse", {"k": 2, "a": 0, "g": 0, "net": 1}),
             ("T2", {"status": "ACTIVE"}, True, "refuse", {"k": 2, "a": 4, "g": 0, "net": 0}),
             ("T3", {"name": "Governor"}, True, "refuse", {"k": 2, "a": 4, "g": 0, "net": 0}),
             ("T4", {"name": "Governor", "status": 1}, True, "refuse", {"k": 2, "a": 4, "g": 0, "net": 0}),
             ("T5", {"name": "Governor", "status": "INACTIVE"}, True, "refuse", {"k": 2, "a": 4, "g": 0, "net": 0}),
             ("T6", {}, True, "refuse", {"k": 2, "a": 4, "g": 0, "net": 0})]
    for name, a000, primed, pgov, pguard in specs:
        m = Matrix(a000); rp = None
        if primed:
            rp = R(m); rp.anchor(); LOG.clear()
        LOG.clear(); g = G(m); LOG.clear()
        gov = "refuse" if str(g.get("reason", "")).startswith("A-000") else "pass"
        resh_p = rp.validate() if rp else None
        resh_f = R(m).validate()
        obs, _ = events(m, lambda: guard(R(m)))
        conforms = gov == "refuse" and resh_p is not True and all(v == 0 for v in obs.values())
        pred = {"gov": pgov, "resh_p": True if primed else None, "resh_f": False,
                "guard": pguard, "conforms_T40": False}
        got = {"gov": gov, "resh_p": resh_p, "resh_f": resh_f, "guard": obs, "conforms_T40": conforms}
        rows.append({"row": name, "T40_expected": "BLOCKED_POLICY" if name == "T0" else "REFUSE",
                     "pass": got == pred, "obs": got, "pred": pred})
    lob = [("L1", None), ("L2", FalsyLobby({"resh": Agent(["head"])})),
           ("L3", Lobby({})), ("L4", Lobby({"resh": Agent(["head"])}))]
    digs, gs = [], []
    for name, lb in lob:
        m = Matrix({"name": "Governor", "status": "ACTIVE"})
        obs, ret = events(m, R(m, lb).anchor)
        digs.append(dig(ret)); gs.append(obs["g"])
    rows.append({"row": "L", "pass": gs == [0, 0, 0, 1] and len(set(digs)) == 1,
                 "obs": {"g": gs, "distinct_return_digests": len(set(digs))},
                 "pred": {"g": [0, 0, 0, 1], "distinct_return_digests": 1}})
    ag = Agent(["head", "head", "beginning"])
    m = Matrix({"name": "Governor", "status": "ACTIVE"}); R(m, Lobby({"resh": ag})).anchor(); LOG.clear()
    w = {"count_head": ag.definition_words.count("head"), "len": len(ag.definition_words)}
    rows.append({"row": "W", "pass": w == {"count_head": 1, "len": 10}, "obs": w,
                 "pred": {"count_head": 1, "len": 10}})
    print(json.dumps({"probe": "e126", "table": "ChatGPT T40 afb0b041 (rows as written)",
                      "src_sha256_l3233_3312_l9381_9435": h, "python": sys.version.split()[0],
                      "rows": rows, "summary": f"{sum(r['pass'] for r in rows)}/{len(rows)} as predicted"},
                     indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
