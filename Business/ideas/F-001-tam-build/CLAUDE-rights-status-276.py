"""F-001 rights-status ledger (Claude 07Z, §276). Reads DECISION-UNITS-175.tsv (69 units) and U70-GATE-ROW-232.tsv
presence (U70 candidate), prints one rights row per unit with status UNREVIEWED (no unit has a recorded human rights
decision yet), then a fail-closed release-scope verdict. Never reads or prints TAM text. Statuses allowed:
UNREVIEWED | OWN_PHRASING | THIRD_PARTY_PERMITTED | THIRD_PARTY_REMOVE | REJECTED; only a Timothy-recorded decision
may change a row (none exists). Verdict rule (PROPOSED): RIGHTS_OK only if every unit in scope is OWN_PHRASING or
THIRD_PARTY_PERMITTED with a reviewer; any REJECTED -> RIGHTS_REJECTED; otherwise RIGHTS_UNVERIFIED.
Usage: python3 -I CLAUDE-rights-status-276.py <dir containing DECISION-UNITS-175.tsv>"""
import sys, os, json, csv
d = sys.argv[1]
units = []
with open(os.path.join(d, "DECISION-UNITS-175.tsv"), newline="") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        units.append({"unit": r["unit"], "files": r["files"], "n_rows": int(r["n_rows"]),
                      "rights_status": "UNREVIEWED", "reviewer": "-", "basis": "-", "candidate": False})
if os.path.isfile(os.path.join(d, "U70-GATE-ROW-232.tsv")):
    units.append({"unit": "U70", "files": "Collective information", "n_rows": 1,
                  "rights_status": "UNREVIEWED", "reviewer": "-", "basis": "-", "candidate": True})
def verdict(rows):
    if any(r["rights_status"] == "REJECTED" for r in rows): return "RIGHTS_REJECTED"
    ok = all(r["rights_status"] in ("OWN_PHRASING", "THIRD_PARTY_PERMITTED") and r["reviewer"] != "-" for r in rows)
    return "RIGHTS_OK" if rows and ok else "RIGHTS_UNVERIFIED"
print("unit\tfiles\tn_rows\tcandidate\trights_status\treviewer\tbasis")
for r in units:
    print(f'{r["unit"]}\t{r["files"]}\t{r["n_rows"]}\t{"yes" if r["candidate"] else "no"}\t{r["rights_status"]}\t{r["reviewer"]}\t{r["basis"]}')
# fixtures: the rule must fail closed on these synthetic edits (no real decision is implied)
fx = {}
fx["R0_current_ledger"] = verdict(units)
fx["R1_empty_scope"] = verdict([])
fx["R2_all_own_no_reviewer"] = verdict([dict(r, rights_status="OWN_PHRASING") for r in units])
fx["R3_all_own_with_reviewer_synthetic"] = verdict([dict(r, rights_status="OWN_PHRASING", reviewer="SYNTHETIC") for r in units])
fx["R4_one_rejected"] = verdict([dict(r, rights_status="OWN_PHRASING", reviewer="SYNTHETIC") for r in units[:-1]] + [dict(units[-1], rights_status="REJECTED")])
fx["R5_caller_string_cleared"] = verdict([dict(r, rights_status="cleared", reviewer="SYNTHETIC") for r in units])
print("# counts " + json.dumps({"units": len(units), "candidates": sum(r["candidate"] for r in units),
      "UNREVIEWED": sum(r["rights_status"] == "UNREVIEWED" for r in units)}, sort_keys=True))
print("# fixtures " + json.dumps(fx, sort_keys=True))
