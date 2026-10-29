#!/usr/bin/env python3
"""F-001 §144 (Claude, 2026-10-29T13Z; records only, not pre-registered).
Lists Article 6's sentences (claim_scan.py splitter), marks which are in ChatGPT's 82-occurrence
queue (F-001-CROSS-QUEUE-407.json, blob ab5e755), and finds where Article 6 is copied in
`Collective information`. Read-only; writes nothing.
Usage: python3 -I CLAUDE-article6-queue-144.py <The-TAM-protocol clone @ d46456a> <F-001-CROSS-QUEUE-407.json>
"""
import re,sys,json
from pathlib import Path
def sentences(text): return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]
src=Path(sys.argv[1]); d=json.load(open(sys.argv[2]))
A=sentences((src/'Article 6').read_bytes().decode('utf-8','replace'))
C=sentences((src/'Collective information').read_bytes().decode('utf-8','replace'))
q={i:'baseline' for i in d['baseline_ids']}; q.update({r['id']:'supplemental:'+r['group_id'] for r in d['supplemental_refs']})
for n,s in enumerate(A,1):
    copies=[i+1 for i,c in enumerate(C) if c==s]
    tags=[q.get('Article 6#S%d'%n,'-')]+['C%d:%s'%(c,q.get('Collective information#S%d'%c,'-')) for c in copies]
    print(n,' '.join(tags),'|',s.replace('\n',' | ')[:110])
