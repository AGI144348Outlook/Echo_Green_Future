"""E60 exploratory probe (Claude 21Z) on Genesis echo_governor_skeleton.py blob 63eb982 (genesis-documentary b9a2299). Read-only; no Genesis change.
Question (ChatGPT Run475 56G-ac/N45, PROPOSED): A-000 protection as an ownership/publication boundary: private authoritative store,
immutable published snapshots, amendment transaction as the only publication operation, aliases enumerated and routed, legacy path
attempts refused or explicitly logged. Fields kept apart: record_digest_equal, history, amendment_receipts, validation_consistent.
A REFERENCE boundary is written here, not in Genesis:
  GuardedKnown(dict): refuses writes to the protected keys through __setitem__/__delitem__/update/setdefault/pop/popitem/clear;
  Boundary: private store per protected key, publishes MappingProxyType over a fresh deep copy per version; amend() is a
  transaction {key, field, value, actor, reason, before, after, version}; a value that cannot be canonicalised is refused before publishing;
  a legacy tripwire keeps (object, digest) of every dict that was the live record before install and reports writes at observe().
Two install points: GATE = boundary installed right after AlgorithmMatrix() and anchor() routed through amend() (no legacy alias can exist);
  LATE = boundary installed after the real anchor() (pre-anchor alias and the old _anchor_entry dict are legacy).
Usage: python3 -I probe.py <dir with skeleton>"""
import sys, json, types, hashlib, copy
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
P = ("A-000", "A-000-RESH")
def canon(x): return json.dumps(x, sort_keys=True)
def dig(x): return hashlib.sha256(canon(x).encode()).hexdigest()[:16]
class Refused(Exception): pass
class GuardedKnown(dict):
    def _chk(self, k):
        if k in P and not getattr(self, "_open", False): raise Refused("protected key " + k)
    def __setitem__(self, k, v): self._chk(k); dict.__setitem__(self, k, v)
    def __delitem__(self, k): self._chk(k); dict.__delitem__(self, k)
    def update(self, *a, **kw):
        for k in dict(*a, **kw): self._chk(k)
        dict.update(self, *a, **kw)
    def setdefault(self, k, d=None):
        if k not in self: self._chk(k)
        return dict.setdefault(self, k, d)
    def pop(self, k, *d): self._chk(k); return dict.pop(self, k, *d)
    def popitem(self): raise Refused("popitem on protected mapping")
    def clear(self): raise Refused("clear on protected mapping")
class Boundary:
    def __init__(self, m):
        self.m, self.log, self.version, self.legacy = m, [], 0, []
        old = m.known
        self.private = {k: copy.deepcopy(dict(old[k])) for k in P if k in old}
        for k in P:
            if k in old and isinstance(old[k], dict): self.legacy.append((k, old[k], dig(old[k])))
        gk = GuardedKnown(); dict.update(gk, old); m.known = gk
        self._publish()
    def _publish(self):
        self.m.known._open = True
        try:
            for k, v in self.private.items(): self.m.known[k] = types.MappingProxyType(copy.deepcopy(v))
        finally: self.m.known._open = False
        self.published = {k: dict.__getitem__(self.m.known, k) for k in self.private}
    def snapshot_digest(self): return dig({k: dict(self.private[k]) for k in self.private})
    def amend(self, key, changes, actor, reason):
        trial = copy.deepcopy(self.private.get(key, {})); trial.update(changes)
        try: canon(trial)
        except TypeError: raise Refused("value cannot be canonicalised; nothing published")
        before = self.snapshot_digest(); self.private[key] = trial; self.version += 1; self._publish()
        r = {"key": key, "fields": sorted(changes), "actor": actor, "reason": reason, "before": before, "after": self.snapshot_digest(), "version": self.version}
        self.log.append(r); return r
    def observe(self):
        try: d = self.snapshot_digest()
        except Exception: return {"digest": None, "history": "UNKNOWN"}
        slot_ok = all(dict.__getitem__(self.m.known, k) is self.published[k] for k in self.published)
        legacy_writes = [k for (k, obj, d0) in self.legacy if dig(obj) != d0]
        return {"digest": d, "published_slot_intact": slot_ok, "legacy_writes_logged": legacy_writes}
def routed_anchor(r, b):   # anchor()'s own field changes and A-000-RESH entry, as two logged transactions
    b.amend("A-000", {"identity_symbol": "resh", "identity_glyph": "ר", "identity_letter": "resh", "identity_meaning": "head beginning leader identity"}, "claude", "anchor() routed (E60 reference)")
    b.amend("A-000-RESH", {"name": "Resh — Governor Identity Anchor", "status": "ACTIVE", "type": "IDENTITY-LETTER", "glyph": "ר", "aliases": ["A-000", "resh", "governor"], "perception_operator": "ayin", "expression_operator": "pe"}, "claude", "anchor() routed (E60 reference)")
    r._anchored = True; r._anchor_entry = b.m.known["A-000-RESH"]
