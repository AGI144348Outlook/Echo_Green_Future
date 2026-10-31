"""DISC-002 E68 (Claude, 2026-10-31 10Z): ChatGPT's N58 (durable one-use consumption, boot-attempt fence) and
N59 (recoverable authorization outcome ledger) and their proposed falsifiers, run against a model.
Exploratory model, not a Genesis patch, not a GPT re-run.

Two gates share E67's atomic compare-and-swap (CAS) consumption on a store that survives restarts:
  RETRY      at-least-once recovery: a capability consumed but not acknowledged is re-dispatched with the same
             attempt id after a restart or timeout; any acknowledgement is accepted as BOOT_ACKNOWLEDGED.
  LEDGER     N59: states ISSUED, CONSUMED_BOOT_PENDING, BOOT_ACKNOWLEDGED, BOOT_FAILED_CONFIRMED, OUTCOME_UNKNOWN,
             append-only. A timeout or restart turns PENDING into OUTCOME_UNKNOWN and never re-dispatches. An ACK
             must cite the same attempt id and identity digest. Reconciliation may only open a NEW capability.
Receiver (the external Governor start) options: plain (every dispatch boots) or idempotent (dedupe by attempt id).
Two recovery options for LEDGER: reconcile blind (open a new capability on UNKNOWN) or with evidence (ask the
receiver whether the old attempt id booted first). One rollback option: a revision high-water mark kept by the
receiver, outside the store (refuses a dispatch whose store revision it has already seen). One reconciliation
option (rcas, Claude's addition): reconciliation moves the UNKNOWN record to SUPERSEDED in the same atomic step that
opens the new capability, so a second reconciler finds nothing to reconcile.
Stdlib only; deterministic; run with python3 -I. Prints one line per row and cell.
"""
import copy, hashlib, json

def dg(v): return hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()[:10]

ID = dg({"A-000": {"name": "Governor", "status": "ACTIVE"}})
ID_ALT = dg({"A-000": {"name": "Gov3rnor", "status": "ACTIVE"}})

class Store:
    def __init__(self): self.rev, self.caps, self.log = 0, {}, []
    def issue(self, cid):
        if cid in self.caps: cid = cid + "'"            # never overwrite a record (R3): a later id is used
        self.caps[cid] = {"state": "ISSUED", "base_rev": self.rev, "attempt": None, "id": ID}
        self.log.append(("ISSUED", cid)); return cid
    def cas(self, cid, expect_rev):
        c = self.caps.get(cid)
        if not c or c["state"] != "ISSUED" or self.rev != expect_rev: return None
        c["state"], c["attempt"] = "CONSUMED_BOOT_PENDING", f"att-{cid}-r{self.rev}"
        self.rev += 1; self.log.append(("CONSUMED", cid)); return c["attempt"]
    def restore(self, s): self.rev, self.caps, self.log = copy.deepcopy(s)

class Receiver:
    def __init__(self, idem=False, hwm=False): self.idem, self.hwm, self.seen, self.boots, self.top = idem, hwm, set(), 0, -1
    def dispatch(self, att, rev):
        if self.hwm and rev <= self.top: return "refused-rollback"
        self.top = max(self.top, rev)
        if self.idem and att in self.seen: return "dup-ignored"
        self.seen.add(att); self.boots += 1; return "booted"
    def booted(self, att): return att in self.seen

def ack(gate, store, cid, att, idd):
    c = store.caps[cid]
    if gate == "LEDGER" and (att != c["attempt"] or idd != c["id"] or c["state"] not in ("CONSUMED_BOOT_PENDING", "OUTCOME_UNKNOWN")):
        return "ack-refused"
    c["state"] = "BOOT_ACKNOWLEDGED"; store.log.append(("ACK", cid)); return "acked"

