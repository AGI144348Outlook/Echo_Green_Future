"""Claude 02Z DISC-002 probe: E20 (ChatGPT run 311: Dev Suite snapshot() as a read surface outside storage()).
Runs on a scratch copy of Dev Suite blob f7cf465; the payload is written directly (Dev Suite has no storage write method);
the witness and redacted_snapshot() are in-process PROPOSED stand-ins, not Dev Suite and not an external authority.
Pre-registered on Issue #13 (6378503837) before execution. Not a frozen test. Usage: python3 -I -B <probe> <algorithm_matrix.py>"""
import copy, hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("am", sys.argv[1]); am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
PAYLOAD = {"note": "protected-payload-E20"}
def booted():
    r = am.AlgorithmMatrixRuntime(); r.run_boot_handshake(); r.sub_matrices["standard:0"]["storage"].update(copy.deepcopy(PAYLOAD)); return r
def try_storage(r):
    try: return ["returned", r.storage("standard:0")]
    except PermissionError as e: return ["PermissionError", str(e)]
out = {}
r = booted(); ctrl = try_storage(r)
r.sub_matrices["standard:0"]["glyph"] = "X"   # revoke: layout digest changes
s = r.snapshot()
out["E20a_glyph_revoked"] = {"storage_control_before": ctrl, "storage_after": try_storage(r),
    "snapshot_alg_002_status": s["system_state"]["alg_002_status"], "snapshot_storage_unlocked": s["system_state"]["storage_unlocked"],
    "snapshot_discloses_payload": s["sub_matrices"]["standard:0"]["storage"] == PAYLOAD}
r = booted(); r.primary["status"] = "LOCKED"; before = (r.primary["status"], r.permit, r.verified)
s = r.snapshot(); leak = s["sub_matrices"]["standard:0"]["storage"] == PAYLOAD
try: hs = ["returned", type(r.run_boot_handshake()).__name__]
except PermissionError as e: hs = ["PermissionError", str(e)]
out["E20b_status_locked_then_handshake"] = {"snapshot_discloses_payload": leak, "handshake": hs,
    "before_status_permit_verified": before, "after_status_permit_verified": (r.primary["status"], r.permit, r.verified),
    "alg_002_after": r.alg_002(), "audit_tail": r.audit[-3:]}
PROTECTED = ("matrix_id", "matrix_data", "active_slots", "governor_context")
def pdigest(r): return hashlib.sha256(json.dumps({k: r.primary.get(k) for k in PROTECTED}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
class Witness:  # PROPOSED stand-in (runs 309/310 token shape)
    def __init__(self, adapter_id, d): self.adapter_id, self._d, self.state, self.iv, self.lv = adapter_id, d, "ACTIVE", 0, 0
    def set_state(self, s): self.state = s; self.lv += 1
    def token(self, d): return (self.adapter_id, self.iv, self.lv, d) if d == self._d and self.state == "ACTIVE" else None
    def check(self, tok):
        if tok is None: return "denied: NO_TOKEN"
        cur = self.token(self._d)
        if cur is None: return "denied: AUTHORITY_SUSPENDED"
        return "accepted" if tok == cur else "denied: VERSION_CHANGED"
def redacted_snapshot(r, w, during_copy=None):  # PROPOSED: token before and after the copy; storage only if both hold and alg_002()
    tok = w.token(pdigest(r)); valid = r.alg_002()
    diag = {"alg_002_status": valid, "storage_unlocked": r.storage_unlocked, "matrix_ids": sorted(r.sub_matrices)}
    if not (valid and r.storage_unlocked) or w.check(tok) != "accepted": return {"released": False, "reason": "REVOKED_OR_NO_TOKEN", "diagnostic": diag}
    data = copy.deepcopy({k: v["storage"] for k, v in r.sub_matrices.items()})
    if during_copy: during_copy(w)
    verdict = w.check(tok)
    if verdict != "accepted": return {"released": False, "reason": verdict.split(": ")[1], "diagnostic": diag}
    return {"released": True, "storage_standard_0": data["standard:0"]}
r = booted(); w = Witness("devsuite", pdigest(r))
valid = redacted_snapshot(r, w)
race = redacted_snapshot(r, w, during_copy=lambda w: (w.set_state("SUSPENDED"), w.set_state("ACTIVE")))
r.sub_matrices["standard:0"]["glyph"] = "X"; revoked = redacted_snapshot(r, w)
out["E20c_redacted_snapshot"] = {"valid": valid, "suspend_restore_during_copy": race,
    "revoked": {k: revoked[k] for k in ("released", "reason")}, "revoked_output_has_payload": "protected-payload-E20" in json.dumps(revoked)}
print(json.dumps(out, indent=1, ensure_ascii=False))
