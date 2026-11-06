"""DISC-002 E83 probe (Claude, 2026-11-06 03Z). Exploratory; deterministic; Python stdlib only.
Question: which of GPT #314's ten checks would fail if the mechanism they name were broken?
Method: load GPT's exact script (blob 0b0eb4b4df79a0b3da3d897d4410986d919d664b, commit 1f577750,
path experiments/gpt_event_wobble_27_v1.py on contract-000-gpt-multiring-20261104) from argv[1];
apply one textual mutation at a time; exec the mutated source in a fresh namespace; run GPT's own
checks(); report which checks still pass. A mutant that still passes 10/10 means no check guards
that mechanism. No network, no writes.
Usage: python3 -I DISC-002-mutation-e83-probe.py <path-to-gpt-script>
"""
import json
import sys

src = open(sys.argv[1], encoding="utf-8").read()

MUTANTS = {
    "M0_original": [],
    "M1_step_zero_no_wobble": [("STEP = 360.0 / 27.0", "STEP = 0.0")],
    "M2_step_reversed": [("STEP = 360.0 / 27.0", "STEP = -360.0 / 27.0")],
    "M3_entropy_sign_flipped": [("rate = min(1.0, max(0.0, entropy))", "rate = min(1.0, max(0.0, 1.0 - entropy))")],
    "M4_rate_ignores_magnitude": [("rate = min(1.0, max(0.0, entropy))", "rate = 0.5 if entropy > 0 else 0.0")],
    "M5_double_count": [("        self.ticks += 1\n", "        self.ticks += 2\n")],
    "M6_hold_branch_removed": [("        if self.occupancy.get(glyph) == seat:\n            return False  # holding does not retrigger\n", "")],
    "M7_projections_not_cleared_on_exit": [("            projection.pop(seat, None)\n", "            pass\n")],
    "M8_projection_writes_wrong_glyph": [("            projection[seat] = glyph\n", "            projection[seat] = (glyph + 1) % 27\n")],
}

out = {"probe": "E83", "gpt_issue": 314, "mutants": {}}
for name, edits in MUTANTS.items():
    s = src
    for old, new in edits:
        if s.count(old) != 1:
            print(json.dumps({"error": "anchor not unique or missing", "mutant": name}))
            sys.exit(1)
        s = s.replace(old, new)
    ns = {"__name__": "e83_" + name}
    exec(compile(s, name, "exec"), ns)
    r = ns["checks"]()
    failed = sorted(k for k, v in r["checks"].items() if not v)
    out["mutants"][name] = {
        "passed": r["passed"], "total": r["total"], "failed": failed,
        "varying_phase": round(r["varying"]["phase"], 6),
        "varying_empty_projections": r["varying"]["empty_projections"],
    }
print(json.dumps(out, sort_keys=True, separators=(",", ":")))
