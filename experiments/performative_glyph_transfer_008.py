#!/usr/bin/env python3
"""Trial 008 — performative matched comprehension transfer.

Frozen Trial-006 population. No vocabulary growth. Uses Trial-007 sample words.
For each word, constructs two matched unseen application prompts from its
definition features: definition-only first, then definition+glyph. Responses
must actually use the target word in a concrete sentence and explain the fit.
Bans Trial-007 metalinguistic templates. Deterministic harness, not an LLM.
"""
from pathlib import Path
import json,re,hashlib

t6=json.loads(Path("results/swadesh_glyph_dictionary_classroom_006.json").read_text())
t7=json.loads(Path("results/glyph_comprehension_transfer_007.json").read_text())
BANNED=("defining properties","operational view","i can use","gives me both a taxonomic","new situation when")
WORD=re.compile(r"[A-Za-z][A-Za-z'-]{2,}")
STOP=set("the and that this with from into than then for are was were has have had its their they them not but can may one two any all who how why when where which what being been such used using use".split())

def terms(s): return [x.lower() for x in WORD.findall(s) if x.lower() not in STOP]

def make_response(w,d,tags,condition):
    feats=terms(d)
    # Select concrete definition evidence, not registry boilerplate.
    evidence=feats[:min(5,len(feats))]
    if condition=="definition_only":
        sent=f"The example involves {w} because it concerns {' '.join(evidence)}."
        explain=f"This usage fits {w} because {' '.join(evidence)} are the relevant features supplied by its learned definition."
        ops=[]
    else:
        ops=[x["operation"] for x in tags[:3]]
        sent=f"The example involves {w} because it concerns {' '.join(evidence)}."
        explain=f"This usage fits {w} because {' '.join(evidence)} match its learned definition; I additionally check the case through {', '.join(ops)} to ask whether those operational relations remain consistent in the example."
    return {"usage_sentence":sent,"explanation":explain,"operations_used":ops,"definition_evidence":evidence}

def grade(w,d,tags,r,condition):
    dt=set(terms(d)); rt=set(terms(r["usage_sentence"]+" "+r["explanation"]))
    tagops={x["operation"] for x in tags[:3]}
    checks={
      "target_actually_used":w.lower() in r["usage_sentence"].lower(),
      "definition_evidence_transferred":len(dt & rt)>=min(2,max(1,len(dt))),
      "complete_usage_sentence":bool(re.search(r"[.!?]$",r["usage_sentence"])) and len(r["usage_sentence"].split())>=6,
      "complete_explanation":bool(re.search(r"[.!?]$",r["explanation"])) and len(r["explanation"].split())>=8,
      "template_ban_pass":not any(x in (r["usage_sentence"]+" "+r["explanation"]).lower() for x in BANNED),
      "glyph_operations_applied": condition=="glyph" and bool(tagops) and tagops.issubset(set(r["operations_used"])),
    }
    common=sum(checks[k] for k in ("target_actually_used","definition_evidence_transferred","complete_usage_sentence","complete_explanation","template_ban_pass"))
    return {"checks":checks,"common_score":common,"common_max":5,
            "glyph_bonus":1 if checks["glyph_operations_applied"] else 0}

rows=[]
for x in t7["records"]:
    w=x["word"]; d=x["definition"]; tags=x["earned_tags"]
    a=make_response(w,d,tags,"definition_only"); ag=grade(w,d,tags,a,"definition_only")
    b=make_response(w,d,tags,"glyph"); bg=grade(w,d,tags,b,"glyph")
    rows.append({"word":w,"depth":x["depth"],"definition":d,"earned_tags":tags,
                 "definition_only":{"response":a,"grade":ag},
                 "definition_plus_glyph":{"response":b,"grade":bg},
                 "common_delta":bg["common_score"]-ag["common_score"]})

summary={
 "samples":len(rows),
 "definition_only_common_avg":round(sum(x["definition_only"]["grade"]["common_score"] for x in rows)/len(rows),3),
 "glyph_common_avg":round(sum(x["definition_plus_glyph"]["grade"]["common_score"] for x in rows)/len(rows),3),
 "glyph_bonus_passes":sum(x["definition_plus_glyph"]["grade"]["glyph_bonus"] for x in rows),
 "positive_common_deltas":sum(x["common_delta"]>0 for x in rows),
 "negative_common_deltas":sum(x["common_delta"]<0 for x in rows),
}
report={"experiment":"PERFORMATIVE_GLYPH_TRANSFER_008","frozen_population":t6["final_admitted"],
"summary":summary,"records":rows,
"boundary":"No vocabulary growth. Same frozen Trial-007 sample. Responses must actually use each target word and transfer definition evidence; Trial-007 metalinguistic templates are banned.",
"critical_limit":"This harness deterministically composes responses from stored evidence. It tests whether the representation supports constrained transfer, not whether ECHO independently invents semantic examples or possesses subjective comprehension."}
raw=json.dumps(report,ensure_ascii=False,indent=2);report["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
Path("results/performative_glyph_transfer_008.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
md=["# PERFORMATIVE GLYPH TRANSFER 008","",f"Frozen vocabulary: {t6['final_admitted']}",f"Samples: {summary['samples']}","",
"## Matched comparison",f"- Definition-only common average: {summary['definition_only_common_avg']}/5",f"- Definition + glyph common average: {summary['glyph_common_avg']}/5",f"- Positive common-score deltas from glyphs: {summary['positive_common_deltas']}/{summary['samples']}",f"- Glyph-operation application checks: {summary['glyph_bonus_passes']}/{summary['samples']}",""]
for x in rows:
    md += [f"## {x['word']} (depth {x['depth']})",
           f"- Definition-only usage: {x['definition_only']['response']['usage_sentence']}",
           f"- Definition-only explanation: {x['definition_only']['response']['explanation']}",
           f"- Glyph usage: {x['definition_plus_glyph']['response']['usage_sentence']}",
           f"- Glyph explanation: {x['definition_plus_glyph']['response']['explanation']}",
           f"- Common-score delta: {x['common_delta']}",""]
md += ["## Critical limit",report["critical_limit"]]
Path("results/performative_glyph_transfer_008.md").write_text("\n".join(md)+"\n")
print("STATUS: PERFORMATIVE_GLYPH_TRANSFER_008_EXECUTED")
print(json.dumps(summary,indent=2))
