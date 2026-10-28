#!/usr/bin/env python3
"""Run424 HOLD-only original F-001 ledger regression; PRE: GitHub Issue #97.
Usage: python -I -B f001_ledger_regression_424.py /path/to/ledger_merge.py [--patched]
All CSVs synthetic and temporary outside the Git repository. Never use real sales.
"""
import csv, hashlib, json, subprocess, sys, tempfile
from pathlib import Path

FIELDS = ['date','fiscal_contract','kind','category','gross','fees','net',
          'asset_or_liability','share','source','source_ref','receipt_ref',
          'evidence','entered_by']
SOURCE_BLOB = '0f706be4229458ed20a25105ae18b58f90b93ff7'

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def run(script, old, incoming, root, name):
    new = root / (name+'-new.csv')
    out = root / (name+'-out.csv')
    def write(path, rows):
        with path.open('w', newline='', encoding='utf-8') as f:
            w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    write(new, incoming)
    prev='-'
    if old is not None:
        prev=root/(name+'-old.csv');write(prev,old)
    proc=subprocess.run([sys.executable,'-I','-B',str(script),str(prev),str(new),str(out)],capture_output=True,text=True,timeout=10)
    assert proc.stdout.startswith('{'),(name,proc.stderr)
    return proc.returncode,json.loads(proc.stdout),out.exists()

def main():
    assert len(sys.argv) in (2,3),__doc__
    script=Path(sys.argv[1]).resolve(); patched=len(sys.argv)==3 and sys.argv[2]=='--patched'
    data=script.read_bytes(); blob=git_blob(data)
    if not patched: assert blob==SOURCE_BLOB, f'wrong original source: {blob}'
    row=dict.fromkeys(FIELDS,'');row.update(date='2026-10-28',category='product sales',gross='9.00',fees='1.00',net='8.00',source_ref='S1')
    cases=[('valid',None,[row],0,False),('missing',None,[dict(row,net='')],1 if patched else 0,True),
           ('invalid',None,[dict(row,net='not-a-decimal')],1 if patched else 0,True),
           ('old-missing',[dict(row,net='')],[dict(row,source_ref='S2')],1 if patched else 0,True),
           ('conflict',[row],[dict(row,net='7.00')],1,False),
           ('unkeyed',None,[dict(row,source_ref='')],1,False)]
    with tempfile.TemporaryDirectory(prefix='f001-synthetic-outside-repo-') as d:
        for name,old,inc,expected,has_missing in cases:
            code,rep,written=run(script,old,inc,Path(d),name)
            assert code==expected,(name,code,expected)
            assert bool(rep['net_missing'])==has_missing,(name,rep)
            assert written,name
            print(f'PASS {name}: exit={code} net_missing={len(rep["net_missing"])}')
    print(f'PASS {len(cases)}/{len(cases)} original-source or patched-source regression cases; blob={blob}; patched={patched}')

if __name__=='__main__':main()
