#!/usr/bin/env python3
"""Run 312 prospective local tests registered in Echo_Green_Future Issue #31."""
import hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys, tempfile
from types import SimpleNamespace
ROOT=pathlib.Path(__file__).resolve().parent
TOOLS=ROOT/'tools'; ART=ROOT/'artifacts'
SRC=TOOLS/'PROPOSED-f001-source-pinned-coordinator-v4.py'
spec=importlib.util.spec_from_file_location('candidate',SRC);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
name={'receipt_v3':'PROPOSED-f001-receipt-verify-v3.py','v5_gate':'PROPOSED-f001-v5-report-gate-v1.py','v4_binding':'PROPOSED-f001-receipt-v4-binding.py','v5_parser':'PROPOSED-f001-disposition-binding-v5.py'}
def args(toolroot=TOOLS):
 return SimpleNamespace(artifact_root=str(ART),tool_root=str(toolroot),pins=str(ART/'pins.json'),receipt=str(ART/'receipt.json'),binding_manifest=str(ART/'binding.json'),v5_report=str(ART/'v5-report.json'),disposition_record=str(ART/'disposition.json'),**{k:str(toolroot/v) for k,v in name.items()})
def verdict(r, expected, reason=None):
 assert r['integrity']==expected and r['release']=='HOLD' and r['readiness']=='BLOCKED' and r['publication_authorization']=='ABSENT',r
 assert r['source_pin_authenticated'] is False and r['approval_authenticated'] is False
 if reason: assert any(reason in x for x in r['issues']),r
 return {'integrity':r['integrity'],'release':r['release'],'readiness':r['readiness'],'issues':r['issues'],'stages':r['stages']}
results={}
# 1: genuine reviewed-script chain, archived public-derived Dataset A, synthetic EPUB/PDF.
r=m.coordinate(args());results['control']=verdict(r,'PASS');assert len(r['stages'])==3
# 2: lexical path confusion; raw string is not allowed to differ from checked path.
with tempfile.TemporaryDirectory() as outside:
 p=pathlib.Path(outside);(p/'sub').mkdir();(p/'pins.json').write_text('{"forged":true}')
 link=ART/'run312_link'
 try:
  link.symlink_to(p/'sub',target_is_directory=True)
  a=args();a.pins=str(link/'..'/'pins.json')
  r=m.coordinate(a);results['lexical_parent_traversal']=verdict(r,'FAIL','parent traversal')
 finally:link.unlink(missing_ok=True)
# 3+4: deliberately unreviewed local stubs with test-only explicit blob overrides.
for case,script,expected_reason in [
 ('nonobject_stdout','print("[]")\n','must be JSON object'),
 ('oversized_stdout','import sys\nsys.stdout.write("x"*1052672)\n','output exceeds bound')]:
 with tempfile.TemporaryDirectory() as td:
  t=pathlib.Path(td);mapping={};expected={}
  for k in name:
   content=script if k=='receipt_v3' else 'import json\nprint(json.dumps({"integrity":"FAIL","release":"HOLD"}))\n'
   f=t/name[k];f.write_text(content);expected[k]=m.git_blob(f.read_bytes())
  r=m.coordinate(args(t),expected_blobs=expected)
  results[case]=verdict(r,'FAIL',expected_reason)
# 5: forged symlink ancestor rejected even without ..
with tempfile.TemporaryDirectory() as td:
 p=pathlib.Path(td);(p/'sub').mkdir();link=ART/'run312_link'
 try:
  link.symlink_to(p/'sub',target_is_directory=True)
  a=args();a.pins=str(link/'pins.json')
  r=m.coordinate(a);results['symlink_path']=verdict(r,'FAIL','symlink')
 finally:link.unlink(missing_ok=True)
results['metadata']={'python':sys.version.split()[0],'candidate_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'candidate_git_blob':m.git_blob(SRC.read_bytes()),'previous_v3_git_blob':m.git_blob((TOOLS/'PROPOSED-f001-source-pinned-coordinator-v3.py').read_bytes()),'tests':len(results),'fixture_kind':'archived public-derived Dataset A and synthetic placeholder EPUB/PDF','pretest_issue':'https://github.com/AGI144348Outlook/Echo_Green_Future/issues/31'}
(ROOT/'evidence'/'v4-results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v['integrity'] for k,v in results.items() if k!='metadata'}));print('CONFIRMED',len(results)-1,'/',len(results)-1)
