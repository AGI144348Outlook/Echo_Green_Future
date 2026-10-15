#!/usr/bin/env python3
"""F-001 candidate A, TAM shape: pre-listing gate (PROPOSED; Contract 000 §24-§25).

Checks a listing text against the build it describes, so the page never claims
what the files do not contain (§21.3). Reads only local files:

  <listing.md>               the listing text Timothy will paste (§21.1 shape)
  <out-dir>/pdf-report.json  written by build_pdf.py (page count, sha256)
  <out-dir>/claims.csv       written by claim_scan.py, status column filled by Timothy;
                             required on every run (missing, empty or any open row = FAIL)
  <out-dir>/*.csv, *.epub    whatever the build produced

Prints PASS / FAIL lines and exits 1 on any FAIL. Never edits the listing,
never uploads, never contacts anyone.

Usage: python3 -I listing_check.py <listing.md> <out-dir>
"""
import csv, json, re, sys
from pathlib import Path

FORBIDDEN = [  # wording §15.2 / §21.3 rule out (case-insensitive)
    r"\bproves?\b(?! its thesis)", r"99\.9\s*%", r">\s*95\s*%", r"\bbestsell", r"\btestimonial",
    r"\b\d(\.\d)?\s*stars?\b", r"\bupdates included\b", r"\bguarantee[sd]?\b(?! .*refund)",
]
CLAIM_SENTENCE = "each claim is marked"
DONE = {"claimed", "inferred", "test", "cut", "sourced"}  # statuses that count as marked


def main(listing, out):
    text = Path(listing).read_text(encoding="utf-8")
    low, out = text.lower(), Path(out)
    fails, passes = [], []
    note = lambda ok, msg: (passes if ok else fails).append(msg)

    left = re.findall(r"\[[^\]\n]{1,60}\]", text)
    note(not left, f"placeholders left unfilled: {left}" if left else "no [placeholders] left")

    for pat in FORBIDDEN:
        # "does not prove" is the honest disclaimer, so a negated "prove" is allowed
        hits = [m.group(0) for m in re.finditer(pat, low)
                if not low[max(0, m.start() - 9):m.start()].rstrip().endswith(("not", "n't"))]
        note(not hits, f"forbidden wording {pat!r}: {hits}" if hits else f"no {pat!r}")

    rep = out / "pdf-report.json"
    pages = json.loads(rep.read_text())["pages"] if rep.exists() else None
    m = re.search(r"about\s+(\d+)\s+pages", low)
    if m:
        note(pages is not None and int(m.group(1)) == pages,
             f"page count: listing {m.group(1)}, build {pages}")

    # Claim ledger: checked on every listing (§27; ChatGPT run 093 found it was
    # checked only when the listing said "each claim is marked").
    rows = list(csv.DictReader(open(out / "claims.csv", encoding="utf-8"))) if (out / "claims.csv").exists() else []
    open_rows = [r for r in rows if (r.get("status") or "").strip().lower() not in DONE]
    note(bool(rows) and not open_rows,
         f"claims.csv: {len(open_rows)} of {len(rows)} rows open" if rows
         else "claims.csv missing or empty: run claim_scan.py and mark every row")
    if CLAIM_SENTENCE in low:
        note(bool(rows) and not open_rows, "listing says 'each claim is marked' and claims.csv agrees"
             if rows and not open_rows else "listing says 'each claim is marked' but claims.csv does not agree")

    if "csv" in low:
        csvs = [p.name for p in out.glob("*.csv") if p.name != "claims.csv"]
        note(bool(csvs), f"listing promises CSV files; build has {csvs or 'none'}")
    if "epub" in low:
        note(any(out.glob("*.epub")), "listing promises an EPUB; build has " + ("one" if any(out.glob("*.epub")) else "none"))

    for p in passes: print("PASS", p)
    for f in fails: print("FAIL", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
