#!/usr/bin/env python3
"""F-001 v2 editorial-state characterization, synthetic fixtures only."""
import json
from pathlib import Path
import runpy
import sys

h = runpy.run_path(str(Path(__file__).with_name('PROPOSED-f001-test-receipt-v2-regression.py')))
run_case = h['run_case']

def noop(root, pins, receipt): pass

def no_flagged(root, pins, receipt):
    receipt['editorial']['status'] = 'NO_FLAGGED_ROWS'

def recorded_unbound(root, pins, receipt):
    receipt['editorial']['status'] = 'RECORDED_UNAUTHENTICATED'

def unsupported_claim(root, pins, receipt):
    receipt['editorial']['disposition_complete'] = True

def wrong_lines(root, pins, receipt):
    receipt['editorial']['flagged_csv_lines'] = []

def forged_authority(root, pins, receipt):
    receipt['editorial']['decision_reference_authenticated'] = True

def false_ready(root, pins, receipt):
    receipt['approved'] = True
    receipt['release'] = 'READY'

cases = [('baseline_pending', noop, 0),
         ('contradiction_no_flagged', no_flagged, 1),
         ('unsupported_recorded', recorded_unbound, 1),
         ('unsupported_claim', unsupported_claim, 1),
         ('wrong_flagged_lines', wrong_lines, 1),
         ('false_editorial_auth', forged_authority, 1),
         ('false_release', false_ready, 1)]
if __name__ == '__main__':
    results = [run_case(*case) for case in cases]
    print(json.dumps({'passed': sum(x['pass'] for x in results), 'total': len(results), 'results': results}, indent=2))
    sys.exit(0 if all(x['pass'] for x in results) else 1)
