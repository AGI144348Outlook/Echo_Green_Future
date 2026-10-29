#!/usr/bin/env python3
"""Run431 F-001 P1-F13 mass-ratio arithmetic; pre-registered Issue #104."""
from decimal import Decimal,localcontext
with localcontext() as c:
    c.prec=30
    a,b=Decimal('13.7'),Decimal('11.4')
    d=a-b; x=d/b*100; y=d/a*100
    tests=[
      ('difference 2.3g',d==Decimal('2.3')),
      ('11.4 denominator between 20 and 21%',20<x<21),
      ('13.7 denominator between 16 and 17%',16<y<17),
      ('11.4 denominator rounds to 20.18%',x.quantize(Decimal('.01'))==Decimal('20.18')),
      ('13.7 denominator rounds to 16.79%',y.quantize(Decimal('.01'))==Decimal('16.79')),
      ('ratios differ',x!=y),
      ('neither is exactly 20%',x!=20 and y!=20)]
    for name,ok in tests:
        assert ok,name
        print('PASS',name)
    print('RATIO_11_4',x,'RATIO_13_7',y,'TOTAL',len(tests),'PASS')
    print('INTERPRETATION: these mass ratios do not establish transaction value loss.')
