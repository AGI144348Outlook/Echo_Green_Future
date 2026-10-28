#!/usr/bin/env python3
"""Run425 synthetic tests; PRE Issue #98. No private sales data.
Usage: python -I -B test_f001_ledger_stage_425.py /path/to/verified/ledger_merge.py
"""
import csv, importlib.util, json, os, subprocess, sys, tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parent
SOURCE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else BASE/'ledger_merge.py'
FIELDS=['date','fiscal_contract','kind','category','gross','fees','net',
        'asset_or_liability','share','source','source_ref','receipt_ref','evidence','entered_by']


def write(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)


def row(**kwargs):
    d=dict.fromkeys(FIELDS,'');d.update(date='2026-10-28',fiscal_contract='F-001',
        kind='income',category='product sales',gross='9.00',fees='1.00',net='8.00',
        source_ref='S1',**kwargs)
    return d


def case(label, old, new, expected, check=None, preexisting=False):
    with tempfile.TemporaryDirectory(prefix='f001-run425-synthetic-') as d:
        root=Path(d);src=root/'new.csv';out=root/'final.csv';write(src,new)
        prior='-'
        if old is not None:
            prior=root/'old.csv';write(prior,old)
        if preexisting:
            out.write_text('SENTINEL')
        cmd=[sys.executable,'-I','-B',str(BASE/'f001_ledger_stage_gate_425.py'),
             str(SOURCE),str(prior),str(src),str(out)]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=12)
        assert p.returncode==expected,(label,p.returncode,p.stdout,p.stderr)
        rep=json.loads(p.stdout)
        assert rep['status']==('PREPARED_HOLD' if expected==0 else 'HOLD'),(label,rep)
        assert out.exists()==(expected==0 or preexisting),(label,out.exists())
        if preexisting:assert out.read_text()=='SENTINEL'
        if expected==0:
            with out.open(newline='') as f: rows=list(csv.DictReader(f))
            assert len(rows)==len(old or [])+len([r for r in new if r['source_ref'] not in {x['source_ref'] for x in old or []}])
        assert not list(root.glob('.f001-stage-*')),label
        if check:check(rep)
        print('PASS',label,'exit',p.returncode,'final',out.exists())


def main():
    script=SOURCE;data=script.read_bytes()
    spec=importlib.util.spec_from_file_location('gate',BASE/'f001_ledger_stage_gate_425.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    assert mod.git_blob(data)==mod.ORIGINAL_GIT_BLOB
    good=row()
    case('valid new row',None,[good],0)
    case('valid existing plus new',[good],[dict(good,source_ref='S2')],0)
    case('same duplicate skipped',[good],[good],0)
    case('conflict',[good],[dict(good,net='7.00')],1)
    case('unkeyed',None,[dict(good,source_ref='')],1)
    case('blank net',None,[dict(good,net='')],1)
    case('invalid net',None,[dict(good,net='bad')],1)
    case('NaN net',None,[dict(good,net='NaN')],1)
    case('Infinity net',None,[dict(good,net='Infinity')],1)
    case('old blank net',[dict(good,net='')],[dict(good,source_ref='S2')],1)
    case('preexisting destination',None,[good],1,preexisting=True)
    case('duplicate old refs',[good,good],[dict(good,source_ref='S2')],1)
    # Isolated report-tamper negatives against the real gate's verifier, not original subprocess.
    with tempfile.TemporaryDirectory(prefix='f001-run425-verifier-') as d:
        path=Path(d)/'candidate.csv';write(path,[good]);base={'ledger_rows':0,'appended':1,'net_total':'8.00',
          'conflicts':[],'unkeyed_not_merged':[],'net_missing':[]}
        for label,rep in [('malformed report',{'status':'ok'}),('wrong total',dict(base,net_total='9.00')),
                          ('conflict flag',dict(base,conflicts=[{'source_ref':'S1'}])),
                          ('wrong row count',dict(base,appended=2))]:
            try:mod.verify_stage(path,rep)
            except ValueError:print('PASS',label,'rejected')
            else:raise AssertionError(label)
    print('PASS 16/16 bounded synthetic cases; source git blob',mod.git_blob(data))


if __name__=='__main__':main()
