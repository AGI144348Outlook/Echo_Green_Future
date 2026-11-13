#!/usr/bin/env python3
"""F-001 read-only release evidence verifier (draft, not release certification).

Usage: python f001_verify.py ROOT manifest.json
No dependencies, network, writes, publication or external effects.
Manifest schema:
{"artifacts":[{"path":"book.pdf","sha256":"64 hex chars","type":"pdf","pages":12},
              {"path":"book.epub","sha256":"64 hex chars","type":"epub"}],
 "evidence":{"rights":"receipts/rights.txt","editorial":"receipts/editorial.txt",
             "accessibility":"receipts/accessibility.txt","android_qa":"receipts/android.txt",
             "approval":"receipts/approval.txt"}}
Evidence presence is NOT authentication of authority. Manual review remains required.
"""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

REQUIRED = ("rights", "editorial", "accessibility", "android_qa", "approval")
HEX = re.compile(r"^[0-9a-f]{64}$")
PDF_PAGE = re.compile(rb"/Type\s*/Page\b")
def inside(root, rel):
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or "\\" in rel:
        raise ValueError("unsafe path")
    p = (root / rel).resolve(strict=True)
    if not p.is_relative_to(root) or not p.is_file():
        raise ValueError("outside release root or not file")
    return p

def inspect_pdf(path, expected):
    # Deliberately fail closed: stdlib cannot independently certify PDF page count.
    data = path.read_bytes()
    if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-2048:]:
        raise ValueError("invalid PDF envelope")
    if not isinstance(expected, int) or expected <= 0:
        raise ValueError("missing positive expected PDF pages")
    raise ValueError("PDF requires independent parser; not certified by regex")

def inspect_epub(path):
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        if z.testzip() is not None:
            raise ValueError("corrupt EPUB member")
        if "mimetype" not in names or z.read("mimetype") != b"application/epub+zip":
            raise ValueError("bad EPUB mimetype")
        if z.infolist()[0].filename != "mimetype" or z.infolist()[0].compress_type != zipfile.ZIP_STORED:
            raise ValueError("EPUB mimetype must be first and uncompressed")
        if "META-INF/container.xml" not in names:
            raise ValueError("missing EPUB container")
        c = ET.fromstring(z.read("META-INF/container.xml"))
        paths = [e.attrib.get("full-path") for e in c.iter() if e.tag.endswith("rootfile")]
        if len(paths) != 1 or paths[0] not in names:
            raise ValueError("invalid OPF reference")
        opf = ET.fromstring(z.read(paths[0]))
        manifest = [e for e in opf.iter() if e.tag.endswith("item")]
        spine = [e for e in opf.iter() if e.tag.endswith("itemref")]
        ids = {e.attrib.get("id") for e in manifest}
        if not manifest or not spine or any(e.attrib.get("idref") not in ids for e in spine):
            raise ValueError("invalid EPUB manifest/spine")
        if any(".." in Path(n).parts or n.startswith("/") for n in names):
            raise ValueError("unsafe EPUB archive member")
    return "EPUB basic structure passed; not accessibility certification"

def verify(root, manifest):
    root = Path(root).resolve(strict=True)
    doc = json.loads(Path(manifest).read_text(encoding="utf-8"))
    artifacts = doc.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("no artifacts")
    kinds = set()
    results = []
    for item in artifacts:
        p = inside(root, item["path"])
        sha = item["sha256"]
        if not isinstance(sha, str) or not HEX.fullmatch(sha):
            raise ValueError("bad SHA-256 receipt")
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != sha:
            raise ValueError("SHA-256 mismatch: " + item["path"])
        kind = item["type"]
        if kind == "pdf":
            inspect_pdf(p, item.get("pages"))
        elif kind == "epub":
            inspect_epub(p)
        else:
            raise ValueError("unsupported artifact type")
        kinds.add(kind)
        results.append({"path": item["path"], "sha256": actual, "type": kind})
    if kinds != {"pdf", "epub"}:
        raise ValueError("PDF and EPUB both required")
    evidence = doc.get("evidence", {})
    for name in REQUIRED:
        if name not in evidence or not inside(root, evidence[name]).stat().st_size:
            raise ValueError("missing evidence: " + name)
    # No machine-readable approval is sufficient to authorize publication.
    return {"status": "HOLD_MANUAL_AUTHENTICATION_REQUIRED", "artifacts": results}

if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            raise ValueError("usage: f001_verify.py ROOT manifest.json")
        print(json.dumps(verify(sys.argv[1], sys.argv[2]), indent=2))
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(json.dumps({"status": "REJECT", "reason": str(exc)}))
        sys.exit(1)
