#!/usr/bin/env python3
"""Trial 015 — Governed Notebook Manipulation.

Purpose: test whether a selector can choose an admissible Hebrew operation and
Mashet tool from repository registries for a novel goal, then execute one
small Notebook transformation without mutating its sources.

Research constraint: this harness does NOT claim autonomous agency. The
selection policy below is explicit, deterministic code. Its choices are
logged as HARNESS_POLICY until a genuine ECHO deliberation/selection interface
is wired in.
"""
from __future__ import annotations
import copy, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
load=lambda p: json.loads((ROOT/p).read_text(encoding="utf-8"))

GOAL="Create a new working object that preserves the information contained in both Notebook objects A and B. Do not alter A or B."
# trigger: Trial 015 baseline execution 2026-09-25 — rerun after syntax fix
A={"handle":"N::X::A","value":["alpha"],"status":"WORKING"}
B={"handle":"N::X::B","value":["beta"],"status":"WORKING"}

def choose_hebrew(goal, glyphs):
    # Explicit baseline policy, not an ECHO-authored choice.
    candidates=[r for r in glyphs["records"] if r["operation"] in {"CONNECT","CONTAIN","TRANSFORM"}]
    score={"CONNECT":3,"CONTAIN":1,"TRANSFORM":1}
    return max(candidates,key=lambda r:score[r["operation"]])

def choose_mashet(goal, manual):
    # Explicit baseline policy derived only from instruction-card roles.
    tokens=set(goal.lower().replace(".","").split())
    def score(c):
        role=c["source_role"].lower()
        s=0
        if "new" in tokens and ("composition" in role or "summation" in role): s+=3
        if "both" in tokens and "composition" in role: s+=2
        if "preserves" in tokens and c["id"]=="M::COMPOSE": s+=2
        if c.get("execution")!="WORKING": s-=100
        return s
    ranked=sorted(manual["cards"],key=lambda c:(score(c),c["id"]),reverse=True)
    return ranked[0],[(c["id"],score(c)) for c in ranked]

def main():
    glyphs=load("matrices/glyphs/hebrew_glyph_registry.json")
    manual=load("matrices/symbols/mashet_instruction_manual.json")
    algebra=load("matrices/symbols/algebra_mashet.json")
    before=(copy.deepcopy(A),copy.deepcopy(B))

    hebrew=choose_hebrew(GOAL,glyphs)
    mashet,ranking=choose_mashet(GOAL,manual)
    alg=next((r for r in algebra["records"] if r["mashet"]==mashet["id"]),None)

    trace=[
      {"stage":"GOAL","actor":"HARNESS","value":GOAL},
      {"stage":"IDENTIFY","actor":"G::ר","value":"Trial-015 request identified"},
      {"stage":"HEBREW_SELECT","actor":"HARNESS_POLICY","selected":hebrew},
      {"stage":"MASHET_SELECT","actor":"HARNESS_POLICY","selected":mashet["id"],"ranking":ranking},
      {"stage":"DEPENDENCY_RESOLVE","actor":"HARNESS","algebra":alg},
    ]

    opened=bool(alg and alg.get("law_status")=="WORKING")
    trace.append({"stage":"VALIDATE_OPEN","actor":"G::ר","opened":opened,
                  "reason":"resolved WORKING algebra dependency" if opened else "dependency unresolved"})

    result=None
    if opened and mashet["id"]=="M::COMPOSE":
        result={"handle":"N::X::trial015_result","operation":"M::COMPOSE",
                "operands":[A["handle"],B["handle"]],
                "value":[copy.deepcopy(A["value"]),copy.deepcopy(B["value"])],
                "status":"WORKING","validated_proposition":False,
                "provenance":{"goal":GOAL,"sources":[A["handle"],B["handle"]]}}
        trace.append({"stage":"OPERATE","actor":"ALGEBRA_EXECUTOR","signature":alg["signature"],"result":result})

    sources_unchanged=(A==before[0] and B==before[1])
    checks={
      "source_A_unchanged":A==before[0],
      "source_B_unchanged":B==before[1],
      "result_has_new_identity":bool(result and result["handle"] not in {A["handle"],B["handle"]}),
      "provenance_closed":bool(result and result["provenance"]["sources"]==[A["handle"],B["handle"]]),
      "result_not_auto_validated":bool(result and result["validated_proposition"] is False),
      "resolved_before_open":opened,
    }
    passed=all(checks.values())
    trace.append({"stage":"POST_VALIDATE","actor":"G::ר","checks":checks,"passed":passed})

    out={"trial":"015","name":"Governed Notebook Manipulation","status":"PASS" if passed else "FAIL",
         "research_label":"BASELINE_HARNESS_POLICY_NOT_AUTONOMOUS_ECHO",
         "goal":GOAL,"inputs":[A,B],"selected":{"hebrew":hebrew,"mashet":mashet["id"]},
         "result":result,"sources_unchanged":sources_unchanged,"trace":trace}
    dest=ROOT/"artifacts"/"trial_015_trace.json"; dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if passed else 1)

if __name__=="__main__": main()
