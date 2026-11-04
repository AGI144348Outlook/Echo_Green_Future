# F-001 release gate — static hardening proposal 597
# DRAFT / UNTESTED. Do not use as a release authorization.
# Offline and read-only. No network or paid inference.
import csv
import hashlib
import json
import sys
from pathlib import Path

REQUIRED = ("tam-draft.md", "tam-draft.epub", "tam-draft.pdf", "dataset-a.csv", "dataset-b.csv", "build-report.json", "epub-report.json", "pdf-report.json")

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            h.update(block)
    return h.hexdigest()

def check(directory):
    root = Path(directory).resolve()
    findings, artifacts = [], {}
    if not root.is_dir():
        return {"status": "HOLD", "findings": ["output directory missing"], "artifacts": {}}
    for name in REQUIRED:
        p = root / name
        try:
            if p.is_symlink() or not p.is_file() or p.stat().st_size == 0:
                findings.append(name + ": missing, empty or symlink")
                continue
            artifacts[name] = {"bytes": p.stat().st_size, "sha256": sha256(p)}
        except OSError as error:
            findings.append(name + ": unreadable (" + type(error).__name__ + ")")
    for name in ("dataset-a.csv", "dataset-b.csv"):
        if name not in artifacts:
            continue
        try:
            with (root / name).open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream))
            if len(rows) < 2 or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
                findings.append(name + ": missing data or inconsistent column counts")
        except (OSError, UnicodeError, csv.Error):
            findings.append(name + ": unreadable or malformed CSV")
    for name in ("build-report.json", "epub-report.json", "pdf-report.json"):
        if name not in artifacts:
            continue
        try:
            data = json.loads((root / name).read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("report must be an object")
            if name == "build-report.json":
                if data.get("missing"):
                    findings.append("missing source chapters")
                if not isinstance(data.get("source_files"), dict) or not data["source_files"]:
                    findings.append("source-file evidence missing")
                epub = data.get("epub")
                if not isinstance(epub, dict) or epub.get("returncode") != 0:
                    findings.append("EPUB build success not evidenced")
                csv_report = data.get("csv")
                if not isinstance(csv_report, dict):
                    findings.append("CSV build evidence missing")
                else:
                    for dataset in ("dataset-a.csv", "dataset-b.csv"):
                        item = csv_report.get(dataset)
                        if not isinstance(item, dict) or not isinstance(item.get("rows_incl_header"), int) or item["rows_incl_header"] < 2:
                            findings.append(dataset + ": build row evidence missing")
            elif name == "epub-report.json":
                results = data.get("results")
                if not isinstance(results, list) or not results or any(
                    not isinstance(row, dict) or row.get("level") != "PASS" for row in results
                ):
                    findings.append("EPUB assertions incomplete, invalid, or non-PASS")
                if data.get("sha256") != artifacts.get("tam-draft.epub", {}).get("sha256"):
                    findings.append("EPUB report digest mismatch")
            else:
                findings.append("PDF report schema and independent review not approved")
        except (OSError, UnicodeError, ValueError, TypeError, KeyError):
            findings.append(name + ": invalid report")
    findings.append("Editorial provenance and quotation rights not independently approved")
    findings.append("Android accessibility and Timothy A1-A6 decisions not verified")
    return {"status": "HOLD", "findings": findings, "artifacts": artifacts}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 -I F001-RELEASE-GATE-597.py <output-directory>", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(check(sys.argv[1]), indent=2, sort_keys=True))
    sys.exit(1)
