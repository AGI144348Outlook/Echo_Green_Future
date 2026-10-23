"""Claude 23Z DISC-002 probe: E17 (ChatGPT run 308 matrix cases E16a/E16b, renamed) on a scratch copy of Dev Suite
blob f7cf465: does bootstrap consult anything beyond slot [0,0]? And a PROPOSED pre-bootstrap witness gate (not Dev
Suite code). Pre-registered on Issue #13 before execution. Not a frozen test. Usage: python3 -I -B <probe> <algorithm_matrix.py>"""
import copy, hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("am", sys.argv[1]); am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
PROTECTED = ("matrix_id", "matrix_data", "active_slots", "governor_context")
def projection_digest(r):
    return hashlib.sha256(json.dumps({k: r.primary.get(k) for k in PROTECTED}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
BASELINE = projection_digest(am.AlgorithmMatrixRuntime())  # witness value recorded out of instance
class Witness:
    def __init__(self, digest, available=True): self._d, self.available = digest, available
    def check(self, digest):
        if not self.available: return "WITNESS_UNAVAILABLE"
        return "OK" if digest == self._d else "IDENTITY_MISMATCH"
def tamper_context(r):
    r.primary["governor_context"]["permission_scope"].append("matrix_data[*]")
    r.primary["governor_context"]["unlock_target"] = "any"; r.primary["active_slots"] = 99
def tamper_slot(r): r.primary["matrix_data"][0]["executable"] = True
def state(r): return {"status": r.primary["status"], "sub_matrices": len(r.sub_matrices), "storage_unlocked": r.storage_unlocked,
                      "audit": [e["event"] + ("" if e["event"] != "DENIED" else ":" + e["reason"]) for e in r.audit]}
def plain(tamper):
    r = am.AlgorithmMatrixRuntime(); tamper(r)
    try: r.run_boot_handshake(); outcome = "completed"
    except PermissionError as e: outcome = "denied: " + str(e)
    return outcome, state(r)
def gated(tamper, witness):  # PROPOSED: compare the protected projection before any alg_001 mutation
    r = am.AlgorithmMatrixRuntime(); tamper(r)
    v = witness.check(projection_digest(r))
    if v != "OK": return "denied before bootstrap: " + v, state(r)
    r.run_boot_handshake(); return "completed", state(r)
none = lambda r: None
print(json.dumps({
 "E17a_context_changed_dev_suite": plain(tamper_context),
 "E17b_slot_changed_dev_suite": plain(tamper_slot),
 "E17c1_context_changed_gated": gated(tamper_context, Witness(BASELINE)),
 "E17c2_witness_unavailable_gated": gated(none, Witness(BASELINE, available=False)),
 "E17c3_matching_gated": gated(none, Witness(BASELINE)),
}, indent=1, ensure_ascii=False))
