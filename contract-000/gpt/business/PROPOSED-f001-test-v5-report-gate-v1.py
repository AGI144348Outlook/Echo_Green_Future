#!/usr/bin/env python3
"""Offline F-001 v5-report bridge characterization; synthetic editorial records only."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
GATE = HERE / 'PROPOSED-f001-v5-report-gate-v1.py'
V5 = HERE / 'PROPOSED-f001-disposition-binding-v5.py'
ARCHIVE = HERE / 'dataset-a-archived.csv'
HEADER = ["object", "measured_g", "units", "registry_sign", "stated_deviation_pct",
          "term", "expected_g", "recomputed_deviation_pct", "stated_matches_recomputed"]
BOUND = ("object", "measured_g", "units", "stated_deviation_pct", "recomputed_deviation_pct")

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, data):
    path.write_bytes(data)
    return path

def v5_output(csv_path, record_path):
    p = subprocess.run([sys.executable, '-I', '-B', str(V5), str(csv_path),
                        str(record_path), sha(csv_path.read_bytes())],
                       capture_output=True, timeout=5)
    assert p.returncode in (0,3), (p.returncode,p.stderr,p.stdout)
    return p.stdout

def disposition(csv_bytes):
    data=list(csv.reader(io.StringIO(csv_bytes.decode(), newline='')))
    assert data[0]==HEADER
    rows=[]
    for n,row in enumerate(data[1:],2):
        if row[-1]=='False':
            record=dict(zip(HEADER,row))
            rows.append({'csv_line':n,**{k:record[k] for k in BOUND},
                         'disposition':'RETAIN_STATED_WITH_DISCLOSURE',
                         'explanation':'SYNTHETIC TEST ONLY; not an editorial decision'})
    return json.dumps({'record_version':2,'dataset_a_sha256':sha(csv_bytes),
                       'decision_reference':'SYNTHETIC-NOT-APPROVED',
                       'rows':rows},sort_keys=True).encode()

def run_case(name, change, expect):
    with tempfile.TemporaryDirectory(prefix='f001-v5-gate-') as temp:
        root=Path(temp)
        csv_path=write(root/'dataset-a.csv',ARCHIVE.read_bytes())
        v5_path=write(root/'v5.py',V5.read_bytes())
        record_path=root/'editorial.json'
        report_path=write(root/'report.json',v5_output(csv_path,record_path))
        flags={'--dataset-a':str(csv_path),'--disposition-record':str(record_path),
               '--v5-script':str(v5_path),'--report-json':str(report_path),
               '--expected-dataset-sha256':sha(csv_path.read_bytes()),
               '--expected-report-sha256':sha(report_path.read_bytes())}
        if name=='recorded_synthetic_control':
            write(record_path,disposition(csv_path.read_bytes()))
            write(report_path,v5_output(csv_path,record_path))
            flags['--expected-report-sha256']=sha(report_path.read_bytes())
        change(root,flags)
        before={str(p):sha(p.read_bytes()) for p in (csv_path,v5_path,record_path,report_path)
                if p.is_file() and not p.is_symlink()}
        args=[sys.executable,'-I','-B',str(GATE)]
        for k,v in flags.items():args.extend([k,v])
        p=subprocess.run(args,capture_output=True,timeout=7)
        try: output=json.loads(p.stdout)
        except Exception as exc:raise AssertionError((name,p.returncode,p.stderr,p.stdout)) from exc
        after={str(p):sha(p.read_bytes()) for p in (csv_path,v5_path,record_path,report_path)
               if p.is_file() and not p.is_symlink()}
        assert before==after,(name,'mutated inputs')
        actual=(p.returncode,output['integrity'],output['release'])
        assert actual==(0 if expect else 1,'PASS' if expect else 'FAIL','HOLD'),(name,actual,output)
        assert output['source_pin_authenticated'] is False and output['approval_authenticated'] is False
        assert output['publication_authorization']=='ABSENT'
        return {'case':name,'expected':'PASS/HOLD' if expect else 'FAIL/HOLD',
                'actual':output['integrity']+'/HOLD','exit':p.returncode,
                'issues':output['issues'],'v5_status':output['v5_status']}

def noop(root,flags):pass

def recorded(root,flags):pass

def corrupt_csv(root,flags): (root/'dataset-a.csv').write_bytes((root/'dataset-a.csv').read_bytes()+b'\n')
def corrupt_v5(root,flags): (root/'v5.py').write_bytes((root/'v5.py').read_bytes()+b'#changed\n')
def wrong_digest(root,flags): flags.__setitem__('--expected-report-sha256','0'*64)
def missing_report(root,flags): (root/'report.json').unlink()
def forged_report(root,flags):
    p=root/'report.json'; obj=json.loads(p.read_text());obj['flagged_csv_lines']=[2,3];p.write_text(json.dumps(obj));flags['--expected-report-sha256']=sha(p.read_bytes())
def false_auth(root,flags):
    p=root/'report.json'; obj=json.loads(p.read_text());obj['source_pin_authenticated']=True;p.write_text(json.dumps(obj));flags['--expected-report-sha256']=sha(p.read_bytes())
def fake_3line(root,flags):
    raw=(root/'dataset-a.csv').read_bytes().splitlines(keepends=True)
    p=root/'dataset-a.csv';p.write_bytes(b''.join(raw[:3]));flags['--expected-dataset-sha256']=sha(p.read_bytes())
    r=root/'report.json';r.write_bytes(v5_output(p,root/'editorial.json'));flags['--expected-report-sha256']=sha(r.read_bytes())
def stale_report(root,flags):
    p=root/'dataset-a.csv';raw=p.read_bytes().replace(b'136.98',b'136.99');p.write_bytes(raw)
    flags['--expected-dataset-sha256']=sha(raw)
def duplicate_key(root,flags):
    p=root/'report.json';raw=p.read_bytes();p.write_bytes(raw[:-2]+b',"release":"HOLD"\n}')
    flags['--expected-report-sha256']=sha(p.read_bytes())
def symlink_report(root,flags):
    p=root/'report.json';q=root/'real-report.json';p.rename(q);p.symlink_to(q)
def oversized_report(root,flags):
    p=root/'report.json';p.write_bytes(b' '*1_048_577);flags['--expected-report-sha256']=sha(p.read_bytes())
def fifo_report(root,flags):
    import os
    p=root/'report.json';p.unlink();os.mkfifo(p)
def bad_record(root,flags):
    p=root/'editorial.json';p.write_bytes(disposition((root/'dataset-a.csv').read_bytes()))
    r=root/'report.json';r.write_bytes(v5_output(root/'dataset-a.csv',p));flags['--expected-report-sha256']=sha(r.read_bytes())
    p.write_bytes(p.read_bytes().replace(b'SYNTHETIC TEST ONLY',b'MUTATED TEST ONLY'))

CASES=[('pending_control',noop,True),('recorded_synthetic_control',recorded,True),
       ('changed_csv',corrupt_csv,False),('changed_v5_script',corrupt_v5,False),
       ('wrong_report_pin',wrong_digest,False),('missing_report',missing_report,False),
       ('forged_flag_lines',forged_report,False),('false_authentication',false_auth,False),
       ('three_line_dataset',fake_3line,False),('stale_report_after_csv_change',stale_report,False),
       ('duplicate_report_key',duplicate_key,False),('symlink_report',symlink_report,False),
       ('oversized_report',oversized_report,False),('fifo_report',fifo_report,False),
       ('changed_editorial_record',bad_record,False)]

def main():
    results=[]
    for name,func,expect in CASES:
        try:results.append(run_case(name,func,expect))
        except Exception as exc:
            print(json.dumps({'case':name,'error':repr(exc),'passed':len(results)},indent=2));return 1
    print(json.dumps({'total':len(results),'passed':len(results),'results':results},indent=2))
    return 0
if __name__=='__main__':sys.exit(main())