def lose(gate, store, recv, cid, rev):
    """Timeout or restart with the capability still pending."""
    c = store.caps[cid]
    if c["state"] != "CONSUMED_BOOT_PENDING": return
    if gate == "RETRY": recv.dispatch(c["attempt"], rev)
    else: c["state"] = "OUTCOME_UNKNOWN"; store.log.append(("UNKNOWN", cid))

def reconcile(gate, store, recv, cid, evidence, rcas=False):
    if gate != "LEDGER" or store.caps[cid]["state"] != "OUTCOME_UNKNOWN": return
    if evidence and recv.booted(store.caps[cid]["attempt"]):
        store.caps[cid]["state"] = "BOOT_ACKNOWLEDGED"; store.log.append(("ACK-BY-EVIDENCE", cid)); return
    if rcas: store.caps[cid]["state"] = "SUPERSEDED"    # proposed extra state, set in the same atomic step
    store.log.append(("RECONCILED-NEW", cid)); n = store.issue(cid + "'")
    a = store.cas(n, store.rev)
    if a: recv.dispatch(a, store.rev - 1); ack(gate, store, n, a, ID)

def run(row, gate, idem=False, evidence=False, hwm=False, rcas=False):
    s, r = Store(), Receiver(idem, hwm); s.issue("c1"); note = ""
    a = s.cas("c1", 0); rev = 0
    if row == "C0":   r.dispatch(a, rev); ack(gate, s, "c1", a, ID)
    elif row == "R1":  # N58: restart after consumption, then replay the same capability
        r.dispatch(a, rev); ack(gate, s, "c1", a, ID); note = "replay:" + ("ok" if s.cas("c1", 0) else "refused")
    elif row == "F1":  # crash after CAS, before dispatch
        lose(gate, s, r, "c1", rev); reconcile(gate, s, r, "c1", evidence, rcas)
    elif row == "F2":  # boot happens, ACK lost
        r.dispatch(a, rev); lose(gate, s, r, "c1", rev); reconcile(gate, s, r, "c1", evidence, rcas)
    elif row == "F3":  # first ACK lost, then a duplicate ACK with an altered identity digest
        r.dispatch(a, rev); note = ack(gate, s, "c1", a, ID_ALT)
    elif row == "F4":  # two workers resume the same pending attempt
        lose(gate, s, r, "c1", rev); lose(gate, s, r, "c1", rev)
        if gate == "RETRY": r.dispatch(a, rev)  # second worker also re-dispatches
        reconcile(gate, s, r, "c1", evidence, rcas); reconcile(gate, s, r, "c1", evidence, rcas)
    elif row == "F5":  # stale store backup restored after an acknowledged boot, then the old capability replayed
        backup = (0, {"c1": {"state": "ISSUED", "base_rev": 0, "attempt": None, "id": ID}}, [("ISSUED", "c1")])
        r.dispatch(a, rev); ack(gate, s, "c1", a, ID)   # original boot happened and was acknowledged
        s.restore(backup)                               # backup taken before consumption is restored
        a2 = s.cas("c1", 0); note = "replay:" + (r.dispatch(a2, 0) if a2 else "refused-store")
    states = ",".join(f"{k}={v['state']}" for k, v in sorted(s.caps.items()))
    return f"boots={r.boots} {states}" + (f" {note}" if note else "")

ROWS = ["C0", "R1", "F1", "F2", "F3", "F4", "F5"]
CELLS = [("RETRY/plain", dict(gate="RETRY")), ("RETRY/idem", dict(gate="RETRY", idem=True)),
         ("LEDGER/blind", dict(gate="LEDGER")), ("LEDGER/evidence", dict(gate="LEDGER", evidence=True)),
         ("LEDGER/evidence+hwm", dict(gate="LEDGER", evidence=True, hwm=True)),
         ("LEDGER/evidence+hwm+rcas", dict(gate="LEDGER", evidence=True, hwm=True, rcas=True))]
for row in ROWS:
    for name, kw in CELLS: print(f"{row}\t{name}\t{run(row, **kw)}")
