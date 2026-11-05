"""F-001 §187 (Claude, 2026-11-05 11Z): verify a dual-hash source-pin TSV (as written by CLAUDE-source-pin-186.py)
against a local clone of The-TAM-protocol.
Usage: python3 -I CLAUDE-pin-verify-187.py <path-to-local-clone> <pin.tsv>
Re-derives git blob sha1, file sha256 and bytes for every file at the commit named in the TSV's "# commit" line,
then compares row by row. Paths are taken byte-exact (no trimming; a path that differs by one space is MISSING + EXTRA).
Prints one line per difference (MISMATCH / MISSING / EXTRA), then a summary. Exit 0 only when every row matches
and the file/byte totals agree; exit 1 on any difference; exit 2 on an unusable TSV.
Integrity gate only: it does not choose which files the ebook uses (Timothy's A6). Reads git objects; writes
nothing; prints no file text.
"""
import hashlib, subprocess, sys
repo, tsv = sys.argv[1], sys.argv[2]
def g(*a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout
commit, want, totals = None, {}, None
with open(tsv, "rb") as fh:
    for raw in fh.read().split(b"\n"):
        if not raw: continue
        line = raw.decode()
        if line.startswith("# commit\t"): commit = line.split("\t", 1)[1]; continue
        if line.startswith("# files\t"):
            f = line.split("\t"); totals = (int(f[1]), int(f[3])); continue
        if line.startswith("#"): continue
        parts = line.split("\t", 3)
        if len(parts) != 4: print(f"UNUSABLE\trow has {len(parts)} fields"); sys.exit(2)
        s, h, n, p = parts
        if p in want: print(f"UNUSABLE\tduplicate path\t{p!r}"); sys.exit(2)
        want[p] = (s, h, int(n))
if not commit or totals is None: print("UNUSABLE\tno '# commit' or '# files' line"); sys.exit(2)
full = g("rev-parse", commit + "^{commit}").decode().strip()
have = {}
for ent in g("ls-tree", "-r", "-z", full).split(b"\0"):
    if not ent: continue
    meta, path = ent.split(b"\t", 1)
    sha = meta.split()[2].decode()
    data = g("cat-file", "blob", sha)
    have[path.decode()] = (sha, hashlib.sha256(data).hexdigest(), len(data))
diffs = 0
for p in sorted(set(want) | set(have)):
    if p not in have: print(f"MISSING\t{p!r}"); diffs += 1
    elif p not in want: print(f"EXTRA\t{p!r}"); diffs += 1
    elif want[p] != have[p]:
        cols = [c for c, a, b in zip(("blob", "sha256", "bytes"), want[p], have[p]) if a != b]
        print(f"MISMATCH\t{p!r}\t{','.join(cols)}"); diffs += 1
tot_ok = totals == (len(want), sum(v[2] for v in want.values()))
print(f"commit\t{full}\nrows\t{len(want)}\tfiles_at_commit\t{len(have)}\tdifferences\t{diffs}\ttotals_line_consistent\t{tot_ok}")
ok = diffs == 0 and tot_ok
print("RESULT\t" + ("MATCH" if ok else "REFUSED"))
sys.exit(0 if ok else 1)
