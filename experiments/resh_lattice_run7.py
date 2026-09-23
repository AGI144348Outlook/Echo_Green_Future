#!/usr/bin/env python3
"""Run #7 — transition from environment repair to lattice-level operation.

The runner first establishes the already-demonstrated runtime context, observes
Workbench lattice output, extracts structural evidence, inventories available
lattice algorithms, ranks them against the observed structural question, then
executes one bounded next operation. This remains an engineered experimental
harness; ranking rules and action vocabulary are experimenter supplied.
"""
from pathlib import Path
import os, re, subprocess, sys, json

ROOT=Path(os.environ.get("RESH_WORKSPACE","agency_workspace/repo")).resolve()
LOG=Path(os.environ.get("RESH_AGENCY_LOG","agency_run7.md")).resolve()
CORE=ROOT/"src/core"
DATA=ROOT/"data/processed"
WORKBENCH=ROOT/"src/algorithms/lattice_workbench.py"

def record(s=""):
    print(s)
    with LOG.open("a",encoding="utf-8") as f: f.write(s+"\n")

def run(path,cwd=DATA,timeout=60):
    env=os.environ.copy()
    env["PYTHONPATH"]=str(CORE)+(os.pathsep+env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    p=subprocess.run([sys.executable,str(path)],cwd=cwd,env=env,text=True,
                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    return p.returncode,p.stdout

LOG.write_text("# Resh Lattice Agency — Run #7\n\n",encoding="utf-8")
record("Objective: move from Workbench troubleshooting to evidence-driven lattice-level operation.")
record("Boundary: supplied Workbench source remains untouched; execution occurs in disposable workspace.")
code,out=run(WORKBENCH)
record(f"Baseline Workbench exit: {code}")
record("Baseline output tail:\n```\n"+"\n".join(out.strip().splitlines()[-20:])+"\n```")
if code:
    record("Status: BASELINE_REGRESSION — stop rather than conceal a changed prerequisite.")
    sys.exit(0)

region=re.search(r"REGION CLOSED after step (\d+)",out)
bricks=re.search(r"Bricks laid \((\d+)\)",out)
flags=re.search(r"Flags closed \((\d+)\)",out)
flag_rows=re.findall(r"^\s+([^\s]+)\s+--\s+(.+)$",out,re.M)
observation={
 "region_closed": bool(region),
 "closure_step": int(region.group(1)) if region else None,
 "brick_count": int(bricks.group(1)) if bricks else None,
 "flag_count": int(flags.group(1)) if flags else None,
 "flags": flag_rows[-(int(flags.group(1)) if flags else 0):] if flags else []
}
record("Structural observation: "+json.dumps(observation,ensure_ascii=False))

candidates=sorted((ROOT/"src/algorithms").glob("lattice_*.py"))
candidates=[p for p in candidates if p.name!="lattice_workbench.py"]
record("Available lattice-level operations: "+json.dumps([p.name for p in candidates]))

# Evidence-derived bounded ranking. The current observation is a closed region,
# so operations whose names directly address regions/constraints/lineage receive
# priority. This policy is explicit so researchers can separate harness design
# from demonstrated behavior.
concepts=[]
if observation["region_closed"]: concepts += ["region","regions"]
if observation["flag_count"]: concepts += ["constraint","constraints","lineage"]
scores=[]
for p in candidates:
    stem=p.stem.lower()
    score=sum(1 for term in concepts if term in stem)
    scores.append((score,p.name,p))
scores.sort(key=lambda x:(-x[0],x[1]))
record("Candidate scores: "+json.dumps([{"algorithm":n,"score":s} for s,n,_ in scores]))
best=scores[0] if scores else None
if not best or best[0]==0:
    record("Decision: no lattice-level operation is justified by the bounded evidence policy.")
    record("Final status: NO_JUSTIFIED_LATTICE_ACTION")
    sys.exit(0)

_,name,path=best
record("Chosen lattice operation: "+json.dumps({"algorithm":name,"reason":"filename semantics overlap observed closed-region/constraint structure","score":best[0]}))
code2,out2=run(path)
record(f"Operation exit: {code2}")
record("Operation output tail:\n```\n"+"\n".join(out2.strip().splitlines()[-30:])+"\n```")
changed=(out2.strip()!=out.strip())
record("Post-action observation: "+json.dumps({"exit_code":code2,"produced_output":bool(out2.strip()),"distinct_from_workbench_output":changed}))
record("Final status: "+("LATTICE_OPERATION_EXECUTED" if code2==0 else "LATTICE_OPERATION_FAILED"))
