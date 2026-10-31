"""E65 exploratory probe (Claude 05Z, 2026-10-31) on Genesis echo_governor_skeleton.py blob 63eb982 (genesis-documentary b9a2299).
Read-only; no Genesis change; nothing frozen. Built on E64 (DISC-002-bound-boot-e64-probe.py): the Known/R/boot/revalidate machinery is E64's,
copied unchanged except where marked SESSION.
Questions: ChatGPT Run483 N53 F1-F5 and Run484 N54 falsifiers 1-5 (both PROPOSED).
Conditions, each in a fresh interpreter (python3 -I):
  MODEL-BOUND    E64's bound boot as published (baseline).
  MODEL-SESSION  MODEL-BOUND plus: (a) a semantic policy PINNED (placeholder for Timothy's semantic-policy ruling: which A-000 fields a
                 receipted amend may not change without a separate decision); revalidate refuses a candidate that moves a pinned field;
                 (b) after boot a Session holds the bundle's snapshot as identity authority; check() compares the live slots with it and,
                 on mismatch, appends a frozen incident (expected/observed fingerprints, witnessed version, receipt head, check sequence
                 number, scope, history UNKNOWN) and blocks new core-dependent ops until reconcile(decision) with a decision naming that
                 incident; no automatic repair, revalidation or approval. The real boot is called exactly as in E64.
Usage: python3 -I probe.py <dir with skeleton>"""
import sys, json, hashlib, subprocess, copy
from types import MappingProxyType as MP
P = ("A-000", "A-000-RESH")
def dig(x): return hashlib.sha256(json.dumps(x, sort_keys=True, default=list).encode()).hexdigest()[:12]
def freeze(v):
    if isinstance(v, list): return tuple(freeze(i) for i in v)
    if isinstance(v, dict): return MP({k: freeze(i) for k, i in v.items()})
    return v
PINNED = {"A-000": ("name", "identity_symbol", "identity_glyph"), "A-000-RESH": ("name", "glyph", "status")}  # placeholder policy
def plain(r): return {k: (list(v) if isinstance(v, tuple) else v) for k, v in dict(r).items()}

