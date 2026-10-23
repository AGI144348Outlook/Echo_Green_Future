#!/usr/bin/env python3
"""F-001 GPT v5 local Linux IO probes; synthetic fixtures only, no publication."""
import csv, hashlib, io, json, os, subprocess, sys, tempfile
from pathlib import Path
SCRIPT = Path(__file__).with_name('PROPOSED-f001-disposition-binding-v5.py')
HEADER = ['object','measured_g','units','registry_sign','stated_deviation_pct','term','expected_g','recomputed_deviation_pct','stated_matches_recomputed']
ROW = ['Synthetic Sample','3.42','g','+','-0.03','test','3.425','-0.146','False']
buf = io.StringIO(newline='')
w = csv.writer(buf, lineterminator='\r\n'); w.writerow(HEADER); w.writerow(ROW)
DATA = buf.getvalue().encode(); PIN = hashlib.sha256(DATA).hexdigest()
REC = json.dumps({'record_version':2,'dataset_a_sha256':PIN,'rows':[{
    'csv_line':2,'object':ROW[0],'measured_g':ROW[1],'units':ROW[2],
    'stated_deviation_pct':ROW[4],'recomputed_deviation_pct':ROW[7],
    'disposition':'RETAIN_STATED_WITH_DISCLOSURE','explanation':'SYNTHETIC, NO APPROVAL'}],
    'decision_reference':None}).encode()

with tempfile.TemporaryDirectory(prefix='f001-v5-csv-') as t:
    root = Path(t); real = root/'real.csv'; real.write_bytes(DATA)
    record = root/'record.json'; record.write_bytes(REC)
    cases = [
        ('baseline', real, PIN, 0, 'RECORDED_UNAUTHENTICATED'),
        ('csv-pin-mismatch', real, '0'*64, 1, 'INVALID'),
    ]
    fifo=root/'fifo.csv'; os.mkfifo(fifo); cases.append(('csv-fifo', fifo, PIN, 1, 'INVALID'))
    directory=root/'folder.csv'; directory.mkdir(); cases.append(('csv-directory', directory, PIN, 1, 'INVALID'))
    sym=root/'sym.csv'; sym.symlink_to(real); cases.append(('csv-symlink', sym, PIN, 1, 'INVALID'))
    broken=root/'broken.csv'; broken.symlink_to(root/'missing.csv'); cases.append(('csv-broken-symlink', broken, PIN, 1, 'INVALID'))
    large=root/'large.csv'; large.write_bytes(DATA + b' '*(1048577-len(DATA)))
    cases.append(('csv-oversize', large, hashlib.sha256(large.read_bytes()).hexdigest(), 1, 'INVALID'))
    cases.append(('csv-device', Path('/dev/zero'), PIN, 1, 'INVALID'))
    dangling_record=root/'dangling-record.json'; dangling_record.symlink_to(root/'missing.json')
    cases.append(('record-broken-symlink', real, PIN, 1, 'INVALID'))
    results=[]
    for name, source, pin, exp_code, exp_status in cases:
        rec_path = dangling_record if name=='record-broken-symlink' else record
        before = {str(p):p.read_bytes() for p in (real,record) if p.exists() and p.is_file()}
        try:
            p=subprocess.run([sys.executable,'-I','-B',str(SCRIPT),str(source),str(rec_path),pin],
                             capture_output=True,text=True,timeout=4)
        except subprocess.TimeoutExpired as e:
            raise AssertionError(f'{name}: hung') from e
        try: out=json.loads(p.stdout)
        except json.JSONDecodeError as e: raise AssertionError(f'{name}: no JSON report {p.stderr}') from e
        assert (p.returncode,out['status'])==(exp_code,exp_status), (name,p.returncode,out)
        assert out['release']=='HOLD' and out['source_pin_authenticated'] is False and out['decision_reference_authenticated'] is False
        assert not p.stderr.strip(), (name,p.stderr)
        assert all(Path(path).read_bytes()==payload for path,payload in before.items()), (name,'input mutation')
        results.append({'case':name,'exit':p.returncode,'status':out['status'],'error':out['errors'][:1]})
        print('PASS',name,p.returncode,out['status'])
    print('PASS',len(results),'/',len(cases))
    (root/'results.json').write_text(json.dumps(results,indent=2))
