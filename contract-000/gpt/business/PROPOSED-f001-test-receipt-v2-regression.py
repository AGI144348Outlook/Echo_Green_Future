#!/usr/bin/env python3
"""Isolated synthetic characterization of proposed receipt verifier; no valid book artifacts."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SCRIPT = Path(__file__).with_name("PROPOSED-f001-receipt-verify-v2.py")
A = ("epub", "pdf", "dataset_a_csv", "dataset_b_csv")
SCRIPTS = ("build.py", "build_pdf.py", "rebuild_datasets.py", "claim_scan.py",
           "listing_check.py", "epub_check.py", "PROPOSED-f001-disposition-binding-v5.py")


def sha(b): return hashlib.sha256(b).hexdigest()


def fixture(root):
    payloads = {"epub": b"SYNTHETIC EPUB PLACEHOLDER, NOT A BOOK",
                "pdf": b"SYNTHETIC PDF PLACEHOLDER, NOT A BOOK",
                "dataset_a_csv": b"entry,measured,stated\nA,1,1\nB,2,2\n",
                "dataset_b_csv": b"entry,value\nC,3\n"}
    pin = {"schema": "f001-pins/v1", "source": {"repository": "AGI144348Outlook/The-TAM-protocol", "commit": "a" * 40},
           "inputs": {"article-1.md": "b" * 40}, "scripts": {k: "c" * 40 for k in SCRIPTS},
           "apply_order_blob": "d" * 40, "applied_patches": {},
           "artifacts": {k: {"sha256": sha(v), "size": len(v)} for k, v in payloads.items()}}
    receipt = {"schema": "f001-receipt/v1", "source": copy.deepcopy(pin["source"]),
               "inputs": copy.deepcopy(pin["inputs"]), "scripts": copy.deepcopy(pin["scripts"]),
               "apply_order_blob": pin["apply_order_blob"], "applied_patches": {},
               "environment": {"platform": "synthetic-linux", "python_version": "3.13", "build_output_realpath": str(root)},
               "artifacts": {k: {"path": k + ".bin", **pin["artifacts"][k]} for k in A},
               "editorial": {"release": "HOLD", "status": "PENDING", "source_pin_authenticated": False,
                             "decision_reference_authenticated": False, "dataset_a_sha256": pin["artifacts"]["dataset_a_csv"]["sha256"],
                             "flagged_csv_lines": [6, 7]},
               "release": "HOLD", "approved": False, "timothy_approval_reference": None}
    for k, v in payloads.items(): (root / (k + ".bin")).write_bytes(v)
    return pin, receipt


def run_case(name, edit, expected):
    with tempfile.TemporaryDirectory(prefix="f001-receipt-") as td:
        root = Path(td)
        pin, receipt = fixture(root)
        edit(root, pin, receipt)
        pins_file, receipt_file = root / "pins.json", root / "receipt.json"
        pins_file.write_text(json.dumps(pin, sort_keys=True))
        if name == "duplicate_json":
            receipt_file.write_text('{"schema":"f001-receipt/v1","schema":"f001-receipt/v1"}')
        else:
            receipt_file.write_text(json.dumps(receipt, sort_keys=True))
        inputs = [p for p in root.rglob("*") if p.is_file() and not p.is_symlink()]
        before = {str(p): sha(p.read_bytes()) for p in inputs}
        cmd = [sys.executable, "-I", "-B", str(SCRIPT), "--pins", str(pins_file),
               "--receipt", str(receipt_file), "--artifact-root", str(root)]
        cp = subprocess.run(cmd, text=True, capture_output=True, timeout=4)
        data = json.loads(cp.stdout)
        after = {str(p): sha(p.read_bytes()) for p in inputs}
        passed = (cp.returncode == expected and data.get("integrity") == ("PASS" if expected == 0 else "FAIL")
                  and data.get("release") == "HOLD" and data.get("source_pin_authenticated") is False
                  and data.get("approval_authenticated") is False and data.get("publication_authorization") == "ABSENT"
                  and data.get("format_accessibility_rights_verified") is False and before == after
                  and not cp.stderr and (bool(data.get("issues")) == (expected != 0)))
        return {"case": name, "pass": passed, "exit": cp.returncode, "integrity": data.get("integrity"),
                "release": data.get("release"), "issues": data.get("issues"), "checked": len(data.get("artifacts_checked", []))}


def noop(root, pin, receipt): pass

def missing_pdf(root, pin, receipt): (root / "pdf.bin").unlink()
def stale_a(root, pin, receipt): (root / "dataset_a_csv.bin").write_bytes(b"tampered")
def wrong_commit(root, pin, receipt): receipt["source"]["commit"] = "f" * 40
def missing_script(root, pin, receipt):
    del pin["scripts"]["build_pdf.py"]
    del receipt["scripts"]["build_pdf.py"]
def false_approval(root, pin, receipt):
    receipt["approved"] = True
    receipt["release"] = "READY"
def traversal(root, pin, receipt): receipt["artifacts"]["epub"]["path"] = "../outside.epub"
def symlink(root, pin, receipt):
    (root / "pdf.bin").rename(root / "real-pdf.bin")
    (root / "pdf.bin").symlink_to("real-pdf.bin")
def forged_hash(root, pin, receipt): receipt["artifacts"]["epub"]["sha256"] = "0" * 64

cases = [("consistent", noop, 0), ("missing_pdf", missing_pdf, 1), ("stale_a", stale_a, 1),
         ("wrong_commit", wrong_commit, 1), ("missing_script", missing_script, 1),
         ("false_approval", false_approval, 1), ("traversal", traversal, 1),
         ("symlink", symlink, 1), ("duplicate_json", noop, 1), ("forged_hash", forged_hash, 1)]

if __name__ == "__main__":
    results = [run_case(*case) for case in cases]
    print(json.dumps({"passed": sum(x["pass"] for x in results), "total": len(results), "results": results}, indent=2))
    sys.exit(0 if all(x["pass"] for x in results) else 1)
