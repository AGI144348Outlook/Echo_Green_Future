#!/usr/bin/env python3
"""Independent ECHO-020 answer scoring. Run AFTER study, not during learning.

This process alone reads the locked 35-question answer key. Score strictly,
report complete raw answers and abstentions. No surrogate model or answer fixup.
"""
from __future__ import annotations
import collections
import json
import re
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
KEYS=HERE/"echo020_grade1_heldout_exam.json"

def normal(s):
    s=str(s or "").lower().replace("−","-")
    s=re.sub(r"[^a-z0-9]+"," ",s).strip()
    return " ".join(s.split())

def contains_exact_alias(response,aliases):
    raw=normal(response)
    if not raw:return False,None
    for alias in aliases:
        expected=normal(alias)
        if expected and re.search(r"(?<!\w)"+re.escape(expected)+r"(?!\w)",raw):
            return True,alias
    return False,None

def grade(phase,answers,keys):
    by_id={x["id"]:x for x in answers}
    questions=keys["questions"]
    if set(by_id)!={x["id"] for x in questions}:
        raise RuntimeError("Missing, additional or duplicate exam response IDs")
    rows=[]
    for q in questions:
        candidate=by_id[q["id"]]
        ok,matched=contains_exact_alias(candidate.get("raw_answer"),q["acceptable"])
        rows.append({
            "id":q["id"],"strand":q["strand"],"skill":q["skill"],
            "prompt":q["question"],"raw_response":candidate.get("raw_answer"),
            "source_refs":candidate.get("source_refs") or [],
            "response_kind":candidate.get("reason"),"correct":bool(ok),
            "matched_alias":matched,"abstained":not bool(candidate.get("raw_answer"))
        })
    by_strand={}
    for strand in keys["strands"]:
        group=[x for x in rows if x["strand"]==strand]
        by_strand[strand]={"correct":sum(x["correct"] for x in group),
            "total":len(group),"abstentions":sum(x["abstained"] for x in group)}
    return {"phase":phase,"correct":sum(x["correct"] for x in rows),"total":len(rows),
            "abstentions":sum(x["abstained"] for x in rows),"by_strand":by_strand,
            "items":rows}

def main():
    if len(sys.argv)!=2:raise SystemExit("Usage: echo020_grade1_score.py <study-output-directory>")
    path=Path(sys.argv[1])
    keys=json.loads(KEYS.read_text())
    if len(keys["questions"])!=35 or {q["strand"] for q in keys["questions"]}!=set(keys["strands"]):
        raise RuntimeError("Answer key differs from frozen pretest specification")
    before=json.loads((path/"before_raw_answers.json").read_text())
    after=json.loads((path/"after_raw_answers.json").read_text())
    b=grade("baseline_before_material",before,keys)
    a=grade("post_300_second_study",after,keys)
    result={
        "exam_id":keys["exam_id"],
        "grading_kind":"strict exact normalized answer phrases; source retrieval sentences may earn credit",
        "grading_limitations":[
            "An answer embedded in a retrieved sentence is credited; this can overstate comprehension.",
            "No human correction or AI judging has occurred.",
            "This is an authored year-end-style assessment, not a standardized state examination.",
            "The 300-second exposure covers specified materials, not a full academic year."
        ],
        "baseline":b,"post":a,
        "change_correct":a["correct"]-b["correct"],
        "test_keys_unseen_by_study":True,
        "no_llm_scoring":True
    }
    (path/"echo020_graded_year_end_assessment.json").write_text(json.dumps(result,indent=2)+"\n")
    compact={"baseline":b["correct"],"post":a["correct"],"total":35,
       "change":result["change_correct"],"baseline_abstentions":b["abstentions"],
       "post_abstentions":a["abstentions"],
       "strands":{s:{"before":b["by_strand"][s]["correct"],
                     "after":a["by_strand"][s]["correct"],"total":b["by_strand"][s]["total"]}
                   for s in keys["strands"]}}
    print("ECHO020_EXAM_RESULT "+json.dumps(compact),flush=True)

if __name__=="__main__":main()
