#!/usr/bin/env python3
"""F-001 §163 (Claude): run ChatGPT's Run464 executable-pin wrapper unchanged on real Git bytes.

Usage: python3 -I -B gpt464_receipt_replay.py <dir>
<dir> holds unchanged copies, taken from contract-000-gpt-run464-20261030-0403 @ 1d254e5d, of:
  f001_custody_receipt_464.py, f001_approval_custody_463.py,
  F-001-EDITORIAL-DECISIONS-458.tsv, F-001-SOURCE-LOCATION-RESULTS-462.tsv,
  F-001-DECISION-INTAKE-PENDING-463.tsv
Negatives are written to <dir>/neg. Nothing is written elsewhere; no network.
Prints one JSON result object. HOLD only: nothing here approves or publishes.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

d = Path(sys.argv[1])
W, G = 'f001_custody_receipt_464.py', 'f001_approval_custody_463.py'
R, L, I = ('F-001-EDITORIAL-DECISIONS-458.tsv', 'F-001-SOURCE-LOCATION-RESULTS-462.tsv',
           'F-001-DECISION-INTAKE-PENDING-463.tsv')


def blob(b):
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def run(*args):
    p = subprocess.run([sys.executable, '-I', '-B', W, *args], cwd=d, capture_output=True)
    return p.returncode, p.stdout, p.stderr.decode().strip()


out = {'inputs': {n: blob((d / n).read_bytes()) for n in (W, G, R, L, I)}}
c1, s1, _ = run(G, R, L, I)
c2, s2, _ = run(G, R, L, I)
out['positive'] = {'exit': [c1, c2], 'byte_identical': s1 == s2,
                   'receipt_sha256': hashlib.sha256(s1).hexdigest(),
                   'receipt': json.loads(s1) if c1 == 0 else None}

neg = d / 'neg'
neg.mkdir(exist_ok=True)
g = (d / G).read_text()
(neg / 'gate_a.py').write_text(g + '# comment\n')               # (a) changed gate, same behaviour
lines = g.split('\n')
k = next(i for i, x in enumerate(lines) if x.strip() == '' and i > 3)
(neg / 'gate_b.py').write_text('\n'.join(lines[:k] + lines[k + 1:]))  # (b) one blank line removed
t = (d / I).read_text().split('\n')
c = t[1].split('\t'); c[5] = 'APPROVED'; c[7] = 'Timothy'; t[1] = '\t'.join(c)
(neg / 'intake_c.tsv').write_text('\n'.join(t))                 # (c) forged approval
b = bytearray((d / R).read_bytes()); j = b.index(b'the'); b[j] = ord('T')
(neg / 'reg_d.tsv').write_bytes(bytes(b))                       # (d) one register byte changed
cases = {'a_gate_comment_added': ('neg/gate_a.py', R, L, I),
         'b_gate_blank_line_removed': ('neg/gate_b.py', R, L, I),
         'c_intake_forged_approved': (G, R, L, 'neg/intake_c.tsv'),
         'd_register_byte_changed': (G, 'neg/reg_d.tsv', L, I),
         'e_missing_path': (G, R, L, 'neg/missing.tsv')}
out['negatives'] = {}
for name, args in cases.items():
    code, so, se = run(*args)
    out['negatives'][name] = {'exit': code, 'stdout_bytes': len(so), 'stderr': se.replace(str(d), '<dir>')}
# control: gate_b alone (not through the wrapper) gives the same gate receipt as the pinned gate
a = subprocess.run([sys.executable, '-I', '-B', G, R, L, I], cwd=d, capture_output=True).stdout
bb = subprocess.run([sys.executable, '-I', '-B', 'neg/gate_b.py', R, L, I], cwd=d, capture_output=True).stdout
out['control_gate_b_same_behaviour_direct'] = a == bb and bool(a)
out['python'] = sys.version.split()[0]
print(json.dumps(out, indent=1, sort_keys=True))
