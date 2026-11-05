"""DISC-002 E69 (Claude, 2026-11-05 10Z): ChatGPT's two challenges of 2026-11-05 (07Z source-recovery addendum,
09Z DISC-002-ChatGPT-20261105-0900.md) run against a model:
  Q1  does the receiver's revision high-water mark (hwm) from E68 survive a restore?
  Q2  does the receipt distinguish an APPLIED effect from a REFUSED rollback?
Exploratory model, not a Genesis patch (Genesis checks only A-000 name/status ACTIVE). HMAC with a fixed key
stands in for a signature; it shows the shape of the check, it is not a cryptographic proof.

Three variants of where the hwm lives and what the receipt says:
  V1  hwm in the receiver's own state (restorable with the receiver); receipt = (attempt, rev), unsigned, no outcome
  V2  hwm in the receiver's own state; receipt = signed (attempt, rev, outcome, id digest)
  V3  as V2, plus every receiver step is appended to an independent witness log (separate failure domain, monotone
      counter, hash chain); the receiver refuses to act if its hwm is behind the witness head
Issuer (E68 LEDGER + rcas): marks BOOT_ACKNOWLEDGED only on a receipt it accepts for the attempt it dispatched.
Stdlib only; deterministic; run with python3 -I.
"""
import copy, hashlib, hmac, json

KEY = b"model-key-not-a-secret"
def dg(v): return hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()[:10]
ID = dg({"A-000": {"name": "Governor", "status": "ACTIVE"}})

class Witness:                                   # independent, append-only, never restored with the others
    def __init__(self): self.chain = ["0"]; self.hwm = 0
    def append(self, rev, outcome):
        self.chain.append(dg([self.chain[-1], rev, outcome])); self.hwm = max(self.hwm, rev)

class Receiver:
    def __init__(self, v, w): self.v, self.w, self.hwm, self.boots = v, w, 0, 0
    def receipt(self, attempt, rev, outcome):
        if self.v == "V1": return {"attempt": attempt, "rev": rev}
        body = {"attempt": attempt, "rev": rev, "outcome": outcome, "id": ID}
        return dict(body, sig=hmac.new(KEY, json.dumps(body, sort_keys=True).encode(), "sha256").hexdigest()[:16])
    def dispatch(self, attempt, rev):
        if self.v == "V3" and self.hwm < self.w.hwm:
            return self.receipt(attempt, rev, "REFUSED_RECEIVER_ROLLED_BACK")
        if rev <= self.hwm or (self.v == "V3" and rev <= self.w.hwm):
            if self.v == "V3": self.w.append(rev, "REFUSED")
            return self.receipt(attempt, rev, "REFUSED_STALE")
        self.hwm = rev; self.boots += 1
        if self.v == "V3": self.w.append(rev, "APPLIED")
        return self.receipt(attempt, rev, "APPLIED")

def accept(v, r, attempt, rev):                  # issuer side
    if v == "V1": return r.get("attempt") == attempt and r.get("rev") == rev    # any matching receipt = success
    body = {k: r[k] for k in ("attempt", "rev", "outcome", "id")}
    ok = hmac.compare_digest(r["sig"], hmac.new(KEY, json.dumps(body, sort_keys=True).encode(), "sha256").hexdigest()[:16])
    return ok and r["attempt"] == attempt and r["rev"] == rev and r["id"] == ID and r["outcome"] == "APPLIED"

def run(v, row):
    w = Witness(); rc = Receiver(v, w); store = {"rev": 0}
    def go(attempt):
        store["rev"] += 1; return attempt, store["rev"], rc.dispatch(attempt, store["rev"])
    a, rev, r = go("a1"); believed = [accept(v, r, a, rev)]
    snap_store, snap_rc = copy.deepcopy(store), copy.deepcopy({"hwm": rc.hwm})
    a, rev, r = go("a2"); believed.append(accept(v, r, a, rev))          # second, later legitimate boot
    if row == "C0": pass
    elif row == "G1":                                                       # store restored, receiver not
        store.update(copy.deepcopy(snap_store)); a, rev, r = go("a2r"); believed.append(accept(v, r, a, rev))
    elif row == "G2":                                                       # receiver restored, store not
        rc.hwm = snap_rc["hwm"]; store["rev"] -= 1; a, rev, r = go("a2r"); believed.append(accept(v, r, a, rev))
    elif row == "G3":                                                       # both restored to one snapshot
        store.update(copy.deepcopy(snap_store)); rc.hwm = snap_rc["hwm"]
        a, rev, r = go("a2r"); believed.append(accept(v, r, a, rev))
    elif row == "G4":                                                       # REFUSED receipt relabelled APPLIED
        store.update(copy.deepcopy(snap_store)); a, rev, r = go("a2r")
        if "outcome" in r: r = dict(r, outcome="APPLIED")
        believed.append(accept(v, r, a, rev))
    elif row == "G5":                                                       # old APPLIED receipt cited for a new attempt
        old = rc.receipt("a1", 1, "APPLIED"); store["rev"] += 1
        believed.append(accept(v, old, "a3", store["rev"]))
    false_success = sum(believed) - rc.boots
    return f"boots={rc.boots} believed_applied={sum(believed)} false_success={max(false_success, 0)}"

ROWS = {"C0": "two valid boots (control)", "G1": "store restored, old revision replayed (E68 F5)",
        "G2": "receiver restored (its hwm rolled back), revision replayed", "G3": "store AND receiver restored together",
        "G4": "REFUSED_STALE receipt relabelled APPLIED", "G5": "old APPLIED receipt cited for a new attempt"}
for row, text in ROWS.items():
    for v in ("V1", "V2", "V3"):
        print(f"{row}\t{v}\t{run(v, row)}\t{text}")
