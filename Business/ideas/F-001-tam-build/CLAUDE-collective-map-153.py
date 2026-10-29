#!/usr/bin/env python3
"""F-001 §153 (Claude, 2026-10-29T22Z; records only, not pre-registered).
For every `Collective information` occurrence in ChatGPT's 82-occurrence queue (F-001-CROSS-QUEUE-407.json,
blob ab5e755c), find exact copies and the closest sentence (difflib ratio) in the other seven TAM files.
Uses claim_scan.py's splitter (same as CLAUDE-article-queue-145.py). Read-only; writes nothing.
Usage: python3 -I CLAUDE-collective-map-153.py <The-TAM-protocol clone @ d46456a> <F-001-CROSS-QUEUE-407.json>
"""
import re,sys,json,difflib
from pathlib import Path
def sentences(t): return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", t) if s.strip()]
def norm(s): return re.sub(r'\s+',' ',s.replace('​','')).strip().lower()
src=Path(sys.argv[1]); d=json.load(open(sys.argv[2]))
FILES=['README.md','Article 1 Hacksilber','Article 2 Water Weight Computes','The Color Dyed and Dental Records','Article 5','Article 6','Article 10']
S={f:sentences((src/f).read_bytes().decode('utf-8','replace')) for f in FILES}
C=sentences((src/'Collective information').read_bytes().decode('utf-8','replace'))
q={i:'baseline' for i in d['baseline_ids']}; q.update({r['id']:r['group_id'] for r in d['supplemental_refs']})
ids=sorted((int(k.split('#S')[1]),v) for k,v in q.items() if k.startswith('Collective information#'))
stats={'exact':0,'near':0,'none':0}
for n,tag in ids:
    c=C[n-1]; nc=norm(c); best=(0,None,None)
    for f in FILES:
        for i,s in enumerate(S[f],1):
            r=difflib.SequenceMatcher(None,nc,norm(s)).ratio()
            if r>best[0]: best=(r,f,i)
    kind='exact' if best[0]==1 else ('near' if best[0]>=0.8 else 'none')
    stats[kind]+=1
    print('C%d\t%s\t%s\t%.3f\t%s#S%s\t%s'%(n,tag,kind,best[0],best[1],best[2],c.replace('\n',' | ')[:220]))
print('collective queue ids',len(ids),stats)
