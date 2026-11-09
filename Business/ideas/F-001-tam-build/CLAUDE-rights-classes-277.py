# F-001 §277 (Claude 08Z): class-level rights decision card derived from RIGHTS-STATUS-276.tsv.
# Reads only the ledger (never TAM text). A class = one source file. A unit is covered by a
# class decision only if EVERY file it draws on has a cleared class (conjunctive, fail-closed).
# Prints a TSV card and synthetic fixtures. Fixtures imply no real decision by anyone.
import sys, json, collections
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8")
        if l.strip() and not l.startswith("#")]
hdr, units = rows[0], rows[1:]
U = [dict(zip(hdr, r)) for r in units]
cls = collections.OrderedDict()
for u in U:
    for f in u["files"].split("|"):
        c = cls.setdefault(f, {"units": 0, "rows": 0, "sole": 0, "shared": 0})
        c["units"] += 1; c["rows"] += int(u["n_rows"])
        c["sole" if "|" not in u["files"] else "shared"] += 1
print("class\tunits\trows\tsole_units\tshared_units\tclass_status")
for f, c in sorted(cls.items(), key=lambda kv: (-kv[1]["units"], kv[0])):
    print(f"{f}\t{c['units']}\t{c['rows']}\t{c['sole']}\t{c['shared']}\tUNDECIDED")
def verdict(cleared, rejected=()):
    out = collections.Counter()
    for u in U:
        fs = u["files"].split("|")
        if any(f in rejected for f in fs): out["RIGHTS_REJECTED"] += 1
        elif all(f in cleared for f in fs): out["CLASS_CLEARED_PENDING_RECORD"] += 1
        else: out["RIGHTS_UNVERIFIED"] += 1
    return dict(sorted(out.items()))
fx = {
  "C0_no_class_decided": verdict(set()),
  "C1_only_Collective_information": verdict({"Collective information"}),
  "C2_all_classes": verdict(set(cls)),
  "C3_all_but_Article_6": verdict(set(cls) - {"Article 6"}),
  "C4_Article_10_rejected_rest_cleared": verdict(set(cls) - {"Article 10"}, {"Article 10"}),
}
print("# decisions per-unit", len(U), "| per-class", len(cls))
print("# fixtures", json.dumps(fx, sort_keys=True))
