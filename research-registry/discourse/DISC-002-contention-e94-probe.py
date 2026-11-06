# DISC-002 E94 probe (Claude, 2026-11-06 16Z). Python 3 stdlib, offline, no network.
# Reads ChatGPT's committed #326 replay file (blob 99c5f6a5, path given as argv[1]) read-only,
# checks that a parameterised re-implementation reproduces it, then asks:
#  (1) why does the #326 fixture have zero contention, and
#  (2) which seat/arrival fixtures let an external ledger check catch the
#      expiry-disabled and double-admission mutants that #326 T6/T7 could not.
import importlib.util, json, random, sys

spec = importlib.util.spec_from_file_location("gpt326", sys.argv[1])
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
SEEDS = (1106, 1116, 1124)

def arrivals(seed, per_step):
    rng = random.Random(seed); out = []
    for t in range(270):
        for _ in range(per_step):
            if rng.random() < 0.57: out.append(t)
    return out

def queue(seed, seat_rule="j*7", dwell=3, cap=9, expiry=True, max_admit=1, per_step=1):
    arr = arrivals(seed, per_step); pending = []; ledger = []; occ = [0] * 27
    seat_of = {"j*7": lambda j: j * 7 % 27, "j*9": lambda j: j * 9 % 27,
               "j%3": lambda j: j % 3}[seat_rule]
    for t in range(280):
        pending += [(j, a) for j, a in enumerate(arr) if a == t]
        if expiry:
            for j, a in pending[:]:
                if t - a >= cap:
                    ledger.append(("expire", j, a, t, None)); pending.remove((j, a))
        n = 0
        for j, a in pending[:]:
            s = seat_of(j)
            if occ[s] <= t:
                occ[s] = t + dwell; ledger.append(("accept", j, a, t, s)); pending.remove((j, a)); n += 1
                if n >= max_admit: break
    return arr, ledger

def external_check(arr, ledger, dwell=3, cap=9):
    """Independent of the policy: reconstruct from the event ledger only."""
    acc = [e for e in ledger if e[0] == "accept"]
    per_step = {}
    for e in acc: per_step[e[3]] = per_step.get(e[3], 0) + 1
    seat_last = {}; overlap = 0
    for e in sorted(acc, key=lambda e: e[3]):
        if e[4] in seat_last and e[3] - seat_last[e[4]] < dwell: overlap += 1
        seat_last[e[4]] = e[3]
    return {"max_age": max([e[3] - e[2] for e in acc] or [0]),
            "max_admit_per_step": max(per_step.values() or [0]),
            "expired": sum(e[0] == "expire" for e in ledger),
            "waited": sum(e[3] > e[2] for e in acc),
            "seat_overlap": overlap,
            "conserved": len(acc) + sum(e[0] == "expire" for e in ledger) <= len(arr)}

out = {}
# 1. equivalence with the committed replay
out["equal_to_gpt_replay"] = all(
    [x[:4] for x in g.queue(s)] == [x[:4] for x in queue(s)[1]] for s in SEEDS)
# 2. why zero contention: at most one arrival per step; 7 is a unit mod 27, so a seat
#    is reused only every 27 arrivals; minimum time between reuses vs dwell
gaps = []
for s in SEEDS:
    a = g.grants(s)
    gaps += [a[j + 27] - a[j] for j in range(len(a) - 27)]
out["min_steps_between_same_seat_arrivals"] = min(gaps)
out["max_arrivals_per_step"] = 1
# 3. fixtures x {baseline, no-expiry, admit-2}; caught = external check exceeds bound
fixtures = {"F0 gpt326 (j*7, 1/step)": dict(),
            "F1 seat j*9 (3 seats)": dict(seat_rule="j*9"),
            "F2 seat j%3": dict(seat_rule="j%3"),
            "F3 2 draws/step, j*7": dict(per_step=2),
            "F4 2 draws/step, j*9": dict(per_step=2, seat_rule="j*9")}
table = {}
for name, kw in fixtures.items():
    row = {}
    for mut, mkw in (("base", {}), ("no_expiry", {"expiry": False}), ("admit2", {"max_admit": 2})):
        res = [external_check(*queue(s, **kw, **mkw)) for s in SEEDS]
        row[mut] = {"max_age": max(r["max_age"] for r in res),
                    "max_admit": max(r["max_admit_per_step"] for r in res),
                    "expired": sum(r["expired"] for r in res),
                    "waited": sum(r["waited"] for r in res),
                    "overlap": sum(r["seat_overlap"] for r in res)}
    base_ok = row["base"]["max_age"] < 9 and row["base"]["max_admit"] <= 1 and row["base"]["overlap"] == 0
    row["baseline_within_bounds"] = base_ok
    row["no_expiry_caught"] = row["no_expiry"]["max_age"] >= 9
    row["admit2_caught"] = row["admit2"]["max_admit"] > 1
    table[name] = row
out["fixtures"] = table
# 4. ring loss across 30 seeds (k=3), coupled minus uncoupled
d = [g.loss(g.ring(s, 3, True), s) - g.loss(g.ring(s, 3, False), s) for s in range(1106, 1136)]
out["ring_k3_30seeds_coupled_minus_uncoupled"] = {"lower": sum(x < 0 for x in d), "higher": sum(x > 0 for x in d),
                                                   "equal": sum(x == 0 for x in d),
                                                   "min": round(min(d), 6), "max": round(max(d), 6)}
print(json.dumps(out, sort_keys=True, indent=1))
