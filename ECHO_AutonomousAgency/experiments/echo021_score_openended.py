#!/usr/bin/env python3
"""Independent ECHO-021 open-ended scoring, never invoked during study.

This scorer reads held-out keys AFTER Echo has produced raw answers/diagrams.
No model or renderer supplies missing solution steps. An evidence-retrieval
arrow is NOT treated as reasoning or a causal explanation.
"""
from __future__ import annotations
import collections
import json
import re
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
KEY_PATH=HERE/"echo021_openended_exam.json"

def norm(value):
    return " ".join(re.findall(r"[a-z0-9]+",str(value or "").lower()))

def has_alias(text,alias):
    s=norm(text)
    a=norm(alias)
    return bool(a and re.search(r"(?<!\w)"+re.escape(a)+r"(?!\w)",s))

def concepts_present(text,concept_groups):
    return all(any(has_alias(text,a) for a in aliases) for aliases in concept_groups)

def inspect_diagram(trace,item):
    relations=trace.get("relations") or []
    nodes=trace.get("nodes") or []
    refs=trace.get("source_refs") or []
    structurally_present=bool(nodes and relations)
    cited=bool(refs) and all(n.get("source_refs") for n in nodes) and all(e.get("source_refs") for e in relations)
    if not structurally_present or not cited:
        return {"present":structurally_present,"sources_cited":cited,"reasoned":False,"reason":"no_supported_structure"}
    relation_types={e.get("predicate") for e in relations}
    if "retrieved_text_for" in relation_types and relation_types=={"retrieved_text_for"}:
        return {"present":True,"sources_cited":True,"reasoned":False,"reason":"retrieval_is_not_reasoning"}
    math=item.get("math")
    if math:
        expected=math["result"]
        source_numbers=sorted([n["quantity"] for n in nodes if n.get("id") in ("given-a","given-b") and isinstance(n.get("quantity"),int)])
        results=[n["quantity"] for n in nodes if n.get("id")=="observed-result" and isinstance(n.get("quantity"),int)]
        op="reported_"+math["op"]
        relevant=[e for e in relations if e.get("predicate")==op and e.get("to")=="observed-result"]
        valid=(len(results)==1 and results[0]==expected and
          source_numbers==sorted(math["operands"]) and len(relevant)>=2 and
          len({e.get("from") for e in relevant})>=2)
        # Mathematical truth is checked HERE, never in OpenDiagram's renderer.
        return {"present":True,"sources_cited":True,"reasoned":bool(valid),
                "reason":"consistent_math_relation" if valid else "incorrect_or_incomplete_math_relation"}
    # Open-ended causal/inferential diagrams must make a genuine asserted
    # conceptual relation, with source references, not just retrieval.
    substantive={"causes","explains","inferred_from","leads_to","compares",
                 "because","supports","motivates","prevents","means"}
    asserted=any(str(e.get("predicate","")).lower() in substantive for e in relations)
    labels=" ".join(n.get("label","") for n in nodes)
    supported=asserted and concepts_present(labels,item["acceptable"])
    return {"present":True,"sources_cited":True,"reasoned":bool(supported),
            "reason":"explicit_reasoning_relation" if supported else "no_supported_causal_inference"}

def grade(answers,traces,keys,phase):
    by_answer={a["id"]:a for a in answers}
    by_trace={t["stimulus_id"]:t for t in traces}
    ids={x["id"] for x in keys["questions"]}
    if set(by_answer)!=ids or set(by_trace)!=ids:
        raise RuntimeError("Question / source-response / structural-trace IDs do not match")
    rows=[]
    for item in keys["questions"]:
        raw=by_answer[item["id"]].get("raw_answer")
        numerical=item.get("math")
        if numerical:
            # Place-value prompts contain concept groups rather than a single
            # expected result; all other math prompts require EXACT number.
            text_match=has_alias(raw,str(numerical["result"]))
        else:
            text_match=concepts_present(raw,item["acceptable"])
        d=inspect_diagram(by_trace[item["id"]],item)
        rows.append({
            "id":item["id"],"subject":item["strand"],"skill":item["skill"],
            "prompt":item["question"],"raw_echo_output":raw,
            "answer_reason":by_answer[item["id"]].get("reason"),
            "source_refs":by_answer[item["id"]].get("source_refs",[]),
            "trace_status":by_trace[item["id"]]["status"],
            "diagram_node_count":len(by_trace[item["id"]]["nodes"]),
            "diagram_relation_count":len(by_trace[item["id"]]["relations"]),
            "text_match":bool(text_match),"diagram_presence":d["present"],
            "diagram_reasoning":d["reasoned"],"diagram_reason":d["reason"],
            "combined_match":bool(text_match or d["reasoned"]),
            "abstained":not raw
        })
    grouped={}
    for subject in sorted({r["subject"] for r in rows}):
        subset=[r for r in rows if r["subject"]==subject]
        grouped[subject]={
            "items":len(subset),
            "text_matches":sum(r["text_match"] for r in subset),
            "diagram_presence":sum(r["diagram_presence"] for r in subset),
            "diagram_reasoned":sum(r["diagram_reasoning"] for r in subset),
            "combined_matches":sum(r["combined_match"] for r in subset),
            "abstentions":sum(r["abstained"] for r in subset)
        }
    return {
        "phase":phase,"total":len(rows),
        "text_matches":sum(r["text_match"] for r in rows),
        "diagram_presence":sum(r["diagram_presence"] for r in rows),
        "diagram_reasoned":sum(r["diagram_reasoning"] for r in rows),
        "combined_matches":sum(r["combined_match"] for r in rows),
        "abstentions":sum(r["abstained"] for r in rows),
        "by_subject":grouped,"items":rows}

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--before",type=Path,required=True)
    p.add_argument("--after",type=Path,required=True)
    p.add_argument("--before-diagrams",type=Path,required=True)
    p.add_argument("--after-diagrams",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    key=json.loads(KEY_PATH.read_text())
    if len(key["questions"])!=18:
        raise RuntimeError("Frozen 18-item benchmark changed")
    j=lambda f:json.loads(f.read_text())
    before=grade(j(args.before),j(args.before_diagrams),key,"before")
    after=grade(j(args.after),j(args.after_diagrams),key,"after")
    report={
      "research":"ECHO-021",
      "grading":"strict concept/number matching; diagram reasoning requires asserted causal/consistent arithmetic source-linked relations, not retrieval",
      "notes":["Text matching may reward copied source words without inference.",
          "WordNet and student curriculum are not a full year of teaching.",
          "No OpenDiagram AI or website answers are used.",
          "The algorithm and diagram adapter are not the full 3³ neuroplastic Echo Governor."],
      "baseline":before,"after":after,
      "delta_text":after["text_matches"]-before["text_matches"],
      "delta_diagram_reasoning":after["diagram_reasoned"]-before["diagram_reasoned"],
      "delta_combined":after["combined_matches"]-before["combined_matches"]
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+"\n")
    print("ECHO021_OPENENDED_RESULT "+json.dumps({
       "questions":18,
       "before":{"text":before["text_matches"],"diagram":before["diagram_reasoned"],
                  "combined":before["combined_matches"],"abstained":before["abstentions"]},
       "after":{"text":after["text_matches"],"diagram":after["diagram_reasoned"],
                "combined":after["combined_matches"],"abstained":after["abstentions"]},
       "post_subjects":after["by_subject"]
    }),flush=True)

if __name__=="__main__":main()
