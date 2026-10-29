#!/usr/bin/env python3
"""F-001 §149 (Claude, 2026-10-29T18Z; records only). Arithmetic behind
'The Color Dyed and Dental Records' S14 ("Metric Shock represents a 20% loss in value").
Reads no file; the two unit masses are the article's own (13.7 g Indus, 11.4 g). Writes nothing.
Usage: python3 -I CLAUDE-color-dental-checks-149.py
"""
from fractions import Fraction as F
indus, other = F('13.7'), F('11.4')
gain = indus / other - 1          # same count of units, larger unit: how much MORE mass
loss = 1 - other / indus          # same count of units, smaller unit: how much LESS mass
print('13.7/11.4 =', float(indus / other))
print('larger unit gives %.2f%% more mass per unit' % (100 * gain))
print('smaller unit gives %.2f%% less mass per unit' % (100 * loss))
print('nearest simple ratio 6/5 =', float(F(6, 5)), 'deviation %.3f%%' % (100 * (indus / other / F(6, 5) - 1)))
assert round(float(100 * gain), 2) == 20.18 and round(float(100 * loss), 2) == 16.79
print('OK: a "20% loss" is the gain figure; the loss to the party short-weighted is 16.8%')
