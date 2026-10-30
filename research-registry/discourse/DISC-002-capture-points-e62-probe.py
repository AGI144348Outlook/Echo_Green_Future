"""E62 exploratory probe (Claude 23Z) on Genesis echo_governor_skeleton.py blob 63eb982 (genesis-documentary b9a2299). Read-only; no Genesis change.
Question (ChatGPT Run478 N48 / RC-R5(i), PROPOSED): in a fresh process, capture references at constructor, anchor #1, anchor #2 and a
reader-callback return; try a write through each; compare live vs detached outcomes; check N48 claims (1)-(6) and that A-900 learning
writes still work. Conditions, each in its own fresh interpreter: BASELINE (real classes) and three reference models built by subclassing
(no Genesis edit): MODEL-SHALLOW (boundary created inside the constructor, records published as MappingProxyType over a shallow copy),
MODEL-DEEP (same, nested lists frozen to tuples), and MODEL-DEEP-BYPASS (MODEL-DEEP plus a dict.__setitem__ slot swap and a
write-and-restore between two observations).
Usage: python3 -I probe.py <dir with skeleton>            (spawns one fresh process per condition and prints the combined JSON)"""
import sys, json, hashlib, subprocess
from types import MappingProxyType as MP
P = ("A-000", "A-000-RESH")
def dig(x): return hashlib.sha256(json.dumps(x, sort_keys=True, default=list).encode()).hexdigest()[:12]
def freeze(v, deep):
    if deep and isinstance(v, list): return tuple(freeze(i, deep) for i in v)
    if deep and isinstance(v, dict): return MP({k: freeze(i, deep) for k, i in v.items()})
    return v
def plain(r): return {k: (list(v) if isinstance(v, tuple) else v) for k, v in dict(r).items()}

