"""Echo-GPT bounded noncanonical portfolio runner v1.
Prospective Issue #330 comment 6703130002. Source only; not yet executed.
No Genesis imports, network, paid inference, CI or production effects.
Run after source freeze/review: python3 -I -B portfolio_runner_v1_DRAFT.py
"""
import copy
import hashlib
import importlib.util
import json
import math
import pathlib
import random
import sys

HERE = pathlib.Path(__file__).resolve().parent
SEEDS = tuple(range(1106, 1136))
GLYPHS = tuple("אבגדהוזחטיכלמנסעפצקרשתךםןףץ")
assert len(GLYPHS) == 27 and len(set(GLYPHS)) == 27
VALUES = (1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90)

def load(filename, name):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def ring(seed, n, mode, steps=64):
    """27 identity-preserving indexed positions; synthetic circular target, not semantics."""
    rng = random.Random(seed)
    initial = [rng.random() * 2 * math.pi for _ in range(n)]
    phases = initial[:]
    perm = list(VALUES)
    if mode == "shuffled":
        rng.shuffle(perm)
    history = []
    for tick in range(steps):
        target = (tick * .137 + math.sin(tick * .21)) % (2 * math.pi)
        selected = []
        for i in range(n):
            angle = phases[i]
            glyph_id = min(range(27), key=lambda k: abs(math.atan2(
                math.sin(angle - 2 * math.pi * k / 27),
                math.cos(angle - 2 * math.pi * k / 27))))
            selected.append(glyph_id)
        prediction = (sum(phases) / n) % (2 * math.pi)
        loss = 1 - math.cos(prediction - target)
        history.append(dict(tick=tick, ids=selected, loss=loss))
        old = phases[:]
        for i in range(n):
            drift = .04 * math.sin(.13 * tick + i)
            coupling = 0.0
            if mode in ("coupled", "shuffled", "deformable", "projected"):
                j = (i + 1) % n
                coupling = .08 * math.sin(old[j] - old[i]) * (perm[selected[i]] / 400)
            deform = .015 * math.sin(tick * .17 + i) if mode == "deformable" else 0.0
            phases[i] = (old[i] + drift + coupling + deform) % (2 * math.pi)
    return dict(seed=seed, n=n, mode=mode, projection=list(range(27)),
                history=history, loss=sum(h["loss"] for h in history[32:]) / 32)

def test_portfolio():
    fixture = load("ledger_census_fixture_v1_DRAFT.py", "echo_fixture_v1")
    oracle = load("independent_ledger_oracle_v2_DRAFT.py", "echo_oracle_v2")
    results = []
    def check(name, seed, predicate, details):
        results.append(dict(test=name, seed=seed, passed=bool(predicate), details=details))
    def witness(seed):
        return tuple((a.ident, a.tick, a.source) for a in fixture.arrivals(seed))
    def verify(p, w):
        return oracle.verify(p, w)["errors"]
    def mutation(name, mutate, expected_code, seed=1106):
        p = fixture.ledger(seed)
        w = witness(seed)
        baseline = verify(p, w)
        q = copy.deepcopy(p)
        activated = mutate(q)
        changed = digest(q["events"]) != digest(p["events"])
        errors = verify(q, w)
        detected = expected_code in {e["code"] for e in errors}
        check(name, seed, not baseline and activated and changed and detected,
              dict(activated=activated, trace_changed=changed,
                   expected=expected_code, observed=sorted({e["code"] for e in errors}),
                   clean_errors=baseline))
    for seed in SEEDS:
        p = fixture.ledger(seed)
        w = witness(seed)
        check("T1-conservation", seed, not verify(p, w),
              dict(errors=verify(p, w), census=fixture.census_digest(fixture.arrivals(seed))))
        q = fixture.ledger(seed)
        check("T8-replay", seed, digest(p) == digest(q), dict(sha256=digest(p)))
    def duplicate(q):
        e = next((e for e in q["events"] if e["kind"] == "expire"), None)
        if e is None: return False
        q["events"].append(dict(e, tick=q["ticks"], kind="open_wait"))
        return True
    mutation("T2-duplicate-terminal", duplicate, "double_terminal")
    def missing(q):
        i = next((i for i,e in enumerate(q["events"]) if e["kind"] in ("open_seat","open_wait")), None)
        if i is None: return False
        q["events"].pop(i)
        return True
    mutation("T3-missing-terminal", missing, "missing_terminal")
    def double(q):
        i = next((i for i,e in enumerate(q["events"]) if e["kind"] == "admit"), None)
        if i is None: return False
        q["events"].insert(i+1, dict(q["events"][i]))
        return True
    mutation("T4-double-admission", double, "double_admit")
    def fifo(q):
        ids = [i for i,e in enumerate(q["events"]) if e["kind"] == "admit"]
        if len(ids) < 2: return False
        q["events"][ids[0]]["id"] = q["events"][ids[1]]["id"]
        return True
    mutation("T5-fifo", fifo, "fifo")
    def dwell(q):
        i = next((i for i,e in enumerate(q["events"]) if e["kind"] == "release"), None)
        if i is None: return False
        q["events"][i]["tick"] += 1
        return True
    mutation("T6-dwell", dwell, "dwell_mismatch")
    def expiry(q):
        i = next((i for i,e in enumerate(q["events"]) if e["kind"] == "expire"), None)
        if i is None: return False
        q["events"][i]["tick"] = q["events"][i]["tick"] - 1
        return True
    mutation("T7-expiry", expiry, "early_expire")
    # T9 causal dwell intervention: independent generator intervention,
    # with no-op control; outcome must differ, not necessarily improve.
    for seed in SEEDS:
        p3 = fixture.ledger(seed, dwell=3)
        p5 = fixture.ledger(seed, dwell=5)
        p3copy = fixture.ledger(seed, dwell=3)
        check("T9-dwell-ablation", seed,
              digest(p3["events"]) != digest(p5["events"]) and digest(p3) == digest(p3copy),
              dict(control=digest(p3), intervention=digest(p5)))
    # T10 paired held-out circular loss; no tuning to test seeds.
    for seed in SEEDS:
        for n in (2,3,4):
            variants = {mode:ring(seed,n,mode) for mode in
                        ("uncoupled","coupled","shuffled","deformable","projected","noop")}
            ids_ok = all(v["projection"] == list(range(27)) and
                         all(len(h["ids"]) == n and all(0 <= x < 27 for x in h["ids"])
                             for h in v["history"]) for v in variants.values())
            check("T10-ring-heldout",seed,ids_ok and
                  all(math.isfinite(v["loss"]) for v in variants.values()),
                  dict(n=n, losses={k:round(v["loss"],8) for k,v in variants.items()},
                       coupling_delta=round(variants["coupled"]["loss"] -
                                            variants["uncoupled"]["loss"],8)))
    return results

if __name__ == "__main__":
    rows = test_portfolio()
    print(json.dumps(dict(schema="echo-gpt-portfolio-v1", seeds=list(SEEDS),
                          python=sys.version, results=rows,
                          pass_count=sum(r["passed"] for r in rows),
                          fail_count=sum(not r["passed"] for r in rows)),
                     ensure_ascii=False, sort_keys=True, indent=2))
