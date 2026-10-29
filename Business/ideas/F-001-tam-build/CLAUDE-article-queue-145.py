#!/usr/bin/env python3
"""F-001 §145 (Claude, 2026-10-29T14Z; records only, not pre-registered).
Generalises CLAUDE-article6-queue-144.py to any TAM article: lists the article's sentences (claim_scan.py
splitter), marks which are in ChatGPT's 82-occurrence queue (F-001-CROSS-QUEUE-407.json, blob ab5e755),
and finds where each sentence is copied in `Collective information`. Read-only; writes nothing.
Usage: python3 -I CLAUDE-article-queue-145.py <The-TAM-protocol clone @ d46456a> <F-001-CROSS-QUEUE-407.json> "<Article name>"
"""
import re,sys,json
from pathlib import Path
def sentences(text): return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]
src=Path(sys.argv[1]); d=json.load(open(sys.argv[2])); name=sys.argv[3]
A=sentences((src/name).read_bytes().decode('utf-8','replace'))
C=sentences((src/'Collective information').read_bytes().decode('utf-8','replace'))
q={i:'baseline' for i in d['baseline_ids']}; q.update({r['id']:'supplemental:'+r['group_id'] for r in d['supplemental_refs']})
inq=0
for n,s in enumerate(A,1):
    copies=[i+1 for i,c in enumerate(C) if c==s]
    tags=[q.get('%s#S%d'%(name,n),'-')]+['C%d:%s'%(c,q.get('Collective information#S%d'%c,'-')) for c in copies]
    inq+=sum(t!='-' and not t.endswith(':-') for t in tags)
    print(n,' '.join(tags),'|',s.replace('\n',' | ')[:400])
print('sentences',len(A),'queue occurrences',inq,'queue ids for this article',sorted(k for k in q if k.startswith(name+'#')))
