"""Run440 preregistered isolated synthetic post-scan custody regression.
Tests EXACT Run439 gate blob, plus Run440 wrapper. NOT real TAM replay.
"""
import hashlib, json, tempfile
from pathlib import Path
import f001_raw_replay_gate_439 as base
import f001_postscan_custody_440 as improved

FAKE_SCANNER = r'''import csv,hashlib,json,sys
from pathlib import Path
src,out=map(Path,sys.argv[1:]); names=['README.md','Article 1 Hacksilber','Article 2 Water Weight Computes','The Color Dyed and Dental Records','Article 5','Article 6','Article 10','Collective information']
rows=[];counts={};hashes={}
for i,name in enumerate(names):
 raw=(src/name).read_bytes();hashes[name]=hashlib.sha256(raw).hexdigest()
 lines=raw.decode().split('|');counts[name]=len(lines)
 for n,line in enumerate(lines,1):rows.append([name,n,'accuracy',line,''])
with (out/'claims.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['file','sentence_no','triggers','sentence','status']);w.writerows(rows)
(out/'claims-report.json').write_text(json.dumps({'source_files':hashes,'per_file':counts,'per_trigger':{'accuracy':len(rows)},'rows':len(rows)}))
if '--mutate-source-after-report' in (src/'attack-control').read_text():
 (src/'Article 10').write_bytes(b'TAMPERED AFTER SCAN')
'''

with tempfile.TemporaryDirectory(prefix='f001-run440-') as temp:
    root=Path(temp);src=root/'src';src.mkdir();scanner=root/'synthetic_scanner.py';scanner.write_text(FAKE_SCANNER)
    base.SCANNER_BLOB=base.git_blob(scanner.read_bytes()) # test-only override; never committed in original gate
    improved.base.SCANNER_BLOB=base.SCANNER_BLOB # separate isolated import of same exact gate
    manifest={'project':'F-001','source_commit':'d46456a18fe412398d0ae37ec5a8c4eebb44e0c9','source_files':[],'rows':[]}
    for i,name in enumerate(base.FILES):
        count=6 if i<2 else 5
        lines=[f'Synthetic accuracy {name} sentence {j}.' for j in range(1,count+1)]
        raw='|'.join(lines).encode();(src/name).write_bytes(raw)
        manifest['source_files'].append({'path':name,'blob_sha':base.git_blob(raw)})
        manifest['rows'] += [{'source':name,'sentence_no':j,'triggers':['accuracy'],'excerpt':line[:170]} for j,line in enumerate(lines,1)]
    mp=root/'manifest.json';mp.write_text(json.dumps(manifest))
    (src/'attack-control').write_text('normal')
    results=[]
    def run(label,fn,mutate,expect_accept):
        (src/'attack-control').write_text('--mutate-source-after-report' if mutate else 'normal')
        # restore every source before each run
        for i,name in enumerate(base.FILES):
            count=6 if i<2 else 5
            (src/name).write_bytes('|'.join(f'Synthetic accuracy {name} sentence {j}.' for j in range(1,count+1)).encode())
        out=root/label
        try:
            r=fn(src,scanner,mp,out)
            accepted=True;reason=r.get('post_scan_source_custody','original accepted')
        except ValueError as e:
            accepted=False;reason=str(e)
        passed=accepted==expect_accept
        results.append({'case':label,'expected_accept':expect_accept,'actual_accept':accepted,'passed':passed,'detail':reason})
    run('original_clean',base.main,False,True)
    run('original_mutated_after_report',base.main,True,True) # documents weakness
    run('new_clean',improved.main,False,True)
    run('new_mutated_after_report',improved.main,True,False)
    print(json.dumps({'passed':sum(x['passed'] for x in results),'total':len(results),'cases':results},indent=2))
    assert all(x['passed'] for x in results)