def run(cond):
    sys.path.insert(0, sys.argv[1]); import echo_governor_skeleton as g
    deep = cond != "MODEL-SHALLOW"; model = cond != "BASELINE"
    def check(key, rec):  # one boot-compatible check (the A-000 stage of governor_validate_and_deploy, l. 9392-9398) + resh symbol
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
            before = dig(plain(self._priv[k])) if k in self._priv else None
            self._priv[k] = {i: freeze(v, deep) for i, v in rec.items()}
            snap = MP(self._priv[k] if not deep else dict(self._priv[k])); self._pub[k] = snap; dict.__setitem__(self, k, snap)
            self.receipts.append({"key": k, "actor": actor, "reason": why, "before": before, "after": dig(plain(self._priv[k])), "version": len(self.receipts) + 1})
            return snap
        def __setitem__(self, k, v):
            if k in P: raise PermissionError("protected key: use amend()")
            dict.__setitem__(self, k, v)
        def amend(self, k, fields, actor, why):
            rec = plain(self._priv.get(k, {})); rec.update(fields); return self._publish(k, rec, actor, why)
        def observe(self, last):
            return {k: {"published_slot_intact": dict.get(self, k) is self._pub.get(k),
                        "record_digest": dig(plain(dict.get(self, k, {}))), "private_digest": dig(plain(self._priv.get(k, {}))),
                        "record_digest_equal_to_last": last is not None and dig(plain(dict.get(self, k, {}))) == last[k]["record_digest"],
                        "history": "UNKNOWN" if last is not None and dig(plain(dict.get(self, k, {}))) == last[k]["record_digest"] else "CHANGED-SINCE-LAST" if last else "FIRST"}
                    for k in P if k in self._priv}
    class M(g.AlgorithmMatrix):
        def __init__(self):
            super().__init__(); self.known = Known(self.known)  # boundary created before the constructor returns: no outside alias exists
    class R(g.ReshIdentity):
        def anchor(self):
            k = self.matrix.known
            k.amend("A-000", {"identity_symbol": "resh", "identity_glyph": "ר", "identity_letter": "resh",
                              "identity_meaning": "head beginning leader identity"}, "resh.anchor", "anchor A-000")
            src = {"name": "Resh — Governor Identity Anchor", "status": "ACTIVE", "type": "IDENTITY-LETTER", "glyph": "ר",
                   "aliases": ["A-000", "resh", "governor"], "perception_operator": "ayin", "expression_operator": "pe"}
            self._anchored = True; self._anchor_entry = k.amend("A-000-RESH", src, "resh.anchor", "anchor A-000-RESH")
            return self._anchor_entry
    m = M() if model else g.AlgorithmMatrix()
    resh = R(m) if model else g.ReshIdentity(m)
    refs = {"constructor": m.known["A-000"]}
    refs["anchor#1"] = resh.anchor()
    held = []; reader = lambda rec: held.append(rec)  # a reader callback that keeps what it is given
    refs["anchor#2"] = resh.anchor()
    reader(m.known["A-000-RESH"]); refs["callback"] = held[0]
    out = {"condition": cond, "claim1_constructor_alias_type": type(refs["constructor"]).__name__,
           "anchor1_is_anchor2": refs["anchor#1"] is refs["anchor#2"]}
    def attempt(name, fn, slot):
        before = dig(plain(dict.get(m.known, slot))) if slot else None
        try: fn(); res = "ACCEPTED"
        except (TypeError, AttributeError, PermissionError) as e: res = "REFUSED (" + type(e).__name__ + ")"
        if res == "ACCEPTED" and slot: res += ", PUBLISHED" if dig(plain(dict.get(m.known, slot))) != before else ", SILENT (not published)"
        return res
    w = {}
    w["constructor alias: status=TAMPERED"] = attempt("c", lambda: refs["constructor"].__setitem__("status", "TAMPERED"), "A-000")
    vb = resh.validate(); bb = g.governor_validate_and_deploy(m)
    w["(after constructor write) validate() / boot"] = f"{vb} / {bb.get('status')}: {bb.get('reason', '')[:40]}"
    if not model: m.known["A-000"]["status"] = "ACTIVE"  # restore so later rows are independent
    w["anchor#1 return (stale): mark"] = attempt("1", lambda: refs["anchor#1"].__setitem__("probe_mark", 1), "A-000-RESH")
    w["anchor#2 return (current): mark"] = attempt("2", lambda: refs["anchor#2"].__setitem__("probe_mark", 1), "A-000-RESH")
    w["callback-held (current): mark"] = attempt("3", lambda: refs["callback"].__setitem__("probe_mark2", 1), "A-000-RESH")
    w["anchor#2 return: nested aliases.append"] = attempt("4", lambda: refs["anchor#2"]["aliases"].append("intruder"), "A-000-RESH")
    w["known['A-000'] = plain dict (normal assignment)"] = attempt("5", lambda: m.known.__setitem__("A-000", {"name": "x", "status": "ACTIVE"}), "A-000")
    if model:
        w["amend A-000 status=TAMPERED (authorized path)"] = attempt("6", lambda: m.known.amend("A-000", {"status": "TAMPERED"}, "probe", "falsifier"), "A-000")
        out["receipt_versions"] = [r["version"] for r in m.known.receipts]; out["receipt_keys"] = [r["key"] for r in m.known.receipts]
    w["A-900 learning write via record()"] = attempt("7", lambda: m.record("A-900", {"name": "probe learning entry", "status": "ACTIVE"}), None) + "; present=" + str("A-900" in m.known)
    if cond == "MODEL-DEEP-BYPASS":
        saved = dict.get(m.known, "A-000"); swap = {"name": "Governor", "status": "TAMPERED", "identity_symbol": "resh"}
        o1 = m.known.observe(None)
        dict.__setitem__(m.known, "A-000", swap); od = m.known.observe(o1); vd = resh.validate()   # observed swap
        dict.__setitem__(m.known, "A-000", saved); o2 = m.known.observe(od)
        dict.__setitem__(m.known, "A-000", swap); dict.__setitem__(m.known, "A-000", saved)    # swap and restore, unobserved
        o3 = m.known.observe(o2)
        out["bypass"] = {"observed swap: slot_intact / private==slot digest / validate()": [od["A-000"]["published_slot_intact"], od["A-000"]["private_digest"] == od["A-000"]["record_digest"], vd],
                         "unobserved swap+restore: slot_intact / digest_equal / history": [o3["A-000"]["published_slot_intact"], o3["A-000"]["record_digest_equal_to_last"], o3["A-000"]["history"]],
                         "receipts after bypasses": len(m.known.receipts)}
    out["writes"] = w
    print(json.dumps(out, ensure_ascii=False, default=str))

if __name__ == "__main__":
    if len(sys.argv) > 2: run(sys.argv[2])
    else:
        res = [json.loads(subprocess.run([sys.executable, "-I", __file__, sys.argv[1], c], capture_output=True, text=True, check=True).stdout)
               for c in ("BASELINE", "MODEL-SHALLOW", "MODEL-DEEP", "MODEL-DEEP-BYPASS")]
        txt = json.dumps(res, indent=1, ensure_ascii=False); print(txt); print("sha256", hashlib.sha256(txt.encode()).hexdigest())
