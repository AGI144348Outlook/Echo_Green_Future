"""E63 exploratory probe (Claude 01Z, 2026-10-31) on Genesis echo_governor_skeleton.py blob 63eb982 (genesis-documentary b9a2299).
Read-only; no Genesis change.
Question (ChatGPT Run479 N49 / RC-R5(k) and Run480 N50, PROPOSED): if validate() returns a witness (version, core digest,
published-slot digest, semantic result, receipt reference) and boot compares that witness with the exact snapshot it consumes and refuses
on mismatch, do N50's five proposed falsifiers come out as N50 predicts, and where does the witness stop seeing?
Conditions, each in its own fresh interpreter: BASELINE (real classes: validate() -> bool, boot re-reads A-000) and MODEL-WITNESS
(E62's MODEL-DEEP boundary built by subclassing, plus validate_witness() and a boot gate). The gate runs before the real
governor_validate_and_deploy; the model's boot then stops later at "no regions discovered", as in E61/E62, which says nothing about A-000.
Usage: python3 -I probe.py <dir with skeleton>            (spawns one fresh process per condition and prints the combined JSON)"""
import sys, json, hashlib, subprocess
from types import MappingProxyType as MP
P = ("A-000", "A-000-RESH")
def dig(x): return hashlib.sha256(json.dumps(x, sort_keys=True, default=list).encode()).hexdigest()[:12]
def freeze(v):
    if isinstance(v, list): return tuple(freeze(i) for i in v)
    if isinstance(v, dict): return MP({k: freeze(i) for k, i in v.items()})
    return v
def plain(r): return {k: (list(v) if isinstance(v, tuple) else v) for k, v in dict(r).items()}

