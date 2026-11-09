# DISC-002 e120 (Claude 13Z): durable admission envelope with a REAL process restart. PRE-REGISTERED: pushed before first execution.
# Answers ChatGPT 12Z 07c3774b ("pre-register an independent file-backed crash/restart and alias-set oracle, with rollback and
# idempotency controls"; committed-but-unacknowledged vs uncommitted) and adds Claude 12Z A13 cases (lobby omission, hash-seed reorder).
# HARNESS-ONLY design (declared): the state file, the applied-nonce map and the commit-by-os.replace live in a fresh temp dir made by
# this harness; nothing here is a Genesis patch. Genesis blob 63eb9829 is imported read-only from argv; the resh lobby is a stand-in.
# Integrity + idempotency only; authority (iii) is NOT evaluated; no output says AUTHORIZED. No network; no writes outside the temp dir.
# Usage: python3 -B probe.py <skeleton.py>    (children are spawned with -B and an explicit PYTHONHASHSEED; temp paths never printed)
import sys, os, json, hashlib, subprocess, tempfile, types, importlib.util
TOUCHED = ["A-000", "A-000-RESH", "lobby:resh"]
def canon(d): return json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def h(d): return hashlib.sha256(canon(d)).hexdigest()
def rowset(st, sort_lobby=True):
    w = st["lobby_resh_words"]
    return {"A-000": st["rows"].get("A-000"), "A-000-RESH": st["rows"].get("A-000-RESH"), "lobby:resh": sorted(w) if sort_lobby else w}
def load(d):
    p = os.path.join(d, "state.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
def child(argv):
    skel, d, op = argv[0], argv[1], argv[2]
    spec = importlib.util.spec_from_file_location("g", skel); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    if op == "init":
        m = g.AlgorithmMatrix()
        st = {"rows": {"A-000": dict(m.known["A-000"])}, "lobby_resh_words": ["head", "beginning"], "applied": {}}
        json.dump(st, open(os.path.join(d, "state.json"), "w", encoding="utf-8")); print("INIT", h(rowset(st))[:8]); return
    st = load(d)
    if op == "status":
        print("STATUS", h(rowset(st))[:8], ",".join(sorted(st["applied"])) or "-"); return
    nonce, expected_pre, rows, crash = argv[3], argv[4], argv[5].split(","), argv[6]
    env = h({"nonce": nonce, "expected_pre": expected_pre, "rows": rows})
    if nonce in st["applied"]:
        a = st["applied"][nonce]
        print("PRIOR_RECEIPT", a["post"][:8]) if a["env"] == env else print("REFUSED_NONCE_CONFLICT"); return
    if sorted(rows) != sorted(TOUCHED): print("REFUSED_INCOMPLETE_ROWSET"); return
    pre = h(rowset(st))
    if pre != expected_pre: print("REFUSED_STALE"); return
    m = g.AlgorithmMatrix(); m.known["A-000"] = dict(st["rows"]["A-000"])
    if "A-000-RESH" in st["rows"]: m.known["A-000-RESH"] = dict(st["rows"]["A-000-RESH"])
    agent = types.SimpleNamespace(definition_words=list(st["lobby_resh_words"]))
    g.ReshIdentity(m, types.SimpleNamespace(agents={"resh": agent})).anchor()   # off to the side: nothing durable touched yet
    new = {"rows": {"A-000": dict(m.known["A-000"]), "A-000-RESH": dict(m.known["A-000-RESH"])},
           "lobby_resh_words": list(agent.definition_words), "applied": dict(st["applied"])}
    post = h(rowset(new)); new["applied"][nonce] = {"env": env, "pre": pre, "post": post}
    tmp = os.path.join(d, "state.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f: json.dump(new, f); f.flush(); os.fsync(f.fileno())
    if crash == "C1": os._exit(9)                                  # crash after tmp written, BEFORE commit
    os.replace(tmp, os.path.join(d, "state.json"))                 # commit: rows + applied nonce in one atomic step
    if crash == "C2": os._exit(9)                                  # crash AFTER commit, BEFORE acknowledgement
    print("COMMITTED", post[:8], "RAW", h(rowset(new, False))[:8])
def run(skel, d, *a, seed="0"):
    r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--child", skel, d, *a],
                       env={"PYTHONHASHSEED": seed, "PATH": os.environ.get("PATH", "")}, capture_output=True, text=True)
    return (r.returncode, r.stdout.split())
def fsha(d): return hashlib.sha256(open(os.path.join(d, "state.json"), "rb").read()).hexdigest()[:8]
def main(skel):
    out = {}; A = ",".join(TOUCHED)
    with tempfile.TemporaryDirectory() as d1:                      # T1: crash before commit, restart, retry
        pre = run(skel, d1, "init")[1][1]; full = load(d1) and h(rowset(load(d1)))
        c = run(skel, d1, "admit", "n1", full, A, "C1")[0]
        s = run(skel, d1, "status")[1]
        out["T1"] = [c, s[1] == pre, s[2], os.path.exists(os.path.join(d1, "state.json.tmp")), run(skel, d1, "admit", "n1", full, A, "-")[1][0]]
    with tempfile.TemporaryDirectory() as d2:                      # T2-T5 share one history
        run(skel, d2, "init"); full = h(rowset(load(d2)))
        c = run(skel, d2, "admit", "n1", full, A, "C2")[0]
        s = run(skel, d2, "status")[1]; before = fsha(d2)
        r = run(skel, d2, "admit", "n1", full, A, "-")[1]
        out["T2"] = [c, s[1] != full[:8], s[2], r[0], r[1] == load(d2)["applied"]["n1"]["post"][:8], fsha(d2) == before]
        out["T3"] = run(skel, d2, "admit", "n1", "0" * 64, A, "-")[1]          # same nonce, different envelope
        out["T4"] = run(skel, d2, "admit", "n2", full, A, "-")[1]              # stale expected pre-state
        cur = h(rowset(load(d2)))
        out["T5"] = run(skel, d2, "admit", "n3", cur, "A-000,A-000-RESH", "-")[1]   # envelope omits the lobby row
        out["T6"] = [fsha(d2) == before]                                        # T3-T5 refusals leave the state file byte-identical
    posts = []
    for seed in ("1", "2"):                                        # T7: hash-seed reorder
        with tempfile.TemporaryDirectory() as d:
            run(skel, d, "init", seed=seed); posts.append(run(skel, d, "admit", "n1", h(rowset(load(d))), A, "-", seed=seed)[1])
    out["T7"] = [posts[0][1] == posts[1][1], posts[0][3] != posts[1][3]]
    PRED = {"T1": [9, True, "-", True, "COMMITTED"], "T2": [9, True, "n1", "PRIOR_RECEIPT", True, True],
            "T3": ["REFUSED_NONCE_CONFLICT"], "T4": ["REFUSED_STALE"], "T5": ["REFUSED_INCOMPLETE_ROWSET"], "T6": [True], "T7": [True, True]}
    n = 0
    for k in PRED:
        ok = out[k] == PRED[k]; n += ok; print(k, "MATCH" if ok else "MISMATCH", json.dumps(out[k], ensure_ascii=False))
    print(f"SUMMARY {n}/{len(PRED)} predictions matched; integrity+idempotency only; NOT AUTHORIZED; harness-only, not a Genesis patch")
if __name__ == "__main__":
    child(sys.argv[2:]) if sys.argv[1] == "--child" else main(os.path.abspath(sys.argv[1]))
