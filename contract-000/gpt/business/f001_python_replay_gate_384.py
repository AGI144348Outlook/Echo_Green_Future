#!/usr/bin/env python3
"""F-001 HOLD-only, opt-in, offline replay of pinned claim_scan.py.

Usage: python3 -I -B f001_python_replay_gate_384.py SOURCE_DIR SCANNER_PY INVENTORY_JSON NEW_OUTPUT_DIR
All inputs are read-only. NEW_OUTPUT_DIR must not exist and must be outside the source tree.
No editorial status is assigned and no publication is authorized.
"""
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PINS = {
    "README.md": "213bcfaf560dcc54fbb7ae79fad932e86b660357",
    "Article 1 Hacksilber": "237bd3335abdcc0f0465817dffe01ad6eaa86055",
    "Article 2 Water Weight Computes": "ec657c3fa0f70da9686fb1ae52983d28f77c6c4c",
    "The Color Dyed and Dental Records": "b525ad60ab37cb2d72ea43c40ba687b0fe2a348d",
    "Article 5": "c8c1bf617c0d81389f6c2408ed975131695857ff",
    "Article 6": "662d745f0b9b41236d1053cdbaa9351f7c020dd0",
    "Article 10": "e82be564872f636662652d34dcb8d3437559f84f",
    "Collective information": "710ad3cd4feeae7bafa329d7437a78df4c40cfa8",
}
SCANNER_PIN = "31f3dcff486c4c8cc96d514eb425da86834d00c3"
INVENTORY_PIN = "d9e36400b90cf534f9914c1c42b39d17f6d8a7fc"


def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def require_pinned(path, pin):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"missing, non-file, or symlink: {path}")
    data = path.read_bytes()
    if blob_sha(data) != pin:
        raise ValueError(f"Git blob mismatch: {path}")
    return data


def run(src, scanner, inventory_path, out):
    src, scanner, inventory_path, out = map(Path, (src, scanner, inventory_path, out))
    if not src.is_dir() or src.is_symlink():
        raise ValueError("source must be a real directory")
    src = src.resolve()
    if out.exists() or out.is_symlink():
        raise ValueError("output must be a new, absent path")
    resolved_out = out.resolve()
    if resolved_out == src or src in resolved_out.parents:
        raise ValueError("output inside source")
    if not out.parent.is_dir() or out.parent.is_symlink():
        raise ValueError("output parent must exist and not be a symlink")
    if not scanner.is_absolute() or not inventory_path.is_absolute():
        raise ValueError("scanner and inventory paths must be absolute")
    require_pinned(scanner, SCANNER_PIN)
    raw_inventory = require_pinned(inventory_path, INVENTORY_PIN)
    inv = json.loads(raw_inventory)
    if inv.get("project") != "F-001" or inv.get("status") != "HOLD" or inv.get("release_authorized"):
        raise ValueError("inventory must be F-001 HOLD without release authority")
    if inv.get("baseline_candidates") != len(inv.get("baseline", [])) or inv.get("supplemental_unflagged_candidates") != len(inv.get("supplemental", [])):
        raise ValueError("inventory counts inconsistent")
    if inv.get("combined_review_queue") != len(inv["baseline"]) + len(inv["supplemental"]):
        raise ValueError("combined inventory count inconsistent")
    listed = {s["file"]: s for s in inv["sources"]}
    if set(listed) != set(PINS):
        raise ValueError("inventory source list mismatch")
    for name, pin in PINS.items():
        if listed[name]["blob_sha"] != pin:
            raise ValueError(f"inventory pin mismatch: {name}")
        require_pinned(src / name, pin)
    # Scanner runs with -I -B and writes only to a new output outside the source.
    subprocess.run([sys.executable, "-I", "-B", str(scanner), str(src), str(out)],
                   check=True, capture_output=True, text=True, timeout=30)
    with (out / "claims.csv").open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["file", "sentence_no", "triggers", "sentence", "status"]:
            raise ValueError("scanner CSV columns changed")
        rows = list(reader)
    report = json.loads((out / "claims-report.json").read_text(encoding="utf-8"))
    expected = {(x["file"], str(x["sentence_no"])): x for x in inv["baseline"]}
    actual = {(x["file"], x["sentence_no"]): x for x in rows}
    if len(actual) != len(rows) or set(actual) != set(expected):
        raise ValueError("scanner baseline row identities differ from inventory")
    for key, item in expected.items():
        row = actual[key]
        if row["status"] or row["triggers"].split(";") != item["triggers"] or not row["sentence"].startswith(item["excerpt"]):
            raise ValueError(f"scanner content or status differs: {key}")
    if report.get("rows") != len(rows) or sum(report.get("per_file", {}).values()) != len(rows):
        raise ValueError("scanner report count mismatch")
    for name, pin in PINS.items():
        data = require_pinned(src / name, pin)  # reject changed inputs during scan
        if report.get("source_files", {}).get(name) != hashlib.sha256(data).hexdigest():
            raise ValueError(f"scanner report source digest mismatch: {name}")
    return {"project": "F-001", "status": "HOLD", "baseline_replayed": len(rows),
            "supplemental_not_scanned": len(inv["supplemental"]),
            "editorial_reviewed": 0, "publication_authorized": False}


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    try:
        print(json.dumps(run(*sys.argv[1:]), indent=2))
    except (ValueError, OSError, subprocess.SubprocessError, KeyError, TypeError) as exc:
        sys.exit(f"HOLD — replay rejected: {exc}")
