"""DISC-002 E91 probe (Claude, 2026-11-06 12Z). Exploratory, stdlib only, no network.
Usage: python3 -I DISC-002-queue-seeds-e91-probe.py <path to GPT queue_11z.py, blob e256b0eb>
Part 1: 30-seed sweep (1106..1135) of simulate() + external_oracle() on the shipped code, unchanged.
Part 2: source-text mutants of the shipped code, evaluate() unchanged; which coded tests catch each.
"""
import hashlib, json, sys, types

src = open(sys.argv[1], encoding="utf-8").read()
print("source_sha256", hashlib.sha256(src.encode()).hexdigest())

def load(text):
    m = types.ModuleType("q")
    exec(compile(text, "queue_11z_variant", "exec"), m.__dict__)
    return m

base = load(src)
sched = [.2] * 135 + [.8] * 135
rows = {}
for p in ("drop", "retry", "queue"):
    acc, lost, ages, seat0, fails, exp_low, exp_high, n_low, n_high = [], [], [], [], 0, 0, 0, 0, 0
    for seed in range(1106, 1136):
        r = base.simulate(sched, p, seed=seed)
        o = base.external_oracle(r)
        if not (o["exact"] and o["age_ok"] and o["no_overlap"] and o["phase_ok"] and o["wraps_ok"]):
            fails += 1
        a = len(r["accepted"]); acc.append(a); lost.append(len(r["grant_ids"]) - a); ages.append(o["max_age"])
        seat0.append(sum(1 for x in r["accepted"] if x[4] == 0) / max(a, 1))
        for gid, (st, _) in r["terminal"].items():
            if gid < 135:
                n_low += 1; exp_low += st != "ACCEPTED"
            else:
                n_high += 1; exp_high += st != "ACCEPTED"
    rows[p] = dict(oracle_fail_seeds=fails, accepted_min=min(acc), accepted_max=max(acc),
                   not_accepted_min=min(lost), not_accepted_max=max(lost), max_age_max=max(ages),
                   seat0_share_min=round(min(seat0), 3), seat0_share_max=round(max(seat0), 3),
                   loss_rate_low_half=round(exp_low / n_low, 3), loss_rate_high_half=round(exp_high / n_high, 3))
wins = sum(1 for s in range(1106, 1136)
           if len(base.simulate(sched, "retry", seed=s)["accepted"]) > len(base.simulate(sched, "queue", seed=s)["accepted"]))
print(json.dumps(dict(sweep=rows, retry_beats_queue_seeds=wins, seeds=30), sort_keys=True))

mutants = {
    "M1_cap_off_by_one": [("t-born>=age_cap", "t-born>age_cap")],
    "M2_no_pre_admission_expiry": [("if not broken_expiry:\n            for row", "if False:\n            for row")],
    "M3_blocked_head_to_front": [("            else:\n                waiting.append((gid,born,g,s,tries+1))",
                                  "            else:\n                waiting.insert(0,(gid,born,g,s,tries+1))")],
    "M4_phase_double_step": [("phase=(phase+STEP)%360", "phase=(phase+2*STEP)%360")],
    "M5_dwell_2": [("if t-at<3}", "if t-at<2}")],
    "M6_no_glyph_guard_EQUIV": [(" and g not in [v[0] for v in live.values()]", "")],
    "M7_retry_tries_5": [("if tries<2:", "if tries<5:")],
}
ref = base.evaluate()
for name, edits in mutants.items():
    t = src
    for a, b in edits:
        assert t.count(a) >= 1, (name, a)
        t = t.replace(a, b)
    try:
        e = load(t).evaluate()
        failed = sorted(k for k, v in e["tests"].items() if not v)
        changed = e["counts"] != ref["counts"]
    except Exception as ex:
        failed, changed = ["EXC:" + type(ex).__name__], True
    print(name, "caught_by=" + (",".join(failed) or "none"), "counts_changed=" + str(changed))
