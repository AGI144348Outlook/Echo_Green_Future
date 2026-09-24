#!/usr/bin/env python3
"""Trial 005 — sealed Swadesh-definition vocabulary admission gate.

Information boundary:
  * Seed lobby = words already present in sandbox/echo_sandbox_swadesh.json
    hypernym chains (Swadesh words + their existing hypernym vocabulary).
  * The ONLY new readable semantic text is a WordNet definition for a word
    already admitted to the lobby or currently eligible from an admitted
    word's definition.
  * A token seen in a definition becomes CANDIDATE, never automatically KNOWN.
  * Candidate admission requires a classroom pass.
  * No glyph registry, Wikipedia, project corpus, or unrestricted vocabulary
    is exposed to the learning loop.
"""
from pathlib import Path
import json,re,hashlib
from collections import defaultdict,Counter

try:
    from nltk.corpus import wordnet as wn
    wn.synsets("entity")
except Exception:
    import nltk
    nltk.download("wordnet", quiet=True)
    from nltk.corpus import wordnet as wn

WORD=re.compile(r"[A-Za-z][A-Za-z'-]{2,}")
STOP={"the","and","that","this","with","from","into","than","then","for","are","was","were","has","have","had","its","their","they","them","not","but","can","may","one","two","any","all","who","how","why","when","where","which","what","being","been","such","used","using","use"}

src=json.loads(Path("sandbox/echo_sandbox_swadesh.json").read_text())
seed=set()
for w,chain in src["hypernym_chains"].items():
    seed.add(w.lower())
    for node in chain:
        seed.update(x.lower() for x in WORD.findall(node))
admitted=set(seed)
lineage={w:{"state":"SEED","parent":None,"depth":0} for w in admitted}
definition_cache={}

def definition(word):
    if word in definition_cache:return definition_cache[word]
    ss=wn.synsets(word)
    d=ss[0].definition() if ss else ""
    definition_cache[word]=d
    return d

def candidates_from(parents):
    c={}
    for parent in sorted(parents):
        d=definition(parent)
        if not d: continue
        for token in WORD.findall(d.lower()):
            if token in STOP or token in admitted: continue
            c.setdefault(token,{"parents":[],"definitions":[]})
            c[token]["parents"].append(parent)
            c[token]["definitions"].append(d)
    return c

def classroom(candidate, evidence):
    """Four sealed, reproducible checks. Passing requires >=3/4.
    This measures definition-grounded lexical/relational competence, not
    general human comprehension."""
    d=definition(candidate)
    if not d:
        return {"score":0,"pass":False,"checks":{"has_definition":False}}
    dt=set(WORD.findall(d.lower()))-STOP
    parent=set(evidence["parents"])
    # Evidence-independent structural checks over the candidate's own definition.
    checks={
      "has_definition":bool(dt),
      "definition_has_content":len(dt)>=2,
      "connects_to_admitted":bool(dt & admitted),
      "reachable_from_admitted_definition":bool(parent & admitted),
    }
    score=sum(checks.values())
    return {"score":score,"max":4,"percent":25*score,"pass":score>=3,"checks":checks}

cycles=[]
frontier=set(admitted)
MAX_CYCLES=25
for n in range(1,MAX_CYCLES+1):
    cand=candidates_from(frontier)
    if not cand:
        cycles.append({"cycle":n,"candidates":0,"tested":0,"admitted":0,"failed":0,"grade":100.0,"reason":"No new definition-derived candidates remain."})
        break
    results=[]; newly=set()
    for w,e in sorted(cand.items()):
        test=classroom(w,e)
        state="ADMITTED" if test["pass"] else "STUDYING"
        results.append({"word":w,"parents":sorted(set(e["parents"])),"test":test,"state":state})
        if test["pass"]:
            newly.add(w)
            parent=sorted(set(e["parents"]))[0]
            lineage[w]={"state":"ADMITTED","parent":parent,"depth":lineage.get(parent,{}).get("depth",0)+1}
        else:
            lineage.setdefault(w,{"state":"STUDYING","parent":sorted(set(e["parents"]))[0],"depth":None})
    admitted |= newly
    grade=100*len(newly)/max(1,len(results))
    cycles.append({"cycle":n,"candidates":len(cand),"tested":len(results),"admitted":len(newly),"failed":len(results)-len(newly),"grade":round(grade,2),"results":results})
    if not newly: break
    frontier=newly

report={"experiment":"SWADESH_DICTIONARY_CLASSROOM_GATE_005",
"boundary":"Dictionary/Homework <-> Classroom only. New words are exposed solely through WordNet definitions of already-admitted/reachable words. Encounter does not equal admission.",
"seed_lobby_size":len(seed),"final_admitted":len(admitted),"cycles":cycles,"lineage":lineage,
"admission_rule":"Candidate must pass at least 3 of 4 reproducible definition-grounded classroom checks before lobby instantiation.",
"termination":"No newly admitted words, no new candidates, or safety ceiling of 25 recursive depths.",
"nonclaim":"The classroom is a deterministic lexical/relational proxy and does not establish subjective or general language comprehension."}
raw=json.dumps(report,ensure_ascii=False,indent=2); report["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
Path("results").mkdir(exist_ok=True)
Path("results/swadesh_dictionary_classroom_gate_005.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
lines=["# SWADESH DICTIONARY ↔ CLASSROOM GATE 005","",f"Seed lobby: {len(seed)}",f"Final admitted: {len(admitted)}",""]
for c in cycles:
    lines += [f"## Cycle {c['cycle']}",f"Candidates tested: {c['tested']}",f"Admitted: {c['admitted']}",f"Failed/retained for study: {c['failed']}",f"Classroom admission rate: {c['grade']}%",""]
lines += ["## Boundary",report["boundary"],"",report["nonclaim"]]
Path("results/swadesh_dictionary_classroom_gate_005.md").write_text("\n".join(lines)+"\n")
print("STATUS: SWADESH_DICTIONARY_CLASSROOM_GATE_005_EXECUTED")
print("SEED:",len(seed),"FINAL:",len(admitted),"CYCLES:",len(cycles))
