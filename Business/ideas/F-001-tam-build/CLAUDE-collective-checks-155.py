#!/usr/bin/env python3
"""F-001 §155 (Claude, 2026-10-30T00Z; records only, not pre-registered).
Arithmetic behind the §155 proposed states for Collective C69, C97, C109. Uses only textbook constants
written below; no outside data is fetched. Read-only; writes nothing. Usage: python3 -I CLAUDE-collective-checks-155.py
"""
import json
out = {}
# C69: "1/15th of a degree" in arcminutes; and the precession rate the C68 "drift" refers to.
out["C69_one_fifteenth_degree_arcmin"] = round(60 / 15, 3)
PREC_ARCSEC_PER_YR = 50.3              # general precession, textbook value
out["C68_years_per_degree_of_precession"] = round(3600 / PREC_ARCSEC_PER_YR, 1)
# C97: sightlines. Polaris altitude ~= observer latitude (Polaris dec ~ +89.3 deg).
# A star of declination d is ever above the horizon at latitude L if  L > d - 90 (north) ...
# rises at all if  L < 90 + d  (for southern stars, d < 0).
def rises(lat, dec): return lat < 90 + dec if dec < 0 else lat > dec - 90
HIGH_ISLAND_LAT, EASTER_LAT = 29.57, -27.12      # approx. degrees
POLARIS_DEC, ACRUX_DEC = 89.3, -63.1            # approx. degrees (J2000 order of magnitude)
out["C97_polaris_altitude_at_high_island_deg_approx"] = round(HIGH_ISLAND_LAT - (90 - POLARIS_DEC), 2)
out["C97_polaris_ever_visible_at_easter_island"] = rises(EASTER_LAT, POLARIS_DEC) and EASTER_LAT > -(90 - POLARIS_DEC)
out["C97_acrux_rises_at_high_island"] = rises(HIGH_ISLAND_LAT, ACRUX_DEC)
out["C97_acrux_rises_only_south_of_lat_deg"] = round(90 + ACRUX_DEC, 1)
# Any coastal point at roughly the same latitude sees the same stars; the altitude a star reaches depends
# on latitude, not on which point along the coast. Local elevation only lowers the horizon by
# dip ~ 1.76' * sqrt(h_m) (standard nautical approximation).
out["C97_horizon_dip_arcmin_at_h_m"] = {h: round(1.76 * h ** 0.5, 2) for h in (5, 10, 20, 50)}
# C109: weight change of 13.7 g lifted h metres (free-air gradient 3.086e-6 s^-2); mass does not change.
G0, GRAD = 9.80665, 3.086e-6
out["C109_relative_weight_change_per_m"] = GRAD / G0
out["C109_apparent_mass_change_ug_for_13p7g"] = {h: round(13.7e6 * GRAD * h / G0, 2) for h in (5, 10, 20, 50)}
print(json.dumps(out, indent=1))
