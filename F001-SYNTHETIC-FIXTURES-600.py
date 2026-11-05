#!/usr/bin/env python3
"""F-001 synthetic fixture constructor, Run600. PREPARATION ONLY, NOT EXECUTED.
All inputs are fabricated. Never read manuscript or customer data.
Companion preregistration: Issue #265. Never claim a passing release gate.
"""
import csv
import hashlib
import json
from pathlib import Path

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def make(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=False)
    (root / "tam-draft.md").write_text("# Synthetic\nTest only\n", encoding="utf-8")
    (root / "tam-draft.epub").write_bytes(b"synthetic-epub-not-real")
    (root / "tam-draft.pdf").write_bytes(b"synthetic-pdf-not-real")
    for name in ("dataset-a.csv", "dataset-b.csv"):
        with (root / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([["id", "value"], ["1", "synthetic"]])
    build = {
        "missing": [],
        "source_files": {"synthetic.md": "fabricated"},
        "epub": {"returncode": 0},
        "csv": {n: {"rows_incl_header": 2} for n in ("dataset-a.csv", "dataset-b.csv")}
    }
    (root / "build-report.json").write_text(json.dumps(build), encoding="utf-8")
    epub = {"results": [{"level": "PASS", "name": "synthetic"}],
            "sha256": digest(root / "tam-draft.epub")}
    (root / "epub-report.json").write_text(json.dumps(epub), encoding="utf-8")
    (root / "pdf-report.json").write_text(json.dumps({"synthetic": True}), encoding="utf-8")
    return {p.name: digest(p) for p in sorted(root.iterdir()) if p.is_file()}

def mutate(root, kind):
    root = Path(root)
    if kind == "duplicate_headers":
        (root / "dataset-a.csv").write_text("id,id\n1,2\n", encoding="utf-8")
    elif kind == "blank_header":
        (root / "dataset-a.csv").write_text("id,\n1,2\n", encoding="utf-8")
    elif kind == "row_count_mismatch":
        p = root / "build-report.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["csv"]["dataset-a.csv"]["rows_incl_header"] = 99
        p.write_text(json.dumps(data), encoding="utf-8")
    elif kind == "malformed_epub_assertion":
        p = root / "epub-report.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["results"] = [None]
        p.write_text(json.dumps(data), encoding="utf-8")
    elif kind == "epub_digest_mismatch":
        (root / "tam-draft.epub").write_bytes(b"changed synthetic artifact")
    elif kind == "ragged_csv":
        (root / "dataset-a.csv").write_text("id,value\n1\n", encoding="utf-8")
    elif kind == "nonobject_json":
        (root / "epub-report.json").write_text("[]", encoding="utf-8")
    elif kind == "zero_bytes":
        (root / "tam-draft.epub").write_bytes(b"")
    elif kind == "quoted_newline":
        (root / "dataset-a.csv").write_text('id,value\n1,"two\\nlines"\n', encoding="utf-8")
    else:
        raise ValueError("unknown scenario")
    return {p.name: digest(p) for p in sorted(root.iterdir()) if p.is_file()}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        raise SystemExit("usage: python3 F001-SYNTHETIC-FIXTURES-600.py ROOT SCENARIO")
    root, scenario = sys.argv[1:]
    hashes = make(root)
    if scenario != "control":
        hashes = mutate(root, scenario)
    print(json.dumps({"scenario": scenario, "sha256": hashes}, indent=2, sort_keys=True))
