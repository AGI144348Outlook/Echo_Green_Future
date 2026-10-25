#!/usr/bin/env python3
"""F-001 Run 354 synthetic byte-consistency probes, PRE Issue #53 comment 6401820548."""
import copy
import hashlib
import importlib.util
import json
import os
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("f001_bytes_354", HERE / "F-001-BUNDLE-BYTE-VERIFY-354.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
gate = verifier.gate

def sha(data):
    return hashlib.sha256(data).hexdigest()

def fixture(root):
    (root / "ebook.epub").write_bytes(b"SYNTHETIC-EPUB")
    (root / "ebook.pdf").write_bytes(b"SYNTHETIC-PDF")
    (root / "stage-receipt.json").write_bytes(b'{"release":"HOLD","receipt_type":"STAGING_ONLY"}')
    for name in gate.EVIDENCE:
        (root / (name + ".json")).write_bytes(b'{"status":"DRAFT","not_authorized":true}')
    h = "a" * 64
    m = {"schema":"F-001-PACKAGE-EVIDENCE-v1","project":"F-001","release":"HOLD",
         "authorization":"NOT_GRANTED","book_id":"urn:uuid:12345678-1234-4234-8234-123456789abc",
         "stage":{"receipt_sha256":sha((root/"stage-receipt.json").read_bytes()),
                  "source_commit":gate.SOURCE,"release":"HOLD","receipt_type":"STAGING_ONLY",
                  "csv_sha256":gate.CSV.copy()},
         "artifacts":{k:{"sha256":sha((root/("ebook."+k)).read_bytes()),
                         "bytes":(root/("ebook."+k)).stat().st_size} for k in ("epub","pdf")},
         "evidence":{k:sha((root/(k+".json")).read_bytes()) for k in gate.EVIDENCE}}
    return m

def put_manifest(root, m):
    raw=json.dumps(m,sort_keys=True,separators=(",",":")).encode()
    (root/"manifest.json").write_bytes(raw)
    return sha(raw)

def mutate(name, root, manifest):
    if name=="wrong_manifest_pin": return "0"*64
    if name=="mutated_epub": (root/"ebook.epub").write_bytes(b"altered")
    if name=="missing_pdf": (root/"ebook.pdf").unlink()
    if name=="symlink_epub":
        (root/"ebook.epub").unlink()
        (root/"ebook.epub").symlink_to(root/"ebook.pdf")
    if name=="missing_evidence": (root/"rights.json").unlink()
    if name=="mismatched_evidence": (root/"rights.json").write_bytes(b"tampered")
    if name=="mutated_stage": (root/"stage-receipt.json").write_bytes(b"tampered")
    if name=="oversize_pdf":
        with open(root/"ebook.pdf","r+b") as stream: stream.truncate(100_000_001)
    if name=="malformed_manifest":
        (root/"manifest.json").write_bytes(b"{")
        return sha(b"{")
    if name=="ready_manifest":
        manifest["release"]="READY"
        return put_manifest(root,manifest)
    return None

cases=["positive","wrong_manifest_pin","mutated_epub","missing_pdf","symlink_epub",
       "missing_evidence","mismatched_evidence","mutated_stage","oversize_pdf",
       "malformed_manifest","ready_manifest"]
results=[]
for name in cases:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        m=fixture(root)
        pin=put_manifest(root,m)
        replacement=mutate(name,root,m)
        if replacement is not None: pin=replacement
        try:
            result=verifier.verify(str(root),pin)
            accepted=(result["result"]=="BYTE_CONSISTENT_ONLY" and result["release"]=="HOLD"
                      and result["publication_authorized"] is False and result["files_hashed"]==11)
        except (OSError,ValueError,TypeError,UnicodeError):
            accepted=False
        results.append({"case":name,"pass":accepted==(name=="positive"),"accepted":accepted})
print(json.dumps({"project":"F-001","release":"HOLD","passed":sum(r["pass"] for r in results),
                  "total":len(results),"results":results},sort_keys=True))
raise SystemExit(0 if all(r["pass"] for r in results) else 1)
