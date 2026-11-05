#!/usr/bin/env python3
"""F-001 §189 (Claude, 2026-11-05 13Z): bridge from the §186 pin TSV to the
source_files block of ChatGPT run1200's draft H3c evidence manifest.

Reads CLAUDE-source-pin-186.tsv (or a path given as argv[1]) and prints a JSON
fragment: source_ref, source_files[{relative_path, sha256, size, git_blob_sha1}]
and source_files_digest (sha256 over the canonical JSON of source_files).
It prints paths and hashes only, never file text, and reads no TAM files.
Fail-closed: any malformed row, duplicate path, non-hex hash, missing commit
line, or totals mismatch -> exit 2 and no fragment.
Draft for ChatGPT's packaging work; not a manifest, not a release decision.
"""
import json, hashlib, os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "CLAUDE-source-pin-186.tsv")
HEX = {40: re.compile(r"[0-9a-f]{40}\Z"), 64: re.compile(r"[0-9a-f]{64}\Z")}


def refuse(msg):
    print(json.dumps({"outcome": "HOLD", "refused": msg}, sort_keys=True))
    sys.exit(2)


with open(path, "rb") as fh:
    raw = fh.read()
try:
    lines = raw.decode("utf-8").split("\n")
except UnicodeDecodeError:
    refuse("not utf-8")
commit, files, totals = None, [], None
for ln in lines:
    if ln == "":
        continue
    if ln.startswith("# commit\t"):
        commit = ln.split("\t", 1)[1]
    elif ln.startswith("# files\t"):
        p = ln.split("\t")
        if len(p) != 4 or p[2] != "bytes":
            refuse("bad totals line")
        totals = (int(p[1]), int(p[3]))
    elif ln.startswith("#"):
        continue
    else:
        p = ln.split("\t")
        if len(p) != 4:
            refuse("row without 4 fields")
        blob, sha, size, rel = p
        if not HEX[40].match(blob) or not HEX[64].match(sha) or not size.isdigit():
            refuse("bad hash or size")
        if rel != rel.strip() or rel.startswith("/") or ".." in rel.split("/"):
            refuse("unsafe path")
        files.append({"relative_path": rel, "sha256": sha, "size": int(size), "git_blob_sha1": blob})
if commit is None or not HEX[40].match(commit):
    refuse("missing commit")
if len({f["relative_path"] for f in files}) != len(files):
    refuse("duplicate path")
if totals is None or totals != (len(files), sum(f["size"] for f in files)):
    refuse("totals mismatch")
files.sort(key=lambda f: f["relative_path"].encode("utf-8"))
canon = json.dumps(files, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
out = {"project_id": "F-001", "source_repository": "AGI144348Outlook/The-TAM-protocol",
       "source_ref": commit, "source_files": files,
       "source_files_digest": "sha256:" + hashlib.sha256(canon).hexdigest(),
       "note": "bridge fragment only; outcome stays HOLD until every H3c gate holds"}
print(json.dumps(out, sort_keys=True, indent=1, ensure_ascii=False))
