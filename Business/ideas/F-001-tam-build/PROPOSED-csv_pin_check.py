#!/usr/bin/env python3
"""F-001 TAM build: delivered CSVs vs a pinned rebuild (PROPOSED, §101; read-only).

Usage: python3 -I -B PROPOSED-csv_pin_check.py <tam-clone> <pin-commit> <delivery-folder>

Checks that <tam-clone> is checked out at <pin-commit> with a clean tree, runs
rebuild_datasets.py (next to this file) into a temporary folder outside any
repository, and compares the sha256 of dataset-a.csv and dataset-b.csv in
<delivery-folder> with the rebuilt files, byte for byte. Exit 0 only if the pin
holds and both files match; exit 1 on any mismatch, missing file or failed
rebuild (fail closed). It prints one JSON line with the four hashes for the
release receipt (§97.3). It writes nothing outside its temporary folder and
edits nothing. It does not authenticate the pin itself: who chose <pin-commit>
is a receipt/records question, not something this script can settle.
"""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

FILES = ("dataset-a.csv", "dataset-b.csv")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv):
    if len(argv) != 4:
        print(__doc__.strip().splitlines()[2]); return 2
    clone, pin, delivery = Path(argv[1]), argv[2], Path(argv[3])
    fails, out = [], {"pin": pin, "files": {}}
    git = lambda *a: subprocess.run(["git", "-C", str(clone), *a], capture_output=True, text=True)
    head = git("rev-parse", "HEAD").stdout.strip()
    if not pin or not head.startswith(pin) or len(pin) < 7:
        fails.append(f"clone HEAD {head or '?'} is not pin {pin}")
    if git("status", "--porcelain").stdout.strip():
        fails.append("clone tree not clean")
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).with_name("rebuild_datasets.py")),
                            str(clone), tmp], capture_output=True, text=True)
        if r.returncode != 0:
            fails.append(f"rebuild failed (exit {r.returncode})")
        for f in FILES:
            rebuilt, got = Path(tmp) / f, delivery / f
            row = {"rebuilt": sha(rebuilt) if rebuilt.is_file() else None,
                   "delivered": sha(got) if got.is_file() else None}
            row["match"] = row["rebuilt"] is not None and row["rebuilt"] == row["delivered"]
            if not row["match"]:
                fails.append(f"{f}: delivered {row['delivered']} != rebuilt {row['rebuilt']}")
            out["files"][f] = row
    out["fails"] = fails
    print(json.dumps(out, sort_keys=True))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
