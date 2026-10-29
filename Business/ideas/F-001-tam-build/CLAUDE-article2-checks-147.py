#!/usr/bin/env python3
"""F-001 §147 (Claude, 2026-10-29T16Z; records only, not pre-registered).
Arithmetic and physics checks for TAM `Article 2 Water Weight Computes` (blob ec657c3, d46456a).
Uses only textbook constants written below. Read-only; reads no file; writes nothing.
Usage: python3 -I CLAUDE-article2-checks-147.py
"""
import math
SYN=29.530589      # mean synodic month, days (standard value)
TROP=365.24219     # mean tropical year, days (standard value)
print("S24  12 synodic months = %.2f d; tropical year %.2f d; gap %.2f d/yr" % (12*SYN, TROP, TROP-12*SYN))
gap=TROP-12*SYN
print("S26-28 cumulative slip y1..3 = %s d" % ", ".join("%.1f" % (gap*k) for k in (1,2,3)))
print("S33  19 tropical yr = %.2f d; 235 months = %.2f d; diff %.2f h per cycle; extra months 235-228 = %d"
      % (19*TROP, 235*SYN, (235*SYN-19*TROP)*24, 235-19*12))
# Hebrew-calendar leap years in the 19-year cycle (standard list) vs S41's "3rd year"
LEAP=[3,6,8,11,14,17,19]; print("S41  year 3 in standard leap list:", 3 in LEAP, LEAP)
# S9/S18: a pot that drains through a hole in its base (Torricelli): outflow rate ~ sqrt(head).
# Cylinder holding N equal 13.7 g units: time for unit k (from the top) as a share of the total.
N=10
t=lambda h: math.sqrt(h)          # time to drain from head h to 0, up to a constant
times=[t((N-k)/N)-t((N-k-1)/N) for k in range(N)]
tot=sum(times)
print("S9/S18 cylinder, %d equal units: first unit %.1f%% of drain time, last unit %.1f%%; ratio last/first %.1f"
      % (N, 100*times[0]/tot, 100*times[-1]/tot, times[-1]/times[0]))
print("S18  equal 13.7 g per equal interval needs a constant head (inflow clock / overflow tank) or a shaped vessel")
