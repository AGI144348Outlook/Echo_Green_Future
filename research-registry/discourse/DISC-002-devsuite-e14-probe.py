"""Claude 19Z DISC-002 probe: Dev Suite alg_002() re-check scope (scratch copy of blob f7cf465). Not a frozen test."""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("am", sys.argv[1]); am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
def fresh():
    r = am.AlgorithmMatrixRuntime(); r.run_boot_handshake(); assert r.alg_002() and r.storage_unlocked; return r
def report(tag, r, extra=""):
    try: s = r.storage("standard:0"); sto = "readable"
    except PermissionError as e: sto = "denied: " + str(e)
    print(f"{tag}: alg_002={r.alg_002()} storage={sto} {extra}")
r = fresh(); r.primary["matrix_data"][0]["algorithm_id"] = "forged"; report("(a) matrix_data changed", r)
r = fresh(); r.primary["governor_context"]["governor_id"] = "other"; report("(b) governor_context changed", r)
r = fresh(); r.primary["active_slots"] = 99; report("(c) active_slots=99", r)
r = fresh(); r.primary["matrix_data"][0]["algorithm_id"] = "forged"; n = len(r.audit); r.run_boot_handshake()
report("(d) handshake after (a)", r, f"new audit events={r.audit[n:]}")
r = fresh(); r.sub_matrices["standard:0"]["storage"]["note"] = "sub-agent payload"; report("(e) storage payload write", r, f"value={r.storage('standard:0') if r.alg_002() else None}")
r = fresh(); r.primary["status"] = "LOCKED"; report("(f) status LOCKED", r, f"verified={r.verified} storage_unlocked={r.storage_unlocked}")
r = fresh(); r.primary["status"] = "LOCKED"
print(f"(f2) before any check: verified={r.verified} storage_unlocked={r.storage_unlocked}")
v = r.alg_002(); print(f"(f2) after alg_002()={v}: verified={r.verified} storage_unlocked={r.storage_unlocked}")
