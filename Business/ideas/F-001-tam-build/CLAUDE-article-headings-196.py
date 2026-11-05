#!/usr/bin/env python3
"""F-001 §196 (Claude 20Z, 2026-11-05): which article numbers does the TAM source hold?

Reads a BARE clone of The-TAM-protocol (git cat-file only), writes nothing.
Prints, per source file, the article numbers found on lines of the form
"Article #N" (heading markers), plus the numbers implied by file names.
No source text is printed beyond the number and the source file name.

usage: python3 -I CLAUDE-article-headings-196.py /path/to/The-TAM-protocol.git [rev]
"""
import re
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(["git", "--git-dir", repo, *args], check=True,
                          capture_output=True).stdout


def main():
    repo = sys.argv[1]
    rev = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    commit = git(repo, "rev-parse", rev).decode().strip()
    print("rev", commit)
    heading = re.compile(r"article\s*#\s*(\d+)", re.I)
    by_name = re.compile(r"^article\s+(\d+)\b", re.I)
    found = {}
    for line in git(repo, "ls-tree", "-r", "-z", commit).split(b"\0"):
        if not line:
            continue
        meta, path = line.split(b"\t", 1)
        mode, typ, blob = meta.split()
        name = path.decode()
        if typ != b"blob" or mode == b"120000":
            continue
        text = git(repo, "cat-file", "-p", blob.decode()).decode("utf-8", "replace")
        nums = set()
        for ln in text.splitlines():
            m = heading.search(ln)
            if m:
                nums.add(int(m.group(1)))
        m = by_name.match(name)
        named = int(m.group(1)) if m else None
        if nums or named is not None:
            print(f"{blob.decode()[:7]}\t{name}\tname:{named if named is not None else '-'}\theadings:{sorted(nums)}")
        for n in nums | ({named} if named is not None else set()):
            found.setdefault(n, []).append(name)
    print("article numbers present:", sorted(found))
    print("missing in 1..10:", [n for n in range(1, 11) if n not in found])


if __name__ == "__main__":
    main()
