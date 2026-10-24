"""Claude 00Z DISC-002 probe: E18 (ChatGPT run 309 ABA case R5b; run 310 R6b/R6c receipt cases) on a scratch copy of
Dev Suite blob f7cf465. Interleaving injected deterministically by wrapping the scratch module's deepcopy; no threads.
Witness and ledger are in-process stand-ins (PROPOSED code, not Dev Suite, not an external authority). Pre-registered on
Issue #13 before execution. Not a frozen test. Usage: python3 -I -B <probe> <algorithm_matrix.py>"""
import copy, hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("am", sys.argv[1]); am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
PROTECTED = ("matrix_id", "matrix_data", "active_slots", "governor_context")
def projection_digest(r):
    return hashlib.sha256(json.dumps({k: r.primary.get(k) for k in PROTECTED}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
class Witness:
    def __init__(self, digest): self._d, self.state, self.lifecycle_version = digest, "ACTIVE", 0
    def set_state(self, s): self.state = s; self.lifecycle_version += 1   # every transition bumps the version
    def token(self, digest):
        if digest != self._d: return None, "IDENTITY_MISMATCH"
        if self.state != "ACTIVE": return None, "AUTHORITY_SUSPENDED"
        return (digest, self.lifecycle_version), "OK"
HOOK = {"fn": None}; real_deepcopy = copy.deepcopy
def hooked(x, *a, **k):
    fn, HOOK["fn"] = HOOK["fn"], None
    if fn: fn()
    return real_deepcopy(x, *a, **k)
am.deepcopy = hooked
def fresh():
    r = am.AlgorithmMatrixRuntime(); r.run_boot_handshake(); r.sub_matrices["standard:0"]["storage"]["note"] = "payload"; return r
def unversioned(r, w):  # 22Z E16c entry+exit re-check: compares digest and ACTIVE only
    t, v = w.token(projection_digest(r))
    if v != "OK": return "denied: " + v
    out = r.storage("standard:0"); t2, v2 = w.token(projection_digest(r))
    return "returned " + json.dumps(out) if v2 == "OK" else "denied: " + v2
def versioned(r, w):  # ChatGPT run 309 PROPOSED: exit token must equal entry token, including lifecycle_version
    t, v = w.token(projection_digest(r))
    if v != "OK": return "denied: " + v
    out = r.storage("standard:0"); t2, v2 = w.token(projection_digest(r))
    if v2 != "OK": return "denied: " + v2
    return "returned " + json.dumps(out) if t2 == t else "denied: VERSION_CHANGED (result discarded)"
def aba(r, w):  # suspended, payload changed while suspended, then restored -- all inside the read window
    def f():
        w.set_state("SUSPENDED"); r.sub_matrices["standard:0"]["storage"]["note"] = "written-while-suspended"; w.set_state("ACTIVE")
    return f
class Ledger:  # stand-in for an external append-only denial ledger
    def __init__(self, fail=False): self.rows, self.fail = {}, fail
    def append(self, decision_id, row):
        if self.fail: raise OSError("ledger unavailable")
        self.rows.setdefault(decision_id, row); return len(self.rows)
def deny(ledger, decision_id, reason):  # ChatGPT run 310 PROPOSED: record before reporting; never claim an unwritten receipt
    try: ledger.append(decision_id, {"reason": reason}); return "DENIED_RECORDED"
    except OSError: return "DENIED_UNRECORDED"
out = {}
r = fresh(); w = Witness(projection_digest(r)); HOOK["fn"] = aba(r, w); out["E18a_ABA_unversioned_entry_exit"] = unversioned(r, w)
r = fresh(); w = Witness(projection_digest(r)); HOOK["fn"] = aba(r, w); out["E18b_ABA_versioned_entry_exit"] = versioned(r, w)
r = fresh(); w = Witness(projection_digest(r)); out["E18c_control_versioned"] = versioned(r, w)
L = Ledger(); out["E18d_deny_twice_same_decision_id"] = [deny(L, "d-1", "IDENTITY_MISMATCH"), deny(L, "d-1", "IDENTITY_MISMATCH"), "ledger rows=%d" % len(L.rows)]
L = Ledger(fail=True); out["E18e_deny_ledger_down"] = [deny(L, "d-2", "IDENTITY_MISMATCH"), "ledger rows=%d" % len(L.rows)]
print(json.dumps(out, indent=1, ensure_ascii=False))
