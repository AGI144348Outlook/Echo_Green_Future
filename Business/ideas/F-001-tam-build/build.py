#!/usr/bin/env python3
"""F-001 candidate A, TAM shape: offline draft build (PROPOSED; Contract 000 §24-§25).

Reads a local clone of AGI144348Outlook/The-TAM-protocol (read-only) and writes,
into an output directory OUTSIDE any repository:
  tam-draft.md     ordered manuscript (title block, articles, appendices)
  dataset-a.csv, dataset-b.csv   the two tables as CSV, only if they are delimited tables
  tam-draft.epub   if pandoc is installed (pandoc is free software)
  build-report.json  word counts, duplicate-sentence check, file fingerprints

It never edits the source, sells, uploads or contacts anything. The output is a
review draft for Timothy, not a product: the editorial pass (§15.2 status marks
and falsification boxes) is not done by this script.

Usage: python3 -I build.py <tam-clone-dir> <out-dir>
"""
import csv, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

ORDER = [  # reading order (§15.3); Article 4 is missing in the source (§15.1)
    ("Introduction", "README.md"),
    ("1. The Metric Shock", "Article 1 Hacksilber"),
    ("2. The Water-Weight Computer", "Article 2 Water Weight Computes"),
    ("3. The Chemistry of the Registry", "The Color Dyed and Dental Records"),
    ("5. The Azores Anomaly", "Article 5"),
    ("6-10. Collected notes", "Collective information"),
]
DUP_ONLY = ["Article 6", "Article 10"]  # their long sentences are inside "Collective information"
DATASETS = [("Appendix A", "Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)", "dataset-a.csv"),
            ("Appendix B", "Dataset_B_Binary_Matrix.md", "dataset-b.csv")]
TITLE = "The TAM Protocol: A Speculative Reconstruction (review draft)"


def sentences(text):
    return {s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.split()) >= 8}


def md_table_to_rows(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows


def main(src, out):
    src, out = Path(src).resolve(), Path(out).resolve()
    if out == src or src in out.parents:
        sys.exit("refusing to write inside the source clone")
    out.mkdir(parents=True, exist_ok=True)
    report = {"source_files": {}, "missing": [], "dup_check": {}, "csv": {}}
    parts = [f"---\ntitle: \"{TITLE}\"\nlang: en\n---\n"]
    collective = (src / "Collective information").read_text(encoding="utf-8", errors="replace")
    for heading, name in ORDER:
        p = src / name
        if not p.exists():
            report["missing"].append(name); continue
        t = p.read_text(encoding="utf-8", errors="replace")
        report["source_files"][name] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "words": len(t.split())}
        body = re.sub(r"^#\s", "## ", t, flags=re.M)  # demote source H1s under the chapter heading
        parts.append(f"\n# {heading}\n\n> Status: source text, not yet edited (claims unmarked; see F-001 §15.2).\n\n{body}\n")
    cs = sentences(collective)
    for name in DUP_ONLY:
        p = src / name
        if p.exists():
            s = sentences(p.read_text(encoding="utf-8", errors="replace"))
            report["dup_check"][name] = {"long_sentences": len(s), "also_in_collective": len(s & cs)}
    for heading, name, csvname in DATASETS:
        p = src / name
        if not p.exists():
            report["missing"].append(name); continue
        t = p.read_text(encoding="utf-8", errors="replace")
        rows = md_table_to_rows(t)
        if rows:
            with open(out / csvname, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(rows)
            report["csv"][csvname] = {"rows_incl_header": len(rows)}
            parts.append(f"\n# {heading}\n\n{t}\n\n(CSV: `{csvname}`)\n")
        else:  # source tables lost their column delimiters; columns need a hand pass
            report["csv"][csvname] = "no delimited table found; CSV not written (needs hand-made columns)"
            parts.append(f"\n# {heading}\n\n```\n{t}\n```\n")
    md = out / "tam-draft.md"
    md.write_text("".join(parts), encoding="utf-8")
    report["draft_words"] = len(md.read_text(encoding="utf-8").split())
    if shutil.which("pandoc"):
        cmd = ["pandoc", str(md), "-o", str(out / "tam-draft.epub"), "--toc"]
        # Reproducible EPUB (F-001 §24, opt-in): a fixed identifier chosen once and
        # recorded, plus SOURCE_DATE_EPOCH for stable timestamps. Unset = old behaviour.
        book_id = os.environ.get("F001_BOOK_ID")
        if book_id:
            if not re.fullmatch(r"urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", book_id):
                sys.exit("F001_BOOK_ID must look like urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
            cmd += ["--metadata", f"identifier={book_id}"]
        # Cover (F-001 §25, opt-in): Timothy's own or a licensed image; JPEG or PNG.
        # Unset = no cover (as before). A bad path or type stops before the EPUB step.
        cover = os.environ.get("F001_COVER")
        if cover:
            cp = Path(cover)
            head = cp.read_bytes()[:8] if cp.is_file() else b""
            if not (head.startswith(b"\xff\xd8\xff") or head.startswith(b"\x89PNG\r\n\x1a\n")):
                sys.exit("F001_COVER must be an existing JPEG or PNG file")
            cmd += ["--epub-cover-image", str(cp)]
            report["cover"] = {"file": cp.name, "sha256": hashlib.sha256(cp.read_bytes()).hexdigest()}
        else:
            report["cover"] = "none (F001_COVER unset)"
        report["epub_reproducible"] = {"identifier": book_id or "random (pandoc default)",
                                       "SOURCE_DATE_EPOCH": os.environ.get("SOURCE_DATE_EPOCH") or "unset"}
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        report["epub"] = {"returncode": r.returncode, "stderr": r.stderr[-500:],
                          "bytes": (out / "tam-draft.epub").stat().st_size if r.returncode == 0 else None}
    else:
        report["epub"] = "pandoc not installed; skipped"
    (out / "build-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
