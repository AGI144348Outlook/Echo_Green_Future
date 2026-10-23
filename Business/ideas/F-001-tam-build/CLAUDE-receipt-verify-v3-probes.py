#!/usr/bin/env python3
"""Claude F-001 §114 probes T1-T6 on GPT receipt verifier v3 (blob 4aafb14). Synthetic fixtures only.
Usage: python3 -I -B CLAUDE-receipt-verify-v3-probes.py <dir holding GPT v3 + v2 regression harness>"""
import json, os, runpy, sys
from pathlib import Path
gpt = Path(sys.argv[1])
h = runpy.run_path(str(gpt / 'PROPOSED-f001-test-receipt-v2-regression.py'))
run_case = h['run_case']
run_case.__globals__['SCRIPT'] = gpt / 'PROPOSED-f001-receipt-verify-v3.py'

def t1(root, p, r): r['environment']['build_output_realpath'] = str(root / 'does-not-exist')
def t2(root, p, r):
    link = root / 'root-link'; os.symlink(root, link)  # inside the temp dir, removed with it
    r['environment']['build_output_realpath'] = str(link)
def t3(root, p, r): r['artifacts']['epub']['approved'] = True
def t4(root, p, r): r['environment']['release'] = 'READY'
def t5(root, p, r): pass  # baseline: 3-line Dataset A still "flags" lines 6, 7
def t6(root, p, r): p['release'] = 'READY'
cases = [('T1_realpath_missing', t1, 1), ('T2_realpath_symlink_to_root', t2, 0),
         ('T3_extra_key_in_artifact_record', t3, 0), ('T4_extra_key_in_environment', t4, 0),
         ('T5_lines_not_bound_to_bytes', t5, 0), ('T6_unknown_key_in_pin_manifest', t6, 0)]
res = [run_case(*c) for c in cases]
print(json.dumps({'as_expected': sum(x['pass'] for x in res), 'total': len(res), 'results': res}, indent=1))
