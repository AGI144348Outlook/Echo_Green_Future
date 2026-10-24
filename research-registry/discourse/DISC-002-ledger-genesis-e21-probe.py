"""Claude 03Z DISC-002 probe: E21 (ChatGPT run 312: R6k receipt/request key binding; Genesis A-000 writer paths).
E21a-d: the ledger, consumers and HMAC witness are in-process PROPOSED stand-ins, not an external authority.
E21e-f: run on a scratch copy of Genesis src/echo_governor_skeleton.py blob 63eb982 (classes used on a stub matrix).
Pre-registered on Issue #13 (6379049975) before execution. Not a frozen test.
Usage: python3 -I -B <probe> <echo_governor_skeleton.py>"""
import hashlib, hmac, importlib.util, json, sys

FIELDS = ("adapter_id", "decision_id", "projection_digest", "identity_version", "lifecycle_version", "verdict", "reason")
def receipt(adapter_id, decision_id, reason="IDENTITY_MISMATCH"):
    return {"adapter_id": adapter_id, "decision_id": decision_id, "projection_digest": "pd-" + decision_id,
            "identity_version": 3, "lifecycle_version": 1, "verdict": "DENIED", "reason": reason}

class BuggyLedger:  # lookup ignores decision_id (stand-in for an index bug); stores receipts by full key
    def __init__(self): self.rows = {}
    def append(self, r): self.rows[(r["adapter_id"], r["decision_id"])] = dict(r)
    def lookup(self, adapter_id, decision_id):
        for (a, _d), r in self.rows.items():
            if a == adapter_id: return dict(r)
        return None

def naive_consumer(ledger, req):
    r = ledger.lookup(req["adapter_id"], req["decision_id"])
    return "DENIED_RECORDED" if r and r.get("verdict") == "DENIED" else "DENIED_UNRECORDED"

def r6k_consumer(ledger, req, verify=None):
    r = ledger.lookup(req["adapter_id"], req["decision_id"])
    if r is None: return "DENIED_UNRECORDED"
    if (r.get("adapter_id"), r.get("decision_id")) != (req["adapter_id"], req["decision_id"]): return "DENIED_UNRECORDED: RECEIPT_KEY_MISMATCH"
    if any(r.get(k) != req[k] for k in FIELDS if k in req): return "DENIED_UNRECORDED: RECEIPT_FIELD_MISMATCH"
    if verify is not None and not verify(r): return "DENIED_UNRECORDED: RECEIPT_UNAUTHENTICATED"
    return "DENIED_RECORDED"

class HmacWitness:  # PROPOSED stand-in: the adapter is never handed this object or its key
    def __init__(self): self._k = hashlib.sha256(b"witness-secret-stand-in").digest()
    def _mac(self, r): return hmac.new(self._k, json.dumps({k: r[k] for k in FIELDS}, sort_keys=True).encode(), "sha256").hexdigest()
    def sign(self, r): s = dict(r); s["mac"] = self._mac(r); return s
    def verify(self, r): return isinstance(r.get("mac"), str) and hmac.compare_digest(r["mac"], self._mac(r))

out = {}
L = BuggyLedger(); L.append(receipt("devsuite", "d-1", reason="AUTHORITY_SUSPENDED"))
req2 = receipt("devsuite", "d-2")
out["E21a_naive_consumer_wrong_receipt"] = {"asked": "d-2", "lookup_returned": L.lookup("devsuite", "d-2")["decision_id"], "consumer_says": naive_consumer(L, req2)}
out["E21b_r6k_consumer_wrong_receipt"] = r6k_consumer(L, req2)
F = BuggyLedger(); F.append(receipt("devsuite", "d-2"))   # adapter writes its own matching receipt
out["E21c_forged_matching_receipt_r6k_only"] = r6k_consumer(F, req2)
W = HmacWitness(); G = BuggyLedger(); G.append(W.sign(receipt("devsuite", "d-2")))
out["E21d_hmac_witness"] = {"genuine": r6k_consumer(G, req2, W.verify), "forged_unsigned": r6k_consumer(F, req2, W.verify),
    "forged_with_guessed_mac": r6k_consumer(type("X", (), {"lookup": lambda s, a, d: dict(receipt("devsuite", "d-2"), mac="0" * 64)})(), req2, W.verify)}

spec = importlib.util.spec_from_file_location("gov", sys.argv[1]); gov = importlib.util.module_from_spec(spec); spec.loader.exec_module(gov)
class StubMatrix:
    def __init__(self): self.known = {"A-000": {"name": "Governor", "status": "ACTIVE"}}
class StubAyin:
    def agentive_entities(self, min_ties=1): return []
m = StubMatrix(); resh = gov.ReshIdentity(m); resh.anchor()
baseline = json.loads(json.dumps(m.known["A-000"]))
m.known["A-000"]["identity_symbol"] = "X"; m.known["A-000"]["name"] = "Impostor"
valid_before = resh.validate()
stub = type("PeStub", (), {})(); stub.resh, stub.ayin = resh, StubAyin()
stub.exchange = lambda word, turns=3: []
logs = gov.PeCommunicator.open_exchanges(stub)
out["E21e_open_exchanges_after_mismatch"] = {"validate_before": valid_before, "returned": logs, "validate_after": resh.validate(),
    "identity_symbol_after": m.known["A-000"].get("identity_symbol"), "name_after": m.known["A-000"].get("name"),
    "a000_equals_baseline": m.known["A-000"] == baseline, "denial_or_trace": False}
m2 = StubMatrix(); r2 = gov.ReshIdentity(m2); r2.anchor(); m2.known["A-000"]["name"] = "Impostor"; m2.known["A-000"]["status"] = "RETIRED"
out["E21f_non_identity_field_change"] = {"validate": r2.validate(), "name": m2.known["A-000"]["name"], "status": m2.known["A-000"]["status"]}
print(json.dumps(out, indent=1, ensure_ascii=False))