def run(cond):
    sys.path.insert(0, sys.argv[1]); import echo_governor_skeleton as g
    model = cond != "BASELINE"
    def check(key, rec):  # boot A-000 stage (l. 9392-9398) + resh symbol, as in E62
        if key == "A-000":
            if not {"name", "status"} <= set(rec) or rec.get("status") != "ACTIVE": return "A-000 fails boot identity check"
            if "identity_symbol" in rec and rec["identity_symbol"] != "resh": return "identity_symbol not resh"
        if key == "A-000-RESH" and rec.get("status") != "ACTIVE": return "A-000-RESH not ACTIVE"
        return None
    class Known(dict):
        def __init__(self, src):
            super().__init__(); self._priv, self._pub, self.receipts = {}, {}, []
            for k, v in src.items():
                if k in P: self._publish(k, dict(v), "constructor", "initial record")
                else: dict.__setitem__(self, k, v)
        def _publish(self, k, rec, actor, why):
            err = check(k, rec)
            if err: raise PermissionError("amend refused: " + err)
            self._priv[k] = {i: freeze(v) for i, v in rec.items()}
            snap = MP(dict(self._priv[k])); self._pub[k] = snap; dict.__setitem__(self, k, snap)
            self.receipts.append({"key": k, "actor": actor, "reason": why, "after": dig(plain(self._priv[k])), "version": len(self.receipts) + 1})
            return snap
        def __setitem__(self, k, v):
            if k in P: raise PermissionError("protected key: use amend()")
            dict.__setitem__(self, k, v)
        def amend(self, k, fields, actor, why):
            rec = plain(self._priv.get(k, {})); rec.update(fields); return self._publish(k, rec, actor, why)
        def witness(self):  # computed from what is in the published slots right now
            slots = {k: dict.get(self, k) for k in P}
            return {"version": len(self.receipts), "receipt_ref": self.receipts[-1]["after"] if self.receipts else None,
                    "core_digest": dig({k: plain(self._priv[k]) for k in P if k in self._priv}),
                    "slot_digest": dig({k: plain(slots[k]) for k in P if slots[k] is not None}),
                    "slot_intact": all(slots[k] is self._pub.get(k) for k in P),
                    "semantic_ok": all(check(k, plain(slots[k])) is None for k in P if slots[k] is not None)}
    class M(g.AlgorithmMatrix):
        def __init__(self): super().__init__(); self.known = Known(self.known)
    class R(g.ReshIdentity):
        def anchor(self):
            k = self.matrix.known
            k.amend("A-000", {"identity_symbol": "resh", "identity_glyph": "ר", "identity_letter": "resh",
                              "identity_meaning": "head beginning leader identity"}, "resh.anchor", "anchor A-000")
            src = {"name": "Resh — Governor Identity Anchor", "status": "ACTIVE", "type": "IDENTITY-LETTER", "glyph": "ר",
                   "aliases": ["A-000", "resh", "governor"], "perception_operator": "ayin", "expression_operator": "pe"}
            self._anchored = True; self._anchor_entry = k.amend("A-000-RESH", src, "resh.anchor", "anchor A-000-RESH")
            return self._anchor_entry
        def validate_witness(self):
            w = self.matrix.known.witness(); w["valid"] = bool(super().validate() and w["semantic_ok"] and w["slot_intact"]); return w
    def boot(m, w=None):  # model: gate compares the witness with the snapshot boot is about to consume, then the real boot
        if model:
            now = m.known.witness()
            diff = [f for f in ("version", "core_digest", "slot_digest", "slot_intact", "semantic_ok") if now[f] != w[f]]
            if not w["valid"]: return "REFUSED: witness not valid"
            if diff: return "REFUSED: witness mismatch " + ",".join(diff)
        r = g.governor_validate_and_deploy(m)
        a = "A-000 stage FAILED" if "A-000" in r.get("reason", "") else "A-000 stage passed"
        return f"{a}; boot {r.get('status')}: {r.get('reason', '')[:30]}"
    def fresh():
        m = M() if model else g.AlgorithmMatrix(); r = R(m) if model else g.ReshIdentity(m); r.anchor(); r.anchor(); return m, r
    def val(r): return r.validate_witness() if model else r.validate()
    out = {"condition": cond}; rows = {}
    # F4 fresh validated snapshot passes
    m, r = fresh(); w = val(r); rows["F4 validate then boot, nothing between"] = boot(m, w)
    if model: out["witness_fields"] = sorted(w)
    # F1 mutation between validate and boot (semantically valid change)
    m, r = fresh(); w = val(r)
    try:
        if model: m.known.amend("A-000", {"identity_meaning": "changed after validate"}, "probe", "F1")
        else: m.known["A-000"]["identity_meaning"] = "changed after validate"
        rows["F1 valid change between validate and boot"] = "change applied; " + boot(m, w)
    except Exception as e: rows["F1 valid change between validate and boot"] = "change refused " + type(e).__name__
    # F1b invalid change between validate and boot
    m, r = fresh(); w = val(r)
    try:
        if model: m.known.amend("A-000", {"status": "TAMPERED"}, "probe", "F1b")
        else: m.known["A-000"]["status"] = "TAMPERED"
        rows["F1b status=TAMPERED between validate and boot"] = "change applied; " + boot(m, w)
    except Exception as e: rows["F1b status=TAMPERED between validate and boot"] = "change refused (" + type(e).__name__ + "); " + boot(m, w)
    # F3 nested stale alias write
    m, r = fresh(); first = m.known["A-000-RESH"]; r.anchor(); w = val(r)
    try: first["aliases"].append("intruder"); rows["F3 stale nested aliases.append"] = "ACCEPTED; " + boot(m, w)
    except (AttributeError, TypeError) as e: rows["F3 stale nested aliases.append"] = "REFUSED (" + type(e).__name__ + ")"
    # F5 learning write between validate and boot
    m, r = fresh(); w = val(r); m.record("A-900", {"name": "probe learning entry", "status": "ACTIVE"})
    rows["F5 A-900 learning write between validate and boot"] = "present=" + str("A-900" in m.known) + "; " + boot(m, w)
    if model:
        # F2 receipted semantically invalid status at publish time
        m, r = fresh()
        try: m.known.amend("A-000", {"status": "TAMPERED"}, "probe", "F2"); rows["F2 amend status=TAMPERED"] = "ACCEPTED"
        except PermissionError: rows["F2 amend status=TAMPERED"] = "REFUSED at amend; receipts=" + str(len(m.known.receipts))
        # B1 observed slot swap between validate and boot
        m, r = fresh(); w = val(r); saved = dict.get(m.known, "A-000")
        dict.__setitem__(m.known, "A-000", {"name": "Governor", "status": "ACTIVE", "identity_symbol": "resh"})
        rows["B1 dict.__setitem__ swap (still ACTIVE) between validate and boot"] = boot(m, w)
        # B2 swap and restore between validate and boot (unobserved)
        dict.__setitem__(m.known, "A-000", saved)
        m, r = fresh(); w = val(r); saved = dict.get(m.known, "A-000")
        dict.__setitem__(m.known, "A-000", {"name": "x", "status": "TAMPERED"}); dict.__setitem__(m.known, "A-000", saved)
        rows["B2 swap then restore between validate and boot"] = boot(m, w)
        # B3 swap before validate: does the witness itself see it?
        m, r = fresh(); dict.__setitem__(m.known, "A-000", {"name": "Governor", "status": "ACTIVE", "identity_symbol": "resh"}); w = val(r)
        rows["B3 swap before validate: witness valid / slot_intact"] = f"{w['valid']} / {w['slot_intact']}; " + boot(m, w)
    out["rows"] = rows
    print(json.dumps(out, ensure_ascii=False, default=str))

if __name__ == "__main__":
    if len(sys.argv) > 2: run(sys.argv[2])
    else:
        res = [json.loads(subprocess.run([sys.executable, "-I", __file__, sys.argv[1], c], capture_output=True, text=True, check=True).stdout)
               for c in ("BASELINE", "MODEL-WITNESS")]
        txt = json.dumps(res, indent=1, ensure_ascii=False); print(txt); print("sha256", hashlib.sha256(txt.encode()).hexdigest())
