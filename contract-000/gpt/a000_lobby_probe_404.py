"""Isolated source-faithful slice of genesis-documentary ReshIdentity.anchor() Lobby update.
NOT the full Genesis class/runtime; only the list(set(...)) expression is transcribed.
"""
import json, os, subprocess, sys
EXTRA = ["governor", "indexing", "algorithm", "identity", "matrix", "aleph", "ayin", "pe"]
BASE = ["resh", "identity", "leader", "head"]
def update(definition_words):
    # Source-faithful operation from src/echo_governor_skeleton.py:3278-3282
    return list(set(definition_words + ["governor", "indexing", "algorithm", "identity", "matrix", "aleph", "ayin", "pe"]))
if '--child' in sys.argv:
    out=update(BASE)
    print(json.dumps({"order":out,"members":sorted(set(out)),"canonical":sorted(out)},ensure_ascii=False))
else:
    results=[]
    for seed in ["0","0","1","2","3","7","13","37","91"]:
        env=os.environ.copy();env['PYTHONHASHSEED']=seed
        cp=subprocess.run([sys.executable,__file__,'--child'],env=env,capture_output=True,text=True,check=True)
        results.append((seed,json.loads(cp.stdout)))
    orders={tuple(x['order']) for _,x in results}
    members={tuple(x['members']) for _,x in results}
    canonical={tuple(x['canonical']) for _,x in results}
    print(json.dumps({"probes":len(results),"distinct_orders":len(orders),"distinct_memberships":len(members),"distinct_canonical_orders":len(canonical),"same_seed_reproducible":results[0][1]['order']==results[1][1]['order'],"seeds":[{"seed":s,"order":r['order']} for s,r in results]},ensure_ascii=False,indent=2))
