# GPT-owned Run 332 draft extending Claude §101 pin checker; NOT RELEASE APPROVED.
# Prospective test issue #50; pins are source records, not authorization by themselves.
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
PIN_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
SOURCE_BLOBS = {
    "Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)": "b62c970a660e0a6685b58db1ef121690daa4fce7",
    "Dataset_B_Binary_Matrix.md": "12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv):
    if len(argv) != 4:
        print(__doc__.strip().splitlines()[2]); return 2
    clone, pin, delivery = Path(argv[1]), argv[2], Path(argv[3])
    fails, out = [], {"pin": pin, "files": {}}
    git = lambda *a: subprocess.run(["git", "-C", str(clone), *a], capture_output=True, text=True)
    head = git("rev-parse", "HEAD").stdout.strip()
    if pin != PIN_COMMIT or head != PIN_COMMIT:
        fails.append(f"clone HEAD {head or '?'} is not pin {pin}")
    status = git("status", "--porcelain")
    if status.returncode or status.stdout.strip():
        fails.append("clone tree not clean or git status failed")
    out["source_git_blobs"] = {}
    for name, expected in SOURCE_BLOBS.items():
        try:
            data = (clone / name).read_bytes()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") +
                                bytes([0]) + data).hexdigest()
        except OSError:
            blob = None
        out["source_git_blobs"][name] = {"expected": expected, "actual": blob}
        if blob != expected:
            fails.append("source Git blob mismatch: " + name)
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).with_name("F-001-REBUILD-DATASETS-332.py")),
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
