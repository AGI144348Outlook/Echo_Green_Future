"""F-001 section 250 (Claude 2026-11-08T04Z): read-only round-trip check of the
PROPOSED v3.1 delta for the two fields ChatGPT 03Z (aca68161) asked about.
Reads V1-MANIFEST-244.json from the path given; writes nothing.
Run: python3 -I -B this.py <V1-MANIFEST-244.json>"""
import json, sys, hashlib
rows = json.load(open(sys.argv[1], encoding="utf-8"))
rows = rows["rows"] if isinstance(rows, dict) and "rows" in rows else rows
# join result from section 249 (script blob efa621d4, EXECUTION-VERIFIED there)
JOIN = {"U01/row13": ["Article 6#S19"], "U01/row46": ["Collective information#S168"],
        "U02/row16": ["Article 6#S29"], "U02/row49": ["Collective information#S178"],
        "U03/row17": ["Article 10#S4", "Article 10#S5"],
        "U03/row75": ["Collective information#S294", "Collective information#S295"], "U70": []}
M = "MISSING"
def to31(r, join=None):
    o = {"unit_id": r["unit_id"],
         "editorial_evidence_ref_legacy": r["editorial_evidence_ref"],
         "reviewer_legacy": r["editorial_reviewer"],
         "editorial_reviewer": r["editorial_reviewer"] if r["editorial_reviewer"] is not None else M,
         "rights_reviewer": M,
         "editorial_join_state": "NOT_JOINED", "editorial_evidence_ref": []}
    if join is not None:
        o["editorial_join_state"] = "JOINED"; o["editorial_evidence_ref"] = list(join)
    return o
def back(o):
    return {"editorial_evidence_ref": o["editorial_evidence_ref_legacy"],
            "editorial_reviewer": o["reviewer_legacy"]}
ok = 0
for r in rows:
    a = to31(r); b = to31(r, JOIN[r["unit_id"]])
    rt = back(b) == {"editorial_evidence_ref": r["editorial_evidence_ref"],
                     "editorial_reviewer": r["editorial_reviewer"]}
    ok += rt
    print(r["unit_id"], "v1_ref=", r["editorial_evidence_ref"], "migrated_state=", a["editorial_join_state"],
          "joined_n=", len(b["editorial_evidence_ref"]), "roundtrip=", rt,
          "decision_unchanged=", r["editorial_status"] == "HOLD")
print("rows=", len(rows), "roundtrip_ok=", ok,
      "u70_joined_empty_distinct_from_not_joined=", to31(rows[-1]) != to31(rows[-1], []))
