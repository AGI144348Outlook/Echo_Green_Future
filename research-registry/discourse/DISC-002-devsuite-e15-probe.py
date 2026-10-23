"""Claude 21Z DISC-002 probe: ChatGPT run 306 E15 candidates and snapshot()/deepcopy nuances on a scratch copy
of Dev Suite blob f7cf465, plus a PROPOSED out-of-instance witness wrapper (not Dev Suite code). Not a frozen test."""
import copy, hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("am", sys.argv[1]); am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
PROTECTED = ("matrix_id", "matrix_data", "active_slots", "governor_context")
def projection_digest(r):
    return hashlib.sha256(json.dumps({k: r.primary.get(k) for k in PROTECTED}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
class Witness:  # PROPOSED: held outside the runtime instance; the runtime cannot write it
    def __init__(self, digest, version=1): self._d, self._v, self.state, self.available = digest, version, "ACTIVE", True
    def check(self, digest):
        if not self.available: return "WITNESS_UNAVAILABLE"
        if digest != self._d: return "IDENTITY_MISMATCH"
        if self.state != "ACTIVE": return "AUTHORITY_SUSPENDED"
        return "OK"
def guarded_storage(r, w, key):  # PROPOSED admission predicate: pure check, no repair, no write on deny
    verdict = w.check(projection_digest(r))
    if verdict != "OK": return "denied: " + verdict
    try: r.storage(key); return "readable"
    except PermissionError as e: return "denied (runtime): " + str(e)
def fresh():
    r = am.AlgorithmMatrixRuntime(); r.run_boot_handshake(); assert r.alg_002() and r.storage_unlocked; return r
def plain(r):
    try: r.storage("standard:0"); return "readable"
    except PermissionError as e: return "denied: " + str(e)
edits = {
    "E15a matrix_data": lambda r: r.primary["matrix_data"][0].__setitem__("algorithm_id", "forged"),
    "E15b active_slots": lambda r: r.primary.__setitem__("active_slots", 99),
    "E15c governor_context": lambda r: r.primary["governor_context"].__setitem__("governor_id", "other"),
    "E15d submatrix storage": lambda r: r.sub_matrices["standard:0"]["storage"].__setitem__("note", "payload"),
}
print("baseline (Dev Suite as is) and PROPOSED wrapper, after a full handshake:")
for name, edit in edits.items():
    r = fresh(); w = Witness(projection_digest(r)); edit(r)
    print(f"  {name}: baseline={plain(r)} | wrapper={guarded_storage(r, w, 'standard:0')}")
r = fresh(); w = Witness(projection_digest(r)); w.state = "SUSPENDED"; n = len(r.audit); before = copy.deepcopy(r.primary)
print(f"  E15e same digest, witness SUSPENDED: wrapper={guarded_storage(r, w, 'standard:0')} audit+={len(r.audit)-n} primary_unchanged={r.primary == before}")
r = fresh(); w = Witness(projection_digest(r)); w.available = False; n = len(r.audit); before = copy.deepcopy(r.primary)
print(f"  E15f witness unavailable: wrapper={guarded_storage(r, w, 'standard:0')} audit+={len(r.audit)-n} primary_unchanged={r.primary == before}")
r = fresh(); r.primary["status"] = "LOCKED"
print(f"snapshot nuance: before snapshot verified={r.verified} storage_unlocked={r.storage_unlocked}")
s = r.snapshot(); print(f"  after snapshot(): alg_002_status={s['system_state']['alg_002_status']} verified={r.verified} storage_unlocked={r.storage_unlocked}")
r.primary["status"] = "UNLOCKED"; print(f"  status restored to UNLOCKED: storage={plain(r)} (exploratory, not pre-registered)")
n = len(r.audit)
try: r.run_boot_handshake(); hs = "completed"
except Exception as e: hs = f"{type(e).__name__}: {e}"
print(f"  handshake after restore: {hs}; storage={plain(r)}; new audit events={[a.get('event') for a in r.audit[n:]]} (exploratory)")
r = fresh(); got = r.storage("standard:0"); got["note"] = "mutated copy"
print(f"deepcopy nuance: mutating storage() result leaves instance unchanged = {'note' not in r.sub_matrices['standard:0']['storage']}")
