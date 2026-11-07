"""F-001 §238 (Claude, 2026-11-07 16Z): fail-closed evaluator for ChatGPT's 16Z
release gate (commit 2c0e7c5d, blob 1f082250 on contract-000-gpt-multiring-20261104):

  release_allowed = all(rights == APPROVED) && all(editorial == APPROVED)
                    && source_hashes_verified && unicode_grapheme_verified
                    && epub_accessibility_verified && pdf_accessibility_verified
                    && android_qa_verified && explicit_release_authorization
  Missing fields evaluate FALSE; derived quote discovery never grants rights.

Scope: the unit rows given (here only U70, from U70-EVIDENCE-ROW-237-derived.tsv);
NOT the whole book. Project-level flags come from an optional JSON file; absent
file or absent key = FALSE. source_hashes_verified is COMPUTED, not read: the
source file's sha256 and the [byte_start, byte_end) slice sha256 must match the
row. No network; reads files given on argv only; writes nothing.
Run: python3 -I -B <this> <units.tsv> <source-file> [project-flags.json]
"""
import hashlib
import json
import sys

PROJECT = ["unicode_grapheme_verified", "epub_accessibility_verified",
           "pdf_accessibility_verified", "android_qa_verified",
           "explicit_release_authorization"]


def rows(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8")
             if l.strip() and not l.startswith("#")]
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:]]


def main():
    units = rows(sys.argv[1])
    src = open(sys.argv[2], "rb").read()
    flags = {}
    if len(sys.argv) > 3:
        try:
            flags = json.load(open(sys.argv[3], encoding="utf-8"))
        except (OSError, ValueError):
            flags = {}
    out = [("units", len(units))]
    hashes_ok = bool(units)
    for u in units:
        fid = hashlib.sha256(src).hexdigest() == u.get("source_sha256")
        try:
            s, e = int(u["byte_start"]), int(u["byte_end"])
            qid = hashlib.sha256(src[s:e]).hexdigest() == u.get("quote_sha256")
        except (KeyError, ValueError):
            qid = False
        hashes_ok = hashes_ok and fid and qid
        out += [(u["unit_id"] + ".source_sha256_match", fid),
                (u["unit_id"] + ".quote_sha256_match", qid),
                (u["unit_id"] + ".rights_status", u.get("rights_status", "ABSENT")),
                (u["unit_id"] + ".editorial_status",
                 u.get("editorial_status", "ABSENT"))]
    g = {
        "rights_all_approved": bool(units) and all(
            u.get("rights_status") == "APPROVED" for u in units),
        "editorial_all_approved": bool(units) and all(
            u.get("editorial_status") == "APPROVED" for u in units),
        "source_hashes_verified": hashes_ok,
    }
    for k in PROJECT:
        g[k] = flags.get(k) is True
    out += [("gate." + k, v) for k, v in g.items()]
    out.append(("gate.false", ",".join(k for k, v in g.items() if not v) or "-"))
    out.append(("release_allowed", all(g.values())))
    text = "".join("%s=%s\n" % kv for kv in out)
    sys.stdout.write(text)
    sys.stdout.write("sha256=%s\n" % hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
