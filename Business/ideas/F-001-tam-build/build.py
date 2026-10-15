#!/usr/bin/env python3
"""F-001 candidate A, TAM shape: offline draft build (PROPOSED; Contract 000 §24-§25).

Reads a local clone of AGI144348Outlook/The-TAM-protocol (read-only) and writes,
into an output directory OUTSIDE any repository:
  tam-draft.md     ordered manuscript (title block, articles, appendices)
  dataset-a.csv, dataset-b.csv   the two tables as CSV, only if they are delimited tables
  tam-draft.epub   if pandoc is installed (pandoc is free software); optional
                   F001_BOOK_ID/SOURCE_DATE_EPOCH (§24), F001_COVER (§25), F001_A11Y (§26)
  build-report.json  word counts, duplicate-sentence and chapter-repeat checks (§28, line check §29), file fingerprints

It never edits the source, sells, uploads or contacts anything. The output is a
review draft for Timothy, not a product: the editorial pass (§15.2 status marks
and falsification boxes) is not done by this script.

Usage: python3 -I build.py <tam-clone-dir> <out-dir>
"""
import csv, hashlib, json, os, re, shutil, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
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


ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff"))


def sentence_list(text):
    """Sentences of 8+ words, in order. Zero-width characters are removed and
    whitespace collapsed first (F-001 §28): the source uses U+200B before some
    lines, which made otherwise identical sentences compare unequal."""
    text = text.translate(ZERO_WIDTH)
    return [" ".join(s.split()) for s in re.split(r"(?<=[.!?])\s+", text) if len(s.split()) >= 8]


def sentences(text):
    return set(sentence_list(text))


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
            # not_in_collective lists the text itself, so nothing is lost if the
            # chapter stays out of the draft (R3: no deletions)
            # a sentence the splitter cut differently (line breaks) still counts as
            # covered when its normalized text occurs inside the Collective
            flat = " ".join(collective.translate(ZERO_WIDTH).split())
            as_text = {x for x in s - cs if x in flat}
            report["dup_check"][name] = {"long_sentences": len(s), "also_in_collective": len(s & cs),
                                         "found_as_text": len(as_text),
                                         "not_in_collective": sorted(s - cs - as_text)}
    # Chapter de-duplication (F-001 §28): a long sentence that appears more than
    # once across the chapters that ARE in the draft. Reported, never removed.
    seen = {}
    for heading, name in ORDER:
        p = src / name
        if p.exists():
            for s in sentence_list(p.read_text(encoding="utf-8", errors="replace")):
                seen.setdefault(s, []).append(name)
    repeats = {s: v for s, v in seen.items() if len(v) > 1}
    # Line check (F-001 §29): the sentence rule splits only at . ! ? so a sentence
    # right after a heading without end punctuation is joined to it and a repeat
    # can be missed. Lines of 4+ words are compared too, after removing markdown
    # markers (#, >, -, *, list numbers) and zero-width characters. Reported only.
    line_seen = {}
    for heading, name in ORDER:
        p = src / name
        if p.exists():
            for ln in p.read_text(encoding="utf-8", errors="replace").translate(ZERO_WIDTH).splitlines():
                ln = re.sub(r"^\s*(?:#+|>|[-*+]|\d+[.)])\s*", "", ln)
                ln = " ".join(ln.split())
                if len(ln.split()) >= 4:
                    line_seen.setdefault(ln, []).append(name)
    line_repeats = {s: v for s, v in line_seen.items() if len(v) > 1}
    report["draft_repeats"] = {"repeated_sentences": len(repeats),
                               "extra_copies": sum(len(v) - 1 for v in repeats.values()),
                               "where": sorted({" + ".join(sorted(set(v))) for v in repeats.values()}),
                               "repeated_lines": len(line_repeats),
                               "extra_line_copies": sum(len(v) - 1 for v in line_repeats.values()),
                               "line_where": sorted({" + ".join(sorted(set(v))) for v in line_repeats.values()})}
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
        # Accessibility metadata (F-001 §26, opt-in): pandoc 3.1.3 drops schema:* <meta>
        # given via --epub-metadata, so a file of such lines (written truthfully by the
        # editor, e.g. a11y-metadata.xml) is inserted into the OPF after pandoc runs.
        # Entry order, compression and timestamps are kept, so §24 reproducibility holds.
        a11y = os.environ.get("F001_A11Y")
        a11y_xml = None
        if a11y:
            ap = Path(a11y)
            try:
                a11y_xml = ap.read_text(encoding="utf-8").strip()
                els = list(ET.fromstring(f"<m>{a11y_xml}</m>"))
            except (OSError, ET.ParseError):
                sys.exit("F001_A11Y must be a readable file of <meta property=\"schema:...\">...</meta> lines")
            if not els or any(e.tag != "meta" or not (e.get("property") or "").startswith("schema:") for e in els):
                sys.exit("F001_A11Y may only hold <meta property=\"schema:...\"> elements")
            report["accessibility_metadata"] = {"file": ap.name, "sha256": hashlib.sha256(ap.read_bytes()).hexdigest(),
                                                "properties": sorted({e.get("property") for e in els})}
        else:
            report["accessibility_metadata"] = "none (F001_A11Y unset)"
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode == 0 and a11y_xml:
            ep = out / "tam-draft.epub"; tmp = out / "tam-draft.epub.tmp"
            with zipfile.ZipFile(ep) as src, zipfile.ZipFile(tmp, "w") as dst:
                for info in src.infolist():
                    data = src.read(info.filename)
                    if info.filename.endswith(".opf"):
                        data = data.replace(b"</metadata>", a11y_xml.encode("utf-8") + b"\n</metadata>", 1)
                    dst.writestr(info, data)
            tmp.replace(ep)
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
