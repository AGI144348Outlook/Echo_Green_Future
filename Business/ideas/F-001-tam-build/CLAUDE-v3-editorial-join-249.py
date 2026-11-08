#!/usr/bin/env python3
"""F-001 §249 (Claude, 2026-11-08 03Z): read-only join of the 82 editorial occurrences
(register F-001-EDITORIAL-DECISIONS-458.tsv, git blob 300dfcf0) to the 7 v1/v3 custody rows
(V1-MANIFEST-244.json) by byte overlap in the same pinned TAM source file.

Method: re-derive claim_scan.py's sentence splitter (blob 31f3dcf: re.split on
(?<=[.!?])\\s+ or \\n{2,}, strip, drop empties) WITH byte offsets, check that the derived
sentence list equals the original splitter's list exactly, then map each occurrence id
'<file>#S<n>' to the byte span of sentence n and intersect with each custody row span.

Prints offsets, ids, counts and hashes only; never quote text. Reads git objects only.
Usage: python3 -I -B CLAUDE-v3-editorial-join-249.py <egf-clone> <tam-clone> <tam-ref> <library-ref>
"""
import hashlib, json, re, subprocess, sys

REG_BLOB = "300dfcf0ba9e9d236326d09b2a4b6c5467d3874c"
MANIFEST = "Business/ideas/F-001-tam-build/V1-MANIFEST-244.json"
SEP = re.compile(r"(?<=[.!?])\s+|\n{2,}")

def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout

def original_sentences(text):  # verbatim from claim_scan.py
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]

def spans(text):
    out, pos = [], 0
    pieces = [(m.start(), m.end()) for m in SEP.finditer(text)] + [(len(text), len(text))]
    for a, b in pieces:
        seg = text[pos:a]
        st = seg.strip()
        if st:
            lead = len(seg) - len(seg.lstrip())
            out.append((pos + lead, pos + lead + len(st)))
        pos = b
    return out

def main(egf, tam, ref, lib):
    reg = git(egf, "cat-file", "-p", REG_BLOB)
    assert hashlib.sha1(b"blob %d\0" % len(reg) + reg).hexdigest() == REG_BLOB
    rows = [l.split("\t") for l in reg.decode("utf-8").splitlines()]
    hdr, rows = rows[0], rows[1:]
    oi = hdr.index("occurrence_id")
    occ = [r[oi] for r in rows]
    man = json.loads(git(egf, "show", f"{lib}:{MANIFEST}"))
    files = sorted({o.rsplit("#S", 1)[0] for o in occ} | {m["source_path"] for m in man})
    sent = {}
    report = {"register_blob": REG_BLOB, "register_rows": len(occ), "tam_ref": ref, "files": {}}
    for f in files:
        raw = git(tam, "cat-file", "-p", f"{ref}:{f}")
        text = raw.decode("utf-8")  # strict: offsets are exact only for valid UTF-8
        sp = spans(text)
        derived = [text[a:b] for a, b in sp]
        assert derived == original_sentences(raw.decode("utf-8", "replace")), f
        bsp = [(len(text[:a].encode()), len(text[:b].encode())) for a, b in sp]
        sent[f] = bsp
        report["files"][f] = {"sha256": hashlib.sha256(raw).hexdigest(), "sentences": len(bsp)}
    bad = [o for o in occ if int(o.rsplit("#S", 1)[1]) > len(sent[o.rsplit("#S", 1)[0]])]
    report["occurrence_ids_out_of_range"] = bad
    occset = set(occ)
    joins = []
    for m in man:
        f, s, e = m["source_path"], m["byte_start"], m["byte_end_exclusive"]
        hit = [i for i, (a, b) in enumerate(sent[f], 1) if a < e and s < b]
        ids = [f"{f}#S{i}" for i in hit]
        joins.append({"unit_id": m["unit_id"], "file": f, "span": [s, e],
                      "sentences": hit,
                      "within_one_sentence": len(hit) == 1 and sent[f][hit[0]-1][0] <= s and e <= sent[f][hit[0]-1][1],
                      "editorial_occurrences": [i for i in ids if i in occset]})
    report["joins"] = joins
    report["units_with_editorial_occurrence"] = sum(1 for j in joins if j["editorial_occurrences"])
    print(json.dumps(report, indent=1, sort_keys=True))

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
