#!/usr/bin/env python3
"""F-001 HOLD-only scanner-output verification, after an independently pinned source receipt.

Usage: python3 -I f001_claim_output_gate_437.py <source-dir> <verified-pin-receipt.json>
       <claims.csv> <claims-report.json>

Never modifies inputs, approves claims, or authorizes publication. The trusted receipt
must already have been produced by the separate external Git pin verifier.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

FILES = ("README.md", "Article 1 Hacksilber", "Article 2 Water Weight Computes",
         "The Color Dyed and Dental Records", "Article 5", "Article 6", "Article 10",
         "Collective information")
TRIGGERS = {
    "certainty": r"\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\b",
    "percent": r"\d+(\.\d+)?\s?%",
    "accuracy": r"\b(accura(te|cy)|precision|precise(ly)?|correlat(es|ed|ion))\b",
    "superlative": r"\b(only|exactly|always|never|impossible)\b",
}
HEADER = ["file", "sentence_no", "triggers", "sentence", "status"]

class GateError(ValueError):
    pass

def unique(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise GateError("duplicate JSON key: " + key)
        obj[key] = value
    return obj

def load_json(path):
    p = Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size > 1_000_000:
        raise GateError("missing, symlink or oversized JSON: " + str(p))
    return json.loads(p.read_text(encoding="utf-8"), object_pairs_hook=unique)

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]

def verify(source, receipt_path, csv_path, report_path):
    source = Path(source)
    if source.is_symlink() or not source.is_dir():
        raise GateError("source must be a real directory")
    root = source.resolve(strict=True)
    for path in (receipt_path, csv_path, report_path):
        p = Path(path)
        if p.is_symlink() or not p.is_file() or p.resolve() == root or root in p.resolve().parents:
            raise GateError("receipt and scanner outputs must be regular files outside source")
    receipt, report = load_json(receipt_path), load_json(report_path)
    if not isinstance(receipt, dict) or receipt.get("schema") != "f001-verified-git-pins/v1" or receipt.get("status") != "HOLD_SOURCE_PIN_MATCH_NOT_EDITORIAL_APPROVAL" or receipt.get("source_count") != 8:
        raise GateError("receipt must be independently verified Git-pin receipt")
    if receipt.get("repository") != "AGI144348Outlook/The-TAM-protocol" or not re.fullmatch(r"[0-9a-f]{40}", str(receipt.get("source_ref", ""))):
        raise GateError("invalid receipt repository or commit pin")
    entries = receipt.get("files")
    if not isinstance(entries, list) or len(entries) != 8 or any(not isinstance(e, dict) for e in entries):
        raise GateError("receipt requires eight source records")
    if any(not isinstance(e.get("name"), str) or not isinstance(e.get("sha256"), str) or not isinstance(e.get("bytes"), int) for e in entries):
        raise GateError("invalid receipt row fields")
    by_name = {e["name"]: e for e in entries}
    if len(by_name) != 8 or set(by_name) != set(FILES):
        raise GateError("receipt source names mismatch")
    if not isinstance(report, dict) or set(report) != {"source_files", "per_file", "per_trigger", "rows"}:
        raise GateError("scanner report shape mismatch")
    if not isinstance(report["source_files"], dict) or not isinstance(report["per_file"], dict) or not isinstance(report["per_trigger"], dict) or not isinstance(report["rows"], int):
        raise GateError("invalid scanner report field types")
    if set(report["source_files"]) != set(FILES) or set(report["per_file"]) != set(FILES):
        raise GateError("scanner skipped a source file")
    expected, file_counts, trig_counts = [], {}, Counter()
    for name in FILES:
        p = root / name
        if p.is_symlink() or not p.is_file() or p.stat().st_size > 8_000_000:
            raise GateError("missing, symlink or oversized source: " + name)
        raw = p.read_bytes()
        if not raw or hashlib.sha256(raw).hexdigest() != by_name[name].get("sha256") or len(raw) != by_name[name].get("bytes"):
            raise GateError("source differs from verified receipt: " + name)
        if report["source_files"][name] != hashlib.sha256(raw).hexdigest():
            raise GateError("scanner report source fingerprint mismatch: " + name)
        n = 0
        for i, sentence in enumerate(sentences(raw.decode("utf-8", "strict")), 1):
            hits = [key for key, rx in TRIGGERS.items() if re.search(rx, sentence, re.I)]
            if hits:
                expected.append({"file": name, "sentence_no": str(i), "triggers": ";".join(hits), "sentence": sentence, "status": ""})
                n += 1
                trig_counts.update(hits)
        file_counts[name] = n
    if report["per_file"] != file_counts or report["per_trigger"] != dict(trig_counts) or report["rows"] != len(expected):
        raise GateError("scanner report count or trigger mismatch")
    csv_file = Path(csv_path)
    if csv_file.stat().st_size > 8_000_000:
        raise GateError("oversized scanner CSV")
    with csv_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != HEADER:
            raise GateError("scanner CSV header mismatch")
        rows = list(reader)
    if rows != expected:
        first = next((i for i, (a, b) in enumerate(zip(rows, expected)) if a != b), min(len(rows), len(expected)))
        raise GateError(f"scanner CSV differs from source-derived candidates at row {first + 1}; actual={len(rows)} expected={len(expected)}")
    return {"status": "HOLD_SCAN_OUTPUT_MATCH_NOT_EDITORIAL_APPROVAL", "source_ref": receipt["source_ref"], "source_count": 8, "candidate_rows": len(expected), "per_file": file_counts, "per_trigger": dict(trig_counts)}

def main(argv):
    if len(argv) != 5:
        raise GateError("usage: gate <source-dir> <verified-pin-receipt> <claims.csv> <claims-report.json>")
    print(json.dumps(verify(*argv[1:]), sort_keys=True))

if __name__ == "__main__":
    try:
        main(sys.argv)
    except (GateError, OSError, UnicodeError, json.JSONDecodeError, csv.Error) as exc:
        print("F-001 HOLD: " + str(exc), file=sys.stderr)
        sys.exit(2)
