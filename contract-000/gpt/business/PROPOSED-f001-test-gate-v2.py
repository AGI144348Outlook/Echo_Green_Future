"""Offline characterization for GPT F-001 gate v2.

Requires the source/, out1/, and rebuild_datasets.py fixtures from the
Contract000_Run294_Handoff.zip. Never writes to a repository or shared Library.
Run: python3 -I -B test_gate_v2.py
"""
import csv, json, shutil, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parent
results={}
script=root/'PROPOSED-f001-dataset-receipt-gate-v2.py'

def run(name, expected_exit, expected_integrity=None, expected_editorial=None, expected_release=None, mutator=None, release=False, invalid=False):
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'delivery'
        shutil.copytree(root/'out1',out)
        src=Path(td)/'source'
        shutil.copytree(root/'source',src)
        if mutator: mutator(out,src)
        cmd=[sys.executable,'-I','-B',str(script)]
        if release:cmd+=['--release-gate']
        if not invalid:cmd += [str(src),str(root/'rebuild_datasets.py'),str(out)]
        p=subprocess.run(cmd,capture_output=True,text=True)
        payload=json.loads(p.stdout) if p.stdout.strip() else None
        checks=[p.returncode==expected_exit]
        if expected_integrity is not None:checks.append(payload['integrity']==expected_integrity)
        if expected_editorial is not None:checks.append(payload['editorial']==expected_editorial)
        if expected_release is not None:checks.append(payload['release']==expected_release)
        if payload:checks.append(payload['source_pin_authenticated'] is False)
        results[name]={'exit':p.returncode,'integrity':payload.get('integrity') if payload else None,'editorial':payload.get('editorial') if payload else None,'release':payload.get('release') if payload else None,'expected_exit':expected_exit,'pass':all(checks),'stderr':p.stderr[:200]}

def mutate_b(out,src,fn):
    path=out/'dataset-b.csv'
    with path.open(newline='') as f:rows=list(csv.reader(f))
    fn(rows)
    with path.open('w',newline='') as f:csv.writer(f).writerows(rows)

run('baseline integrity-only',0,'PASS','HOLD','HOLD')
run('baseline release-gate',3,'PASS','HOLD','HOLD',release=True)
run('truncated B',1,'FAIL','HOLD','HOLD',mutator=lambda out,src:mutate_b(out,src,lambda rows:rows.pop()))
run('changed B ratio',1,'FAIL','HOLD','HOLD',mutator=lambda out,src:mutate_b(out,src,lambda rows:rows[1].__setitem__(0,'999')))
run('changed B registry sign',1,'FAIL','HOLD','HOLD',mutator=lambda out,src:mutate_b(out,src,lambda rows:rows[1].__setitem__(2,'ALTERED')))
run('missing B',1,'FAIL','HOLD','HOLD',mutator=lambda out,src:(out/'dataset-b.csv').unlink())
run('tampered report',1,'FAIL','HOLD','HOLD',mutator=lambda out,src:(out/'dataset-check.json').write_text('{}'))
run('extra B row',1,'FAIL','HOLD','HOLD',mutator=lambda out,src:mutate_b(out,src,lambda rows:rows.append(rows[-1][:])))
run('tampered source',1,'FAIL','HOLD','HOLD',mutator=lambda out,src:(src/'Dataset_B_Binary_Matrix.md').write_text('tampered'))
run('usage error',64,invalid=True)
Path(root/'test-results-v2.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'count':len(results),'passed':sum(v['pass'] for v in results.values()),'cases':results},indent=2))
if not all(v['pass'] for v in results.values()):sys.exit(1)
