"""Claude 02Z F-001 probes W0-W3 on GPT coordinator v3 (blob ade012e), via GPT's v2 harness fixture (blob 5edc210) with v3 swapped in.
Stub scripts only; pre-registered on Issue #13 (6378503837). Usage: python3 -I -B <this> <v2-harness.py> <v3.py> <marker-dir>"""
import hashlib, importlib.util, json, os, sys, time
from pathlib import Path
harness, v3path, markdir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
spec = importlib.util.spec_from_file_location("h", harness); h = importlib.util.module_from_spec(spec)
sys.argv = sys.argv[:1]; spec.loader.exec_module(h)
spec = importlib.util.spec_from_file_location("v3", v3path); v3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v3)
h.mod = v3                     # run_case() resolves the global `mod` at call time
OK = {"integrity": "PASS", "release": "HOLD", "source_pin_authenticated": False, "approval_authenticated": False, "publication_authorization": "ABSENT"}
def gate(status, extra=""):
    return extra + "import json\nprint(json.dumps(" + repr(dict(OK, v5_status=status)) + "))\n"
def set_gate(src):
    def change(a, r, t, s, b):
        s["v5_gate"].write_text(src); b["v5_gate"] = v3.git_blob(s["v5_gate"].read_bytes())
    return change
def capture(name, change):
    # run_case asserts integrity; capture the raw coordinator result instead by wrapping coordinate()
    box = {}; orig = v3.coordinate
    def wrapped(a, expected_blobs=None): box["r"] = orig(a, expected_blobs=expected_blobs); box["record_exists"] = os.path.exists(a.disposition_record); return box["r"]
    v3.coordinate = wrapped
    try:
        try: h.run_case(name, change, True)
        except AssertionError: pass
    finally: v3.coordinate = orig
    r = box["r"]; return {"integrity": r["integrity"], "release": r["release"], "readiness": r["readiness"], "editorial_status": r["editorial_status"],
                          "blockers": r["readiness_blockers"], "issues": r["issues"], "disposition_record_exists": box["record_exists"]}
out = {}
out["W0_default_v2_stubs"] = capture("W0a", None)
out["W0_pending_control"] = capture("W0b", set_gate(gate("PENDING")))
LOG = {}
def w1(a, r, t, s, b):
    set_gate(gate("PENDING"))(a, r, t, s, b)
    outside = r.parent / "outside"; (outside / "sub").mkdir(parents=True)
    forged = outside / "pins.json"; forged.write_text(json.dumps({"forged": True}))
    (r / "link").symlink_to(outside / "sub", target_is_directory=True)
    a.pins = str(r / "link" / ".." / "pins.json"); log = r.parent / "opened.sha256"
    s["receipt_v3"].write_text("import sys, json, hashlib\na=sys.argv\np=a[a.index('--pins')+1]\n"
        f"open({str(log)!r},'w').write(hashlib.sha256(open(p,'rb').read()).hexdigest())\nprint(json.dumps({OK!r}))\n")
    b["receipt_v3"] = v3.git_blob(s["receipt_v3"].read_bytes())
    LOG.update(checked=hashlib.sha256((r / "pins.json").read_bytes()).hexdigest(), forged=hashlib.sha256(forged.read_bytes()).hexdigest())
    return lambda: LOG.__setitem__("opened", log.read_text() if log.exists() else None)
w = capture("W1", w1); w["stage_opened_forged_file"] = LOG["opened"] == LOG["forged"]; w["stage_opened_checked_file"] = LOG["opened"] == LOG["checked"]
out["W1_dotdot_through_symlink"] = w
out["W2_recorded_claim_without_record"] = capture("W2", set_gate(gate("RECORDED_UNAUTHENTICATED")))
marker = markdir / "grandchild.marker"
if marker.exists(): marker.unlink()
child = f"import time; time.sleep(6); open({str(marker)!r}, 'w').write('alive')"
spawn = f"import subprocess, sys, time\nsubprocess.Popen([sys.executable, '-I', '-c', {child!r}])\ntime.sleep(8)\n"
t0 = time.monotonic(); w = capture("W3", set_gate(spawn)); w["coordinator_returned_after_s"] = round(time.monotonic() - t0, 2)
w["marker_at_return"] = marker.exists(); time.sleep(3); w["marker_3s_after_return"] = marker.exists()
out["W3_grandchild_outlives_timeout"] = w
print(json.dumps(out, indent=1))
