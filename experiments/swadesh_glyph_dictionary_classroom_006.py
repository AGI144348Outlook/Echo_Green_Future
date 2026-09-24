#!/usr/bin/env python3
"""Trial 006 — Swadesh dictionary homework + glyph abstraction + classroom gate.

Inputs are intentionally limited to:
1. sandbox/echo_sandbox_swadesh.json (starting lobby)
2. ECHO_GlyphRegistry/*.md (operation reference)
3. WordNet definitions reachable from admitted words.

A candidate word is tagged from its definition by lexical overlap with the
registry operation reference. Encounter/tagging does NOT instantiate it.
Admission requires a classroom gate that tests reachability, definition
structure, tag evidence, and relational grounding. Full evidence is retained.
"""
from pathlib import Path
from collections import Counter
import json,re,hashlib

try:
    from nltk.corpus import wordnet as wn
    wn.synsets("entity")
except Exception:
    import nltk
    nltk.download("wordnet",quiet=True)
    from nltk.corpus import wordnet as wn

WORD=re.compile(r"[A-Za-z][A-Za-z'-]{2,}")
STOP=set("the and that this with from into than then for are was were has have had its their they them not but can may one two any all who how why when where which what being been such used using use".split())

def toks(s): return [x.lower() for x in WORD.findall(s) if x.lower() not in STOP]

# Starting vocabulary.
sw=json.loads(Path("sandbox/echo_sandbox_swadesh.json").read_text())
seed=set()
for w,chain in sw["hypernym_chains"].items():
    seed.add(w.lower())
    for node in chain: seed.update(toks(node))

# Build 22 operation profiles from reference material, not traditional symbolism.
profiles={}
for p in sorted(Path("ECHO_GlyphRegistry").glob("[0-9][0-9]-*.md")):
    text=p.read_text(encoding="utf-8")
    glyph=re.search(r"\| \*\*Glyph\*\* \| ([^|]+)",text)
    op=re.search(r"\| \*\*Algorithmic Operation\*\* \| ([^|]+)",text)
    cls=re.search(r"\| \*\*Operation Class\*\* \| ([^|]+)",text)
    if not (glyph and op): continue
    # Whole registry file is visible reference evidence. Weight operation/class.
    bag=Counter(toks(text))
    opname=op.group(1).strip()
    for x in toks(opname+" "+(cls.group(1).strip() if cls else "")): bag[x]+=8
    profiles[opname]={"glyph":glyph.group(1).strip(),"terms":bag,"source":str(p)}
assert len(profiles)==22

cache={}
def definition(w):
    if w not in cache:
        ss=wn.synsets(w)
        cache[w]=ss[0].definition() if ss else ""
    return cache[w]

def tag_word(w,d):
    dt=Counter(toks(d))
    ranked=[]
    for op,p in profiles.items():
        shared=set(dt)&set(p["terms"])
        score=sum(dt[x]*p["terms"][x] for x in shared)
        if score:
            ranked.append({"operation":op,"glyph":p["glyph"],"score":score,
                           "evidence":sorted(shared),"source":p["source"]})
    ranked.sort(key=lambda x:(-x["score"],x["operation"]))
    return ranked[:3]

def expose(parents,admitted):
    out={}
    for parent in sorted(parents):
        d=definition(parent)
        for w in toks(d):
            if w in admitted: continue
            x=out.setdefault(w,{"parents":set(),"exposure":[]})
            x["parents"].add(parent); x["exposure"].append(d)
    return out

def classroom(w,e,admitted):
    d=definition(w); tags=tag_word(w,d) if d else []
    dt=set(toks(d))
    checks={
      "dictionary_definition":bool(d),
      "definition_content":len(dt)>=2,
      "reachable_parent":bool(e["parents"] & admitted),
      "glyph_abstraction_evidence":bool(tags and tags[0]["evidence"]),
      "relational_grounding":bool(dt & admitted),
    }
    score=sum(checks.values())
    # Glyph evidence is mandatory; 4/5 total required.
    passed=score>=4 and checks["glyph_abstraction_evidence"]
    return {"score":score,"max":5,"percent":20*score,"pass":passed,
            "checks":checks,"glyph_tags":tags}

admitted=set(seed); lineage={w:{"state":"SEED","parent":None} for w in seed}
frontier=set(seed); cycles=[]; MAX_DEPTH=25
for n in range(1,MAX_DEPTH+1):
    candidates=expose(frontier,admitted)
    if not candidates: break
    new=set(); rows=[]
    for w,e in sorted(candidates.items()):
        t=classroom(w,e,admitted)
        state="ADMITTED" if t["pass"] else "STUDYING"
        rows.append({"word":w,"definition":definition(w),
                     "parents":sorted(e["parents"]),"state":state,"classroom":t})
        if t["pass"]:
            new.add(w); lineage[w]={"state":"ADMITTED","parent":sorted(e["parents"])[0],
                                    "glyph_tags":t["glyph_tags"]}
        else:
            lineage.setdefault(w,{"state":"STUDYING","parent":sorted(e["parents"])[0],
                                  "glyph_tags":t["glyph_tags"]})
    cycles.append({"cycle":n,"tested":len(rows),"admitted":len(new),
                   "retained_for_study":len(rows)-len(new),
                   "admission_rate":round(100*len(new)/max(1,len(rows)),2),
                   "records":rows})
    if not new: break
    admitted |= new; frontier=new

tag_counts=Counter()
for w in admitted:
    for t in lineage.get(w,{}).get("glyph_tags",[]): tag_counts[t["operation"]]+=1
report={
 "experiment":"SWADESH_GLYPH_DICTIONARY_CLASSROOM_006",
 "seed_lobby_size":len(seed),"final_admitted":len(admitted),
 "cycles":cycles,"lineage":lineage,"glyph_tag_counts":dict(tag_counts),
 "admission_rule":"Candidate must score >=4/5, including explicit registry-overlap evidence for at least one glyph-operation tag.",
 "boundary":"Only Swadesh/hypernym starting vocabulary, reachable WordNet definitions, and supplied ECHO GlyphRegistry operation reference are visible.",
 "nonclaim":"Tags are evidence-bearing lexical abstractions from definition/reference overlap. They are hypotheses/classifications, not proof that English words intrinsically encode Hebrew glyph operations."
}
raw=json.dumps(report,ensure_ascii=False,indent=2); report["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
Path("results").mkdir(exist_ok=True)
Path("results/swadesh_glyph_dictionary_classroom_006.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
md=["# SWADESH + GLYPH + DICTIONARY ↔ CLASSROOM 006","",
    f"Seed lobby: {len(seed)}",f"Final admitted: {len(admitted)}","",
    "## Cycle summary",""]
for c in cycles:
    md += [f"- Cycle {c['cycle']}: tested {c['tested']}; admitted {c['admitted']}; retained {c['retained_for_study']}; admission rate {c['admission_rate']}%"]
md += ["","## Earned glyph-tag distribution",""]
for op,n in tag_counts.most_common(): md.append(f"- {op}: {n}")
md += ["","## Boundary",report["boundary"],"",report["nonclaim"]]
Path("results/swadesh_glyph_dictionary_classroom_006.md").write_text("\n".join(md)+"\n")
print("STATUS: SWADESH_GLYPH_DICTIONARY_CLASSROOM_006_EXECUTED")
print("SEED",len(seed),"FINAL",len(admitted),"CYCLES",len(cycles))
