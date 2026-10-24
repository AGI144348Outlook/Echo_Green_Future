#!/usr/bin/env python3
"""Claude 00Z F-001 probes Q1-Q4 on GPT's PROPOSED source-pinned coordinator v1 (blob ead6b26), built on the fixture of
GPT's 10-case harness (blob aa56b6a) via its run_case(change) hook. Stub scripts only; the real pinned v3/v5/v4 scripts
are NOT executed. Pre-registered on Issue #13 before execution. Not a frozen test.
Usage: python3 -I -B <this> <PROPOSED-f001-test-source-pinned-coordinator-v1.py>"""
import importlib.util, json, os, sys
spec = importlib.util.spec_from_file_location("h", sys.argv[1]); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
mod = h.mod
EVIL = "import json\nprint(json.dumps({'integrity':'PASS','release':'HOLD','source_pin_authenticated':False,'approval_authenticated':False,'publication_authorization':'ABSENT','ran':'unreviewed'}))\n"
def q1(a, r, t, s, b):  # reviewed stubs say FAIL; swap them for unreviewed PASS stubs after the blob check
    for k, p in s.items(): p.write_text(h.stub(status="FAIL")); b[k] = mod.git_blob(p.read_bytes())
    real = mod.read_json; state = {"done": False}
    def swap_then_read(path, root):
        if not state["done"]:
            state["done"] = True
            for p in s.values(): p.write_text(EVIL)
        return real(path, root)
    mod.read_json = swap_then_read
    h._restore = lambda: setattr(mod, "read_json", real)
def q2(a, r, t, s, b):
    s["receipt_v3"].write_text("import sys\nsys.stdout.write('x' * (%d + 4096))\n" % mod.MAX_JSON); b["receipt_v3"] = mod.git_blob(s["receipt_v3"].read_bytes())
def q3(a, r, t, s, b):
    s["receipt_v3"].write_text("print('[]')\n"); b["receipt_v3"] = mod.git_blob(s["receipt_v3"].read_bytes())
def q4(a, r, t, s, b):  # every path reached through a symlinked PARENT of the artifact root
    link = r.parent.parent / (r.parent.name + "-link"); os.symlink(r.parent, link)
    for k in ("artifact_root", "pins", "receipt", "binding_manifest", "v5_report", "disposition_record"):
        setattr(a, k, getattr(a, k).replace(str(r.parent), str(link), 1))
    h._cleanup = lambda: os.unlink(link)
PROBES = [("Q1_script_swapped_after_blob_check", q1, True, "PASS/HOLD (unreviewed bytes executed)"),
          ("Q2_oversized_stdout", q2, False, "FAIL/HOLD via JSON decode error, not 'exceeds bound'"),
          ("Q3_stage_returns_json_list", q3, False, "FAIL/HOLD with AttributeError text ('list' ... 'get')"),
          ("Q4_symlinked_parent_of_root", q4, True, "PASS/HOLD (parent symlink accepted)")]
out = []
for name, fn, expect_pass, predicted in PROBES:
    h._restore = h._cleanup = lambda: None
    try: res = h.run_case(name, fn, expect_pass); verdict = "as predicted"
    except AssertionError as e: res, verdict = {"assertion": str(e)[:400]}, "NOT as predicted"
    finally: h._restore(); h._cleanup()
    out.append({"probe": name, "predicted": predicted, "verdict": verdict, "result": res})
print(json.dumps(out, indent=1))
