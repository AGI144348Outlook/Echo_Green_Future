#!/usr/bin/env python3
"""F-001 §164 (Claude): run ChatGPT's Run465 snapshot wrapper unchanged on real Git bytes.

Usage: python3 -I -B gpt465_snapshot_replay.py <dir>
<dir> holds unchanged copies, taken from contract-000-gpt-run465-20261030-0500 @ f011356f, of:
  f001_custody_snapshot_465.py, f001_approval_custody_463.py,
  F-001-EDITORIAL-DECISIONS-458.tsv, F-001-SOURCE-LOCATION-RESULTS-462.tsv,
  F-001-DECISION-INTAKE-PENDING-463.tsv
Negatives and control copies are written to <dir>/neg. No network.
Prints one JSON result object. HOLD only: nothing here approves or publishes.
"""
import glob
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

d = Path(sys.argv[1]).resolve()
W, G = 'f001_custody_snapshot_465.py', 'f001_approval_custody_463.py'
R, L, I = ('F-001-EDITORIAL-DECISIONS-458.tsv', 'F-001-SOURCE-LOCATION-RESULTS-462.tsv',
           'F-001-DECISION-INTAKE-PENDING-463.tsv')


def blob(b):
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def run(*args):
    p = subprocess.run([sys.executable, '-I', '-B', W, *args], cwd=d, capture_output=True)
    return p.returncode, p.stdout, p.stderr.decode().strip()


def leftovers():
    return sorted(glob.glob(str(Path(tempfile.gettempdir()) / 'f001-verified-snapshot-*')))


out = {'inputs': {n: blob((d / n).read_bytes()) for n in (W, G, R, L, I)},
       'snapshot_dirs_before': len(leftovers())}

# 1. positives
c1, s1, _ = run(G, R, L, I)
c2, s2, _ = run(G, R, L, I)
out['positive'] = {'exit': [c1, c2], 'byte_identical': s1 == s2,
                   'receipt_sha256': hashlib.sha256(s1).hexdigest(),
                   'receipt': json.loads(s1) if c1 == 0 else None}

# 2. pre-read negatives
neg = d / 'neg'
neg.mkdir(exist_ok=True)
(neg / 'gate_a.py').write_bytes((d / G).read_bytes() + b'# comment\n')
b = bytearray((d / R).read_bytes()); j = b.index(b'the'); b[j] = ord('T')
(neg / 'reg_b.tsv').write_bytes(bytes(b))
t = (d / I).read_text().split('\n')
c = t[1].split('\t'); c[5] = 'APPROVED'; c[7] = 'Timothy'; t[1] = '\t'.join(c)
(neg / 'intake_c.tsv').write_text('\n'.join(t))
cases = {'a_gate_comment_added': ('neg/gate_a.py', R, L, I),
         'b_register_byte_changed': (G, 'neg/reg_b.tsv', L, I),
         'c_intake_forged_approved': (G, R, L, 'neg/intake_c.tsv'),
         'd_missing_path': (G, R, L, 'neg/missing.tsv')}
out['negatives'] = {}
for name, args in cases.items():
    code, so, se = run(*args)
    out['negatives'][name] = {'exit': code, 'stdout_bytes': len(so),
                              'stderr': se.replace(str(d), '<dir>')}

# 3. changed-original-path controls (in-process, wrapper module unchanged)
work = neg / 'swap'
if work.exists():
    shutil.rmtree(work)
work.mkdir()
for n in (G, R, L, I):
    shutil.copyfile(d / n, work / n)
spec = importlib.util.spec_from_file_location('w465', d / W)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
real_run = subprocess.run
forged = {R: (neg / 'reg_b.tsv').read_bytes(), I: (neg / 'intake_c.tsv').read_bytes(),
          L: (d / L).read_bytes() + b'X\tforged\n'}


def swap_then_run(cmd, **kw):
    for n, data in forged.items():
        (work / n).write_bytes(data)
    return real_run(cmd, **kw)


w.subprocess.run = swap_then_run
try:
    r = w.attest(work / G, work / R, work / L, work / I)
    swap = {'result': 'receipt', 'equals_positive': json.dumps(r, sort_keys=True, separators=(',', ':'),
                                                                ensure_ascii=False).encode() + b'\n' == s1}
except Exception as e:  # noqa: BLE001 - record any refusal as data
    swap = {'result': 'refused', 'error': str(e)}
swap['originals_were_changed'] = all((work / n).read_bytes() == v for n, v in forged.items())
out['control_swap_after_verify'] = swap
w.subprocess.run = real_run

# detection control: the gate run directly on the forged originals must refuse,
# otherwise control 3 could not have detected a reread of the original paths
p = real_run([sys.executable, '-I', '-B', str(work / G), str(work / R), str(work / L), str(work / I)],
             capture_output=True)
out['control_gate_direct_on_forged_originals'] = {'exit': p.returncode, 'stdout_bytes': len(p.stdout)}
out['snapshot_dirs_after'] = len(leftovers())
out['python'] = sys.version.split()[0]
print(json.dumps(out, indent=1, sort_keys=True))
