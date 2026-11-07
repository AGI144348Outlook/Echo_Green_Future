"""F-001 §234 (Claude, 2026-11-07 12Z): U70 duplication reconciliation against the 69 existing
rights units (DECISION-UNITS-175.tsv) and the 77 quoted-span rows (rights_rows.py, §173).
PRE-REGISTERED: committed and pushed before its first run.

Checks, counts only (no source text printed):
 (1) overlap: which of the 77 rows (and so which units) overlap U70's char range [2075, 2346)
     in `Collective information`. PREDICTION: 0 rows, 0 units (§230: the 6-line quotation was
     missed by triage because the single-line pattern cannot span newlines).
 (2) exact duplicate: occurrences of U70's byte slice in every corpus file (FILES).
     PREDICTION: none stated (Collective information repeats Article text; reported, not predicted).
 (3) normalized duplicate: same after removing U+200B and collapsing whitespace. Reported.
 (4) control: row 24 (Collective information, line 55) must overlap itself -> 1 row.
Run: python3 -I -B CLAUDE-u70-dup-234.py <tam-checkout @ d46456a1>"""
import hashlib, json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from rights_scan import FILES, PAT

root = sys.argv[1]
SPAN = re.compile(PAT["quoted_spans_40plus"])
NAME = "Collective information"
U70 = (2075, 2346)                       # char range, §232
SB, EB = 2123, 2394                      # byte range, §230/§231


def spans():
    n = 0
    for f in FILES:
        p = os.path.join(root, f)
        if not os.path.isfile(p):
            continue
        t = open(p, "rb").read().decode("utf-8", "replace")
        for m in SPAN.finditer(t):
            n += 1
            yield n, f, m.start(), m.end()


units = {}
for line in open(os.path.join(here, "DECISION-UNITS-175.tsv"), encoding="utf-8").read().splitlines()[1:]:
    c = line.split("\t")
    for r in c[1].split(","):
        units.setdefault(int(r), []).append(c[0])

all_rows = list(spans())
ov = [r for r in all_rows if r[1] == NAME and r[2] < U70[1] and U70[0] < r[3]]
ctl = [r for r in all_rows if r[0] == 24]
ctl_ov = [r for r in all_rows if r[1] == ctl[0][1] and r[2] < ctl[0][3] and ctl[0][2] < r[3]]

raw = open(os.path.join(root, NAME), "rb").read()
sl = raw[SB:EB]
assert hashlib.sha256(sl).hexdigest().startswith("f16fe6eb")


def norm(b):
    s = b.decode("utf-8", "replace").replace("​", "")
    return re.sub(r"\s+", " ", s).strip()


nsl = norm(sl)
exact, normd = {}, {}
for f in FILES:
    p = os.path.join(root, f)
    if not os.path.isfile(p):
        continue
    b = open(p, "rb").read()
    exact[f] = b.count(sl)
    normd[f] = norm(b).count(nsl)

out = {
    "source_ref_file": NAME, "u70_chars": list(U70), "u70_bytes": [SB, EB],
    "rows_scanned": len(all_rows), "units_in_table": len({u for v in units.values() for u in v}),
    "overlap_rows": [r[0] for r in ov],
    "overlap_units": sorted({u for r in ov for u in units.get(r[0], [])}),
    "exact_occurrences": {k: v for k, v in exact.items() if v},
    "normalized_occurrences": {k: v for k, v in normd.items() if v},
    "control_row24_overlap_rows": [r[0] for r in ctl_ov],
    "prediction_overlap_0": len(ov) == 0,
    "control_ok": [r[0] for r in ctl_ov] == [24],
}
sys.stdout.write(json.dumps(out, sort_keys=True, indent=1) + "\n")
