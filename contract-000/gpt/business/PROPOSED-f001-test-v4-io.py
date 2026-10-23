#!/usr/bin/env python3
"""Offline Linux characterization of GPT F-001 v4 regular-file reader. Synthetic only."""
import csv, hashlib, io, json, os, subprocess, sys, tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name('PROPOSED-f001-disposition-binding-v4.py')
HEADER = ['object','measured_g','units','registry_sign','stated_deviation_pct','term','expected_g','recomputed_deviation_pct','stated_matches_recomputed']
row = ['Synthetic Sample','3.42','g','+','-0.03','test','3.425','-0.146','False']
b = io.StringIO(newline=''); w = csv.writer(b, lineterminator='\r\n'); w.writerow(HEADER); w.writerow(row)
CSV = b.getvalue().encode(); PIN = hashlib.sha256(CSV).hexdigest()
RECORD = json.dumps({'record_version':2,'dataset_a_sha256':PIN,'rows':[{
    'csv_line':2,'object':row[0],'measured_g':row[1],'units':row[2],
    'stated_deviation_pct':row[4],'recomputed_deviation_pct':row[7],
    'disposition':'RETAIN_STATED_WITH_DISCLOSURE','explanation':'SYNTHETIC; NOT APPROVED'
}], 'decision_reference':None}).encode()

with tempfile.TemporaryDirectory(prefix='f001-v4-io-') as tmp:
    d=Path(tmp); csv_path=d/'a.csv'; csv_path.write_bytes(CSV)
    cases=[('regular',0,'RECORDED_UNAUTHENTICATED'),('exact-bound',0,'RECORDED_UNAUTHENTICATED'),
           ('over-bound',1,'INVALID'),('fifo',1,'INVALID'),('symlink',1,'INVALID'),
           ('directory',1,'INVALID'),('device',1,'INVALID')]
    for name, expected_code, expected_status in cases:
        p=d/name
        if name=='regular': p.write_bytes(RECORD)
        elif name=='exact-bound': p.write_bytes(RECORD+b' '*(1048576-len(RECORD)))
        elif name=='over-bound': p.write_bytes(RECORD+b' '*(1048577-len(RECORD)))
        elif name=='fifo': os.mkfifo(p)
        elif name=='symlink': p.symlink_to(d/'regular')
        elif name=='directory': p.mkdir()
        elif name=='device': p=Path('/dev/zero')
        try:
            proc=subprocess.run([sys.executable,'-I','-B',str(SCRIPT),str(csv_path),str(p),PIN],
                                capture_output=True,text=True,timeout=4)
        except subprocess.TimeoutExpired as exc: raise AssertionError(f'{name}: HANG') from exc
        try: result=json.loads(proc.stdout)
        except json.JSONDecodeError as exc: raise AssertionError(f'{name}: no JSON report') from exc
        assert (proc.returncode,result['status'])==(expected_code,expected_status), (name,proc.returncode,result)
        assert result['release']=='HOLD' and result['source_pin_authenticated'] is False
        assert result['decision_reference_authenticated'] is False and not proc.stderr.strip()
        assert csv_path.read_bytes()==CSV
        print('PASS',name,proc.returncode,result['status'])
    print('PASS 7/7')
