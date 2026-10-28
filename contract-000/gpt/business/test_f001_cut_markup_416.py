#!/usr/bin/env python3
"""Synthetic pre-registered Run416 markup-aware F-001 cut-gate controls."""
import csv, importlib.util, json, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cut416',HERE/'F-001-CUT-MARKUP-GATE-416.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
BASE={'file':'Article 1','sentence_no':'1','triggers':'certainty','sentence':'A source claim should be cut.','status':'cut'}
def run_case(root,manuscript,rows=None,expected=None):
    c=root/'claims.csv'; m=root/'draft.md'
    with c.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=gate.HEADER);w.writeheader();w.writerows([BASE] if rows is None else rows)
    m.write_text(manuscript,encoding='utf-8')
    try: return gate.check(c,m,expected),c,m
    except ValueError as e: return str(e),c,m

def main():
    tests={}
    with tempfile.TemporaryDirectory(prefix='f001-markup416-') as td:
        root=Path(td)
        for label,text in {
            'literal':'A source claim should be cut.',
            'markdown_bold':'A source **claim** should be cut.',
            'markdown_italic':'A source _claim_ should be cut.',
            'markdown_link':'A source [claim](https://example.invalid) should be cut.',
            'html_em':'A source <em>claim</em> should be cut.',
            'html_span':'A source <span>claim</span> should be cut.',
            'linebreak':'A source\nclaim should be cut.',
            'zero_width':'A source\u200b claim should be cut.',
            'nfkc':'Ａ source claim should be cut.',
        }.items():
            result,_,_=run_case(root,text)
            tests['reject_'+label]=isinstance(result,str) and 'cut claim remains' in result
        result,_,_=run_case(root,'A different statement.')
        tests['positive_cut_absent_hold']=isinstance(result,dict) and result['release_authorized'] is False and result['cut_rows_absent_in_projection']==1
        result,_,_=run_case(root,'A source claim should be cut.',[{**BASE,'status':'sourced'}])
        tests['positive_sourced_no_release']=isinstance(result,dict) and result['release_authorized'] is False
        result,_,_=run_case(root,'No claim.',[{**BASE,'status':''}]);tests['reject_unreviewed']=isinstance(result,str)
        result,_,_=run_case(root,'No claim.',[BASE,BASE]);tests['reject_duplicate']=isinstance(result,str) and 'duplicate' in result
        result,_,_=run_case(root,'No claim.',[]);tests['reject_empty']=isinstance(result,str)
        result,_,_=run_case(root,'No claim.',expected=2);tests['reject_count_mismatch']=isinstance(result,str)
        result,_,_=run_case(root,'No claim.',expected=1);tests['positive_count_match']=isinstance(result,dict)
        result,c,m=run_case(root,'No claim.');c.unlink();
        try:gate.check(c,m);tests['reject_missing']=False
        except (ValueError,OSError):tests['reject_missing']=True
        result,c,m=run_case(root,'No claim.');m.unlink();m.symlink_to(c)
        try:gate.check(c,m);tests['reject_symlink']=False
        except ValueError:tests['reject_symlink']=True
    print(json.dumps({'passed':sum(tests.values()),'total':len(tests),'checks':tests},indent=2))
    if not all(tests.values()):raise SystemExit(1)
if __name__=='__main__':main()
