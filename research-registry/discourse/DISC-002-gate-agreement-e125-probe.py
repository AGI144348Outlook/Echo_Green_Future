"""DISC-002 probe e125 (falsifier T37a): do the two A-000 identity gates of
the UNMODIFIED Genesis source agree on the same state?

Source: branch autonomous-agency, src/echo_governor_skeleton.py,
blob 63eb982989b4f3478d649430b555c8f4ba755c27.
  - class ReshIdentity, lines 3233-3312, exec'd verbatim (gate R:
    ReshIdentity.validate(), L3297-3302).
  - governor_validate_and_deploy(), lines 9381-9435, exec'd verbatim
    (gate G). Only its IDENTIFY/VALIDATE steps are judged: a result whose
    reason starts with "A-000" is an identity refusal; any other result
    (here "tool belt empty", because the stand-in matrix has no A-101 and
    no regions) means the identity steps PASSED. Deploy is never reached.
  - the open_exchanges() guard, lines 3519-3520, applied by a stub that
    stops there (as in e123), to build the T36c states.

PRE-REGISTERED: DISC-002 2026-11-12 14Z (Claude). This file is committed
and pushed BEFORE its first execution in the same run. Only py_compile was
run before the push. Nothing is changed after seeing results.

Rows and predictions (written before any run). R = gate R accepts,
G = gate G identity steps pass, gw = net changes to matrix.known made by
calling gate G (digest compare), agree = (R == G):
  C1 control: A-000 {name, status ACTIVE}, anchor()ed.
     Predict R True, G True, agree True, gw 0.
  A1 (e123 T36c-a state): no A-000, guard calls anchor() -> A-000 has only
     the 4 identity_* keys. Predict R True, G False, agree False, gw 0.
  A2 (e123 T36c-b state): A-000 anchored, deleted by a third party, guard
     re-creates it. Predict R True, G False, agree False, gw 0.
  A3: A-000 absent, guard NOT applied, never anchored by R.
     Predict R False, G False, agree True, gw 0.
  A4: A-000 {name, status "INACTIVE"}, anchor()ed.
     Predict R True, G False, agree False, gw 0.
T37a's target for a candidate (not this baseline) is agree True on every
row, with both gates refusing A1, A2, A3, A4 and zero write events.
A row PASS below means the observation equals the PREDICTION (the
baseline disagreement is real); it never shows protection.

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
    ns = {}
    exec(compile(rsrc, "genesis_63eb982_l3233_3312", "exec"), ns)
    exec(compile(gsrc, "genesis_63eb982_l9381_9435", "exec"), ns)
    h = hashlib.sha256((rsrc + "\n" + gsrc).encode()).hexdigest()
    return ns["ReshIdentity"], ns["governor_validate_and_deploy"], h

class Matrix:
    def __init__(self, a000=None):
        self.known = {} if a000 is None else {"A-000": dict(a000)}
        self.regions = {}

def dig(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":")).encode()).hexdigest()

def guard(r):
    if not r.validate():
        r.anchor()

def run_row(name, m, r, G, pred):
    R_ok = r.validate()
    before = dig(m.known)
    res = G(m)
    gw = 0 if dig(m.known) == before else 1
    G_ok = not str(res.get("reason", "")).startswith("A-000")
    obs = {"R": R_ok, "G": G_ok, "agree": R_ok == G_ok, "gw": gw,
           "g_reason": res.get("reason"),
           "a000_keys": sorted(m.known.get("A-000", {}).keys())}
    ok = all(obs[k] == v for k, v in pred.items())
    return {"row": name, "pass": ok, "obs": obs, "pred": pred}

def main(path):
    R, G, h = load(path)
    GOV = {"name": "Governor", "status": "ACTIVE"}
    out = []
    m = Matrix(GOV); r = R(m); r.anchor()
    out.append(run_row("C1", m, r, G, {"R": True, "G": True, "agree": True, "gw": 0}))
    m = Matrix(); r = R(m); guard(r)
    out.append(run_row("A1", m, r, G, {"R": True, "G": False, "agree": False, "gw": 0}))
    m = Matrix(GOV); r = R(m); r.anchor(); del m.known["A-000"]; guard(r)
    out.append(run_row("A2", m, r, G, {"R": True, "G": False, "agree": False, "gw": 0}))
    m = Matrix(); r = R(m)
    out.append(run_row("A3", m, r, G, {"R": False, "G": False, "agree": True, "gw": 0}))
    m = Matrix({"name": "Governor", "status": "INACTIVE"}); r = R(m); r.anchor()
    out.append(run_row("A4", m, r, G, {"R": True, "G": False, "agree": False, "gw": 0}))
    print(json.dumps({"probe": "e125", "falsifier": "T37a",
                      "src_sha256_l3233_3312_l9381_9435": h,
                      "python": sys.version.split()[0], "rows": out,
                      "summary": f"{sum(x['pass'] for x in out)}/{len(out)} as predicted"},
                     indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
