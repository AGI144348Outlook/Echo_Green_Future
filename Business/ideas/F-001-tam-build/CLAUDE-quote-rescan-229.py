# F-001 §229 (Claude 2026-11-07 07Z): re-scan of The-TAM-protocol@d46456a1 for ALL quotation pairs, no length floor
# (proposal §228 (b)). Straight U+0022 quotes are paired on each line in order (1-2, 3-4, ...); a line with an odd
# number of straight quotes is reported UNPAIRED and none of its straight quotes is paired. Curly quotes are paired
# U+201C with the next U+201D on the same line. Offsets are 1-based line / 1-based code-point column; `chars` counts
# the span including both quote marks. No quoted text is printed or written: only offsets, lengths and sha256.
# Writes a TSV dataset (argv[3]) and prints a JSON summary. Also checks every QUOTED-SPANS-TRIAGE-174 row against it.
# Usage: python3 -I -B CLAUDE-quote-rescan-229.py <path to The-TAM-protocol clone> <TRIAGE-174 tsv> <out tsv>
import csv, hashlib, json, subprocess, sys
repo, tri, outp = sys.argv[1], sys.argv[2], sys.argv[3]
REV = "d46456a1"
ls = subprocess.run(["git", "-C", repo, "ls-tree", "-r", REV], capture_output=True, check=True).stdout.decode()
rows, files, skipped, unpaired_lines = [], {}, [], []
for entry in ls.strip().split("\n"):
    meta, path = entry.split("\t", 1); blob = meta.split()[2]
    raw = subprocess.run(["git", "-C", repo, "cat-file", "-p", blob], capture_output=True, check=True).stdout
    try:
        t = raw.decode("utf-8")
    except UnicodeDecodeError:
        skipped.append(path); continue
    files[path] = (blob[:7], t)
    for ln, L in enumerate(t.split("\n"), 1):
        st = [i for i, c in enumerate(L) if c == '"']
        pairs = []
        if len(st) % 2:
            unpaired_lines.append([path, ln, len(st)])
        else:
            pairs += [("straight", st[k], st[k + 1]) for k in range(0, len(st), 2)]
        i = 0
        while True:
            a = L.find("“", i)
            if a < 0: break
            b = L.find("”", a + 1)
            if b < 0: break
            pairs.append(("curly", a, b)); i = b + 1
        for style, a, b in sorted(pairs, key=lambda p: p[1]):
            span = L[a:b + 1]
            rows.append(dict(file=path, blob=blob[:7], line=ln, col=a + 1, chars=len(span), style=style,
                             inner_words=len(span[1:-1].split()),
                             sha256=hashlib.sha256(span.encode("utf-8")).hexdigest()))
with open(outp, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(rows)
bins = {"1-10": 0, "11-30": 0, "31-60": 0, "61-132": 0, ">132": 0}
for r in rows:
    n = r["chars"]; k = "1-10" if n <= 10 else "11-30" if n <= 30 else "31-60" if n <= 60 else "61-132" if n <= 132 else ">132"
    bins[k] += 1
# triage rows: is the triage span exactly one rescan pair, or does it start at a pair's closing quote?
idx = {(r["file"], r["line"], r["col"]): r for r in rows}
close_at = {(r["file"], r["line"], r["col"] + r["chars"] - 1) for r in rows}
tri_res = {"exact_pair": [], "starts_at_closing_quote": [], "other": []}
for t in csv.DictReader(open(tri, encoding="utf-8"), delimiter="\t"):
    key = (t["file"], int(t["line"]), int(t["col"]))
    p = idx.get(key)
    if p and p["chars"] == int(t["chars"]): tri_res["exact_pair"].append(int(t["row"]))
    elif key in close_at: tri_res["starts_at_closing_quote"].append(int(t["row"]))
    else: tri_res["other"].append(int(t["row"]))
summary = {"rev": REV, "files_scanned": len(files), "files_skipped_non_utf8": skipped,
           "pairs": len(rows), "straight": sum(r["style"] == "straight" for r in rows),
           "curly": sum(r["style"] == "curly" for r in rows), "length_bins_chars": bins,
           "single_word_pairs": sum(r["inner_words"] == 1 for r in rows),
           "pairs_per_file": {f: sum(r["file"] == f for r in rows) for f in files},
           "unpaired_lines": unpaired_lines,
           "triage_174_rows": {k: v for k, v in tri_res.items()},
           "out_tsv_sha256": hashlib.sha256(open(outp, "rb").read()).hexdigest()}
print(json.dumps(summary, sort_keys=True))