def boot_a000(m):
    res = g.governor_validate_and_deploy(m)
    return "FAILED_AT_A000" if str(res.get("reason", "")).startswith("A-000") else "PASSED_A000_STAGE"
def setup(mode):
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m); alias = m.known["A-000"]
    if mode == "GATE":
        b = Boundary(m); routed_anchor(r, b)
        try: g.ReshIdentity(m).anchor(); real_anchor_after = "ACCEPTED"
        except (Refused, TypeError) as e: real_anchor_after = "REFUSED:" + type(e).__name__
    else:
        r.anchor(); b = Boundary(m); real_anchor_after = "n/a"
    return m, r, alias, b, real_anchor_after
CASES = ["0_CONTROL", "1_ALIAS_PRE_INSTALL", "2_OLD_ANCHOR_ENTRY", "3_SNAPSHOT_WRITE", "4_KEY_REPLACE", "5_RECORD_API", "6_UPDATE_API",
         "7_DICT_SETITEM_BYPASS", "8_AUTHORIZED_AMEND", "9_AUTHORIZED_STATUS_TAMPERED", "10_ABA_AMEND", "11_UNCANONICAL_AMEND", "12_LEARNING_WRITE"]
def run(mode, case):
    m, r, alias, b, ra = setup(mode); before = b.snapshot_digest(); n0 = len(b.log); refused = None
    try:
        if case == "1_ALIAS_PRE_INSTALL": alias["status"] = "TAMPERED"
        elif case == "2_OLD_ANCHOR_ENTRY":
            e = r._anchor_entry
            if isinstance(e, dict): e["status"] = "TAMPERED"
            else: e["status"] = "TAMPERED"
        elif case == "3_SNAPSHOT_WRITE": m.known["A-000"]["status"] = "TAMPERED"
        elif case == "4_KEY_REPLACE": m.known["A-000"] = {"name": "Governor", "status": "TAMPERED"}
        elif case == "5_RECORD_API": m.record("A-000", {"name": "Governor", "status": "TAMPERED"})
        elif case == "6_UPDATE_API": m.known.update({"A-000": {"name": "Governor", "status": "TAMPERED"}})
        elif case == "7_DICT_SETITEM_BYPASS": dict.__setitem__(m.known, "A-000", {"name": "Governor", "status": "TAMPERED", "identity_symbol": "resh"})
        elif case == "8_AUTHORIZED_AMEND": b.amend("A-000", {"note": "reviewed update"}, "claude", "E60 fixture")
        elif case == "9_AUTHORIZED_STATUS_TAMPERED": b.amend("A-000", {"status": "TAMPERED"}, "claude", "E60 fixture")
        elif case == "10_ABA_AMEND":
            b.amend("A-000", {"status": "TAMPERED"}, "claude", "E60 A"); b.amend("A-000", {"status": "ACTIVE"}, "claude", "E60 A'")
        elif case == "11_UNCANONICAL_AMEND": b.amend("A-000", {"bad": {("tuple", "key"): 1}}, "claude", "E60 fixture")
        elif case == "12_LEARNING_WRITE":
            m.record("A-900", {"name": "learned", "status": "ACTIVE"}); m.known.update({"A-901": {"name": "learned2"}}); m.known["A-902"] = {"name": "learned3"}
    except (Refused, TypeError) as e:
        refused = type(e).__name__
    o = b.observe(); v = r.validate(); bt = boot_a000(m)
    out = {"refused": refused, "record_digest_equal": o["digest"] == before if o["digest"] else None, "history": "UNKNOWN" if o["digest"] == before else ("RECEIPTS" if len(b.log) > n0 else "UNEXPLAINED"),
           "amendment_receipts_added": len(b.log) - n0, "published_slot_intact": o["published_slot_intact"], "legacy_writes_logged": o["legacy_writes_logged"],
           "status_seen": m.known["A-000"].get("status"), "resh_validate": v, "boot_a000": bt, "validation_consistent": v == (bt == "PASSED_A000_STAGE")}
    if case == "12_LEARNING_WRITE": out["learned_present"] = all(k in m.known for k in ("A-900", "A-901", "A-902"))
    if case == "0_CONTROL": out["real_anchor_after_install"] = ra; out["anchor_entry_type"] = type(r._anchor_entry).__name__
    return out
res = {mode: {c: run(mode, c) for c in CASES} for mode in ["GATE", "LATE"]}
print(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=True))
