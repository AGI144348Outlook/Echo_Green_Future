#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import json,re,hashlib
from nltk.corpus import wordnet as wn
state=json.loads(Path("state/lesson_001_subject_spectrum.json").read_text())
glyphs=[]
for p in sorted(Path("ECHO_GlyphRegistry").glob("[0-9][0-9]-*.md")):
 txt=p.read_text(); gm=re.search(r"\\*\\*Glyph\\*\\* \\| ([^|]+)\\|",txt); op=re.search(r"\\*\\*Algorithmic Operation\\*\\* \\| ([^|]+)\\|",txt)
 hm=re.search(r"## Operation Hypernym Chain[\\s\\S]*?```\\s*([\\s\\S]*?)```",txt)
 if not(op and hm):continue
 chain=[x.strip() for x in hm.group(2).replace("\\n"," ").split("→") if x.strip()]
 glyphs.append({"file":str(p),"glyph":gm.group(1).strip() if gm else "?","operation":op.group(1).strip(),"chain":chain})
def terms(x):return set(re.sub(r"[^a-z]+"," ",x.lower()).split())
generic={"act","operation","function","algorithm","system","component"}
for g in glyphs:g["evidence_terms"]=sorted(set().union(*(terms(x) for x in g["chain"]))-generic)
seeds=["study","learn","focus","identify","differentiate","instantiate","designate","symbol"]; records=[]; byword=defaultdict(list)
for word in seeds:
 for s in wn.synsets(word):
  if s.name() not in state["experienced_nodes"]:continue
  evidence=terms(" ".join([word,s.definition()]+s.lemma_names())); cand=[]
  for g in glyphs:
   overlap=sorted(evidence & set(g["evidence_terms"]))
   if overlap:cand.append({"glyph":g["glyph"],"operation":g["operation"],"chain":g["chain"],"registry_file":g["file"],"matched_evidence":overlap})
  cand.sort(key=lambda x:(-len(x["matched_evidence"]),x["operation"],x["registry_file"])); top=len(cand[0]["matched_evidence"]) if cand else 0; selected=[c for c in cand if len(c["matched_evidence"])==top] if top else []
  records.append({"word":word,"node":s.name(),"definition":s.definition(),"instantiated":True,"resh_governance":{"candidate_count":len(cand),"selection_rule":"max direct lexical evidence overlap; preserve ties","selected":selected}})
  for c in selected:byword[word].append({"node":s.name(),"glyph_string":"ר→"+c["glyph"],"operation_string":"GOVERN→"+c["operation"],"operation_hypernym_string":c["chain"],"evidence":c["matched_evidence"],"source_file":c["registry_file"]})
out={"trial":"014","name":"resh_hebrew_operational_hypernymization","input_state_sha":state["sha256_without_sha_field"],"registry_files_loaded":len(glyphs),"lesson_words":seeds,"instantiated_senses":len(records),"records":records,"operational_strings_by_word":dict(byword),"measurements":{"senses_with_glyph_evidence":sum(bool(r["resh_governance"]["selected"]) for r in records),"senses_without_glyph_evidence":sum(not r["resh_governance"]["selected"] for r in records),"selected_operational_strings":sum(len(r["resh_governance"]["selected"]) for r in records)},"attribution":{"glyph_chains":"PARSED FROM REPOSITORY GLYPH FILES","selection":"HARNESS-GENERATED lexical evidence; no word-to-glyph mapping","resh_role":"HUMAN-SPECIFIED governance rule","interpretation":"NONE"},"boundary":"Lexical overlap is eligibility evidence, not proof a glyph intrinsically represents an English word."}
raw=json.dumps(out,sort_keys=True); out["sha256_without_sha_field"]=hashlib.sha256(raw.encode()).hexdigest()
Path("results/resh_hebrew_operational_hypernymization_014.json").write_text(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True)+"\\n")
print(json.dumps({"trial":"014",**out["measurements"],"registry_files_loaded":len(glyphs),"instantiated_senses":len(records),"sample":{k:v[:3] for k,v in byword.items()}},ensure_ascii=False,indent=2))