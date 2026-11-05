"""F-001 §186 (Claude, 2026-11-05 10Z): dual-hash source-pin inventory of The-TAM-protocol at one commit.
Usage: python3 -I CLAUDE-source-pin-186.py <path-to-local-clone> <commit>
Prints, for every file at that commit: git blob sha1, file sha256, bytes, path (tab-separated, sorted by path).
Inventory only: which files the ebook uses is Timothy's A6 decision, not this script's. Reads git objects only;
writes nothing; prints no file text.
"""
import hashlib, subprocess, sys
repo, commit = sys.argv[1], sys.argv[2]
def g(*a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout
full = g("rev-parse", commit + "^{commit}").decode().strip()
print(f"# commit\t{full}")
print("# columns: git_blob_sha1\tfile_sha256\tbytes\tpath")
rows = []
for ent in g("ls-tree", "-r", "-z", full).split(b"\0"):
    if not ent: continue
    meta, path = ent.split(b"\t", 1)
    mode, typ, sha = meta.split()
    data = g("cat-file", "blob", sha.decode())
    rows.append((path.decode(), sha.decode(), hashlib.sha256(data).hexdigest(), len(data)))
for p, s, h, n in sorted(rows):
    print(f"{s}\t{h}\t{n}\t{p}")
print(f"# files\t{len(rows)}\tbytes\t{sum(r[3] for r in rows)}")
