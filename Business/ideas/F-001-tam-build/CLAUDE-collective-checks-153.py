#!/usr/bin/env python3
"""F-001 §153 (Claude, 2026-10-29T22Z): arithmetic checks for the first `Collective information` batch.
Longitudes are the ones printed in the C35 table (TAM d46456a); no outside data. Read-only; writes nothing."""
from itertools import combinations
L={'Indus':68.1,'Eshtemoa':35.0,'Persepolis':52.8,'Cabo Verde':-23.6}
def sep(a,b):
    d=abs(L[a]-L[b])%360; return min(d,360-d)
pairs={(a,b):round(sep(a,b),1) for a,b in combinations(L,2)}
for k,v in pairs.items(): print('lon separation',k,v)
print('any pair at 72 or 108 deg (+/-1):',[k for k,v in pairs.items() if min(abs(v-72),abs(v-108))<=1])
print('any pair at 49.3 deg (+/-1):',[k for k,v in pairs.items() if abs(v-49.3)<=1])
print('C90 13.7% of 360 =',round(0.137*360,3))
print('C128 13.7 t / 13.7 g =',13.7e6/13.7, '(true for any n: n t / n g = 1e6)')
print('C27/C57 13.73 km vs 13.7 g: different dimensions; km figure changes with unit (13.73 km = %.2f mi = %.2f nmi)'%(13.73/1.609344,13.73/1.852))
