#!/usr/bin/env python3
"""F-001 §195 (Claude 19Z, 2026-11-05). Offline check of the §194 pinned rename table and the
F-001-only caps ChatGPT adopted at 18Z (64 entries, 1 MiB/file, 4 MiB total, 64 KiB manifest).

Usage: python3 -I CLAUDE-rename-caps-check-195.py <bare TAM clone> <commit>
Reads `git ls-tree -r -l <commit>` only; writes nothing. Then runs eight synthetic adversarial
fixtures that must each be REJECTED. Prints PASS/REJECT lines and a final verdict.
Not the verifier itself (ChatGPT owns that); a reference ChatGPT can preregister against.
"""
import re, subprocess, sys

MAX_ENTRIES, MAX_FILE, MAX_TOTAL, MAX_MANIFEST = 64, 1 << 20, 4 << 20, 64 << 10
TABLE = {  # source path -> (blob prefix, output name), §194
    "Article 1 Hacksilber": ("237bd33", "article-1-hacksilber.md"),
    "Article 10": ("e82be56", "article-10.md"),
    "Article 2 Water Weight Computes": ("ec657c3", "article-2-water-weight-computes.md"),
    "Article 5": ("c8c1bf6", "article-5.md"),
    "Article 6": ("662d745", "article-6.md"),
    "Collective information": ("710ad3c", "collective-information.md"),
    "Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)":
        ("b62c970", "dataset-a-the-eshtemoa-inventory-forensic-weight-distribution.md"),
    "Dataset_B_Binary_Matrix.md": ("12ef0fc", "dataset-b-binary-matrix.md"),
    "README.md": ("213bcfa", "readme.md"),
    "The Color Dyed and Dental Records": ("b525ad6", "the-color-dyed-and-dental-records.md"),
    "URLs to storedNotebookLM Diagramed Infographics":
        ("127cca3", "urls-to-storednotebooklm-diagramed-infographics.md"),
}
SAFE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.[a-z0-9]{1,4}$")

def check(entries, table, manifest_bytes):
    """entries: list of (mode, blob, size, path). Returns list of reasons (empty = PASS)."""
    why = []
    if len(entries) > MAX_ENTRIES: why.append("too many entries")
    if manifest_bytes > MAX_MANIFEST: why.append("manifest too large")
    if sum(e[2] for e in entries) > MAX_TOTAL: why.append("total too large")
    outs = set()
    for mode, blob, size, path in entries:
        if mode != "100644": why.append(f"mode {mode}: {path}")
        if size > MAX_FILE: why.append(f"file too large: {path}")
        if path not in table: why.append(f"unpinned path: {path}"); continue
        pin, out = table[path]
        if not blob.startswith(pin): why.append(f"stale pin: {path}")
        if not SAFE.match(out) or ".." in out or "/" in out: why.append(f"unsafe output: {out}")
        if out.casefold() in outs: why.append(f"output collision: {out}")
        outs.add(out.casefold())
    return why

def real(repo, commit):
    raw = subprocess.run(["git", "--git-dir", repo, "ls-tree", "-r", "-l", "-z", commit],
                         capture_output=True, check=True).stdout.decode()
    out = []
    for rec in filter(None, raw.split("\0")):
        meta, path = rec.split("\t", 1)
        mode, _typ, blob, size = meta.split()
        out.append((mode, blob, int(size), path))
    return out

def main():
    ents = real(sys.argv[1], sys.argv[2])
    manifest = sum(len(p) + 80 for *_x, p in ents)  # rough manifest size estimate
    why = check(ents, TABLE, manifest)
    print(f"real {sys.argv[2][:7]}: {len(ents)} entries, {sum(e[2] for e in ents)} bytes:",
          "PASS" if not why else "REJECT " + "; ".join(why))
    base = [e for e in ents]
    first = base[0]
    t2 = dict(TABLE); t2["Article 5"] = ("c8c1bf6", "Article-10.md")
    t3 = dict(TABLE); t3["Article 5"] = ("c8c1bf6", "article-10.md")
    t4 = dict(TABLE); t4["Article 5"] = ("c8c1bf6", "../article-5.md")
    t5 = dict(TABLE); t5["Article 5"] = ("c8c1bf6", "dataset-a:x.md")
    fixtures = [
        ("F1 65 entries", base + [("100644", "0"*40, 1, f"x{i}") for i in range(54)], TABLE, 1000),
        ("F2 file over 1 MiB", [(first[0], first[1], MAX_FILE + 1, first[3])] + base[1:], TABLE, 1000),
        ("F3 total over 4 MiB", [(m, b, 400_000, p) for m, b, _s, p in base], TABLE, 1000),
        ("F4 manifest over 64 KiB", base, TABLE, MAX_MANIFEST + 1),
        ("F5 unpinned new file", base + [("100644", "1"*40, 10, "Article 3")], TABLE, 1000),
        ("F6 stale pin (blob changed)", [(m, ("f"*40 if p == "Article 5" else b), s, p) for m, b, s, p in base], TABLE, 1000),
        ("F7 output casefold collision", base, t3, 1000),
        ("F8 traversal output", base, t4, 1000),
        ("F9 colon output", base, t5, 1000),
        ("F10 uppercase output", base, t2, 1000),
        ("F11 symlink mode", [("120000" if p == "README.md" else m, b, s, p) for m, b, s, p in base], TABLE, 1000),
    ]
    bad = 0
    for name, e, t, mb in fixtures:
        w = check(e, t, mb)
        bad += not w
        print(f"{name}: {'REJECT ' + w[0] if w else 'PASS (WRONG)'}")
    print("verdict:", "OK" if not why and bad == 0 else "FAIL")

if __name__ == "__main__":
    main()
