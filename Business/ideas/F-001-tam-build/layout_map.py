#!/usr/bin/env python3
"""F-001 §38: stage the branch layout of The-TAM-protocol under main's file names (PROPOSED).

The build tools in this folder read main's file names (d46456a). The unmerged
branch claude/github-claude-code-connection-98qkbx (5f8612b, F-001 §37) holds the
same material as articles/, datasets/, reference/. This script COPIES the branch
files into a staging directory OUTSIDE any repository under main's names, so
build.py can run on either layout unchanged. It never edits, moves or deletes
anything in the source clone (R3).

Usage: python3 -I layout_map.py <branch-layout-clone> <staging-dir>
Exit 1 if any mapped file is missing or the staging dir is inside the clone.
"""
import hashlib, json, shutil, sys
from pathlib import Path

# main name (d46456a)  ->  branch path (5f8612b); LICENSE/.gitignore exist only on the branch
MAP = {
    "README.md": "README.md",
    "Article 1 Hacksilber": "articles/article-01-hacksilber.md",
    "Article 2 Water Weight Computes": "articles/article-02-water-weight-computes.md",
    "Article 5": "articles/article-05.md",
    "Article 6": "articles/article-06.md",
    "Article 10": "articles/article-10.md",
    "Collective information": "reference/collective-information.md",
    "The Color Dyed and Dental Records": "reference/the-color-dyed-and-dental-records.md",
    "URLs to storedNotebookLM Diagramed Infographics": "reference/notebooklm-diagrammed-infographics.md",
    "Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)":
        "datasets/dataset-a-eshtemoa-inventory-forensic-weight-distribution.md",
    "Dataset_B_Binary_Matrix.md": "datasets/dataset-b-binary-matrix.md",
}


def main(src, dst):
    src, dst = Path(src).resolve(), Path(dst).resolve()
    if dst == src or src in dst.parents:
        sys.exit("staging dir must be outside the source clone")
    missing = [b for b in MAP.values() if not (src / b).is_file()]
    if missing:
        print(json.dumps({"missing": missing}, indent=2)); sys.exit(1)
    dst.mkdir(parents=True, exist_ok=True)
    rows = []
    for main_name, branch_path in MAP.items():
        data = (src / branch_path).read_bytes()
        (dst / main_name).write_bytes(data)
        rows.append({"main_name": main_name, "branch_path": branch_path,
                     "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    unmapped = sorted(str(p.relative_to(src)) for p in src.rglob("*")
                      if p.is_file() and ".git" not in p.parts
                      and str(p.relative_to(src)) not in MAP.values())
    report = {"mapped": rows, "unmapped_branch_files": unmapped}
    (dst.parent / (dst.name + "-layout-map.json")).write_text(json.dumps(report, indent=2))
    print(json.dumps({"mapped": len(rows), "unmapped_branch_files": unmapped}))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
