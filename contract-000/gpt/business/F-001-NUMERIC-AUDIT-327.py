#!/usr/bin/env python3
"""Read-only numeric audit of pinned public TAM Dataset A/B; NOT a history test."""
from decimal import Decimal as D, ROUND_HALF_UP
import json
BASE = D('13.7')
A = [
    ('Ingot Slice (Heavy)', '136.98', '10', '-0.01'),
    ('Coiled Wire (Large)', '68.52', '5', '+0.03'),
    ('Hacksilber Scraps (x3)', '13.71', '1', '+0.07'),
    ('Flattened Foil', '6.86', '0.5', '+0.14'),
    ('Silver Droplet', '3.42', '0.25', '-0.03'),
    ('Small Scrap', '1.71', '0.125', '<0.01'),
]
B = [
    ('1','0.85','0.0625','Trace/Gerah Base'),
    ('2','1.71','0.125','Matches Small Scrap'),
    ('4','3.42','0.25','Matches Silver Droplet'),
    ('8','6.85','0.5','Beqa'),
    ('16','13.70','1','Sanctuary Shekel'),
    ('32','27.40','2','Commercial Standard'),
    ('80','68.50','5','Matches Coiled Wire'),
    ('160','137.00','10','Matches Ingot Slice'),
]
P = D('0.005')
ROUND = D('0.01')
def pdev(m, f):
    return (m - BASE*f) / (BASE*f) * D(100)
def fmt(x, n='0.000000'):
    return str(x.quantize(D(n)))
res={'base_g':'13.7','source_a_blob':'b62c970a660e0a6685b58db1ef121690daa4fce7',
     'source_b_blob':'12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4',
     'method':'Decimal exact displayed values; nearest-hundredth g interval is an explicit hypothetical assumption, not source-reported measurement uncertainty',
     'A':[],'B':[],'summary':{}}
for name,m,f,printed in A:
    mass,fraction=D(m),D(f)
    dev=pdev(mass,fraction)
    low,high=pdev(mass-P,fraction),pdev(mass+P,fraction)
    if printed.startswith('<'):
        stated_match=abs(dev)<D(printed[1:])
        interval_compatible=low < D(printed[1:]) and high > -D(printed[1:])
    else:
        stated_match=dev.quantize(ROUND,rounding=ROUND_HALF_UP)==D(printed)
        # A displayed percentage at two decimals represents values in +/-0.005 percentage points.
        target=D(printed)
        interval_compatible=(low<target+D('0.005') and high>=target-D('0.005'))
    res['A'].append({'name':name,'mass_g':m,'unit_fraction':f,'expected_g':fmt(BASE*fraction),
       'computed_deviation_percent':fmt(dev), 'printed_deviation_percent':printed,
       'matches_from_displayed_mass':stated_match,
       'possible_if_mass_rounded_to_0.01g':interval_compatible,
       'percent_range_from_rounded_mass':[fmt(low),fmt(high)]})
for ratio,m,f,label in B:
    mass,fraction=D(m),D(f)
    dev=pdev(mass,fraction)
    res['B'].append({'ratio':ratio,'mass_g':m,'unit_fraction':f,'expected_g':fmt(BASE*fraction),
       'difference_g':fmt(mass-BASE*fraction),'deviation_percent':fmt(dev),
       'exact_expected_inside_rounded_mass_interval':abs(mass-BASE*fraction)<=P,
       'source_label':label})
res['summary']={'A_matches_displayed':sum(r['matches_from_displayed_mass'] for r in res['A']),
    'A_nonmatches_displayed':sum(not r['matches_from_displayed_mass'] for r in res['A']),
    'A_interval_compatible':sum(r['possible_if_mass_rounded_to_0.01g'] for r in res['A']),
    'B_exact_expected_within_rounding_interval':sum(r['exact_expected_inside_rounded_mass_interval'] for r in res['B']),
    'B_outside_rounding_interval':[r['ratio'] for r in res['B'] if not r['exact_expected_inside_rounded_mass_interval']],
    'gerah_conflict':'A Small Scrap: Gerah = 1/8 Unit; B Trace/Gerah Base: 1/16 Unit'}
assert len(A)==6 and len(B)==8
assert res['summary']['A_matches_displayed']==3
assert res['summary']['A_nonmatches_displayed']==3
assert res['summary']['A_interval_compatible']==6
assert res['summary']['B_outside_rounding_interval']==['1']
print(json.dumps(res,indent=2))
