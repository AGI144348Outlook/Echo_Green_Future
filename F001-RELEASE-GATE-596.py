#!/usr/bin/env python3
"""F-001 draft release gate. Offline only. UNTESTED; not publication approval.
Usage: python3 -I f001_release_gate.py <output-directory>
Does not execute builds, change source, upload, or access network.
"""
import hashlib
import json
import sys
from pathlib import Path

REQUIRED = ("tam-draft.md", "tam-draft.epub", "tam-draft.pdf",
            "dataset-a.csv", "dataset-b.csv", "build-report.json",
            "epub-report.json", "pdf-report.json")
def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def check(directory):
    root = Path(directory).resolve()
    failures, evidence = [], {}
    if not root.is_dir():
        return {"status":"HOLD", "failures":["output directory missing"], "artifacts":{}}
    for name in REQUIRED:
        p = root / name
        if not p.is_file() or p.is_symlink() or p.stat().st_size == 0:
            failures.append(name + ": missing, empty, or symlink")
            continue
        evidence[name] = {"bytes":p.stat().st_size, "sha256":digest(p)}
    for name in ("build-report.json", "epub-report.json", "pdf-report.json"):
        if name not in evidence: continue
        try:
            data = json.loads((root / name).read_text(encoding="utf-8"))
            if not isinstance(data, dict): raise ValueError("not object")
            if name == "build-report.json":
                if data.get("missing"): failures.append("source chapters missing")
                if not isinstance(data.get("source_files"),dict) or not data["source_files"]:
                    failures.append("source-file fingerprints missing")
                if data.get("epub") == "pandoc not installed; skipped":
                    failures.append("EPUB skipped")
                elif not isinstance(data.get("epub"),dict) or data["epub"].get("returncode") != 0:
                    failures.append("EPUB build not successful")
                for dataset in ("dataset-a.csv","dataset-b.csv"):
                    v = data.get("csv",{}).get(dataset)
                    if not isinstance(v,dict) or v.get("rows_incl_header",0)<2:
                        failures.append(dataset + ": table structure not evidenced")
            elif name == "epub-report.json":
                results = data.get("results")
                if not isinstance(results,list) or not results:
                    failures.append("EPUB assertions missing")
                elif any(x.get("level") != "PASS" for x in results):
                    failures.append("EPUB contains FAIL or WARN (review required)")
                if data.get("sha256") != evidence.get("tam-draft.epub",{}).get("sha256"):
                    failures.append("EPUB report hash mismatch")
            else:
                # No current authoritative PDF report schema: require explicit
                # independently reviewed evidence, not a guessed PASS key.
                failures.append("PDF report schema/independent review not yet approved")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            failures.append(name + ": invalid report (" + type(exc).__name__ + ")")
    failures.append("Editorial provenance and rights approval not machine-verifiable")
    failures.append("Android accessibility and Timothy A1-A6 approval outstanding")
    return {"status":"HOLD" if failures else "REVIEW_REQUIRED",
            "failures":failures, "artifacts":evidence}

if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit(__doc__)
    result = check(sys.argv[1])
    print(json.dumps(result, indent=2, sort_keys=True))
    sys.exit(1 if result["status"] == "HOLD" else 0)
