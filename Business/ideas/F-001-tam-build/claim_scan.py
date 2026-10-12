#!/usr/bin/env python3
"""F-001 candidate A, TAM shape: claim worksheet for the §15.2 editorial pass (PROPOSED).

Reads a local clone of AGI144348Outlook/The-TAM-protocol (read-only) and writes,
OUTSIDE any repository, a worksheet listing every sentence that states a result
strongly enough to need an evidence-state mark (claimed / inferred / proposed test)
before sale:
  claims.csv          file, sentence number, trigger(s), sentence, status (blank: Timothy fills it)
  claims-report.json  counts per file and per trigger, source fingerprints

Triggers are fixed word patterns (certainty words, percentages, accuracy/correlation
figures). The script only finds candidates; it never edits, rates or rewrites the text.
It never sells, uploads or contacts anything.

Usage: python3 -I claim_scan.py <tam-clone-dir> <out-dir>
"""
import csv, hashlib, json, re, sys
from collections import Counter
from pathlib import Path

FILES = ["README.md", "Article 1 Hacksilber", "Article 2 Water Weight Computes",
         "The Color Dyed and Dental Records", "Article 5", "Article 6", "Article 10",
         "Collective information"]
TRIGGERS = {
    "certainty": r"\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\b",
    "percent": r"\d+(\.\d+)?\s?%",
    "accuracy": r"\b(accura(te|cy)|precision|precise(ly)?|correlat(es|ed|ion))\b",
    "superlative": r"\b(only|exactly|always|never|impossible)\b",
}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]


def main(src, out):
    src, out = Path(src).resolve(), Path(out).resolve()
    if out == src or src in out.parents:
        sys.exit("refusing to write inside the source clone")
    out.mkdir(parents=True, exist_ok=True)
    rep = {"source_files": {}, "per_file": {}, "per_trigger": Counter(), "rows": 0}
    with open(out / "claims.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "sentence_no", "triggers", "sentence", "status"])
        for name in FILES:
            p = src / name
            if not p.exists():
                rep["source_files"][name] = None
                continue
            raw = p.read_bytes()
            rep["source_files"][name] = hashlib.sha256(raw).hexdigest()
            n = 0
            for i, s in enumerate(sentences(raw.decode("utf-8", "replace")), 1):
                hits = [k for k, rx in TRIGGERS.items() if re.search(rx, s, re.I)]
                if hits:
                    n += 1
                    rep["per_trigger"].update(hits)
                    w.writerow([name, i, ";".join(hits), s, ""])
            rep["per_file"][name] = n
            rep["rows"] += n
    (out / "claims-report.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(json.dumps({"rows": rep["rows"], "per_file": rep["per_file"], "per_trigger": rep["per_trigger"]}))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
