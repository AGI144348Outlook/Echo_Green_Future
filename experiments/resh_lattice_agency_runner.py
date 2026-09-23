#!/usr/bin/env python3
"""
Run #5 — bounded Resh/Lattice closed-loop experiment.

This runner does not repair the supplied workbench in advance. It observes a
failed execution, derives candidate actions from the evidence available inside
the isolated workspace, chooses a bounded action deterministically, applies it
only to the disposable workspace, and retests. Every observation/choice/result
is logged so agency claims can be judged from evidence rather than workflow
success.
"""
from pathlib import Path
import os, re, subprocess, sys, json

ROOT = Path(os.environ.get("RESH_WORKSPACE", "agency_workspace/repo")).resolve()
LOG = Path(os.environ.get("RESH_AGENCY_LOG", "agency_run5.md")).resolve()
MAX_TURNS = int(os.environ.get("RESH_MAX_TURNS", "6"))

def record(s=""):
    print(s)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(s + "\n")

def run(cmd, cwd=None, timeout=40):
    p = subprocess.run(cmd, cwd=cwd or ROOT, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=timeout)
    return p.returncode, p.stdout

def inventory():
    return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())

def entrypoint(files):
    preferred = [x for x in files if x.endswith("src/algorithms/lattice_workbench.py")]
    return ROOT / (preferred[0] if preferred else next(x for x in files if x.endswith(".py")))

def diagnose(output, files):
    missing = re.search(r"ModuleNotFoundError: No module named ['\"]([^'\"]+)['\"]", output)
    if missing:
        module = missing.group(1)
        candidates = [x for x in files if Path(x).stem == module]
        return {
            "kind": "missing_module",
            "module": module,
            "evidence": output.strip().splitlines()[-1] if output.strip() else "",
            "candidates": candidates,
        }
    file_missing = re.search(r"FileNotFoundError: .*?['\"]([^'\"]+)['\"]", output)
    if file_missing:
        return {"kind":"missing_file","path":file_missing.group(1),"evidence":output.strip().splitlines()[-1]}
    return {"kind":"unknown","evidence":"\n".join(output.strip().splitlines()[-8:])}

def choose_action(diag, target):
    if diag["kind"] == "missing_module" and diag.get("candidates"):
        module_file = ROOT / diag["candidates"][0]
        # General repair hypothesis: Python cannot see a sibling source directory.
        # Prefer a runtime search-path adapter over modifying unfamiliar source.
        source_dir = module_file.parent
        return {
            "action": "extend_pythonpath",
            "reason": f"Requested module {diag['module']} exists at {module_file.relative_to(ROOT)}; expose its directory without editing workbench source.",
            "path": str(source_dir),
        }
    if diag["kind"] == "missing_file":
        wanted = Path(diag["path"]).name
        matches = [p for p in ROOT.rglob(wanted) if p.is_file()]
        if matches:
            return {
                "action":"run_from_matching_context",
                "reason":f"Requested file {wanted} exists in workspace; retest from its containing context.",
                "cwd":str(matches[0].parent),
            }
    return {"action":"inspect","reason":"No bounded repair is justified by current evidence."}

def execute(target, action, env):
    if action["action"] == "extend_pythonpath":
        old = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = action["path"] + (os.pathsep + old if old else "")
        return run([sys.executable, str(target)], cwd=ROOT, timeout=40)
    if action["action"] == "run_from_matching_context":
        return run([sys.executable, str(target)], cwd=action["cwd"], timeout=40)
    return 125, "No executable action selected."

LOG.write_text("# Resh Lattice Agency — Run #5\n\n", encoding="utf-8")
files = inventory()
target = entrypoint(files)
record(f"Objective: independently progress the supplied workbench toward executable Hebrew-lattice operation.")
record(f"Boundary: disposable workspace only: {ROOT}")
record(f"Target selected from inventory: {target.relative_to(ROOT)}")
record(f"Workspace files observed: {len(files)}")
env = os.environ.copy()

code, out = run([sys.executable, str(target)], cwd=ROOT)
for turn in range(1, MAX_TURNS + 1):
    record(f"\n## Turn {turn}")
    record(f"Observation exit code: {code}")
    record("Observation tail:\n```\n" + "\n".join(out.strip().splitlines()[-12:]) + "\n```")
    if code == 0:
        record("Decision: target executed successfully; stop repair loop and preserve output for lattice-stage evaluation.")
        break
    diag = diagnose(out, files)
    record("Diagnosis: " + json.dumps(diag, ensure_ascii=False))
    action = choose_action(diag, target)
    record("Chosen action: " + json.dumps(action, ensure_ascii=False))
    if action["action"] == "inspect":
        record("Decision: stop rather than invent an unsupported modification.")
        break
    code, out = execute(target, action, env)
else:
    record("Iteration budget exhausted.")

record(f"\nFinal exit code: {code}")
record("Final status: " + ("WORKBENCH_EXECUTED" if code == 0 else "UNRESOLVED"))
sys.exit(0)
