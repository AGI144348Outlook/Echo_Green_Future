"""E59 exploratory probe (Claude 19Z) on Genesis echo_governor_skeleton.py blob 63eb982 (genesis-documentary b9a2299). Read-only; no Genesis change.
Question (ChatGPT Run474 56G-ab/N44, PROPOSED): an A-000 record integrity observation plus a controlled, logged amendment path.
Runs N44's five falsifiers against (a) the real unguarded record and (b) two REFERENCE guards written here, not in Genesis:
  PROXY_LIVE  : known["A-000"] replaced by a read-only MappingProxyType over the SAME dict (retained aliases still write)
  PROXY_COPY  : read-only MappingProxyType over a private deep copy (retained aliases write a stale dict)
Both guards expose amend(field, value, actor, reason) that writes the private dict and returns a receipt.
Observer: sha256 of canonical JSON of known["A-000"] and known["A-000-RESH"] (sort_keys), version tag.
Real AlgorithmMatrix, ReshIdentity, governor_validate_and_deploy(); no Lobby, no callbacks needed.
Usage: python3 -I probe.py <dir with skeleton>"""
import sys, json, types, hashlib, copy
sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
OBS = {"scope": "matrix.known[A-000,A-000-RESH]", "canon": "json-sort_keys-v1", "hash": "sha256"}
def observe(m):
    try:
        return hashlib.sha256(json.dumps({k: dict(m.known[k]) for k in ("A-000", "A-000-RESH")}, sort_keys=True).encode()).hexdigest()[:16]
    except Exception:
        return None
def classify(b, a, receipts):
    if b is None or a is None: return {"a000_record_changed": None, "history": "UNKNOWN"}
    if b == a: return {"a000_record_changed": False, "history": "UNKNOWN"}
    if receipts and receipts[-1]["after"] == a: return {"a000_record_changed": True, "history": "AUTHORIZED_RECEIPT_MATCHES"}
    return {"a000_record_changed": True, "history": "UNAUTHORIZED_OR_UNEXPLAINED"}
class Guard:
    def __init__(self, m, mode):
        self.m, self.receipts = m, []
        self.private = m.known["A-000"] if mode == "PROXY_LIVE" else copy.deepcopy(m.known["A-000"])
        m.known["A-000"] = types.MappingProxyType(self.private)
    def amend(self, field, value, actor, reason):
        before = observe(self.m); self.private[field] = value
        r = {"field": field, "actor": actor, "reason": reason, "before": before, "after": observe(self.m)}
        self.receipts.append(r); return r
def a000_check(m):   # governor_validate_and_deploy() stops at regions on this fixture; report only its A-000 stage
    res = g.governor_validate_and_deploy(m)
    return "FAILED_AT_A000" if str(res.get("reason", "")).startswith("A-000") else "PASSED_A000_STAGE"
def setup(mode):
    m = g.AlgorithmMatrix(); r = g.ReshIdentity(m)
    alias = m.known["A-000"]        # a reference taken before any guard (anchor() itself does this, line 3258)
    r.anchor()
    gd = Guard(m, mode) if mode != "UNGUARDED" else None
    return m, r, alias, gd
def run(mode, case):
    m, r, alias, gd = setup(mode); before = observe(m); refused = None; receipts = gd.receipts if gd else []
    try:
        if case == "1_STATUS_ONLY":
            m.known["A-000"]["status"] = "TAMPERED"
        elif case == "2_MUTATE_RESTORE":
            m.known["A-000"]["status"] = "TAMPERED"; m.known["A-000"]["status"] = "ACTIVE"
        elif case == "3_RETAINED_ALIAS":
            alias["status"] = "TAMPERED"
        elif case == "4_AUTHORIZED_AMEND":
            if gd: gd.amend("note", "reviewed update", "claude", "E59 fixture")
            else: m.known["A-000"]["note"] = "reviewed update"
        elif case == "5_FAILED_SNAPSHOT":
            if gd: gd.amend("bad", {("tuple", "key"): 1}, "claude", "E59 fixture")
            else: m.known["A-000"]["bad"] = {("tuple", "key"): 1}
    except TypeError as e:
        refused = type(e).__name__
    after = observe(m)
    return {"refused": refused, **classify(before, after, receipts),
            "status_seen_via_known": m.known["A-000"].get("status"),
            "resh_validate": r.validate(),
            "governor_a000_check": a000_check(m) if case != "5_FAILED_SNAPSHOT" else "skipped",
            "receipts": len(receipts)}
out = {"observer": OBS}
for mode in ["UNGUARDED", "PROXY_LIVE", "PROXY_COPY"]:
    out[mode] = {c: run(mode, c) for c in ["1_STATUS_ONLY", "2_MUTATE_RESTORE", "3_RETAINED_ALIAS", "4_AUTHORIZED_AMEND", "5_FAILED_SNAPSHOT"]}
m, r, alias, _ = setup("UNGUARDED")
out["source_alias_check"] = {"anchor_entry_is_known_A000_RESH": r._anchor_entry is m.known["A-000-RESH"],
                             "pre_anchor_ref_is_known_A000": alias is m.known["A-000"]}
print(json.dumps(out, indent=1, sort_keys=True))
