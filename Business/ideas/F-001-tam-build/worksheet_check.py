"""F-001 quoted-span worksheet checker and triage cues (Claude 21Z, §174). Read-only on a TAM checkout.
check: refuses (exit 1) a worksheet whose rows no longer point at a quoted span on the pinned text: each row's
  (file, blob, line, col, chars) must name a span matched by the SAME §172 pattern, starting exactly there with exactly
  that length, and the blob must equal the file's current git blob; classification must be blank or one of
  own / third-party / unsure. So a human classification cannot silently survive a change to the text.
triage: prints the §173 positions plus two more counts-only cues, never the quoted text:
  repeats_in_other_files = number of OTHER listed TAM files containing the exact span (a pointer to Timothy's own
  recurring phrasing or to a shared source; not proof of either); verse_ref_within_60 = scripture-style
  references (Book 3:16) inside the span or within 60 characters (translation choice matters for rights).
units (Claude 22Z, §175): groups the rows into decision units, one per distinct quoted text (rows whose inner text is
  identical share a unit), prints unit, rows, files, cued, read_order; never the text. check also refuses a worksheet in
  which two rows of the same unit carry different non-blank classifications (one human decision per text).
Usage: python3 -I worksheet_check.py check <tam dir> <worksheet.tsv>
       python3 -I worksheet_check.py triage <tam dir> <worksheet.tsv>  > triage.tsv
       python3 -I worksheet_check.py units <tam dir> <triage.tsv>  > units.tsv"""
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rights_scan import FILES, PAT  # same pattern and file list as §172/§173

SPAN = re.compile(PAT["quoted_spans_40plus"])
VERSE = re.compile(r"\b(?:[1-3]\s?)?[A-Z][a-z]+\.?\s\d{1,3}:\d{1,3}\b")
OK_CLASS = {"", "own", "third-party", "unsure"}


def load(d):
    d = os.path.abspath(d)  # §181: git -C d resolves p against d, so a relative d gave an empty blob
    out = {}
    for f in FILES:
        p = os.path.join(d, f)
        if os.path.isfile(p):
            blob = subprocess.run(["git", "-C", d, "hash-object", p], capture_output=True, text=True).stdout.strip()[:7]
            out[f] = (blob, open(p, "rb").read().decode("utf-8", "replace"))
    return out


def locate(t, line, col):
    starts = [0] + [i + 1 for i, c in enumerate(t) if c == "\n"]
    return starts[line - 1] + col - 1 if 1 <= line <= len(starts) else None


def read_ws(path):
    rows = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8") if l.strip()]
    head, body = rows[0], rows[1:]
    return head, [dict(zip(head, r + [""] * (len(head) - len(r)))) for r in body]


def check(d, ws):
    texts, (_, body), errs = load(d), read_ws(ws), []
    spans = {f: {(m.start(), m.end() - m.start()) for m in SPAN.finditer(t)} for f, (_, t) in texts.items()}
    for r in body:
        f, rid = r["file"], r["row"]
        if f not in texts: errs.append(f"row {rid}: file missing"); continue
        blob, t = texts[f]
        if r["blob"] != blob: errs.append(f"row {rid}: blob {r['blob']} != current {blob}")
        try: pos = locate(t, int(r["line"]), int(r["col"])); n = int(r["chars"])
        except ValueError: errs.append(f"row {rid}: non-numeric position"); continue
        if pos is None or (pos, n) not in spans[f]: errs.append(f"row {rid}: no quoted span of {r['chars']} chars at line {r['line']} col {r['col']}")
        if r.get("classification", "") not in OK_CLASS: errs.append(f"row {rid}: classification not in own/third-party/unsure/blank")
    seen = {}
    for r in body:
        if r["file"] not in texts: continue
        t = texts[r["file"]][1]
        try: pos = locate(t, int(r["line"]), int(r["col"])); n = int(r["chars"])
        except ValueError: continue
        if pos is None: continue
        c = r.get("classification", "")
        if c:
            k = t[pos + 1:pos + n - 1]
            if k in seen and seen[k][1] != c: errs.append(f"row {r['row']}: classification {c} differs from row {seen[k][0]} ({seen[k][1]}) for the same quoted text")
            seen.setdefault(k, (r["row"], c))
    n_spans = sum(len(s) for s in spans.values())
    if len(body) != n_spans: errs.append(f"worksheet has {len(body)} rows, text has {n_spans} spans")
    print(f"rows={len(body)} spans_in_text={n_spans} errors={len(errs)}")
    for e in errs: print("REFUSED " + e)
    return 1 if errs else 0


def triage(d, ws):
    texts, (head, body) = load(d), read_ws(ws)
    cols = ["row", "file", "blob", "line", "col", "chars", "cue_words_within_60", "url_same_line",
            "repeats_in_other_files", "verse_ref_within_60", "classification"]
    print("\t".join(cols))
    for r in body:
        t = texts[r["file"]][1]; pos = locate(t, int(r["line"]), int(r["col"])); n = int(r["chars"])
        s = t[pos + 1:pos + n - 1]  # inner text, never printed
        rep = sum(1 for g, (_, u) in texts.items() if g != r["file"] and s in u)
        win = t[max(0, pos - 60):pos + n + 60]
        print("\t".join([r[c] for c in cols[:8]] + [str(rep), str(len(VERSE.findall(win))), r.get("classification", "")]))
    return 0


def units(d, ws):
    texts, (head, body) = load(d), read_ws(ws)
    groups = {}
    for r in body:
        t = texts[r["file"]][1]; pos = locate(t, int(r["line"]), int(r["col"])); n = int(r["chars"])
        groups.setdefault(t[pos + 1:pos + n - 1], []).append(r)
    def cued(rs): return any(int(r.get("cue_words_within_60") or 0) or r.get("url_same_line") == "yes"
                             or int(r.get("repeats_in_other_files") or 0) or int(r.get("verse_ref_within_60") or 0) for r in rs)
    def tier(rs):  # §174 reading order: reporting-word cue first, then shared texts, then the rest
        if any(int(r.get("cue_words_within_60") or 0) for r in rs): return 1
        return 2 if len({r["file"] for r in rs}) > 1 else 3
    order = sorted(groups.values(), key=lambda rs: (tier(rs), int(rs[0]["row"])))
    print("\t".join(["unit", "rows", "files", "n_rows", "cued", "read_order"]))
    for i, rs in enumerate(order, 1):
        print("\t".join([f"U{i:02d}", ",".join(r["row"] for r in rs), "|".join(sorted({r["file"] for r in rs})),
                         str(len(rs)), "yes" if cued(rs) else "no", str(tier(rs))]))
    return 0


if __name__ == "__main__":
    sys.exit({"check": check, "triage": triage, "units": units}[sys.argv[1]](sys.argv[2], sys.argv[3]))
