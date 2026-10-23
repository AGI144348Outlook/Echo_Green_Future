#!/usr/bin/env python3
"""Claude 23Z F-001 probes P1-P4 on GPT's PROPOSED receipt-v4 binding preflight (blob 848040f), using the C0 fixture
of GPT's 14-case harness (blob a8ecd5b). Synthetic JSON only; pre-registered on Issue #13 before execution.
Not a frozen test. Usage: python3 -I -B <this> <PROPOSED-f001-receipt-v4-binding.py> <PROPOSED-f001-test-receipt-v4-binding.py>"""
import importlib.util, json, os, subprocess, sys, tempfile
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
v4 = load("v4", sys.argv[1]); harness = load("h", sys.argv[2])
def p1(v): v[3]["publish"] = "READY"
def p2(v): v[2]["artifacts_checked"][0]["approved"] = True
def p3(v): v[0]["artifacts"]["epub"] = []
def p4(v): v[3]["v5_status"] = "RECORDED_UNAUTHENTICATED"  # self-declared v5_report_sha256 left unchanged
PROBES = [("P1_v5_extra_top_key", p1, "PASS/HOLD"), ("P2_v3_item_extra_key", p2, "PASS/HOLD"),
          ("P3_pin_artifact_list", p3, "AttributeError; CLI traceback, no JSON"), ("P4_v5_bytes_changed_digest_kept", p4, "PASS/HOLD")]
out = []
for name, fn, expected in PROBES:
    vals = harness.fixture(); fn(vals)
    try:
        r = v4.check_binding(*vals); pure = r["integrity"] + "/" + r["release"] + " " + json.dumps(r["issues"])
    except Exception as e:
        pure = "raised " + type(e).__name__
    with tempfile.TemporaryDirectory() as d:
        args = []
        for key, val in zip(("pins", "receipt", "v3-result", "v5-result", "binding-manifest"), vals):
            p = os.path.join(d, key + ".json"); open(p, "w").write(json.dumps(val)); args += ["--" + key, p]
        cp = subprocess.run([sys.executable, "-I", "-B", sys.argv[1]] + args, capture_output=True, text=True, timeout=5)
        try: cli = json.loads(cp.stdout)["integrity"] + "/HOLD"
        except Exception: cli = "no JSON; stderr last line: " + (cp.stderr.strip().splitlines() or [""])[-1]
    out.append({"probe": name, "expected": expected, "pure": pure, "cli_exit": cp.returncode, "cli": cli})
print(json.dumps(out, indent=1))
