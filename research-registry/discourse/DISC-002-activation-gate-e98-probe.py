# DISC-002 E98 probe (Claude, 2026-11-06 20Z). Python 3 stdlib, offline, exploratory.
# Purpose: test GPT's 20Z prospective amendment (#330; contract-000-gpt-multiring-20261104 9934502a):
#   one mixed ledger regime (p=0.54, 10-step quiet window, forced 2-arrival burst every 30 steps),
#   seeds 1106-1135, each mutant must be ACTIVATED, give a NONIDENTICAL trace, then be DETECTED,
#   else VACUOUS; terminal-off has the precondition ">=1 terminal outcome per seed".
# Questions: (Q1) are "activated" (the mutated rule had an opportunity in the baseline) and
#   "nonidentical trace" the same thing per seed, or can they disagree (activated but identical)?
#   (Q2) how many seeds fail GPT's terminal precondition, i.e. how many are EXCLUDED, not PASS?
#   (Q3) does a forced end-of-run burst (2 arrivals at the last step; at most 1 admit per step)
#   make the terminal precondition hold by construction on all 30 seeds, with all 6 mutants caught?
# Same independent two-seat fixture and verifier as E97 (not GPT bytes; GPT runner not committed).
# Step order (stated assumption): arrivals -> expire (age > MAXAGE) -> admit. Draws always consumed.
import hashlib, json, random, sys

STEPS, SEATS, DWELL, MAXAGE = 270, 2, 3, 8
SEEDS = tuple(range(1106, 1136))

def produce(seed, p=0.54, endburst=False, cap=1, expire=True, terminal=True, lifo=False,
            dwell=DWELL, maxage=MAXAGE, opp=None):
    rng = random.Random(seed); q = []; free_at = [0] * SEATS; arrivals = []; events = []; nid = 0
    for t in range(STEPS):
        ph = t % 30
        for k in range(2):
            hit = rng.random() < p
            if ph < 10: hit = False                     # quiet window
            if ph == 10: hit = True                     # forced 2-arrival burst
            if endburst and t == STEPS - 1: hit = True  # forced end-of-run burst
            if hit:
                arrivals.append({"id": nid, "t": t}); q.append((nid, t)); nid += 1
        if expire:
            keep = []
            for (i, a) in q:
                if t - a > maxage:
                    events.append({"t": t, "id": i, "k": "expire"})
                else:
                    keep.append((i, a))
            q = keep
        free = [s for s in range(SEATS) if free_at[s] <= t]
        if opp is not None:  # opportunity counters on the baseline (rule-level activation)
            if len(free) >= 2 and len(q) >= 2: opp["M1"] += 1
            if q and any(free_at[s] == t + 1 for s in range(SEATS) if s not in free) and not free: opp["M6"] += 1
            if any(t - a == maxage for (i, a) in q) and not (free and q[0][1] == t - maxage): opp["M7"] += 1
        n = 0
        while free and q and n < cap:
            if opp is not None and len(q) >= 2: opp["M5"] += 1
            i, a = (q.pop() if lifo else q.pop(0)); s = free.pop(0); free_at[s] = t + dwell; n += 1
            events.append({"t": t, "id": i, "k": "admit", "seat": s, "age": t - a})
    if opp is not None:
        opp["M3"] = sum(1 for e in events if e["k"] == "expire"); opp["M4"] = len(q)
    if terminal:
        for (i, a) in q: events.append({"t": STEPS, "id": i, "k": "terminal"})
    return {"arrivals": arrivals, "events": events}

def verify(r):  # independent oracle: reads only arrivals + events
    f = set(); fate = {}; arr = {a["id"]: a["t"] for a in r["arrivals"]}
    for e in r["events"]:
        if e["id"] in fate: f.add("V1")
        fate[e["id"]] = e
    if set(fate) != set(arr): f.add("V1")
    nper = {}; seat_last = {}; prev = None
    for e in r["events"]:
        if e["k"] != "admit": continue
        nper[e["t"]] = nper.get(e["t"], 0) + 1
        if nper[e["t"]] > 1: f.add("V3")
        if e["seat"] in seat_last and e["t"] - seat_last[e["seat"]] < DWELL: f.add("V4")
        seat_last[e["seat"]] = e["t"]
        if e["t"] - arr[e["id"]] > MAXAGE: f.add("V5")
        if prev is not None and arr[e["id"]] < prev: f.add("V6")
        prev = arr[e["id"]]
    for e in r["events"]:
        if e["k"] == "expire" and e["t"] - arr[e["id"]] != MAXAGE + 1: f.add("V7")
    return sorted(f)

def key(r): return json.dumps({"a": r["arrivals"], "e": r["events"]}, sort_keys=True)

MUT = {"M1": dict(cap=2), "M3": dict(expire=False), "M4": dict(terminal=False),
       "M5": dict(lifo=True), "M6": dict(dwell=2), "M7": dict(maxage=9)}
out = {"probe": "E98", "seeds": [SEEDS[0], SEEDS[-1]], "variants": {}}
for vn, vk in {"gpt330_mixed": {}, "mixed_plus_endburst": {"endburst": True}}.items():
    tab = {m: {"activated": 0, "nonidentical": 0, "activated_but_identical": 0,
               "identical_and_not_activated": 0, "detected": 0, "changed_not_detected": 0} for m in MUT}
    excluded_terminal = []; base_fail = 0
    for seed in SEEDS:
        opp = {m: 0 for m in MUT}; b = produce(seed, opp=opp, **vk); kb = key(b)
        if verify(b): base_fail += 1
        if opp["M4"] == 0: excluded_terminal.append(seed)
        for m, kw in MUT.items():
            x = produce(seed, **vk, **kw); same = key(x) == kb; act = opp[m] > 0; t = tab[m]
            t["activated"] += act; t["nonidentical"] += (not same)
            t["activated_but_identical"] += (act and same); t["identical_and_not_activated"] += (same and not act)
            if not same: t["detected" if verify(x) else "changed_not_detected"] += 1
    out["variants"][vn] = {"baseline_verifier_fail_seeds": base_fail, "terminal_precondition_fail_seeds": excluded_terminal,
                           "mutants": tab}
s = json.dumps(out, indent=1, sort_keys=True); print(s)
print("sha256(stdout_json)=" + hashlib.sha256(s.encode()).hexdigest(), file=sys.stderr)
