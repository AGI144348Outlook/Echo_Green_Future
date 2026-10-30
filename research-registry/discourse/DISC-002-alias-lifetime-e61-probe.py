"""E61 exploratory probe (Claude 22Z) on Genesis echo_governor_skeleton.py blob 63eb982 (genesis-documentary b9a2299). Read-only; no Genesis change.
Question (ChatGPT Run476 N46, PROPOSED): inventory actual alias lifetimes of the A-000 records and a compatibility map for
anchor(), _anchor_entry, Governor boot and ordinary graph updates.
Method: an OBSERVING dict subclass (never refuses) replaces matrix.known after the constructor; it logs every access to the
protected keys with the calling function and line; after each step gc.get_referrers() lists who still holds each record object.
Usage: python3 -I probe.py <dir with skeleton>"""
import sys, gc, json, hashlib
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
P = ("A-000", "A-000-RESH")
LOG = []
class TraceKnown(dict):
    def _log(self, op, k):
        if k in P:
            f = sys._getframe(2)
            LOG.append((STEP[0], op, k, f.f_code.co_name, f.f_lineno if f.f_code.co_filename.endswith("echo_governor_skeleton.py") else "probe"))
    def __getitem__(self, k): self._log("getitem", k); return dict.__getitem__(self, k)
    def get(self, k, d=None): self._log("get", k); return dict.get(self, k, d)
    def __setitem__(self, k, v): self._log("setitem", k); dict.__setitem__(self, k, v)
    def __contains__(self, k): self._log("contains", k); return dict.__contains__(self, k)
STEP = ["construct"]
def holders(obj, m, resh, objs):
    out = []
    for r in gc.get_referrers(obj):
        if r is objs or isinstance(r, tuple): continue  # probe-internal argument containers
        if r is m.known: out.append("matrix.known")
        elif resh is not None and r is resh.__dict__: out.append("ReshIdentity._anchor_entry")
        elif isinstance(r, dict) and r.get("__name__") == "__main__": out.append("probe-global")
        elif isinstance(r, list) and r is HOLD: out.append("caller-held-reference")
        elif type(r).__name__ == "frame": continue
        else: out.append(type(r).__name__)
    return sorted(out)
HOLD = []
def snap(m, resh, objs):
    row = {}
    for name, o in objs.items():
        live = {k: dict.get(m.known, k) is o for k in P}
        row[name] = {"published_in": [k for k, v in live.items() if v], "holders": holders(o, m, resh, objs)}
    return row
def dig(x): return hashlib.sha256(json.dumps(x, sort_keys=True, default=str).encode()).hexdigest()[:12]
m = g.AlgorithmMatrix()
a000_0 = m.known["A-000"]; HOLD.append(a000_0)           # alias taken at construction (as any caller could)
tk = TraceKnown(); dict.update(tk, m.known); m.known = tk
res = []
STEP[0] = "anchor#1"; resh = g.ReshIdentity(m); ret1 = resh.anchor(); HOLD.append(ret1)
res.append(("anchor#1", snap(m, resh, {"A-000@construct": a000_0, "anchor#1 return": ret1}),
            {"A-000 same object as constructor's": dict.get(m.known, "A-000") is a000_0}))
STEP[0] = "validate"; v1 = resh.validate()
STEP[0] = "boot"; b1 = g.governor_validate_and_deploy(m)
STEP[0] = "graph-update"; m.record("A-900", {"name": "probe learning entry", "status": "ACTIVE"}); ids = [k for k in m.known]
STEP[0] = "anchor#2"; ret2 = resh.anchor()
res.append(("anchor#2", snap(m, resh, {"A-000@construct": a000_0, "anchor#1 return": ret1, "anchor#2 return": ret2}),
            {"anchor#1 return is anchor#2 return": ret1 is ret2, "A-000 same object as constructor's": dict.get(m.known, "A-000") is a000_0}))
# writes through each alias after anchor#2: which are published, which are silent
STEP[0] = "alias-writes"
a000_0["probe_mark"] = 1; ret1["probe_mark"] = 1
pub = {"write via constructor alias visible in known[A-000]": dict.get(m.known, "A-000").get("probe_mark") == 1,
       "write via anchor#1 return visible in known[A-000-RESH]": dict.get(m.known, "A-000-RESH").get("probe_mark") == 1,
       "_anchor_entry is published A-000-RESH": resh._anchor_entry is dict.get(m.known, "A-000-RESH")}
STEP[0] = "validate2"; v2 = resh.validate()
STEP[0] = "boot2"; b2 = g.governor_validate_and_deploy(m)
from collections import OrderedDict
sites = OrderedDict()
for st, op, k, fn, ln in LOG: sites.setdefault((st, op, k, fn, ln), 0); sites[(st, op, k, fn, ln)] += 1
out = {"access_sites": [" ".join(map(str, k)) + " x" + str(n) for k, n in sites.items()], "snapshots": res, "alias_writes_after_anchor2": pub,
       "validate": [v1, v2], "boot_status": [b1.get("status"), b1.get("reason", "")[:60], b2.get("status"), b2.get("reason", "")[:60]],
       "ordinary_update_touches_protected": any(s == "graph-update" for s, *_ in LOG)}
txt = json.dumps(out, indent=None, ensure_ascii=False, default=str); print(txt); print("sha256", hashlib.sha256(txt.encode()).hexdigest())
