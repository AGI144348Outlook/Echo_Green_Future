#!/usr/bin/env python3
"""F-001 candidate A, TAM shape: offline PDF step (PROPOSED; Contract 000 §24-§25).

Turns the review draft written by build.py (<out-dir>/tam-draft.md) into
<out-dir>/tam-draft.pdf with pandoc (free software), trying XeLaTeX first and
falling back to wkhtmltopdf (also free) when the LaTeX install is incomplete;
records engine, page count and sha256 in <out-dir>/pdf-report.json.

Offline only: no upload, no sale, no contact. The PDF is a review draft for
Timothy, not a product; nothing here edits The-TAM-protocol.

Usage: python3 -I build_pdf.py <out-dir>
"""
import hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

ENGINES = [  # (pdf engine, extra pandoc args); first one that succeeds wins
    ("xelatex", ["-V", "mainfont=DejaVu Serif", "-V", "geometry:margin=1in", "-V", "fontsize=11pt"]),
    ("wkhtmltopdf", ["-V", "margin-top=20mm", "-V", "margin-bottom=20mm", "-V", "margin-left=20mm", "-V", "margin-right=20mm", "--metadata", "pagetitle=TAM review draft"]),
]


def main(out):
    out = Path(out).resolve()
    md, pdf = out / "tam-draft.md", out / "tam-draft.pdf"
    if not md.exists():
        sys.exit("run build.py first: tam-draft.md not found")
    if not shutil.which("pandoc"):
        sys.exit("pandoc not installed; PDF step skipped")
    report = {"attempts": []}
    for engine, extra in ENGINES:
        if not shutil.which(engine):
            report["attempts"].append({"engine": engine, "skipped": "not installed"}); continue
        cmd = ["pandoc", md.name, "-o", pdf.name, f"--pdf-engine={engine}", "--toc"] + extra
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=out)
        errs = [l for l in r.stderr.splitlines() if l.strip()][:8]
        report["attempts"].append({"engine": engine, "returncode": r.returncode, "stderr_head": errs})
        if r.returncode == 0 and pdf.exists():
            data = pdf.read_bytes()
            report.update(engine=engine, cmd=cmd, bytes=len(data),
                          sha256=hashlib.sha256(data).hexdigest(),
                          pages=len(re.findall(rb"/Type\s*/Page[^s]", data)))
            break
    (out / "pdf-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    sys.exit(0 if "engine" in report else 1)


if __name__ == "__main__":
    main(sys.argv[1])
