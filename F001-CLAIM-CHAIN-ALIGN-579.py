#!/usr/bin/env python3
"""F-001 claim-chain alignment gate v579. DRAFT / UNTESTED / RELEASE HOLD.
Usage: python3 -I F001-CLAIM-CHAIN-ALIGN-577.py <source-dir> <worksheet-dir>
Changes from v577: reject malformed top-level JSON reports and zero-trigger corpora.
Pinned scanner reference: claim_scan.py blob 31f3dcff486c4c8cc96d514eb425da86834d00c3.
This separately reconstructs its FILES, segmentation and trigger classification;
a future source change requires an explicit reviewed update. Read-only.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

FILES = ["README.md", "Article 1 Hacksilber", "Article 2 Water Weight Computes",
         "The Color Dyed and Dental Records", "Article 5", "Article 6",
         "Article 10", "Collective information"]
TRIGGERS = {
    "certainty": r"\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\b",
    "percent": r"\d+(\.\d+)?\s?%",
    "accuracy": r"\b(accura(te|cy)|precision|precise(ly)?|correlat(es|ed|ion))\b",
    "superlative": r"\b(only|exactly|always|never|impossible)\b",
}
COLUMNS = ["file", "sentence_no", "triggers", "sentence", "status"]
STATUSES = {"claimed", "inferred", "test", "cut", "sourced"}

def evaluate(source_dir, output_dir):
    src, out = Path(source_dir).resolve(), Path(output_dir).resolve()
    errors = []
    report = json.loads((out / "claims-report.json").read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        return ["claims-report.json must contain a JSON object"]
    with (out / "claims.csv").open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            return ["worksheet columns differ from pinned scanner"]
        rows = list(reader)
    if not isinstance(report.get("source_files"), dict) or set(report["source_files"]) != set(FILES):
        errors.append("source manifest differs from pinned FILES")
    expected, hashes, per_file, per_trigger = [], {}, {}, Counter()
    for name in FILES:
        path = src / name
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(src):
            errors.append("missing, linked or unsafe source: " + name)
            continue
        raw = path.read_bytes()
        hashes[name] = hashlib.sha256(raw).hexdigest()
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", raw.decode("utf-8", "replace")) if s.strip()]
        count = 0
        for index, sentence in enumerate(sentences, 1):
            hits = [key for key, pattern in TRIGGERS.items() if re.search(pattern, sentence, re.I)]
            if hits:
                expected.append((name, str(index), ";".join(hits), sentence))
                per_trigger.update(hits)
                count += 1
        per_file[name] = count
    if report.get("source_files") != hashes:
        errors.append("source fingerprints do not match actual required inputs")
    if report.get("per_file") != per_file:
        errors.append("per-file counts differ from recomputed scanner output")
    if report.get("per_trigger") != dict(per_trigger):
        errors.append("trigger counts differ from recomputed scanner output")
    if report.get("rows") != len(expected):
        errors.append("total report count differs from recomputed scanner output")
    actual = [(r["file"], r["sentence_no"], r["triggers"], r["sentence"]) for r in rows]
    if not expected:
        errors.append("no triggered claims available for editorial review; release remains HOLD")
    if actual != expected:
        errors.append("worksheet row sequence/content differs from recomputed scanner output")
    if any((r["status"] or "").strip().lower() not in STATUSES for r in rows):
        errors.append("unreviewed or invalid editorial status")
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: gate <source-dir> <worksheet-dir>")
    try:
        problems = evaluate(sys.argv[1], sys.argv[2])
    except (OSError, ValueError, UnicodeError, csv.Error, TypeError, KeyError) as exc:
        problems = ["input error: " + type(exc).__name__]
    for problem in problems:
        print("FAIL", problem)
    if not problems:
        print("PASS scanner/worksheet alignment ONLY; RELEASE HOLD")
    sys.exit(bool(problems))
