"""DISC-002 E84 probe (Claude, 2026-11-06 04Z). Exploratory; synthetic only.

Injects one-line mutants into the IMPLEMENTATION of GPT's Issue #316 source
(contract-000-gpt-multiring-20261104 @ c94cdfde,
contract-000/gpt/experiments/event_ring_mutants_04z.py, blob 1762a0ba)
and re-runs GPT's own run() unchanged, so a check "catches" a mutant only
if that check turns False when the shipped code is broken.
Each mutant is an exact-text replacement that must match exactly once.

Usage: python -I DISC-002-mutant-injection-e84-probe.py <path to event_ring_mutants_04z.py>
No network, packages, files written, or external effects.
"""
import json, sys, types

MUTANTS = [
    ("step_zero", "def __init__(self,step=STEP,", "def __init__(self,step=0,"),
    ("step_reversed", "def __init__(self,step=STEP,", "def __init__(self,step=-STEP,"),
    ("double_tick", "self.occ[g]=s;self.ticks+=1", "self.occ[g]=s;self.ticks+=2"),
    ("hold_same_seat_removed", "if self.occ.get(g)==s or s in self.occ.values():return False",
     "if s in self.occ.values():return False"),
    ("all_guards_removed", "if self.occ.get(g)==s or s in self.occ.values():return False", "pass"),
    ("wrong_glyph_default", "clear=True,wrong=False):", "clear=True,wrong=True):"),
    ("no_clear_default", "def __init__(self,step=STEP,clear=True,", "def __init__(self,step=STEP,clear=False,"),
    ("project_one_domain_only", "  for p in self.projections:p[s]=", "  for p in self.projections[:1]:p[s]="),
    ("one_projection_total", "self.projections=[{} for _ in range(7)]", "self.projections=[{} for _ in range(1)]"),
    ("leave_keeps_occupancy", "s=self.occ.pop(g)", "s=self.occ[g]"),
    ("clear_first_domain_only", "   for p in self.projections:p.pop(s,None)", "   for p in self.projections[:1]:p.pop(s,None)"),
    ("entropy_ignored", "rng.random() < max(0,min(1,1-e if invert else e))", "rng.random() < 0.5"),
    ("entropy_inverted_default", "def events(schedule,seed=1106,invert=False):", "def events(schedule,seed=1106,invert=True):"),
    ("order_ignored", "return [i for i,e in enumerate(schedule)", "return [i for i,e in enumerate(sorted(schedule))"),
]

def load(src):
    m = types.ModuleType("gpt316")
    exec(compile(src, "gpt316", "exec"), m.__dict__)
    return m

def after_27_free_seat(m):
    """Extra probe (not GPT's): after 27 enter/leave pairs, can a fresh glyph still enter seat 0?"""
    r = m.Ring()
    for i in range(27):
        r.enter(i, i); r.leave(i)
    return r.enter(0, 0)

def main(path):
    src = open(path, encoding="utf-8").read()
    base = load(src).run()
    out = {"source": path, "baseline_passed": base["passed"], "baseline_total": base["total"], "mutants": {}}
    for name, old, new in MUTANTS:
        n = src.count(old)
        if n != 1:
            out["mutants"][name] = {"error": f"pattern count {n}"}
            continue
        m = load(src.replace(old, new))
        res = m.run()
        failed = sorted(k for k, v in res["checks"].items() if not v)
        out["mutants"][name] = {"passed": res["passed"], "failed_checks": failed,
                                "survives": not failed, "seat_reusable_after_27": after_27_free_seat(m)}
    out["survivors"] = sorted(k for k, v in out["mutants"].items() if v.get("survives"))
    out["baseline_seat_reusable_after_27"] = after_27_free_seat(load(src))
    print(json.dumps(out, sort_keys=True, indent=1))

if __name__ == "__main__":
    main(sys.argv[1])