def run(cond):
    sys.path.insert(0, sys.argv[1]); import echo_governor_skeleton as g
    bound = True; session = cond == "MODEL-SESSION"
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
        if session:
            moved = [f"{k}.{f}" for k in P for f in PINNED.get(k, ()) if old["snapshot"][k].get(f) != new["snapshot"][k].get(f)]
            if moved: return None, "REFUSED: policy-pinned field changed (" + ",".join(moved) + "); needs a semantic-policy decision, not receipts"
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
    class Session:  # SESSION (N54): bound identity authority separate from registry integrity alarm
        def __init__(self, m, b): self.m, self.b, self.incidents, self.blocked, self.seq = m, b, [], False, 0
        def check(self):
            self.seq += 1
            obs = {k: dict.get(self.m.known, k) for k in P}
            exp_d = dig({k: plain(self.b["snapshot"][k]) for k in P}); obs_d = dig({k: plain(obs[k]) for k in P if obs[k] is not None})
            if obs_d == exp_d: return "no incident (slots equal session snapshot at check " + str(self.seq) + "; history UNKNOWN)"
            inc = MP({"expected": exp_d, "observed": obs_d, "witnessed_version": self.b["witness"]["version"],
                      "receipt_head": self.m.known.receipts[-1]["after"], "check_seq": self.seq, "scope": "A-000/A-000-RESH",
                      "history": "UNKNOWN", "repair": "none"})
            inc = MP(dict(inc, id=dig(plain(inc)))); self.incidents.append(inc); self.blocked = True
            return "INCIDENT " + inc["id"] + " expected " + exp_d + " observed " + obs_d
        def core_op(self):  # any new operation that would read A-000 as authoritative
            if self.blocked: return "REFUSED: core-dependent op blocked by incident " + self.incidents[-1]["id"]
            return "core op ran on session identity " + self.b["snapshot"]["A-000"]["name"]
        def reconcile(self, decision):
            if not self.incidents or decision != self.incidents[-1]["id"]: return "REFUSED: decision does not name the open incident"
            self.m.known.amend("A-000", {}, "reconcile:" + decision, "republish validated record")  # receipted, caller-authorized
            r2 = self.check(); self.blocked = r2.startswith("INCIDENT"); return "reconciled by decision; recheck: " + r2
    def booted(m, b, hook=None):
        out = boot(m, b, b["witness"]["id"], hook=hook); return out, (Session(m, b) if session else None)
    impostor = {"name": "Impostor Governor", "status": "ACTIVE", "identity_symbol": "resh"}
    rows = {}
    # N53 F1: valid receipted amend after validation -> old refused, new explicit decision permitted
    m, r = fresh(); b = r.validate_bundle(); m.known.amend("A-000", {"identity_meaning": "amended after validate"}, "probe", "F1")
    rows["N53-F1a old decision after valid amend"] = boot(m, b, b["witness"]["id"])
    nb, msg = revalidate(m, r, b); rows["N53-F1b revalidate"] = msg
    if nb: rows["N53-F1c new decision, approval names it"] = boot(m, nb, nb["witness"]["id"])
    # N53 F2: continuous receipts but changed semantics (same shape, still ACTIVE/resh, new name)
    m, r = fresh(); b = r.validate_bundle(); m.known.amend("A-000", {"name": "Impostor Governor"}, "probe", "F2")
    nb, msg = revalidate(m, r, b); rows["N53-F2 receipted rename of A-000, revalidate"] = msg
    if nb: rows["N53-F2b ...then boot with approval naming it"] = boot(m, nb, nb["witness"]["id"])
    # N53 F3 stale nested alias
    m, r = fresh(); first = m.known["A-000-RESH"]; r.anchor()
    try: first["aliases"].append("intruder"); rows["N53-F3 stale nested aliases.append"] = "ACCEPTED"
    except (AttributeError, TypeError) as e: rows["N53-F3 stale nested aliases.append"] = "REFUSED (" + type(e).__name__ + ")"
    # N53 F4 / N54-2 part: A-900 write
    m, r = fresh(); b = r.validate_bundle(); m.record("A-900", {"name": "probe learning entry", "status": "ACTIVE"})
    rows["N53-F4 A-900 write after validate"] = boot(m, b, b["witness"]["id"])
    # N53 F5 = N54-1: impostor written after gate (callback stand-in)
    m, r = fresh(); b = r.validate_bundle()
    out, s = booted(m, b, hook=lambda mm: dict.__setitem__(mm.known, "A-000", impostor))
    rows["N53-F5/N54-1 impostor after gate: boot"] = out
    rows["N54-1 post-boot check"] = s.check() if s else "no check exists (E64 left the slot unreported)"
    if s:
        rows["N54-2a core-dependent op after incident"] = s.core_op()
        m.record("A-900", {"name": "learning after incident", "status": "ACTIVE"}); rows["N54-2b A-900 write after incident"] = "accepted; A-900 present=" + str("A-900" in m.known)
        rows["N54-3 live slot after report (no auto repair)"] = "live name=" + repr(dict.get(m.known, "A-000")["name"]) + "; approvals created=0; revalidations=0"
        try: s.incidents[-1]["expected"] = "x"; rows["N54-4a overwrite incident"] = "ACCEPTED"
        except TypeError as e: rows["N54-4a overwrite incident"] = "REFUSED (" + type(e).__name__ + ")"
        try: s.b["snapshot"]["A-000"]["name"] = "x"; rows["N54-4b overwrite session witness snapshot"] = "ACCEPTED"
        except TypeError as e: rows["N54-4b overwrite session witness snapshot"] = "REFUSED (" + type(e).__name__ + ")"
        rows["N54-6a reconcile, wrong decision"] = s.reconcile("not-the-incident")
        rows["N54-6b reconcile, decision names incident"] = s.reconcile(s.incidents[-1]["id"])
        rows["N54-6c core op after reconcile"] = s.core_op()
    # N54-5: swap and restore before the check
    m, r = fresh(); b = r.validate_bundle(); out, s = booted(m, b); saved = dict.get(m.known, "A-000")
    dict.__setitem__(m.known, "A-000", impostor); dict.__setitem__(m.known, "A-000", saved)
    rows["N54-5 swap+restore after boot, then check"] = s.check() if s else "no check exists"
    print(json.dumps({"condition": cond, "rows": rows}, ensure_ascii=False, default=str))

if __name__ == "__main__":
    if len(sys.argv) > 2: run(sys.argv[2])
    else:
        res = [json.loads(subprocess.run([sys.executable, "-I", __file__, sys.argv[1], c], capture_output=True, text=True, check=True).stdout)
               for c in ("MODEL-BOUND", "MODEL-SESSION")]
        txt = json.dumps(res, indent=1, ensure_ascii=False); print(txt); print("sha256", hashlib.sha256(txt.encode()).hexdigest())
