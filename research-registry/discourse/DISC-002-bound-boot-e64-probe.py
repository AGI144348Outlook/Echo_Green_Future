"""E64 exploratory probe (Claude 04Z, 2026-10-31) on Genesis echo_governor_skeleton.py blob 63eb982 (genesis-documentary b9a2299).
Read-only; no Genesis change; nothing frozen.
Question (ChatGPT Run481 N51 and Run482 N52, PROPOSED): if boot consumes ONE bound argument (an immutable core snapshot plus the witness
computed on it) instead of a witness plus a later read of matrix.known["A-000"], and a revalidation after an authorized amend only yields a
NEW CANDIDATE that needs an explicit approval naming the new witness, do N51's seven candidate falsifiers and N52's four test candidates
come out as proposed, and what does E63's compare-then-reread gate do on the same cases?
Conditions, each in its own fresh interpreter (python3 -I):
  MODEL-WITNESS  E63's gate: compare witness with the live slots, then call the real governor_validate_and_deploy(m), which re-reads A-000.
  MODEL-BOUND    boot(bundle, approval): bundle = (frozen core snapshot, witness on that snapshot); refuse unless the approval names the
                 bundle's witness id and the registry version still equals the bundle's; then the real governor_validate_and_deploy is called
                 on a shallow view of the matrix whose known holds the bundle's snapshot for A-000/A-000-RESH (never the live slots).
                 revalidate(old) returns a new candidate bundle only if receipts continue old.version+1..now with no gap and the new
                 snapshot passes the semantic check; it never boots.
A hook (H) can run "inside boot" after the gate and before the real boot reads A-000, standing in for a callback or another thread.
In every condition the real boot later stops at "no regions discovered", as in E61-E63; only the A-000 stage is reported.
Usage: python3 -I probe.py <dir with skeleton>   (spawns one fresh process per condition and prints the combined JSON + sha256)"""
import sys, json, hashlib, subprocess, copy
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
    bound = cond == "MODEL-BOUND"
    def check(key, rec):  # boot A-000 stage (l. 9392-9398) + resh symbol, as in E62/E63
        if key == "A-000":
            if not {"name", "status"} <= set(rec) or rec.get("status") != "ACTIVE": return "A-000 fails boot identity check"
            if "identity_symbol" in rec and rec["identity_symbol"] != "resh": return "identity_symbol not resh"
        if key == "A-000-RESH" and rec.get("status") != "ACTIVE": return "A-000-RESH not ACTIVE"
        return None
    class Known(dict):  # E62/E63 MODEL-DEEP boundary: private store, frozen published snapshots, receipted amend()
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
            self.receipts.append({"key": k, "actor": actor, "after": dig(plain(snap)), "version": len(self.receipts) + 1})
            return snap
        def __setitem__(self, k, v):
            if k in P: raise PermissionError("protected key: use amend()")
            dict.__setitem__(self, k, v)
        def amend(self, k, fields, actor, why):
            rec = plain(self._priv.get(k, {})); rec.update(fields); return self._publish(k, rec, actor, why)
        def version(self): return self.receipts[-1]["version"] if self.receipts else 0
        def witness(self):
            slots = {k: dict.get(self, k) for k in P}
            w = {"version": self.version(), "core_digest": dig({k: plain(self._priv[k]) for k in P if k in self._priv}),
                 "slot_digest": dig({k: plain(slots[k]) for k in P if slots[k] is not None}),
                 "slot_intact": all(slots[k] is self._pub.get(k) for k in P),
                 "semantic_ok": all(check(k, plain(slots[k])) is None for k in P if slots[k] is not None), "history": "UNKNOWN"}
            w["id"] = dig([w[f] for f in ("version", "core_digest", "slot_digest")]); return w
        def bundle(self):  # snapshot objects taken together with the witness on them
            w = self.witness(); return {"snapshot": MP({k: self._pub[k] for k in P}), "witness": w}
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
        def validate_bundle(self):
            b = self.matrix.known.bundle(); w = b["witness"]
            w["valid"] = bool(super().validate() and w["semantic_ok"] and w["slot_intact"]); return b
    def revalidate(m, r, old):  # N51: new candidate only on continuous receipts + semantic check; never boots
        vs = [x["version"] for x in m.known.receipts if x["version"] > old["witness"]["version"]]
        if vs != list(range(old["witness"]["version"] + 1, m.known.version() + 1)) or not vs: return None, "REFUSED: receipt gap or no change"
        new = r.validate_bundle()
        if not new["witness"]["valid"]: return None, "REFUSED: new snapshot not valid"
        return new, "NEW CANDIDATE " + new["witness"]["id"] + " (old " + old["witness"]["id"] + "); not booted"
    def real_boot(view):
        res = g.governor_validate_and_deploy(view); a000 = view.known.get("A-000") or {}
        st = "A-000 stage FAILED" if "A-000" in res.get("reason", "") else "A-000 stage passed"
        return f"{st} (boot read name={a000.get('name', '?')!r}, status={a000.get('status', '?')}); boot {res.get('status')}"
    def boot(m, b, approval=None, hook=None):
        w = b["witness"]
        if not w["valid"]: return "REFUSED: witness not valid"
        if bound:
            if approval != w["id"]: return "REFUSED: approval does not name witness " + w["id"]
            now = m.known.witness()
            if now["version"] != w["version"]: return "REFUSED: registry version moved " + str(w["version"]) + "->" + str(now["version"]) + "; revalidate for a new candidate"
            if not now["slot_intact"]: return "REFUSED: published slot replaced outside amend()"
            if hook: hook(m)
            view = copy.copy(m); kv = {k: v for k, v in dict.items(m.known) if k not in P}; kv.update(b["snapshot"]); view.known = kv
            return real_boot(view)
        now = m.known.witness()
        diff = [f for f in ("version", "core_digest", "slot_digest", "slot_intact", "semantic_ok") if now[f] != w[f]]
        if diff: return "REFUSED: witness mismatch " + ",".join(diff)
        if hook: hook(m)
        return real_boot(m)
    def fresh():
        m = M(); r = R(m); r.anchor(); r.anchor(); return m, r
    impostor = {"name": "Impostor Governor", "status": "ACTIVE", "identity_symbol": "resh"}
    rows = {}
    m, r = fresh(); b = r.validate_bundle(); rows["G0 validate then boot, nothing between"] = boot(m, b, b["witness"]["id"])
    # G1 valid receipted amend after validation -> new candidate, not implicit boot
    m, r = fresh(); b = r.validate_bundle(); m.known.amend("A-000", {"identity_meaning": "amended after validate"}, "probe", "G1")
    rows["G1a boot old bundle after valid receipted amend"] = boot(m, b, b["witness"]["id"])
    nb, msg = revalidate(m, r, b); rows["G1b revalidate"] = msg
    if nb:
        rows["G1c boot new candidate with old approval"] = boot(m, nb, b["witness"]["id"])
        rows["G1d boot new candidate with approval naming new witness"] = boot(m, nb, nb["witness"]["id"])
    # G2 unauthorized same-shape slot replacement after validation
    m, r = fresh(); b = r.validate_bundle(); dict.__setitem__(m.known, "A-000", impostor)
    rows["G2 same-shape slot replacement (dict.__setitem__) after validate"] = boot(m, b, b["witness"]["id"])
    # G3 change after the gate, inside boot (callback/thread stand-in): which record does boot read?
    m, r = fresh(); b = r.validate_bundle()
    rows["G3 impostor slot written after gate, before boot reads"] = boot(m, b, b["witness"]["id"], hook=lambda mm: dict.__setitem__(mm.known, "A-000", impostor))
    m, r = fresh(); b = r.validate_bundle()
    rows["G3b TAMPERED slot written after gate, before boot reads"] = boot(m, b, b["witness"]["id"], hook=lambda mm: dict.__setitem__(mm.known, "A-000", {"name": "x", "status": "TAMPERED"}))
    # G4 receipt gap
    m, r = fresh(); b = r.validate_bundle(); m.known.amend("A-000", {"identity_meaning": "g4 one"}, "probe", "G4")
    m.known.amend("A-000", {"identity_meaning": "g4 two"}, "probe", "G4"); del m.known.receipts[-2]
    nb, msg = revalidate(m, r, b); rows["G4 revalidate with one receipt missing"] = msg
    # G5 semantically invalid receipted status
    m, r = fresh(); b = r.validate_bundle(); n = len(m.known.receipts)
    try: m.known.amend("A-000", {"status": "TAMPERED"}, "probe", "G5"); rows["G5 amend status=TAMPERED"] = "ACCEPTED"
    except PermissionError: rows["G5 amend status=TAMPERED"] = f"REFUSED at amend; receipts {n}->{len(m.known.receipts)}; " + boot(m, b, b["witness"]["id"])
    # G6 A-900 learning write
    m, r = fresh(); b = r.validate_bundle(); m.record("A-900", {"name": "probe learning entry", "status": "ACTIVE"})
    rows["G6 A-900 learning write after validate"] = "present=" + str("A-900" in m.known) + "; " + boot(m, b, b["witness"]["id"])
    # G7 change and restore: no false history claim
    m, r = fresh(); b = r.validate_bundle(); saved = dict.get(m.known, "A-000")
    dict.__setitem__(m.known, "A-000", {"name": "x", "status": "TAMPERED"}); dict.__setitem__(m.known, "A-000", saved)
    rows["G7 swap then restore after validate"] = boot(m, b, b["witness"]["id"]) + "; history=" + b["witness"]["history"]
    # N52 nested alias escape: stale reference to an earlier A-000-RESH
    m, r = fresh(); first = m.known["A-000-RESH"]; r.anchor(); b = r.validate_bundle()
    try: first["aliases"].append("intruder"); rows["N52 stale nested aliases.append"] = "ACCEPTED"
    except (AttributeError, TypeError) as e: rows["N52 stale nested aliases.append"] = "REFUSED (" + type(e).__name__ + "); " + boot(m, b, b["witness"]["id"])
    # N52 snapshot built from a caller-controlled mutable alias (constructor path)
    m, r = fresh(); b = r.validate_bundle()
    try: b["snapshot"]["A-000"]["status"] = "TAMPERED"; rows["N52 write into bundle snapshot"] = "ACCEPTED"
    except TypeError as e: rows["N52 write into bundle snapshot"] = "REFUSED (" + type(e).__name__ + ")"
    print(json.dumps({"condition": cond, "rows": rows}, ensure_ascii=False, default=str))

if __name__ == "__main__":
    if len(sys.argv) > 2: run(sys.argv[2])
    else:
        res = [json.loads(subprocess.run([sys.executable, "-I", __file__, sys.argv[1], c], capture_output=True, text=True, check=True).stdout)
               for c in ("MODEL-WITNESS", "MODEL-BOUND")]
        txt = json.dumps(res, indent=1, ensure_ascii=False); print(txt); print("sha256", hashlib.sha256(txt.encode()).hexdigest())
