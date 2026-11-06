"""DISC-002 E100 probe (Claude, 2026-11-06 23Z): first execution of ChatGPT's
NOT-RUN independent ledger oracle draft (INDEPENDENT-LEDGER-ORACLE-DRAFT-20261106-22z.py,
contract-000-gpt-multiring-20261104 @ 79d2671e) against traces from a separate
reference generator written here, plus single-fault mutants.

Usage: python3 -I -B DISC-002-oracle-draft-e100-probe.py <path to GPT oracle draft>
Read-only: the draft is loaded from outside and never modified. Prints one JSON object.
The generator below is a toy for this probe (2 seats, dwell 3, max_age 8, FIFO,
one admit per seat per step); it is not the #330 runner.
"""
import copy, hashlib, importlib.util, json, random, sys

path = sys.argv[1]
src = open(path, "rb").read()
spec = importlib.util.spec_from_file_location("gpt_oracle", path)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
out = {"draft_git_blob": hashlib.sha1(b"blob %d\x00" % len(src) + src).hexdigest()}
SEATS, DWELL, MAX_AGE, H = 2, 3, 8, 40

def gen(seed, p=0.55, release_first=True, finalize=True):
    rng = random.Random(seed); ev = []; q = []; seat = {}; nid = 0; arr = {}
    for t in range(H):
        step = []
        rel = [(s, i) for s, (i, a) in seat.items() if t - a >= DWELL]
        for s, i in rel:
            step.append({"id": i, "kind": "release", "t": t, "seat": s}); del seat[s]
        for i in list(q):
            if t - arr[i] > MAX_AGE:
                step.append({"id": i, "kind": "expire", "t": t, "seat": None}); q.remove(i)
        for _ in range(2 if rng.random() < 0.3 else (1 if rng.random() < p else 0)):
            arr[nid] = t; q.append(nid)
            step.append({"id": nid, "kind": "arrive", "t": t, "seat": None}); nid += 1
        adm = []
        for s in range(SEATS):
            if s not in seat and q:
                i = q.pop(0); seat[s] = (i, t); adm.append({"id": i, "kind": "admit", "t": t, "seat": s})
        if release_first: step += adm
        else:
            rels = [e for e in step if e["kind"] == "release"]
            step = adm + [e for e in step if e["kind"] != "release"] + rels
        ev += step
    if finalize:
        t = H
        for s, (i, a) in sorted(seat.items()):
            ev.append({"id": i, "kind": "release", "t": t + DWELL, "seat": s})
        for i in q:
            ev.append({"id": i, "kind": "expire", "t": t + MAX_AGE + 1, "seat": None})
    return ev

def first(ev, kind):
    return next(k for k, e in enumerate(ev) if e["kind"] == kind)

def mutants(ev):
    m = {}
    e = copy.deepcopy(ev); a = [k for k, x in enumerate(e) if x["kind"] == "admit"]
    # swap ids of two admits at different times (FIFO break)
    e[a[2]]["id"], e[a[3]]["id"] = e[a[3]]["id"], e[a[2]]["id"]; m["fifo_swap"] = e
    e = copy.deepcopy(ev); k = first(e, "release"); del e[k]; m["drop_release_mid"] = e
    e = copy.deepcopy(ev); r = [k for k, x in enumerate(e) if x["kind"] == "release"]; del e[r[-1]]; m["drop_final_release"] = e
    e = copy.deepcopy(ev); k = first(e, "release"); e[k]["t"] -= 1; m["short_dwell"] = e
    e = copy.deepcopy(ev); k = first(e, "admit"); e.insert(k + 1, dict(e[k], seat=1 - e[k]["seat"])); m["double_admit"] = e
    e = copy.deepcopy(ev); k = first(e, "arrive"); e.insert(k + 1, dict(e[k])); m["dup_arrival"] = e
    e = copy.deepcopy(ev); k = first(e, "admit"); e[k]["seat"] = None; m["admit_seat_none"] = e
    e = copy.deepcopy(ev); k = first(e, "admit"); e[k]["seat"] = 7; m["admit_seat_out_of_range"] = e
    e = copy.deepcopy(ev); k = first(e, "release"); e[k]["kind"] = "expire"; m["release_as_expire"] = e
    e = copy.deepcopy(ev); e.append(dict(e[-1], kind="release")); m["double_terminal_tail"] = e
    e = copy.deepcopy(ev); e.append({"id": 10**6, "kind": "arrive", "t": e[-1]["t"], "seat": None}); m["unfinalized_arrival"] = e
    e = copy.deepcopy(ev); i = [x for x in e if x["kind"] == "arrive"][-1]["id"]
    e = [x for x in e if x["id"] != i]; m["drop_whole_lifecycle"] = e
    e = copy.deepcopy(ev); e.append({"id": 10**6 + 1, "kind": "expire", "t": e[-1]["t"], "seat": None}); m["expire_never_arrived"] = e
    return m

def run(ev):
    try:
        r = mod.audit(ev, seats=SEATS, dwell=DWELL, max_age=MAX_AGE)
        return {"n_err": len(r["errors"]), "kinds": sorted({x[0] for x in r["errors"]})}
    except Exception as x:
        return {"exception": type(x).__name__}

seeds = list(range(1100, 1110))
out["valid_release_first"] = [run(gen(s))["n_err"] for s in seeds]
out["valid_admit_before_release_same_step"] = [run(gen(s, release_first=False)) for s in seeds[:3]]
out["valid_no_finalization"] = [run(gen(s, finalize=False)) for s in seeds[:3]]
res = {}
for s in seeds:
    for name, ev in mutants(gen(s)).items():
        r = run(ev); res.setdefault(name, {"detected": 0, "missed": 0, "exception": 0, "kinds": set()})
        if "exception" in r: res[name]["exception"] += 1
        elif r["n_err"]: res[name]["detected"] += 1; res[name]["kinds"] |= set(r["kinds"])
        else: res[name]["missed"] += 1
out["mutants"] = {k: dict(v, kinds=sorted(v["kinds"])) for k, v in res.items()}
bad = [{"id": 0, "kind": "arrive"}, {"id": [1], "kind": "arrive", "t": 0}, {"id": 0, "kind": "arrive", "t": "0"}]
out["malformed"] = [run([b]) if i != 2 else run([{"id": 9, "kind": "arrive", "t": 0, "seat": None}, b]) for i, b in enumerate(bad)]
print(json.dumps(out, sort_keys=True))
