"""DISC-002 probe e123 (falsifier T36c): can the open_exchanges() guard
CREATE A-000 when it is absent, on the UNMODIFIED Genesis source?

Source: branch autonomous-agency, src/echo_governor_skeleton.py,
blob 63eb982989b4f3478d649430b555c8f4ba755c27.
  - class ReshIdentity, lines 3233-3312, exec'd verbatim.
  - the guard of PeExchange.open_exchanges(), lines 3519-3520, checked
    verbatim (asserted text) and applied by a stub that stops there.

PRE-REGISTERED: DISC-002 2026-11-12 12Z (Claude). This file is committed
and pushed BEFORE its first execution in the same run. Only py_compile was
run before the push. Nothing is changed after seeing results.

Rows and predictions (written before any run):
  C1 control: A-000 present, anchor()ed, intact. Guard sees validate()
     True and does not call anchor(). Predict: anchor_called False,
     known digest unchanged.
  T36c-a: matrix has NO A-000, fresh ReshIdentity. Guard sees validate()
     False and calls anchor(). Predict: anchor_called True, A-000 created,
     its keys are exactly the 4 identity_* fields, validate() True after,
     writes > 0, refused False.
  T36c-b: A-000 present ({name, status}), anchor()ed, then A-000 deleted
     by a third party. Predict: validate() False before guard; guard calls
     anchor(); A-000 re-created with only the 4 identity_* fields (name and
     status absent); validate() True after; refused False.
The target behaviour for R5 is "refused True, zero writes" in T36c-a/b.
A row PASS below means the observation equals the PREDICTION (i.e. the
baseline vulnerability is real); it never shows protection.

Nothing here edits Genesis, main, A-000 or any file.
Run: python3 -I -B <this> <path to blob 63eb982 as a file>
"""
import sys, json, hashlib

IDENT = ["identity_glyph", "identity_letter", "identity_meaning", "identity_symbol"]

def load(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    src = "\n".join(lines[3232:3312])            # l. 3233-3312, 1-based
    assert src.startswith("class ReshIdentity:"), src[:40]
    guard = [l.strip() for l in lines[3518:3520]]  # l. 3519-3520
    assert guard == ["if not self.resh.validate():", "self.resh.anchor()"], guard
    ns = {}
    exec(compile(src, "genesis_63eb982_l3233_3312", "exec"), ns)
    return ns["ReshIdentity"], hashlib.sha256(src.encode()).hexdigest()

class Matrix:
    def __init__(self, with_a000=True):
        self.known = {"A-000": {"name": "Governor", "status": "ACTIVE"}} if with_a000 else {}

def dig(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":")).encode()).hexdigest()

class PeGuardStub:
    """Applies exactly the two guard lines L3519-3520; stops before Ayin."""
    def __init__(self, resh): self.resh = resh; self.anchor_called = False
    def open_exchanges_guard(self):
        if not self.resh.validate():
            self.anchor_called = True
            self.resh.anchor()

def changed_keys(a, b):
    ks = set(a) | set(b)
    return sorted(k for k in ks if dig(a.get(k)) != dig(b.get(k)))

def run_row(name, m, r, pred):
    before = json.loads(json.dumps(m.known))
    v0 = r.validate()
    g = PeGuardStub(r); g.open_exchanges_guard()
    after = m.known
    obs = {"validate_before": v0, "anchor_called": g.anchor_called,
           "a000_present": "A-000" in after,
           "a000_keys": sorted(after.get("A-000", {}).keys()),
           "validate_after": r.validate(),
           "writes": len(changed_keys(before, after)),
           "refused": False}   # the baseline has no refusal path
    ok = all(obs[k] == v for k, v in pred.items())
    return {"row": name, "pass": ok, "obs": obs, "pred": pred,
            "known_before": dig(before), "known_after": dig(after)}

def main(path):
    R, src_sha = load(path)
    out = []
    m = Matrix(); r = R(m); r.anchor()
    out.append(run_row("C1", m, r, {"validate_before": True, "anchor_called": False, "writes": 0}))
    m = Matrix(with_a000=False); r = R(m)
    out.append(run_row("T36c-a", m, r, {"validate_before": False, "anchor_called": True,
        "a000_present": True, "a000_keys": IDENT, "validate_after": True, "refused": False}))
    m = Matrix(); r = R(m); r.anchor(); del m.known["A-000"]
    out.append(run_row("T36c-b", m, r, {"validate_before": False, "anchor_called": True,
        "a000_present": True, "a000_keys": IDENT, "validate_after": True, "refused": False}))
    print(json.dumps({"probe": "e123", "src_sha256_l3233_3312": src_sha,
                      "python": sys.version.split()[0], "rows": out,
                      "summary": f"{sum(x['pass'] for x in out)}/{len(out)} as predicted"},
                     indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
