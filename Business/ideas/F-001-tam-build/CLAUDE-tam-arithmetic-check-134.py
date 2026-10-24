"""F-001 §134 independent arithmetic check (Claude, 2026-10-24T17Z) of GPT run 327 (Issue #46).
Usage: python3 -I -B F-001-tam-arithmetic-check-134.py DATASET_A_FILE DATASET_B_FILE
Public The-TAM-protocol d46456a: Dataset A blob b62c970, Dataset B blob 12ef0fc. Parses the files (no hand transcription). Records only.
"""
import sys, re, json
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_DOWN
U = D('13.7'); out = {}
rowsA = []
for l in open(sys.argv[1], encoding='utf-8').read().splitlines():
    m = re.search(r'([\d.]+)g ([\d.]+) Units? .*?(<0\.01|[+-][\d.]+)\\%', l)
    if not m: continue  # header/prose lines
    mass, units, pdev = D(m.group(1)), D(m.group(2)), m.group(3)
    exp = U * units; dev = 100 * (mass - exp) / exp
    lo = 100 * (mass - D('0.005') - exp) / exp; hi = 100 * (mass + D('0.005') - exp) / exp
    if pdev == '<0.01': direct = abs(dev) < D('0.01'); inside = lo < D('0.01') and hi > D('-0.01')
    else:  # printed value is itself rounded to 0.01 %: compare bands, not points
        direct = dev.quantize(D('0.01'), ROUND_HALF_UP) == D(pdev); inside = lo <= D(pdev) + D('0.005') and hi >= D(pdev) - D('0.005')
    point = pdev != '<0.01' and lo <= D(pdev) <= hi
    rowsA.append({'mass': str(mass), 'units': str(units), 'printed': pdev, 'dev': f'{dev:.6f}',
                  'interval': [f'{lo:.4f}', f'{hi:.4f}'], 'direct': direct, 'in_interval': inside, 'point_in_interval': point})
out['A_rows'] = len(rowsA); out['A_direct'] = sum(r['direct'] for r in rowsA); out['A_in_interval'] = sum(r['in_interval'] for r in rowsA); out['A_point_in_interval_of_5_numeric'] = sum(r['point_in_interval'] for r in rowsA)
out['A'] = rowsA
rowsB = []
for l in open(sys.argv[2], encoding='utf-8').read().splitlines():
    m = re.match(r'^(\d+) ([\d.]+)g ', l)
    if not m: continue
    ratio, mass = int(m.group(1)), D(m.group(2)); exact = U * ratio / 16
    rowsB.append({'ratio': ratio, 'printed': str(mass), 'exact': str(exact),
                  'half_up': mass == exact.quantize(D('0.01'), ROUND_HALF_UP),
                  'half_even': mass == exact.quantize(D('0.01'), ROUND_HALF_EVEN),
                  'truncate': mass == exact.quantize(D('0.01'), ROUND_DOWN),
                  'within_0005_inclusive': abs(mass - exact) <= D('0.005')})
out['B_rows'] = len(rowsB)
for k in ('half_up', 'half_even', 'truncate', 'within_0005_inclusive'): out['B_' + k] = sum(r[k] for r in rowsB)
out['B_ties'] = [r['ratio'] for r in rowsB if abs(D(r['printed']) - D(r['exact'])) == D('0.005')]
out['B'] = rowsB
print(json.dumps(out, indent=1))
