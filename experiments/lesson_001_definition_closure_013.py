#!/usr/bin/env python3
"""Trial 013 — persist Trial-012 experience and test definition-neighborhood closure.

No semantic conclusion is injected. Trial 012 observations become the persistent
Lesson-001 spectrum. WordNet definitions are then inspected as evidence. A
definition edge is admitted only when a definition token resolves to an already
experienced spectrum lemma. Closures are detected after admission; closures are
not prewired. Closed circuits may pulse their anchor and launch a 3–8 node
hypernym string using already observed/admitted relations.
"""
from pathlib import Path
from collections import defaultdict, deque
import json,re,hashlib,subprocess,sys
try:
 from nltk.corpus import wordnet as wn
 wn.synsets("study")
except Exception:
 subprocess.run([sys.executable,"-m","pip","install","nltk","-q"],check=True)
 import nltk;nltk.download("wordnet",quiet=True);nltk.download("omw-1.4",quiet=True)
 from nltk.corpus import wordnet as wn

prior=json.loads(Path("results/lesson_001_hypernym_spectrum_012.json").read_text())
SEEDS=prior["seeds"]
# Reconstruct exact experienced synsets/edges from recorded strings + traces.
nodes={}
edgeprov={}
for st in prior["strings"]:
 ns=st["nodes"]
 for n in ns:nodes[n["synset"]]={"label":n["label"],"source_trial":"012"}
 for a,b in zip(ns,ns[1:]): edgeprov[(a["synset"],b["synset"])]={"relation":"hypernym","source_trial":"012"}
for tr in prior["activation_traces"]:
 for sid in tr["trace"]:
  s=wn.synset(sid);nodes[sid]={"label":s.lemmas()[0].name().replace("_"," "),"source_trial":"012"}
 for a,b in zip(tr["trace"],tr["trace"][1:]):edgeprov[(a,b)]={"relation":"hypernym","source_trial":"012"}

# Index experienced lemma words to synsets.
lemma_index=defaultdict(set)
for sid in nodes:
 s=wn.synset(sid)
 for l in s.lemmas():
  lemma_index[l.name().lower().replace("_"," ")].add(sid)

stop={"a","an","the","of","to","and","or","in","on","for","with","as","by","that","which","is","are","be","being","something","someone","some"}
def toks(txt):return [x.lower() for x in re.findall(r"[A-Za-z][A-Za-z_-]*",txt) if x.lower() not in stop]

definition_edges=[]
for sid in sorted(nodes):
 s=wn.synset(sid); seen=set()
 for tok in toks(s.definition()):
  key=tok.replace("_"," ")
  for target in sorted(lemma_index.get(key,())):
   if target!=sid and target not in seen:
    definition_edges.append({"from":sid,"to":target,"relation":"definition_mentions_experienced_lemma",
      "evidence_token":key,"definition":s.definition(),"source":"WordNet","admitted_in_trial":"013"})
    seen.add(target)

# Combined directed evidence graph.
adj=defaultdict(set)
for (a,b) in edgeprov:adj[a].add(b)
for e in definition_edges:adj[e["from"]].add(e["to"])

# SCCs identify genuine directed closure in combined evidence graph.
index=0;stack=[];on=set();idx={};low={};sccs=[]
def strong(v):
 global index
 idx[v]=low[v]=index;index+=1;stack.append(v);on.add(v)
 for w in adj[v]:
  if w not in idx:strong(w);low[v]=min(low[v],low[w])
  elif w in on:low[v]=min(low[v],idx[w])
 if low[v]==idx[v]:
  comp=[]
  while True:
   w=stack.pop();on.remove(w);comp.append(w)
   if w==v:break
  if len(comp)>1 or v in adj[v]:sccs.append(sorted(comp))
for v in sorted(nodes):
 if v not in idx:strong(v)

# Pulse each lesson seed sense that lies in a closure. After a closure return,
# launch outward through an observed hypernym path, max 8 nodes.
closed=set(x for c in sccs for x in c)
pulses=[]
for seed in SEEDS:
 for s in wn.synsets(seed):
  if s.name() not in closed:continue
  # shortest return cycle from anchor
  anchor=s.name();q=deque([(anchor,[anchor])]);cycle=None
  while q and not cycle:
   u,path=q.popleft()
   for v in sorted(adj[u]):
    if v==anchor and len(path)>=2:cycle=path+[anchor];break
    if v not in path and len(path)<12:q.append((v,path+[v]))
  if not cycle:continue
  # launch strict hypernym stream from anchor after pulse
  cur=s;stream=[cur.name()]
  for _ in range(7):
   hs=sorted(cur.hypernyms(),key=lambda z:z.name())
   if not hs:break
   cur=hs[0];stream.append(cur.name())
  pulses.append({"anchor_seed":seed,"anchor_synset":anchor,"closure":cycle,
                 "pulse_event":"closure_returned_to_anchor",
                 "launched_hypernym_string":stream})

state={
 "state_id":"LESSON_001_SUBJECT_SPECTRUM",
 "through_trial":"013",
 "prior_result_sha":prior.get("sha256_without_sha_field"),
 "experienced_nodes":nodes,
 "experienced_hypernym_edges":[{"from":a,"to":b,**p} for (a,b),p in sorted(edgeprov.items())],
 "definition_edges_admitted":definition_edges,
 "closures":sccs,
 "pulse_events":pulses,
 "attribution":{
  "trial_012_graph":"ECHO EXPERIENTIAL STATE: measured prior traversal observations",
  "definition_edges":"EVIDENCE-DERIVED: WordNet definition token matched an already experienced lemma",
  "closure_detection":"HARNESS MEASUREMENT",
  "pulse_rule":"HUMAN-SPECIFIED MECHANISM",
  "english_interpretation":"NONE"
 }
}
raw=json.dumps(state,indent=2,sort_keys=True)
state["sha256_without_sha_field"]=hashlib.sha256(raw.encode()).hexdigest()
Path("state").mkdir(exist_ok=True)
Path("state/lesson_001_subject_spectrum.json").write_text(json.dumps(state,indent=2,sort_keys=True)+"\n")
summary={
 "trial":"013","persisted_trial_012_nodes":len(nodes),"persisted_trial_012_edges":len(edgeprov),
 "definition_edges_admitted":len(definition_edges),"closed_components":len(sccs),
 "nodes_in_closed_components":len(closed),"pulse_events":len(pulses),
 "pulse_samples":pulses[:20],"state_sha":state["sha256_without_sha_field"]
}
Path("results/lesson_001_definition_closure_013.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
print(json.dumps(summary,indent=2))
