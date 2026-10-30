#!/usr/bin/env python3
"""F-001 §162 (Claude): replay ChatGPT Run463 custody preflight UNCHANGED on the real Git bytes.
Usage: python3 -I -B gpt463_custody_replay.py SRC_DIR WORK_DIR
SRC_DIR holds the five files exported with `git show 387e1849:contract-000/gpt/business/<name>`.
Builds six negative intakes/registers in WORK_DIR, runs the CLI, prints one JSON receipt. Edits nothing in SRC_DIR."""
import hashlib, json, subprocess, sys
from pathlib import Path

SRC, WORK = Path(sys.argv[1]), Path(sys.argv[2])
WORK.mkdir(parents=True, exist_ok=True)
CLI = "f001_approval_custody_463.py"
R, M, I = "F-001-EDITORIAL-DECISIONS-458.tsv", "F-001-SOURCE-LOCATION-RESULTS-462.tsv", "F-001-DECISION-INTAKE-PENDING-463.tsv"
PINS = {CLI: "5a767d9", "test_f001_approval_custody_463.py": "f6e92a1", R: "300dfcf", M: "7fb5cd9", I: "4cc1617"}

def blob(p):
    d = p.read_bytes(); return hashlib.sha1(b"blob %d\0" % len(d) + d).hexdigest()

def run(reg, intake):
    p = subprocess.run([sys.executable, "-I", "-B", str(SRC / CLI), str(reg), str(SRC / M), str(intake)], capture_output=True, text=True)
    return p.returncode, p.stdout.strip()

pins = {k: blob(SRC / k) for k in PINS}
assert all(pins[k].startswith(v) for k, v in PINS.items()), pins
lines = (SRC / I).read_bytes().decode().split("\n")
def edit(i, col, val, L=None):
    L = list(L or lines); c = L[i].split("\t"); c[col] = val; L[i] = "\t".join(c); return L
neg = {"N-a approved+approved_by": edit(1, 7, "Timothy", edit(1, 5, "APPROVED")),
       "N-b release_authorized=true": edit(1, 9, "true"),
       "N-c replacement_text filled": edit(1, 6, "replacement")}
L = list(lines); L[1], L[2] = L[2], L[1]; neg["N-e rows 1/2 swapped"] = L
L = list(lines); del L[-2]; neg["N-f last row dropped"] = L
out = {"section": "F-001 §162", "gpt_commit": "387e1849748e49a459b4418439ef4d002635cc13", "input_blobs": pins,
       "python": sys.version.split()[0], "positive": None, "negatives": {}}
code, so = run(SRC / R, SRC / I); out["positive"] = {"exit": code, "receipt": json.loads(so) if code == 0 else so}
for name, L in neg.items():
    f = WORK / (name.split()[0] + ".tsv"); f.write_text("\n".join(L)); out["negatives"][name] = dict(zip(("exit", "message"), run(SRC / R, f)))
reg = bytearray((SRC / R).read_bytes()); reg[200] = 65 if reg[200] != 65 else 66
f = WORK / "N-d-register.tsv"; f.write_bytes(bytes(reg)); out["negatives"]["N-d register byte 200 changed"] = dict(zip(("exit", "message"), run(f, SRC / I)))
out["all_negatives_refused"] = all(v["exit"] == 2 for v in out["negatives"].values())
print(json.dumps(out, indent=1, sort_keys=True))
