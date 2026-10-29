import csv
import hashlib
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import tempfile

HERE=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('gate',HERE/'F-001-SCANNER-SNAPSHOT-GATE-453.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
SCANNER=HERE/'claim_scan.py'
FILES=list(gate.PINS)
results={}

def check(name,condition):
    results[name]=bool(condition)
    if not condition: print('FAILED:',name)

check('scanner_exact_git_blob',gate.blob_sha(SCANNER.read_bytes())==gate.SCANNER_BLOB)
with tempfile.TemporaryDirectory() as tmp:
    p=pathlib.Path(tmp);src=p/'source';src.mkdir()
    (src/FILES[0]).write_text('Proof. Plain.',encoding='utf-8')
    baseline=subprocess.run([sys.executable,'-I',str(SCANNER),str(src),str(p/'baseline')],capture_output=True,text=True)
    rep=json.loads((p/'baseline'/'claims-report.json').read_text())
    check('original_scanner_missing_files_silent_success',baseline.returncode==0 and rep['rows']==1 and sum(v is None for v in rep['source_files'].values())==7)
    try: gate.snapshot(src,p/'snap');ok=False
    except (FileNotFoundError,ValueError,OSError):ok=True
    check('gate_rejects_missing_files',ok)
    for f in FILES[1:]: (src/f).write_text('Ordinary text. ',encoding='utf-8')
    pins={f:gate.blob_sha((src/f).read_bytes()) for f in FILES}
    snap=p/'snap';snap.mkdir()
    evidence=gate.snapshot(src,snap,pins)
    check('all_eight_snapshot_pins',len(evidence)==8 and all((snap/f).read_bytes()==(src/f).read_bytes() for f in FILES))
    (src/FILES[1]).write_text('Changed.',encoding='utf-8')
    (p/'snap2').mkdir()
    try: gate.snapshot(src,p/'snap2',pins);ok=False
    except ValueError:ok=True
    check('gate_rejects_tamper',ok)
    (src/FILES[1]).write_text('Ordinary text. ',encoding='utf-8')
    (src/FILES[2]).unlink();(src/FILES[2]).symlink_to(src/FILES[1])
    (p/'snap3').mkdir()
    try: gate.snapshot(src,p/'snap3',pins);ok=False
    except OSError:ok=True
    check('gate_rejects_symlink',ok)
    (src/FILES[2]).unlink();(src/FILES[2]).write_text('Ordinary text. ',encoding='utf-8')
    (p/'snap4').mkdir()
    try: gate.snapshot(src,p/'snap4',{FILES[0]:pins[FILES[0]]});ok=False
    except ValueError:ok=True
    check('gate_rejects_partial_manifest',ok)
    gate.PINS=pins
    result=gate.run(src,p/'good',SCANNER)
    check('guarded_synthetic_run_HOLD',result['status']=='HOLD' and result['rows']==1 and len(result['source_files'])==8)
    try: gate.run(src,p/'good',SCANNER);ok=False
    except ValueError:ok=True
    check('gate_no_clobber',ok)
    try: gate.run(src,src/'inside',SCANNER);ok=False
    except ValueError:ok=True
    check('gate_rejects_in_source_output',ok)
    src_link=p/'src_link';src_link.symlink_to(src,target_is_directory=True)
    try: gate.run(src_link,p/'symlinked',SCANNER);ok=False
    except ValueError:ok=True
    check('gate_rejects_symlink_root',ok)
    print(json.dumps({'results':results,'pass':sum(results.values()),'total':len(results),'synthetic_output_sha256':result['claims_csv_sha256']},indent=2))
    if not all(results.values()):sys.exit(1)
