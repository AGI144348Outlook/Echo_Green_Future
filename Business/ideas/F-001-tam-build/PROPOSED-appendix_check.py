#!/usr/bin/env python3
"""F-001 TAM build: appendix vs CSV cross-check (PROPOSED, §96; read-only).

Usage: python3 -I -B PROPOSED-appendix_check.py <delivery-or-out-folder>

Reads tam-draft.epub, dataset-a.csv and dataset-b.csv in the folder and checks
that every measured mass in each CSV (column 2) appears, as "<mass>g", in the
EPUB chapter headed "Appendix A" / "Appendix B" at least as many times as it
appears in the CSV. Tokens found in an appendix but not in its CSV are listed
as INFO (the source prose repeats some values, e.g. the 13.7g base).

It writes nothing and edits nothing. Exit 0 if every CSV mass is found, exit 1
on any FAIL (missing EPUB, CSV or appendix chapter, or a CSV mass the EPUB does
not show). It does not prove the EPUB is the right book; listing_check.py
--terms and the records chain do that. It only catches an EPUB and CSV pair
that disagree on the dataset values (the §95.3 gap).
"""
import csv, html, re, sys, zipfile
from collections import Counter
from pathlib import Path

MASS = re.compile(r"(?<![\d.])(\d+\.\d+)g\b")
PAIRS = [("Appendix A", "dataset-a.csv"), ("Appendix B", "dataset-b.csv")]


def chapter_texts(epub):
    out = {}
    with zipfile.ZipFile(epub) as z:
        for n in z.namelist():
            if not n.endswith(".xhtml") or n.endswith("nav.xhtml"):
                continue
            raw = z.read(n).decode("utf-8", "replace")
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
            if not h1:
                continue
            title = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h1.group(1))).split())
            out[title] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return out


def main(folder):
    folder = Path(folder)
    fails, lines = 0, []
    epub = folder / "tam-draft.epub"
    if not epub.exists():
        print("FAIL tam-draft.epub not found"); return 1
    chapters = chapter_texts(epub)
    for heading, csvname in PAIRS:
        p = folder / csvname
        if not p.exists():
            lines.append(f"FAIL {csvname} not found"); fails += 1; continue
        with open(p, newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh))[1:]
        want = Counter(r[1] for r in rows if len(r) > 1)
        text = next((t for k, t in chapters.items() if k.startswith(heading)), None)
        if text is None:
            lines.append(f"FAIL no EPUB chapter headed '{heading}'"); fails += 1; continue
        have = Counter(MASS.findall(text))
        missing = {m: c - have[m] for m, c in want.items() if have[m] < c}
        extra = sorted((have - want).elements())
        if missing:
            fails += 1
            lines.append(f"FAIL {heading}: {csvname} masses not shown in the EPUB: "
                         + ", ".join(f"{m}g x{c}" for m, c in sorted(missing.items())))
        else:
            lines.append(f"PASS {heading}: all {sum(want.values())} {csvname} masses shown in the EPUB")
        if extra:
            lines.append(f"INFO {heading}: in the EPUB but not in {csvname}: " + ", ".join(m + "g" for m in extra))
    print("\n".join(lines))
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
