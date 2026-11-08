"""F-001 section 251 (Claude 2026-11-08T05Z): synthetic 0/1/N cardinality check of
the PROPOSED v3.1 migration, renamed per ChatGPT 04Z (b11afdc5): the legacy scalar
stays in `editorial_evidence_ref` (type unchanged) and the list is a NEW field
`editorial_evidence_refs`. Synthetic fixtures only; reads no file; writes nothing.
Non-promoting: no decision field is created or changed.
Run: python3 -I -B this.py"""
import json, hashlib
M = "MISSING"
class Reject(Exception): pass
def migrate(r, join=None):
    legacy = r.get("editorial_evidence_ref")
    if legacy is not None and not (isinstance(legacy, str) and legacy.strip()):
        raise Reject("legacy editorial_evidence_ref not null and not a non-empty string")
    refs = [] if legacy is None else [legacy]
    state = "NOT_JOINED"
    if join is not None:
        state = "JOINED"
        refs = refs + list(join)          # keep order; never collapse duplicates
    dups = sorted({x for x in refs if refs.count(x) > 1})
    o = dict(r)                           # every v1 field kept verbatim
    o.update({"editorial_evidence_refs": refs, "editorial_join_state": state,
              "editorial_duplicate_refs": dups, "rights_reviewer": r.get("rights_reviewer", M)})
    return o
def back(o):
    return {k: v for k, v in o.items() if k not in
            ("editorial_evidence_refs", "editorial_join_state", "editorial_duplicate_refs", "rights_reviewer")}
F = [  # (name, v1 row, join or None, expected)
 ("C0_null_notjoined", {"unit_id": "S0", "editorial_evidence_ref": None, "editorial_status": "HOLD"}, None, (0, "NOT_JOINED")),
 ("C0_null_joined_empty", {"unit_id": "S0", "editorial_evidence_ref": None, "editorial_status": "HOLD"}, [], (0, "JOINED")),
 ("C1_scalar", {"unit_id": "S1", "editorial_evidence_ref": "Art6#S19", "editorial_status": "HOLD"}, None, (1, "NOT_JOINED")),
 ("CN_scalar_plus_join", {"unit_id": "S2", "editorial_evidence_ref": "Art10#S4", "editorial_status": "HOLD"}, ["Art10#S5"], (2, "JOINED")),
 ("CN_null_two_overlaps", {"unit_id": "S3", "editorial_evidence_ref": None, "editorial_status": "HOLD"}, ["CI#S294", "CI#S295"], (2, "JOINED")),
 ("CD_duplicate_kept", {"unit_id": "S4", "editorial_evidence_ref": "X#1", "editorial_status": "HOLD"}, ["X#1"], (2, "JOINED")),
 ("R1_nonstring", {"unit_id": "S5", "editorial_evidence_ref": 7, "editorial_status": "HOLD"}, None, "REJECT"),
 ("R2_empty_string", {"unit_id": "S6", "editorial_evidence_ref": "  ", "editorial_status": "HOLD"}, None, "REJECT"),
]
ok = 0; out = []
for name, r, j, exp in F:
    try:
        o = migrate(r, j)
        got = (len(o["editorial_evidence_refs"]), o["editorial_join_state"])
        good = got == exp and back(o) == r and o["editorial_status"] == r["editorial_status"]
        line = f"{name} n={got[0]} state={got[1]} dups={o['editorial_duplicate_refs']} roundtrip={back(o)==r} pass={good}"
    except Reject as e:
        good = exp == "REJECT"; line = f"{name} REJECT ({e}) pass={good}"
    ok += good; out.append(line)
a = migrate(F[0][1]); b = migrate(F[1][1], [])
out.append(f"fixtures={len(F)} pass={ok} joined_empty_distinct={a != b}")
print("\n".join(out))
