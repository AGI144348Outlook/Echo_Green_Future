#!/usr/bin/env python3
"""14 synthetic-only pre-registered F-001 v4 report binding cases, no production files."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'PROPOSED-f001-receipt-v4-binding.py'
spec = importlib.util.spec_from_file_location('receipt_v4', SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def sha(x): return hashlib.sha256(x).hexdigest()

def fixture():
    contents = {k: ('SYNTHETIC-' + k).encode() for k in sorted(mod.ARTIFACTS)}
    pin = {'schema':'f001-pins/v1', 'source': {'repository':'AGI144348Outlook/The-TAM-protocol', 'commit':'a'*40},
           'inputs':{'article-1.md':'b'*40},
           'scripts':{'PROPOSED-f001-disposition-binding-v5.py':mod.V5_PARSER_BLOB,'build.py':'c'*40},
           'apply_order_blob':'d'*40,'applied_patches':{},
           'artifacts':{k:{'sha256':sha(v),'size':len(v)} for k,v in contents.items()}}
    rec = {'schema':'f001-receipt/v1', 'source':copy.deepcopy(pin['source']),
           'inputs':copy.deepcopy(pin['inputs']), 'scripts':copy.deepcopy(pin['scripts']),
           'apply_order_blob':pin['apply_order_blob'], 'applied_patches':{},
           'environment':{'platform':'synthetic','python_version':'3.13','build_output_realpath':'/synthetic'},
           'artifacts':{k:{'path':k+'.bin',**pin['artifacts'][k]} for k in contents},
           'editorial':{'release':'HOLD','status':'PENDING','source_pin_authenticated':False,
                        'decision_reference_authenticated':False,
                        'dataset_a_sha256':pin['artifacts']['dataset_a_csv']['sha256'],
                        'flagged_csv_lines':[6,7]},
           'release':'HOLD','approved':False,'timothy_approval_reference':None}
    v3={'schema':'f001-receipt-verification/v3','integrity':'PASS','release':'HOLD',
        'source_pin_authenticated':False,'approval_authenticated':False,
        'publication_authorization':'ABSENT','format_accessibility_rights_verified':False,
        'issues':[], 'artifacts_checked':[{'artifact':k,'sha256':sha(v),'bytes':len(v)} for k,v in contents.items()]}
    v5={'schema':'f001-v5-report-gate/v1','integrity':'PASS','release':'HOLD',
        'source_pin_authenticated':False,'approval_authenticated':False,
        'publication_authorization':'ABSENT','issues':[],
        'dataset_a_sha256':pin['artifacts']['dataset_a_csv']['sha256'],
        'v5_report_sha256':'e'*64,'v5_status':'PENDING','flagged_csv_lines':[6,7]}
    manifest={'schema':'f001-receipt-v4-binding/v1',
              'dataset_a_sha256':pin['artifacts']['dataset_a_csv']['sha256'],
              'v5_report_sha256':'e'*64,'v5_parser_blob':mod.V5_PARSER_BLOB,
              'v5_gate_blob':mod.V5_GATE_BLOB,'receipt_v3_blob':mod.V3_BLOB,
              'publication_authorized':False}
    return [pin,rec,v3,v5,manifest]

def modify(name, values):
    pin,rec,v3,v5,man=values
    if name=='C1_extra_pin_key':pin['publish']='READY'
    elif name=='C2_extra_pin_artifact_key':pin['artifacts']['epub']['approved']=True
    elif name=='C3_extra_receipt_artifact_key':rec['artifacts']['epub']['approved']=True
    elif name=='C4_extra_environment_key':rec['environment']['release']='READY'
    elif name=='C5_v5_wrong_dataset_sha':v5['dataset_a_sha256']='0'*64
    elif name=='C6_v5_wrong_flags':v5['flagged_csv_lines']=[6]
    elif name=='C7_wrong_v5_report_pin':man['v5_report_sha256']='0'*64
    elif name=='C8_wrong_parser_blob':man['v5_parser_blob']='0'*40
    elif name=='C9_receipt_v3_failed':v3['integrity']='FAIL'
    elif name=='C10_v5_gate_failed':v5['integrity']='FAIL'
    elif name=='C11_false_release':rec['release']='READY';rec['approved']=True
    elif name=='C12_three_line_v5_disagrees':v5['flagged_csv_lines']=[]
    elif name=='C13_boolean_size':pin['artifacts']['epub']['size']=True

CASES=['C0_consistent','C1_extra_pin_key','C2_extra_pin_artifact_key',
       'C3_extra_receipt_artifact_key','C4_extra_environment_key',
       'C5_v5_wrong_dataset_sha','C6_v5_wrong_flags','C7_wrong_v5_report_pin',
       'C8_wrong_parser_blob','C9_receipt_v3_failed','C10_v5_gate_failed',
       'C11_false_release','C12_three_line_v5_disagrees','C13_boolean_size']

def run(name):
    data=fixture();modify(name,data)
    before=sha(json.dumps(data,sort_keys=True).encode())
    result=mod.check_binding(*data)
    after=sha(json.dumps(data,sort_keys=True).encode())
    expected='PASS' if name=='C0_consistent' else 'FAIL'
    with tempfile.TemporaryDirectory(prefix='f001-v4-') as temp:
        root=Path(temp)
        files=[]
        for key,value in zip(('pins','receipt','v3-result','v5-result','binding-manifest'),data):
            p=root/(key+'.json');p.write_text(json.dumps(value,sort_keys=True));files.extend(['--'+key,str(p)])
        cp=subprocess.run([sys.executable,'-I','-B',str(SOURCE),*files],capture_output=True,text=True,timeout=5)
        cli=json.loads(cp.stdout)
    good=(before==after and result==cli and result['integrity']==expected and
          result['release']=='HOLD' and result['source_pin_authenticated'] is False and
          result['approval_authenticated'] is False and result['publication_authorization']=='ABSENT' and
          cp.returncode==(0 if expected=='PASS' else 1) and not cp.stderr)
    return {'case':name,'expected':expected+'/HOLD','actual':result['integrity']+'/HOLD',
            'exit':cp.returncode,'pass':good,'issues':result['issues']}

if __name__=='__main__':
    records=[run(x) for x in CASES]
    print(json.dumps({'total':len(records),'passed':sum(x['pass'] for x in records),'results':records},indent=2))
    sys.exit(0 if all(x['pass'] for x in records) else 1)
