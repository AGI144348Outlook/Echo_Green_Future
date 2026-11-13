#!/usr/bin/env python3
"""Independent ECHO-022 evidence assessment, NOT part of Echo's 300s study.
This cannot score retrieval fragments as genuine inference.
"""
import argparse, collections, json
from pathlib import Path

def assess(answers,phase):
    by_strand=collections.defaultdict(lambda:{"responses":0,"retrieval_only":0,"abstentions":0,"math_operator":0})
    details=[]
    for item in answers:
        text=item.get("raw_answer")
        reason=item.get("reason")
        strand=item["strand"]
        d=by_strand[strand]
        if text:d["responses"]+=1
        if reason=="source_retrieval_fragment":d["retrieval_only"]+=1
        if not text:d["abstentions"]+=1
        if reason in ("observed_math_structure","observed_math_operator"):d["math_operator"]+=1
        # A source-retrieval fragment or observed arithmetic calculation does
        # not prove general-context causal inference/permission reasoning.
        details.append({"id":item["id"],"strand":strand,"raw_output":text,
                        "mechanism":reason,"source_refs":item.get("source_refs",[]),
                        "verified_independent_inference":False,
                        "why":"No agent-authored multi-premise inference trace/justification was emitted by this respondent"})
    return {"phase":phase,"total":len(answers),"nonempty":sum(bool(x.get("raw_answer")) for x in answers),
            "retrieval_only":sum(x.get("reason")=="source_retrieval_fragment" for x in answers),
            "abstentions":sum(not x.get("raw_answer") for x in answers),
            "independent_inference_attested":0,
            "by_strand":dict(by_strand),"items":details}

def main():
    p=argparse.ArgumentParser()
    for x in ["before","after","out"]:p.add_argument("--"+x,type=Path,required=True)
    args=p.parse_args()
    before=json.loads(args.before.read_text())
    after=json.loads(args.after.read_text())
    keys1=[i["id"] for i in before];keys2=[i["id"] for i in after]
    if keys1!=keys2 or len(keys1)!=len(set(keys1)):
        raise RuntimeError("Question ID mismatch / duplicate IDs")
    b=assess(before,"before");a=assess(after,"after")
    report={"protocol":"ECHO022-honest-assessment/v1","before":b,"after":a,
      "delta_nonempty":a["nonempty"]-b["nonempty"],
      "delta_retrieval_only":a["retrieval_only"]-b["retrieval_only"],
      "inference_claim":"No independent inference is credited without model-produced causal/relational proofs and held-out verification.",
      "interpretation_limits":"Exact or lexical answers can be memorized or copied; this report does not claim semantic generalization."}
    args.out.write_text(json.dumps(report,indent=2)+"\n")
    print("ECHO022_ASSESSMENT "+json.dumps({"before_nonempty":b["nonempty"],
      "after_nonempty":a["nonempty"],"after_retrieval_only":a["retrieval_only"],
      "independent_inference_attested":0,"before_abstentions":b["abstentions"],
      "after_abstentions":a["abstentions"]}),flush=True)
if __name__=="__main__":main()
