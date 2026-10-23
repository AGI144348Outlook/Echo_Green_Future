"""Offline characterization for GPT F-001 gate v4.

Requires the source/, out1/, and rebuild_datasets.py fixtures from the
Contract000_Run296_Handoff.zip. Never writes to a repository or shared Library.
Run: python3 -I -B PROPOSED-f001-test-gate-v4.py
"""
import csv, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parent
results={}
script=root/'PROPOSED-f001-dataset-receipt-gate-v4.py'

def run(name, expected_exit, expected_integrity=None, expected_editorial=None, expected_release=None, mutator=None, release=False, invalid=False, gate_mutator=None):
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'delivery'
        shutil.copytree(root/'out1',out)
        src=Path(td)/'source'
        shutil.copytree(root/'source',src)
        if mutator: mutator(out,src)
        gate_script=script
        if gate_mutator:
            gate_script=Path(td)/'gate-under-test.py'
            gate_script.write_bytes(script.read_bytes())
            gate_mutator(gate_script,out,src)
        cmd=[sys.executable,'-I','-B',str(gate_script)]
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

# Claude §103 regression cases: do not claim clean editorial state if A is
# unreadable, structurally invalid, or byte-inconsistent with the pin.
run('missing A',1,'FAIL','NOT_EVALUATED','HOLD',mutator=lambda out,src:(out/'dataset-a.csv').unlink(),release=True)
def corrupt_a_header(out,src):
    p=out/'dataset-a.csv'
    p.write_bytes(p.read_bytes().replace(b'object,',b'obj,',1))
run('wrong A header',1,'FAIL','NOT_EVALUATED','HOLD',mutator=corrupt_a_header,release=True)
def corrupt_a_value(out,src):
    p=out/'dataset-a.csv'
    p.write_bytes(p.read_bytes().replace(b'3.42',b'3.43',1))
run('changed A bytes, valid header',1,'FAIL','NOT_EVALUATED','HOLD',mutator=corrupt_a_value,release=True)
run('changed A source',1,'FAIL','NOT_EVALUATED','HOLD',mutator=lambda out,src:(src/'Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)').write_text('tampered'),release=True)
# Claude §104 clean-A re-pin characterization: scratch ONLY. The delivered CSV
# changes both flagged booleans, and the temporary gate's A output digest is
# deliberately updated. This is NOT a new authenticated TAM source pin.
def clean_a_scratch_repin(gate_script,out,src):
    path=out/'dataset-a.csv'
    with path.open(newline='',encoding='utf-8') as fh: rows=list(csv.reader(fh))
    changed=0
    for row in rows[1:]:
        if row[-1]=='False': row[-1]='True'; changed+=1
    assert changed==2, f'expected two flagged rows, got {changed}'
    with path.open('w',newline='',encoding='utf-8') as fh: csv.writer(fh).writerows(rows)
    new_hash=hashlib.sha256(path.read_bytes()).hexdigest()
    original='d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2'
    code=gate_script.read_text()
    assert code.count(original)==1, 'expected one A digest literal'
    gate_script.write_text(code.replace(original,new_hash))

run('clean-A scratch re-pin integrity',0,'PASS','NO_FLAGGED_ROWS','OTHER_GATES_PENDING',gate_mutator=clean_a_scratch_repin)
run('clean-A scratch re-pin release',3,'PASS','NO_FLAGGED_ROWS','OTHER_GATES_PENDING',gate_mutator=clean_a_scratch_repin,release=True)

Path(root/'test-results-v4.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'count':len(results),'passed':sum(v['pass'] for v in results.values()),'cases':results},indent=2))
if not all(v['pass'] for v in results.values()):sys.exit(1)
