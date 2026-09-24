from pathlib import Path
import json, hashlib
from collections import defaultdict

rows=json.loads(Path("lobbies/glyph/registry.json").read_text(encoding="utf-8"))

# Instantiate 22 copies of one common scaffold. Their lexical lobbies remain empty.
agents=[]
for r in rows:
    agents.append({
        "agent_id":f"glyph-{r['id']:02d}",
        "glyph":r["glyph"],
        "operation":r["operation"],
        "operation_class":r["operation_class"],
        "hypernyms":r["hypernyms"],
        "lexical_lobby":[],
    })

# Governor joins agents only through shared declared hypernym nodes.
node_members=defaultdict(list)
for a in agents:
    for depth,node in enumerate(a["hypernyms"]):
        node_members[node].append({"agent":a["agent_id"],"glyph":a["glyph"],"depth":depth})

shared={k:v for k,v in node_members.items() if len(v)>1}
edges=[]
for node,members in shared.items():
    ids=sorted({m["agent"] for m in members})
    for i,a in enumerate(ids):
        for b in ids[i+1:]:
            edges.append({"a":a,"b":b,"via":node})

pair_nodes=defaultdict(list)
for e in edges:
    pair_nodes[(e["a"],e["b"])].append(e["via"])

strongest=sorted(
    [{"a":a,"b":b,"shared":sorted(set(nodes)),"count":len(set(nodes))}
     for (a,b),nodes in pair_nodes.items()],
    key=lambda x:(-x["count"],x["a"],x["b"])
)

report={
    "experiment":"GLYPH_GOVERNOR_HYPERNYM_001",
    "agents":len(agents),
    "lexical_lobby_members":sum(len(a["lexical_lobby"]) for a in agents),
    "shared_hypernym_nodes":{k:len(v) for k,v in sorted(shared.items())},
    "pairwise_connections":len(strongest),
    "strongest_pairs":strongest[:30],
    "boundary":"Connections are derived from registry-declared hypernym chains only; this run does not demonstrate emergent cognition or autonomous agency."
}
payload=json.dumps(report,ensure_ascii=False,indent=2)
report["sha256"]=hashlib.sha256(payload.encode()).hexdigest()
Path("results/glyph_governor_hypernym_001.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

print("# GLYPH GOVERNOR HYPERNYM 001")
print("Subagent scaffolds:",len(agents))
print("Lexical lobby members:",report["lexical_lobby_members"])
print("Shared hypernym nodes:",len(shared))
print("Pairwise connected agent pairs:",len(strongest))
print("Strongest pairs:")
for x in strongest[:12]:
    print(x["a"],x["b"],x["count"],",".join(x["shared"]))
print("STATUS: GLYPH_GOVERNOR_HYPERNYM_001_EXECUTED")
