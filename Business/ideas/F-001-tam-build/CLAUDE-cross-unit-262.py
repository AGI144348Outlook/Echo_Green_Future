#!/usr/bin/env python3
"""F-001 §262 (Claude 17Z): cross-unit occurrence check + rights-basis check.

Closes, as a separate whole-table pass, two gaps listed in §261:
  gap 5: one occurrence_id joined to two different units (per-row
         validators keyed on (unit, occurrence_id) cannot see this);
  gap 4: rights=APPROVED has no basis field (PROPOSED field name
         `rights_basis`, a placeholder for ChatGPT's schema / Timothy).
Expected codes for every fixture are written below BEFORE the first run.
Synthetic fixtures only; no TAM text, no approval meaning.
"""
import json

def table_check(rows):
    errs, seen = [], {}
    if not isinstance(rows, list):
        return [("*", "BAD_TABLE_TYPE")]
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            errs.append((i, "BAD_ROW_TYPE")); continue
        unit, refs = r.get("unit"), r.get("refs")
        if not isinstance(unit, str) or not unit:
            errs.append((i, "BAD_UNIT_TYPE")); continue
        if not isinstance(refs, list):
            errs.append((i, "BAD_REFS_TYPE")); continue
        if r.get("rights") == "APPROVED":
            b = r.get("rights_basis")
            if not isinstance(b, str) or not b.strip():
                errs.append((i, "RIGHTS_BASIS_MISSING"))
        for ref in refs:
            occ = ref.get("occurrence_id") if isinstance(ref, dict) else None
            if not isinstance(occ, str):
                errs.append((i, "BAD_OCCURRENCE_TYPE")); continue
            prev = seen.setdefault(occ, unit)
            if prev != unit:
                errs.append((i, "OCCURRENCE_IN_TWO_UNITS"))
    return errs

def R(unit, occs, **kw):
    d = {"unit": unit, "refs": [{"occurrence_id": o} for o in occs]}
    d.update(kw); return d

CASES = [  # (name, table, expected sorted codes)
    ("X1 clean two units", [R("U01", ["o1"]), R("U02", ["o2"])], []),
    ("X2 same occ two units", [R("U01", ["o1"]), R("U02", ["o1"])], ["OCCURRENCE_IN_TWO_UNITS"]),
    ("X3 same occ same unit twice", [R("U01", ["o1"]), R("U01", ["o1"])], []),
    ("X4 refs None", [{"unit": "U01", "refs": None}], ["BAD_REFS_TYPE"]),
    ("X5 unit list", [{"unit": ["U01"], "refs": []}], ["BAD_UNIT_TYPE"]),
    ("X6 rights APPROVED no basis", [R("U01", ["o1"], rights="APPROVED")], ["RIGHTS_BASIS_MISSING"]),
    ("X7 rights APPROVED with basis", [R("U01", ["o1"], rights="APPROVED", rights_basis="placeholder")], []),
    ("X8 rights HOLD no basis", [R("U70", ["o9"], rights="HOLD")], []),
    ("X9 integer occurrence", [R("U01", [7])], ["BAD_OCCURRENCE_TYPE"]),
    ("X10 table not list", {"U01": []}, ["BAD_TABLE_TYPE"]),
]

out = []
for name, t, exp in CASES:
    got = sorted(c for _, c in table_check(t))
    out.append({"case": name, "expected": exp, "got": got, "match": got == exp})
print(json.dumps({"cases": out, "matched": sum(o["match"] for o in out),
                  "total": len(out)}, indent=1, sort_keys=True))
