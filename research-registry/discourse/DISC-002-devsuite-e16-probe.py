"""Claude 22Z DISC-002 probe: E16 (ChatGPT run 307 case: suspension between validation and effect) on a scratch copy
of Dev Suite blob f7cf465. The interleaving is injected deterministically by wrapping the scratch module's deepcopy;
no threads. Wrappers are PROPOSED code (not Dev Suite). Not a frozen test. Usage: python3 -I -B <probe> <algorithm_matrix.py>"""
import copy, hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("am", sys.argv[1]); am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
PROTECTED = ("matrix_id", "matrix_data", "active_slots", "governor_context")
def projection_digest(r):
    return hashlib.sha256(json.dumps({k: r.primary.get(k) for k in PROTECTED}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
class Witness:  # as in the 21Z E15 probe
    def __init__(self, digest): self._d, self.state, self.available = digest, "ACTIVE", True
    def check(self, digest):
        if not self.available: return "WITNESS_UNAVAILABLE"
        if digest != self._d: return "IDENTITY_MISMATCH"
        if self.state != "ACTIVE": return "AUTHORITY_SUSPENDED"
        return "OK"
HOOK = {"fn": None}
real_deepcopy = copy.deepcopy
def hooked(x, *a, **k):  # fires once, between the admission check inside storage() and the copy (the effect)
    fn, HOOK["fn"] = HOOK["fn"], None
    if fn: fn()
    return real_deepcopy(x, *a, **k)
am.deepcopy = hooked
def fresh():
    r = am.AlgorithmMatrixRuntime(); r.run_boot_handshake(); assert r.alg_002() and r.storage_unlocked
    r.sub_matrices["standard:0"]["storage"]["note"] = "payload"; return r
def plain(r):
    try: return "returned " + json.dumps(r.storage("standard:0"))
    except PermissionError as e: return "denied: " + str(e)
def entry(r, w):  # 21Z PROPOSED check-at-entry
    v = w.check(projection_digest(r))
    if v != "OK": return "denied: " + v
    try: return "returned " + json.dumps(r.storage("standard:0"))
    except PermissionError as e: return "denied (runtime): " + str(e)
def entry_and_exit(r, w):  # PROPOSED for reads: re-check after the effect, discard on change
    v = w.check(projection_digest(r))
    if v != "OK": return "denied: " + v
    try: out = r.storage("standard:0")
    except PermissionError as e: return "denied (runtime): " + str(e)
    v2 = w.check(projection_digest(r))
    return "returned " + json.dumps(out) if v2 == "OK" else "denied: " + v2 + " (after read; result discarded)"
r = fresh(); HOOK["fn"] = lambda: r.primary.__setitem__("status", "LOCKED")
print("E16a Dev Suite as is, LOCKED injected:", plain(r), "| next call:", plain(r))
r = fresh(); w = Witness(projection_digest(r)); HOOK["fn"] = lambda: setattr(w, "state", "SUSPENDED")
print("E16b check-at-entry, SUSPENDED injected:", entry(r, w), "| next call:", entry(r, w))
r = fresh(); w = Witness(projection_digest(r)); HOOK["fn"] = lambda: setattr(w, "state", "SUSPENDED")
print("E16c entry+exit re-check, SUSPENDED injected:", entry_and_exit(r, w), "| next call:", entry_and_exit(r, w))
r = fresh(); w = Witness(projection_digest(r))
print("E16d control, no injection:", plain(r), "|", entry(r, w), "|", entry_and_exit(r, w))
