#!/usr/bin/env python3
"""F-001 §143 (Claude, 2026-10-29T12Z; records only, not pre-registered).
Maps every ID in ChatGPT's cross-queue audit (F-001-CROSS-QUEUE-407.json: 45 baseline + 37
supplemental occurrences) to its sentence text, using the same splitter as claim_scan.py, and
reports occurrences whose text is byte-identical. Read-only; writes nothing.
Usage: python3 -I CLAUDE-queue-dup-check-143.py <The-TAM-protocol clone @ d46456a> <F-001-CROSS-QUEUE-407.json>
"""
import re,sys,json,hashlib,subprocess
from pathlib import Path
from collections import defaultdict
def sentences(text): return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]
src=Path(sys.argv[1]); d=json.load(open(sys.argv[2]))
S={}; blobs={}
for name in ["README.md","Article 1 Hacksilber","Article 2 Water Weight Computes","The Color Dyed and Dental Records","Article 5","Article 6","Article 10","Collective information"]:
    S[name]=sentences((src/name).read_bytes().decode('utf-8','replace'))
    blobs[name]=subprocess.run(['git','-C',str(src),'rev-parse','HEAD:'+name],capture_output=True,text=True).stdout.strip()
ids=[('B',i) for i in d['baseline_ids']]+[('S',r['id']) for r in d['supplemental_refs']]
bad=[r for r in d['supplemental_refs'] if blobs[r['file']]!=r['blob_sha']]
print('ids',len(ids),'distinct',len({i for _,i in ids}),'supp blob mismatches',len(bad))
by=defaultdict(list)
for q,i in ids:
    f,n=i.rsplit('#S',1); t=S[f][int(n)-1]; by[hashlib.sha256(t.encode()).hexdigest()].append(q+':'+i)
dups={k:v for k,v in by.items() if len(v)>1}
print('distinct texts',len(by),'dup groups',len(dups))
for k,v in dups.items(): print(' ',v)
