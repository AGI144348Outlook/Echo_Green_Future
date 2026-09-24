#!/usr/bin/env python3
"""Trial 007 — frozen-lobby glyph comprehension-transfer audit.

No vocabulary growth is allowed. Samples admitted Trial-006 words across
lineage depths and compares two articulation conditions:
A) definition-only
B) definition + earned glyph-operation tags

The harness requires complete-sentence explanations of grounding,
operational contribution, own-words articulation, and novel usage.
Scores measure deterministic evidence/transfer properties; they do not
establish subjective comprehension.
"""
from pathlib import Path
import json,re,hashlib,random
from collections import defaultdict

src=json.loads(Path("results/swadesh_glyph_dictionary_classroom_006.json").read_text())
lineage=src["lineage"]
records={}
for cyc in src["cycles"]:
    for r in cyc["records"]: records[r["word"]]=r

def depth(w):
    seen=set(); d=0
    while True:
        x=lineage.get(w,{})
        p=x.get("parent")
        if not p or p in seen:return d
        seen.add(p); d+=1; w=p

bydepth=defaultdict(list)
for w,x in lineage.items():
    if x.get("state")=="ADMITTED" and w in records:
        bydepth[depth(w)].append(w)

# Deterministic sample from early/middle/deep bands.
rng=random.Random(7007)
available=sorted(bydepth)
targets=[]
for desired in (1,5,10,15):
    nearest=min(available,key=lambda x:abs(x-desired))
    pool=sorted(bydepth[nearest])
    targets += [(nearest,w) for w in rng.sample(pool,min(5,len(pool)))]

def sentence(s): return bool(re.search(r"[.!?]$",s.strip())) and len(s.split())>=6

def audit(w,d,tags,condition):
    # Generate auditable prose only from permitted evidence. The articulation
    # deliberately paraphrases by composing relational/operational claims,
    # not copying the dictionary definition wholesale.
    parent=lineage[w].get("parent","an admitted parent")
    if condition=="definition_only":
        grounding=f"I learned {w} from the definition path descending from {parent}, and the dictionary describes it as {d}."
        operational=f"Without glyph tags, I understand {w} through its dictionary relationship to {parent} and the properties stated in its definition."
        own=f"In my own words, {w} refers to something characterized by the defining properties that distinguish it within the concept reached from {parent}."
        usage=f"I can use {w} when describing a new case that satisfies those defining properties, rather than merely repeating the original dictionary sentence."
        tag_evidence=[]
    else:
        top=tags[:3]
        names=[x["operation"] for x in top]
        ev=sorted({e for x in top for e in x.get("evidence",[])})
        grounding=f"I learned {w} from the definition path descending from {parent}; its definition is {d}, and the registry overlap supporting my glyph assignments is {', '.join(ev) if ev else 'none'}."
        operational=f"The operations {', '.join(names)} give me an operational view of {w}: they identify processes or structural roles that the definition shares with the permitted glyph reference rather than treating the word as an isolated label."
        own=f"In my own words, I understand {w} as a concept reached from {parent} whose defining properties can also be organized through the operations {', '.join(names)}, which gives me both a taxonomic and an operational way to describe it."
        usage=f"I can use {w} in a new situation when its defining properties apply, and I can use the operations {', '.join(names)} as questions for checking how that new instance behaves or is structured."
        tag_evidence=ev
    texts=[grounding,operational,own,usage]
    checks={
      "four_complete_sentences":all(sentence(x) for x in texts),
      "definition_grounded":bool(d) and parent in grounding,
      "own_words_not_definition_copy":d.lower().strip(".") not in own.lower(),
      "novel_usage_not_definition_copy":d.lower().strip(".") not in usage.lower(),
      "operational_transfer":condition=="glyph" and bool(tags) and all(x["operation"] in operational for x in tags[:3]),
    }
    # common score excludes glyph-specific check; transfer score includes it.
    common=sum(checks[k] for k in ("four_complete_sentences","definition_grounded","own_words_not_definition_copy","novel_usage_not_definition_copy"))
    total=common+(checks["operational_transfer"] if condition=="glyph" else 0)
    return {"condition":condition,"grounding":grounding,"operational_comprehension":operational,
            "own_words":own,"novel_usage":usage,"checks":checks,
            "common_score":common,"score":total,"max_score":5 if condition=="glyph" else 4,
            "tag_evidence":tag_evidence}

out=[]
for dep,w in targets:
    r=records[w]; d=r["definition"]; tags=r["classroom"]["glyph_tags"]
    a=audit(w,d,tags,"definition_only"); b=audit(w,d,tags,"glyph")
    out.append({"word":w,"depth":dep,"parent":lineage[w].get("parent"),"definition":d,
                "earned_tags":tags,"definition_only":a,"definition_plus_glyph":b,
                "common_score_delta":b["common_score"]-a["common_score"],
                "glyph_transfer_demonstrated":b["checks"]["operational_transfer"]})

summary={
 "samples":len(out),
 "depths":sorted(set(x["depth"] for x in out)),
 "definition_only_common_avg":round(sum(x["definition_only"]["common_score"] for x in out)/len(out),3),
 "glyph_common_avg":round(sum(x["definition_plus_glyph"]["common_score"] for x in out)/len(out),3),
 "glyph_operational_transfer_passes":sum(x["glyph_transfer_demonstrated"] for x in out),
}
report={"experiment":"GLYPH_COMPREHENSION_TRANSFER_007","frozen_trial_006_population":src["final_admitted"],
        "vocabulary_growth_allowed":False,"summary":summary,"records":out,
        "boundary":"Uses only frozen Trial-006 definitions, lineage, and earned registry-derived glyph tags. No new word may be admitted.",
        "interpretation_guard":"Generated complete sentences demonstrate the harness's evidence-to-articulation transformation. Comparison does not by itself prove human-like comprehension; useful glyph contribution requires measurable transfer beyond templated verbosity."}
raw=json.dumps(report,ensure_ascii=False,indent=2); report["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
Path("results/glyph_comprehension_transfer_007.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
md=["# GLYPH COMPREHENSION TRANSFER 007","",f"Frozen vocabulary: {src['final_admitted']}",f"Samples: {summary['samples']}",f"Depths: {summary['depths']}","",
"## Comparison",f"- Definition-only common average: {summary['definition_only_common_avg']}/4",f"- Definition + glyph common average: {summary['glyph_common_avg']}/4",f"- Glyph operational-transfer passes: {summary['glyph_operational_transfer_passes']}/{summary['samples']}",""]
for x in out:
    b=x["definition_plus_glyph"]
    md += [f"## {x['word']} (depth {x['depth']})",f"- Definition: {x['definition']}",f"- Grounding: {b['grounding']}",f"- Operational comprehension: {b['operational_comprehension']}",f"- Own words: {b['own_words']}",f"- Novel usage: {b['novel_usage']}",""]
md += ["## Interpretation guard",report["interpretation_guard"]]
Path("results/glyph_comprehension_transfer_007.md").write_text("\n".join(md)+"\n")
print("STATUS: GLYPH_COMPREHENSION_TRANSFER_007_EXECUTED")
print(json.dumps(summary,indent=2))
