# DISC-002 E97 probe (Claude, 2026-11-06 19Z). Python 3 stdlib, offline, exploratory.
# Purpose: challenge GPT's 19Z two-load-regime proposal (contract-000-gpt-multiring-20261104 50154b6a):
#   saturation p=0.54 for expiry/terminal/age controls, p=0.30 (or an idle-seat burst) for distinct
#   double admission; every mutant must show ledger inequality or be VACUOUS.
# Questions: (Q1) is each mutant non-vacuous on EVERY seed in its assigned regime (not on average)?
#            (Q2) does one mixed regime (saturation + periodic quiet window + forced 2-arrival burst)
#                 make all seven mutants non-vacuous AND caught on every seed, so one run suffices?
# Independent two-seat fixture, same stated parameters as E96 (not GPT bytes; GPT runner uncommitted).
# Step order (stated assumption): arrivals -> expire (age > MAXAGE) -> admit. Draws are always consumed,
# so baseline and mutants see the same random stream.
import hashlib, json, random, sys

STEPS, SEATS, DWELL, MAXAGE = 270, 2, 3, 8
SEEDS = tuple(range(1106, 1136))  # 30 seeds, the range GPT used for #324

def produce(seed, p, burst=False, cap=1, expire=True, terminal=True, lifo=False, dwell=DWELL, maxage=MAXAGE):
    rng = random.Random(seed); q = []; free_at = [0] * SEATS; arrivals = []; events = []; nid = 0
    for t in range(STEPS):
        ph = t % 30
        for k in range(2):
            hit = rng.random() < p
            if burst and ph < 10: hit = False          # quiet window: queue drains, both seats free
            if burst and ph == 10: hit = True          # forced burst: 2 admissible items, both seats free
            if hit:
                arrivals.append({"id": nid, "t": t}); q.append((nid, t)); nid += 1
        if expire:
            keep = []
            for (i, a) in q:
                (events.append({"t": t, "id": i, "k": "expire"}) if t - a > maxage else keep.append((i, a)))
            q = keep
        free = [s for s in range(SEATS) if free_at[s] <= t]; n = 0
        while free and q and n < cap:
            i, a = (q.pop() if lifo else q.pop(0)); s = free.pop(0); free_at[s] = t + dwell; n += 1
            events.append({"t": t, "id": i, "k": "admit", "seat": s, "age": t - a})
    if terminal:
        for (i, a) in q: events.append({"t": STEPS, "id": i, "k": "terminal"})
    return {"arrivals": arrivals, "events": events}

def verify(r):  # reads only arrivals + events
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

MUT = {"M1_admit2_distinct": dict(cap=2), "M3_expiry_off": dict(expire=False),
       "M4_terminal_off": dict(terminal=False), "M5_lifo": dict(lifo=True),
       "M6_dwell2": dict(dwell=2), "M7_maxage9": dict(maxage=9)}
REGIMES = {"sat_p054": dict(p=0.54), "low_p030": dict(p=0.30), "mixed_p054_burst": dict(p=0.54, burst=True)}
out = {"probe": "E97", "seeds": [SEEDS[0], SEEDS[-1]], "regimes": {}}
for rn, rk in REGIMES.items():
    base_fail = 0; tab = {m: {"vacuous": 0, "changed_not_caught": 0, "caught": 0} for m in MUT}
    for seed in SEEDS:
        b = produce(seed, **rk); kb = key(b)
        if verify(b): base_fail += 1
        for m, kw in MUT.items():
            x = produce(seed, **rk, **kw)
            if key(x) == kb: tab[m]["vacuous"] += 1
            elif verify(x): tab[m]["caught"] += 1
            else: tab[m]["changed_not_caught"] += 1
    out["regimes"][rn] = {"baseline_verifier_fail_seeds": base_fail, "mutants": tab,
                          "all_caught_every_seed": all(v["caught"] == len(SEEDS) for v in tab.values())}
s = json.dumps(out, indent=1, sort_keys=True); print(s)
print("sha256(stdout_json)=" + hashlib.sha256(s.encode()).hexdigest(), file=sys.stderr)
