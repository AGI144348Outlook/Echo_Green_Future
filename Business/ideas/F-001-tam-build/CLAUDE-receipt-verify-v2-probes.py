#!/usr/bin/env python3
"""Claude F-001 §113 probes Q1-Q5 on GPT receipt verifier v2 (blob aa410ee). Synthetic fixtures only."""
import json, runpy, sys
from pathlib import Path
gpt = Path(sys.argv[1])
h = runpy.run_path(str(gpt / 'PROPOSED-f001-test-receipt-v2-regression.py'))
run_case = h['run_case']

def q1(root, p, r): r['editorial']['flagged_csv_lines'] = [6.0, 7.0]
def q2(root, p, r): r['artifacts']['epub']['size'] = float(r['artifacts']['epub']['size'])
def q3(root, p, r): pass  # baseline: 3-line Dataset A still "flags" lines 6, 7
def q4(root, p, r): r['publish'] = 'READY'
def q5(root, p, r): r['environment']['build_output_realpath'] = '/elsewhere/not-the-artifact-root'
cases = [('Q1_float_lines', q1, 0), ('Q2_float_size', q2, 0), ('Q3_lines_not_bound_to_bytes', q3, 0),
         ('Q4_unknown_top_level_ready', q4, 0), ('Q5_realpath_not_compared', q5, 0)]
res = [run_case(*c) for c in cases]
print(json.dumps({'as_expected': sum(x['pass'] for x in res), 'total': len(res), 'results': res}, indent=1))
