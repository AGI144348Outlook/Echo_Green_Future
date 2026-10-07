#!/usr/bin/env python3
import json, hashlib, sys
from pathlib import Path

def sha256_text(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def form(data, raw):
    records=data.get("records",[])
    glyphs={}
    adjacency={}
    occurrences=[]
    descriptions={}
    for rec in records:
        rid=rec.get("id")
        desc=rec.get("description")
        descriptions.setdefault(desc,[]).append(rid)
        seq=[]
        for pos,g in enumerate(rec.get("graphemes",[])):
            gid=g.get("id"); feat=g.get("features",[])
            seq.append(gid)
            glyphs.setdefault(gid,{"id":gid,"observed_feature_vectors":[],"occurrences":0})
            glyphs[gid]["occurrences"]+=1
            if feat not in glyphs[gid]["observed_feature_vectors"]:
                glyphs[gid]["observed_feature_vectors"].append(feat)
            occurrences.append({"record_id":rid,"position":pos,"grapheme_id":gid,"features":feat})
        for a,b in zip(seq,seq[1:]):
            key=a+"→"+b
            adjacency[key]=adjacency.get(key,0)+1
    return {
      "registry_of_registries":[
        {"index":0,"name":"DSL Registry","status":"EMPTY","reason":"No IVS semantics or executable DSL declared by source sample."},
        {"index":1,"name":"Source Registry","count":1},
        {"index":2,"name":"Inscription Registry","count":len(records)},
        {"index":3,"name":"Grapheme Registry","count":len(glyphs)},
        {"index":4,"name":"Occurrence Registry","count":len(occurrences)},
        {"index":5,"name":"Adjacency Registry","count":len(adjacency)},
        {"index":6,"name":"Description Registry","count":len(descriptions)}
      ],
      "source_registry":[{"source":data.get("source"),"sha256":sha256_text(raw),"status":"OBSERVED"}],
      "inscription_registry":records,
      "grapheme_registry":sorted(glyphs.values(),key=lambda x:x["id"]),
      "occurrence_registry":occurrences,
      "adjacency_registry":[{"pair":k,"count":v,"status":"OBSERVED"} for k,v in sorted(adjacency.items())],
      "description_registry":[{"description":k,"record_ids":v,"status":"OBSERVED"} for k,v in descriptions.items()],
      "invariants":{
        "definition_is_not_authority":True,
        "registration_is_not_execution":True,
        "semantic_decipherment_attempted":False,
        "source_values_repaired":False
      }
    }

if __name__=="__main__":
    src=Path(sys.argv[1] if len(sys.argv)>1 else "IVS/tests/registry-formation-001/input/sample.json")
    out=Path(sys.argv[2] if len(sys.argv)>2 else "IVS/tests/registry-formation-001/output/result.json")
    raw=src.read_text(encoding="utf-8")
    result=form(json.loads(raw),raw)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["registry_of_registries"],indent=2))
