#!/usr/bin/env python3
"""Trial 009 — autonomous proposition construction from frozen semantic relations.

Removes Trial-007/008 prose templates. The engine receives only stored semantic
atoms for each frozen sample: target, lineage parent, definition terms, and
earned glyph operations. It must choose a relation and build a proposition
from those atoms using a minimal grammar composer. No canned "I understand",
"the example involves", or "this usage fits" frames are permitted.

This tests proposition construction from ECHO's graph representation, not
subjective comprehension.
"""
from pathlib import Path
import json,re,hashlib

t6=json.loads(Path("results/swadesh_glyph_dictionary_classroom_006.json").read_text())
t7=json.loads(Path("results/glyph_comprehension_transfer_007.json").read_text())
WORD=re.compile(r"[A-Za-z][A-Za-z'-]{2,}")
STOP=set("the and that this with from into than then for are was were has have had its their they them not but can may one two any all who how why when where which what being been such used using use your own".split())
BANNED=("i understand","the example involves","this usage fits","defining properties","operational view","i can use")

def terms(s):
    out=[]
    for x in WORD.findall(s):
        x=x.lower()
        if x not in STOP and x not in out: out.append(x)
    return out

# Minimal grammar realizes a proposition chosen from graph relations; it does
# not contain word-specific sentences or dictionary definitions.
def proposition(word,parent,definition,tags):
    feats=terms(definition)
    ops=[x["operation"].lower() for x in tags[:3]]
    # choose predicate family from evidence structure
    if any(x in feats for x in ("cause","make","become","perform","act","acts")):
        relation="process"
    elif any(x in feats for x in ("part","organ","units","link","between")):
        relation="structure"
    elif any(x in feats for x in ("sequence","recurring","flow","vibration","curve","curl")):
        relation="dynamic"
    else:
        relation="classification"
    core=feats[:4] or ["entity"]
    if relation=="process":
        tokens=[word,"acts","through"]+core
    elif relation=="structure":
        tokens=[word,"relates","to"]+core
    elif relation=="dynamic":
        tokens=[word,"describes"]+core
    else:
        tokens=[word,"is","associated","with"]+core
    # glyphs are additional predicates/questions, not copied prose.
    if ops: tokens += ["while"]+ops+["constrain","its","operational","interpretation"]
    sentence=" ".join(tokens).capitalize()+"."
    trace={"selected_relation":relation,"subject":word,"parent":parent,
           "definition_atoms":core,"glyph_predicates":ops,"realization_tokens":tokens}
    return sentence,trace

def grade(word,definition,tags,sentence,trace):
    low=sentence.lower(); dt=set(terms(definition)); st=set(terms(sentence))
    ops={x["operation"].lower() for x in tags[:3]}
    checks={
      "target_present":word.lower() in low,
      "definition_atoms_present":len(dt&st)>=min(2,max(1,len(dt))),
      "graph_relation_selected":trace["selected_relation"] in {"process","structure","dynamic","classification"},
      "glyph_predicates_present":bool(ops) and ops.issubset(st),
      "complete_sentence":sentence.endswith(".") and len(sentence.split())>=6,
      "no_prior_scaffold":not any(x in low for x in BANNED),
    }
    return {"checks":checks,"score":sum(checks.values()),"max":len(checks)}

rows=[]
for x in t7["records"]:
    s,tr=proposition(x["word"],x["parent"],x["definition"],x["earned_tags"])
    rows.append({"word":x["word"],"depth":x["depth"],"inputs":{"parent":x["parent"],
      "definition_atoms":terms(x["definition"]),"glyph_operations":[z["operation"] for z in x["earned_tags"]]},
      "proposition_trace":tr,"constructed_sentence":s,
      "grade":grade(x["word"],x["definition"],x["earned_tags"],s,tr)})

summary={"samples":len(rows),"mean_score":round(sum(x["grade"]["score"] for x in rows)/len(rows),3),
"full_passes":sum(x["grade"]["score"]==x["grade"]["max"] for x in rows),
"relation_counts":{k:sum(x["proposition_trace"]["selected_relation"]==k for x in rows) for k in ("process","structure","dynamic","classification")}}
report={"experiment":"AUTONOMOUS_PROPOSITION_CONSTRUCTION_009","frozen_population":t6["final_admitted"],
"sentence_templates_from_007_008":False,"summary":summary,"records":rows,
"boundary":"No vocabulary growth and no Trial-007/008 articulation frames. A minimal grammar composer realizes propositions selected from stored definition, lineage, and glyph relations.",
"critical_limit":"The relation selector and grammar rules are still programmed mechanisms. Success would show graph-to-proposition composition without canned word-specific prose, not unconstrained natural-language generation or subjective comprehension."}
raw=json.dumps(report,ensure_ascii=False,indent=2);report["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
Path("results/autonomous_proposition_construction_009.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
md=["# AUTONOMOUS PROPOSITION CONSTRUCTION 009","",f"Frozen vocabulary: {t6['final_admitted']}",f"Samples: {summary['samples']}",f"Mean score: {summary['mean_score']}/6",f"Full passes: {summary['full_passes']}/{summary['samples']}","",f"Relation selection: {summary['relation_counts']}",""]
for x in rows:
    md += [f"## {x['word']} (depth {x['depth']})",f"- Inputs: parent={x['inputs']['parent']}; atoms={x['inputs']['definition_atoms']}; glyphs={x['inputs']['glyph_operations']}",f"- Chosen relation: {x['proposition_trace']['selected_relation']}",f"- Constructed sentence: {x['constructed_sentence']}",f"- Score: {x['grade']['score']}/6",""]
md += ["## Critical limit",report["critical_limit"]]
Path("results/autonomous_proposition_construction_009.md").write_text("\n".join(md)+"\n")
print("STATUS: AUTONOMOUS_PROPOSITION_CONSTRUCTION_009_EXECUTED")
print(json.dumps(summary,indent=2))
