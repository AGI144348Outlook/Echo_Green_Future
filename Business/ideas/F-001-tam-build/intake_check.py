"""F-001 §176 (Claude 23Z): check a quotation-unit intake sheet against DECISION-UNITS-175.tsv.
Reads two TSV files only (no manuscript text). Usage:
  python3 -I intake_check.py DECISION-UNITS-175.tsv INTAKE.tsv
Checks: same header columns the intake needs; exactly the 69 units, each once, in any order; for each unit the rows, files and cue
equal the unit map (cue = 'yes' iff cued); every *_DRAFT field is blank or the row's review_state is not UNREVIEWED; review_state is
one of UNREVIEWED / IN-REVIEW / DECIDED; no unit's rows overlap another's. Prints a one-line JSON summary; exit 0 if no errors, 1 otherwise.
It classifies nothing and clears no rights."""
import sys, csv, json
STATES = {"UNREVIEWED", "IN-REVIEW", "DECIDED"}
NEED = ["unit", "rows", "files", "cue", "review_state"]
def read(p):
    with open(p, newline="", encoding="utf-8") as f: return list(csv.DictReader(f, delimiter="\t"))
def main(units_p, intake_p):
    units = {r["unit"]: r for r in read(units_p)}; intake = read(intake_p); err = []
    if not intake: err.append("intake empty")
    missing = [c for c in NEED if intake and c not in intake[0]]
    if missing: err.append("missing columns " + ",".join(missing))
    seen, rows_seen = {}, {}
    for i, r in enumerate(intake, 2):
        if missing: break
        u = r["unit"]
        if u in seen: err.append(f"line {i}: unit {u} repeated (line {seen[u]})"); continue
        seen[u] = i
        if u not in units: err.append(f"line {i}: unit {u} not in unit map"); continue
        m = units[u]
        if r["rows"] != m["rows"]: err.append(f"line {i}: {u} rows differ")
        if r["files"] != m["files"]: err.append(f"line {i}: {u} files differ")
        if r["cue"] != m["cued"]: err.append(f"line {i}: {u} cue differs")
        if r["review_state"] not in STATES: err.append(f"line {i}: {u} unknown review_state")
        drafts = [c for c in r if c and c.endswith("_DRAFT") and (r[c] or "").strip()]
        if drafts and r["review_state"] == "UNREVIEWED": err.append(f"line {i}: {u} has filled draft fields but is UNREVIEWED")
        for n in r["rows"].split(","):
            if n in rows_seen and rows_seen[n] != u: err.append(f"line {i}: row {n} in {u} and {rows_seen[n]}")
            rows_seen[n] = u
    absent = sorted(set(units) - set(seen))
    if absent and not missing: err.append(f"{len(absent)} units absent: " + ",".join(absent[:5]))
    states = {}
    for r in intake:
        if not missing: states[r["review_state"]] = states.get(r["review_state"], 0) + 1
    print(json.dumps({"units_in_map": len(units), "intake_rows": len(intake), "rows_covered": len(rows_seen), "states": states,
                      "errors": len(err), "first_errors": err[:5]}, sort_keys=True))
    return 1 if err else 0
if __name__ == "__main__": sys.exit(main(sys.argv[1], sys.argv[2]))
