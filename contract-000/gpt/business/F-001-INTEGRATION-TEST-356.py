#!/usr/bin/env python3
"""Run 356 synthetic full-chain F-001 regression; NOT a release test.

Requires unmodified 353 shape gate, 354 byte verifier and 355 closure wrapper
in the same directory. No network, CI, real book, paid inference or publication.
Prospective plan: Echo_Green_Future Issue #53 PRE 6403209278; D1/D2 amendment
6403239964. This harness is a reproducible follow-up to the local 14-case run.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "F-001-BUNDLE-CLOSURE-355.py"
SOURCE = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
CSV = {
    "dataset-a.csv": "989d83c16568f23a97251d93919068f3a5e726c738644625af909b278f395fdb",
    "dataset-b.csv": "ff442e48acaf00900a3bc3d7900bf987995355a34226b749dbd5b81878e2f7c0",
}
EVIDENCE = ("editorial", "rights", "attribution", "independent_rebuild",
            "epubcheck", "ace", "pdf_review", "listing_parity")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def fixture(root):
    root.mkdir()
    bodies = {"stage-receipt.json": b'{"release":"HOLD","type":"SYNTHETIC"}',
              "ebook.epub": b"FAKE_EPUB_NOT_A_REAL_BOOK",
              "ebook.pdf": b"%PDF-SYNTHETIC-NOT-VALID"}
    bodies.update({k + ".json": b'{"status":"DRAFT","synthetic":true}'
                   for k in EVIDENCE})
    for name, raw in bodies.items():
        (root / name).write_bytes(raw)
    return {
        "schema": "F-001-PACKAGE-EVIDENCE-v1", "project": "F-001",
        "release": "HOLD", "authorization": "NOT_GRANTED",
        "book_id": "urn:uuid:00000000-0000-4000-8000-000000000001",
        "stage": {"receipt_sha256": sha(bodies["stage-receipt.json"]),
                  "source_commit": SOURCE, "release": "HOLD",
                  "receipt_type": "STAGING_ONLY", "csv_sha256": CSV},
        "artifacts": {k: {"sha256": sha(bodies["ebook." + k]),
                          "bytes": len(bodies["ebook." + k])}
                      for k in ("epub", "pdf")},
        "evidence": {k: sha(bodies[k + ".json"]) for k in EVIDENCE},
    }


def write_manifest(root, obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    (root / "manifest.json").write_bytes(raw)
    return sha(raw)


def evaluate(label, kind=None, edit=None, accept=False):
    with tempfile.TemporaryDirectory(prefix="f001-run356-") as temp:
        root = Path(temp) / "bundle"
        obj = fixture(root)
        if kind == "manifest":
            edit(obj)
        pin = write_manifest(root, obj)
        if kind == "file":
            edit(root)
        if kind == "pin":
            pin = "0" * 64
        if kind == "raw":
            raw = edit((root / "manifest.json").read_bytes())
            (root / "manifest.json").write_bytes(raw)
            pin = sha(raw)
        if kind == "circular":
            raw = b"CHANGED_FAKE_EPUB_SELF_SIGNED"
            (root / "ebook.epub").write_bytes(raw)
            obj["artifacts"]["epub"] = {"sha256": sha(raw), "bytes": len(raw)}
            pin = write_manifest(root, obj)
        result = subprocess.run([sys.executable, "-I", "-B", str(RUNNER),
                                 str(root), pin], capture_output=True,
                                text=True, timeout=20)
        receipt = json.loads(result.stdout)
        hold = (receipt.get("release") == "HOLD" and
                receipt.get("publication_authorized") is False)
        good = (result.returncode == 0 and hold and
                receipt.get("result") == "CLOSED_BYTE_CONSISTENT_ONLY")
        bad = (result.returncode == 1 and hold and
               receipt.get("result") == "REJECTED")
        return {"case": label, "pass": good if accept else bad,
                "exit": result.returncode, "result": receipt.get("result"),
                "reason": receipt.get("reason")}


def main():
    cases = [
        ("synthetic positive", None, None, True),
        ("wrong pin", "pin", None, False),
        ("mutated EPUB", "file", lambda r: (r / "ebook.epub").write_bytes(b"tampered"), False),
        ("extra hidden", "file", lambda r: (r / ".unexpected").write_text("x"), False),
        ("symlink PDF", "file", lambda r: ((r / "ebook.pdf").unlink(),
                                       (r / "ebook.pdf").symlink_to("ebook.epub")), False),
        ("hardlink evidence", "file", lambda r: ((r / "rights.json").unlink(),
                                              os.link(r / "editorial.json", r / "rights.json")), False),
        ("missing evidence", "file", lambda r: (r / "ace.json").unlink(), False),
        ("READY manifest", "manifest", lambda m: m.update(release="READY"), False),
        ("wrong source", "manifest", lambda m: m["stage"].update(source_commit="0"*40), False),
        ("corrupt evidence", "file", lambda r: (r / "rights.json").write_bytes(b"tampered"), False),
        ("duplicate key with stale pin", "file",
         lambda r: (r / "manifest.json").write_bytes(
             (r / "manifest.json").read_bytes().replace(
                 b'"project":"F-001"', b'"project":"F-001","project":"F-001"')), False),
        ("duplicate key with fresh pin", "raw",
         lambda b: b.replace(b'"project":"F-001"', b'"project":"F-001","project":"F-001"'), False),
        ("oversized manifest", "file",
         lambda r: (r / "manifest.json").write_bytes((r / "manifest.json").read_bytes()+b" "*65536), False),
        ("self-selected pin circularity", "circular", None, True),
    ]
    rows = [evaluate(*row) for row in cases]
    print(json.dumps({"project": "F-001", "run": 356,
                      "synthetic_only": True, "release": "HOLD",
                      "passed": sum(row["pass"] for row in rows),
                      "total": len(rows), "cases": rows}, sort_keys=True))
    return 0 if all(row["pass"] for row in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
