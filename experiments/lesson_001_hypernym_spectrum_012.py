#!/usr/bin/env python3
"""Trial 012 — Lesson-001 subject-spectrum hypernym recurrence baseline.

Research question: when the Governor-style hypernym streamer is restricted to a
bounded lesson spectrum, do the accumulated WordNet hypernym paths themselves
form closures/cycles, and can an activation continue without artificial reseeding?

This is deliberately a baseline. It does NOT add reverse edges, similarity
edges, synonyms-as-transitions, or restart dead paths. Those can be treatments
later. Raw WordNet synset IDs are retained so polysemy cannot be hidden by a
surface word.
"""
from pathlib import Path
from collections import defaultdict, Counter, deque
import json, hashlib, subprocess, sys

try:
    from nltk.corpus import wordnet as wn
    wn.synsets("study")
except Exception:
    subprocess.run([sys.executable,"-m","pip","install","nltk","-q"],check=True)
    import nltk
    nltk.download("wordnet",quiet=True); nltk.download("omw-1.4",quiet=True)
    from nltk.corpus import wordnet as wn

SEEDS=["study","learn","focus","identify","differentiate","instantiate","designate","symbol"]
MINLEN,MAXLEN=3,8

def label(s):
    return s.lemmas()[0].name().replace("_"," ")

nodes={}
edges=[]
strings=[]
for seed in SEEDS:
    senses=wn.synsets(seed)
    for s in senses:
        q=deque([(s,[s])])
        while q:
            cur,path=q.popleft()
            hs=cur.hypernyms()
            if len(path)>=MINLEN:
                strings.append({
                    "seed":seed,
                    "sense":s.name(),
                    "nodes":[{"synset":x.name(),"label":label(x)} for x in path[:MAXLEN]],
                    "length":min(len(path),MAXLEN)
                })
            if len(path)>=MAXLEN: continue
            for h in hs:
                edges.append({"from":cur.name(),"to":h.name(),"relation":"hypernym","seed":seed})
                q.append((h,path+[h]))
            nodes[cur.name()]={"label":label(cur),"definition":cur.definition()}
            for h in hs: nodes[h.name()]={"label":label(h),"definition":h.definition()}

# Unique directed graph. Cycle detection uses synset identity, not labels.
adj=defaultdict(set)
for e in edges: adj[e["from"]].add(e["to"])
cycles=[]
state={}
stack=[]
pos={}
def dfs(u):
    state[u]=1; pos[u]=len(stack); stack.append(u)
    for v in sorted(adj[u]):
        if state.get(v,0)==0: dfs(v)
        elif state.get(v)==1:
            cyc=stack[pos[v]:]+[v]
            if 3 <= len(cyc) <= 32: cycles.append(cyc)
    stack.pop(); pos.pop(u,None); state[u]=2
for u in sorted(nodes):
    if state.get(u,0)==0: dfs(u)

# Convergence: synsets reached by multiple lesson seeds.
reach=defaultdict(set)
for e in edges:
    reach[e["to"]].add(e["seed"])
convergences=[
    {"synset":n,"label":nodes.get(n,{}).get("label",n),"seeds":sorted(ss),"seed_count":len(ss)}
    for n,ss in reach.items() if len(ss)>1
]
convergences.sort(key=lambda x:(-x["seed_count"],x["synset"]))

# One initial activation per seed/sense. Follow deterministic first hypernym only.
# This is not claimed as cognition; it answers whether strict upward streaming
# can keep moving or naturally becomes inert.
traces=[]
for seed in SEEDS:
    for s in wn.synsets(seed):
        cur=s; tr=[cur.name()]
        for pulse in range(1,65):
            hs=sorted(cur.hypernyms(),key=lambda x:x.name())
            if not hs: break
            cur=hs[0]; tr.append(cur.name())
            if cur.name() in tr[:-1]: break
        traces.append({"seed":seed,"sense":s.name(),"trace":tr,
                       "pulses":len(tr)-1,
                       "state":"RECURRENT" if tr[-1] in tr[:-1] else "INERT"})

out={
 "trial":"012",
 "name":"lesson_001_subject_spectrum_hypernym_recurrence_baseline",
 "attribution":{
   "curriculum":"HUMAN-AUTHORED",
   "traversal":"WORDNET HYPERNYM RELATIONS SELECTED BY DETERMINISTIC GOVERNOR-STYLE HARNESS",
   "report":"HARNESS-GENERATED",
   "interpretation":"NOT INCLUDED IN RAW RESULT"
 },
 "lesson_issue":4,
 "experiment_issue":6,
 "seeds":SEEDS,
 "string_bounds":[MINLEN,MAXLEN],
 "node_count":len(nodes),
 "edge_observations":len(edges),
 "unique_edges":sum(len(v) for v in adj.values()),
 "strings_recorded":len(strings),
 "cross_seed_convergences":len(convergences),
 "top_convergences":convergences[:30],
 "directed_cycles_found":len(cycles),
 "cycles":cycles[:100],
 "activation_traces":traces,
 "recurrent_traces":sum(t["state"]=="RECURRENT" for t in traces),
 "inert_traces":sum(t["state"]=="INERT" for t in traces),
 "strings":strings,
 "research_boundary":"A cycle is counted only if strict directed WordNet hypernym edges close on a previously visited synset. Surface-label collisions do not count. No reverse, synonym, similarity, cross-seed, or restart edge is injected."
}
payload=json.dumps(out,indent=2,sort_keys=True)
out["sha256_without_sha_field"]=hashlib.sha256(payload.encode()).hexdigest()
Path("results").mkdir(exist_ok=True)
Path("results/lesson_001_hypernym_spectrum_012.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({k:out[k] for k in ["trial","seeds","node_count","unique_edges","strings_recorded","cross_seed_convergences","directed_cycles_found","recurrent_traces","inert_traces","sha256_without_sha_field"]},indent=2))
