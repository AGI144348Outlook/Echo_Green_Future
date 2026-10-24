"""Claude 01Z DISC-002 probe: E19 (ChatGPT run 310 addendum cases R6h, R6i, R6j). Witness and ledgers are in-process
stand-ins (PROPOSED code, not Dev Suite, not an external authority). E19e runs on a scratch copy of Dev Suite blob
f7cf465 with the interleaving injected as in E18; no threads. Pre-registered on Issue #13 (6377905839) before execution.
Not a frozen test. Usage: python3 -I -B <probe> <algorithm_matrix.py>"""
import copy, hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("am", sys.argv[1]); am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
PROTECTED = ("matrix_id", "matrix_data", "active_slots", "governor_context")
def projection_digest(r):
    return hashlib.sha256(json.dumps({k: r.primary.get(k) for k in PROTECTED}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
class E18Ledger:  # exactly my 00Z E18 stand-in: keyed by decision_id only, first row wins silently
    def __init__(self): self.rows = {}
    def append(self, decision_id, row): self.rows.setdefault(decision_id, row); return "DENIED_RECORDED"
class KeyedLedger:  # PROPOSED (run 310 addendum): key (adapter_id, decision_id); the row binds every decision field
    FIELDS = ("projection_digest", "identity_version", "lifecycle_version", "verdict", "reason")
    def __init__(self): self.rows = {}
    def append(self, adapter_id, decision_id, row):
        key, row = (adapter_id, decision_id), {k: row[k] for k in self.FIELDS}
        old = self.rows.get(key)
        if old is None: self.rows[key] = row; return "DENIED_RECORDED", dict(row)
        if old == row: return "DENIED_RECORDED (original receipt)", dict(old)
        return "DECISION_ID_CONFLICT", dict(old)
class Witness:
    def __init__(self, adapter_id, digest): self.adapter_id, self._d, self.state, self.identity_version, self.lifecycle_version = adapter_id, digest, "ACTIVE", 0, 0
    def set_state(self, s): self.state = s; self.lifecycle_version += 1
    def token_e18(self, digest):  # E18 shape: (digest, lifecycle_version), no adapter
        return (digest, self.lifecycle_version) if digest == self._d and self.state == "ACTIVE" else None
    def accept_e18(self, tok): return tok == self.token_e18(self._d)
    def token_scoped(self, digest):  # PROPOSED run 309/310 shape
        return (self.adapter_id, self.identity_version, self.lifecycle_version, digest) if digest == self._d and self.state == "ACTIVE" else None
    def accept_scoped(self, tok):
        if tok is None: return "denied: NO_TOKEN"
        if tok[0] != self.adapter_id: return "denied: ADAPTER_MISMATCH"
        cur = self.token_scoped(self._d)
        if cur is None: return "denied: AUTHORITY_SUSPENDED"
        return "accepted" if tok == cur else "denied: VERSION_CHANGED"
row = lambda reason: {"projection_digest": "d" * 64, "identity_version": 0, "lifecycle_version": 0, "verdict": "DENY", "reason": reason}
out = {}
L = E18Ledger(); a = [L.append("d-1", {"reason": "IDENTITY_MISMATCH"}), L.append("d-1", {"reason": "AUTHORITY_SUSPENDED"})]
out["E19a_E18_ledger_same_id_different_reason"] = a + ["rows=%d" % len(L.rows), "kept reason=" + L.rows["d-1"]["reason"]]
K = KeyedLedger(); K.append("devsuite", "d-1", row("IDENTITY_MISMATCH")); v, kept = K.append("devsuite", "d-1", row("AUTHORITY_SUSPENDED"))
out["E19b_keyed_same_key_different_fields"] = [v, "rows=%d" % len(K.rows), "kept reason=" + kept["reason"]]
K = KeyedLedger(); first = K.append("devsuite", "d-1", row("IDENTITY_MISMATCH")); again = K.append("devsuite", "d-1", row("IDENTITY_MISMATCH"))
out["E19c_keyed_identical_retry"] = [first[0], again[0], "same receipt=%s" % (first[1] == again[1]), "rows=%d" % len(K.rows)]
dg = "e" * 64; dev, gen = Witness("devsuite", dg), Witness("genesis", dg)   # equal projections and versions by construction
out["E19d_cross_adapter_replay"] = {"E18_token_accepted_by_genesis": gen.accept_e18(dev.token_e18(dg)),
                                    "scoped_token_at_genesis": gen.accept_scoped(dev.token_scoped(dg)),
                                    "scoped_token_at_devsuite_control": dev.accept_scoped(dev.token_scoped(dg))}
r = am.AlgorithmMatrixRuntime(); r.run_boot_handshake(); w = Witness("devsuite", projection_digest(r))
stale = w.token_scoped(projection_digest(r)); w.set_state("SUSPENDED"); w.set_state("ACTIVE")
out["E19e_stale_token_after_restore"] = [w.state, w.accept_scoped(stale), "fresh token: " + w.accept_scoped(w.token_scoped(projection_digest(r)))]
print(json.dumps(out, indent=1))
