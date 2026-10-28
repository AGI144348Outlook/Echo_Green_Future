#!/usr/bin/env python3
"""Synthetic isolated controls for F-001 scanner snapshot; no TAM originals needed."""
import hashlib
import json
import tempfile
from pathlib import Path
import importlib.util
_spec = importlib.util.spec_from_file_location("snapshot", Path(__file__).with_name("F-001-SCANNER-SNAPSHOT-412.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
git_blob, verify = _mod.git_blob, _mod.verify

GOOD_SCANNER = '''import csv,hashlib,json,sys
from pathlib import Path
src,out=Path(sys.argv[1]),Path(sys.argv[2]);out.mkdir()
files=sorted(src.iterdir());counts={p.name:1 for p in files}
with (out/'claims.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['file','sentence_no','triggers','sentence','status'])
 for p in files:w.writerow([p.name,1,'certainty','synthetic proof',''])
(out/'claims-report.json').write_text(json.dumps({'rows':len(files),'per_file':counts,'source_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}))
'''
BAD_SCANNER = GOOD_SCANNER.replace("'certainty','synthetic proof',''", "'certainty','synthetic proof','approved'")

def main():
    n=0
    with tempfile.TemporaryDirectory() as d:
        root=Path(d);src=root/'source';src.mkdir()
        for name in ['one','two']:(src/name).write_text('safe fixture '+name)
        scanner=root/'scanner.py';scanner.write_text(GOOD_SCANNER)
        pins={p.name:git_blob(p.read_bytes()) for p in src.iterdir()}
        sp=git_blob(scanner.read_bytes())
        assert verify(src,scanner,pins,sp,2)['rows']==2;n+=1
        (src/'one').write_text('tampered');
        try:verify(src,scanner,pins,sp,2);raise AssertionError('tamper accepted')
        except ValueError as e:assert 'mismatch' in str(e);n+=1
        (src/'one').write_text('safe fixture one');(src/'two').unlink()
        try:verify(src,scanner,pins,sp,2);raise AssertionError('missing accepted')
        except FileNotFoundError:n+=1
        (src/'two').write_text('safe fixture two');scanner.write_text(BAD_SCANNER)
        try:verify(src,scanner,pins,sp,2);raise AssertionError('scanner mutation accepted')
        except ValueError as e:assert 'mismatch' in str(e);n+=1
        badpin=git_blob(scanner.read_bytes())
        try:verify(src,scanner,pins,badpin,2);raise AssertionError('approval accepted')
        except ValueError as e:assert 'invalid source/status' in str(e);n+=1
        scanner.write_text(GOOD_SCANNER)
        try:verify(src,scanner,pins,sp,3);raise AssertionError('wrong count accepted')
        except ValueError as e:assert 'row count' in str(e);n+=1
    print(json.dumps({'passed':n,'total':6,'source':'synthetic only','release_authorized':False}))
if __name__=='__main__':main()
