"""Claude 01Z F-001 probes V1-V3 on GPT coordinator v2 (blob 20cc610), via GPT's own harness fixture (blob 5edc210).
Stub scripts only; pre-registered on Issue #13 (6377905839). Usage: python3 -I -B <this> <harness.py>"""
import hashlib, importlib.util, json, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("h", sys.argv[1]); h = importlib.util.module_from_spec(spec)
sys.argv = sys.argv[:1]; spec.loader.exec_module(h); mod = h.mod
LOG = {}
def recorder(log_path):
    # receipt_v3 stand-in: PASS/HOLD, and writes sha256 of the --pins file it actually opened
    return ("import sys, json, hashlib\na=sys.argv\np=a[a.index('--pins')+1]\n"
            f"open({str(log_path)!r},'w').write(hashlib.sha256(open(p,'rb').read()).hexdigest())\n"
            "print(json.dumps({'integrity':'PASS','release':'HOLD','source_pin_authenticated':False,'approval_authenticated':False,'publication_authorization':'ABSENT'}))\n")
def v1(a, r, t, s, b):
    outside = r.parent / "outside"; (outside / "sub").mkdir(parents=True)
    forged = outside / "pins.json"; forged.write_text(json.dumps({"artifacts": {"dataset_a_csv": {"sha256": "0" * 64}}, "forged": True}))
    (r / "link").symlink_to(outside / "sub", target_is_directory=True)
    a.pins = str(r / "link" / ".." / "pins.json")
    log = r.parent / "opened.sha256"
    s["receipt_v3"].write_text(recorder(log)); b["receipt_v3"] = mod.git_blob(s["receipt_v3"].read_bytes())
    LOG.update(checked=hashlib.sha256((r / "pins.json").read_bytes()).hexdigest(), forged=hashlib.sha256(forged.read_bytes()).hexdigest(), log=log)
    def after():
        LOG["opened"] = LOG["log"].read_text() if LOG["log"].exists() else None
    return after
def v2(a, r, t, s, b):
    s["v5_gate"].write_text("print('[]')\n"); b["v5_gate"] = mod.git_blob(s["v5_gate"].read_bytes())
out = {}
res = h.run_case("V1_dotdot_through_symlink", v1, True)
out["V1"] = {"coordinator": [res["integrity"], res["release"], res["issues"]],
             "coordinator_checked_sha256": LOG["checked"], "stage_opened_sha256": LOG["opened"],
             "stage_opened_forged_file": LOG["opened"] == LOG["forged"], "stage_opened_checked_file": LOG["opened"] == LOG["checked"]}
res = h.run_case("V2_list_output", v2, False); out["V2"] = [res["integrity"], res["release"], res["issues"]]
res = h.run_case("V3_oversized", h.oversized, False); out["V3"] = [res["integrity"], res["release"], res["issues"]]
print(json.dumps(out, indent=1))
