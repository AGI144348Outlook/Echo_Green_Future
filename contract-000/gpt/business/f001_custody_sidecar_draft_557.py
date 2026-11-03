#!/usr/bin/env python3
"""F-001 custody sidecar draft generator; offline, no release authority.

Produces internal-consistency metadata only. Does not authenticate GitHub,
a test execution, a person, or a publication decision. UNTESTED successor; no release authority.
"""
import argparse
import hashlib
import json
import pathlib
import re
import stat
import sys

HEX40 = re.compile(r"^[0-9a-f]{40}$")
SAFE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("evidence_dir", type=pathlib.Path)
    p.add_argument("--source-commit", required=True)
    p.add_argument("--verifier-blob", required=True)
    p.add_argument("--harness-blob", required=True)
    p.add_argument("--out", required=True, type=pathlib.Path)
    a = p.parse_args(argv)
    if any(not HEX40.fullmatch(s) for s in (a.source_commit, a.verifier_blob, a.harness_blob)):
        p.error("expected lowercase 40-character git object ids")
    root = a.evidence_dir
    if not root.is_absolute() or root.is_symlink() or not root.is_dir():
        p.error("evidence_dir must be an absolute, real directory")
    if not a.out.is_absolute():
        p.error("output must be an absolute path")
    # Resolve the parent before comparing containment; the output may be nested
    # below the evidence root or reached through a symlinked parent.
    resolved_root = root.resolve(strict=True)
    resolved_parent = a.out.parent.resolve(strict=True)
    if resolved_parent == resolved_root or resolved_root in resolved_parent.parents:
        p.error("output must be outside the evidence directory")
    if a.out.exists() or a.out.is_symlink():
        p.error("output must be new, not a symlink or existing file")
    entries = []
    for item in sorted(root.iterdir(), key=lambda x: x.name):
        if not SAFE.fullmatch(item.name):
            p.error("unsafe evidence name")
        mode = item.lstat().st_mode
        if not stat.S_ISREG(mode):
            p.error("nonregular evidence entry")
        # One pass only: a concurrent modification is not excluded.
        data = item.read_bytes()
        entries.append({"path": item.name, "sha256": digest(data), "bytes": len(data)})
    if not entries:
        p.error("empty evidence directory")
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    sidecar = {
        "schema_version": "f001-custody-draft-1",
        "repo_full_name": "AGI144348Outlook/Echo_Green_Future",
        "source_commit_sha": a.source_commit,
        "verifier_blob_sha": a.verifier_blob,
        "harness_blob_sha": a.harness_blob,
        "evidence_files": entries,
        "bundle_sha256": digest(canonical),
        "expected_case_ids": [],
        "observed_case_ids": [],
        "independent_witness": None,
        "release_status": "HOLD",
        "limitations": ["self-reported identifiers", "no independent witness",
                        "no execution coverage assertion", "no atomic filesystem snapshot"],
    }
    with a.out.open("x", encoding="utf-8") as f:
        json.dump(sidecar, f, indent=2, sort_keys=True)
        f.write("\n")
    print("DRAFT ONLY; RELEASE HOLD")
    return 0

if __name__ == "__main__":
    sys.exit(main())
