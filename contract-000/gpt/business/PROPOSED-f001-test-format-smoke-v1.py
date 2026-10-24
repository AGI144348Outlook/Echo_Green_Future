#!/usr/bin/env python3
"""Run 317 preregistered F0-F9 synthetic tests; Issue #36 is pre-test record.

No real book, external network, CI, paid inference or release authority.
"""
import hashlib
import importlib.util
import io
import json
import re
from pathlib import Path
import tempfile
import zipfile

GATE = Path(__file__).with_name("PROPOSED-f001-format-smoke-gate-v1.py")
spec = importlib.util.spec_from_file_location("f001_format_smoke_v1", GATE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

MIMETYPE = b"application/epub+zip"
CONTAINER = b"""<?xml version="1.0"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
<rootfiles><rootfile full-path="OPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""
OPF = b"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Test book</dc:title></metadata>
<manifest><item id="c" href="chapter.xhtml" media-type="application/xhtml+xml"/></manifest>
<spine><itemref idref="c"/></spine>
</package>"""
XHTML = b"""<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Test</title></head>
<body><p>A test page.</p></body></html>"""


def epub_bytes(case="control"):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr("mimetype", MIMETYPE,
                   compress_type=zipfile.ZIP_DEFLATED if case == "compressed-mimetype" else zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   CONTAINER.replace(b"OPS/package.opf", b"OPS/missing.opf")
                   if case == "missing-opf" else CONTAINER)
        z.writestr("OPS/package.opf",
                   OPF.replace(b'idref="c"', b'idref="absent"')
                   if case == "bad-spine" else OPF)
        z.writestr("OPS/chapter.xhtml", XHTML)
        if case == "traversal":
            z.writestr("../escape.txt", "not extracted")
        if case == "duplicate":
            z.writestr("OPS/chapter.xhtml", XHTML)
    return b.getvalue()


def pdf_bytes():
    b = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>",
        b"<< /Length 0 >>\nstream\n\nendstream",
    ]
    for n, obj in enumerate(objs, 1):
        offsets.append(len(b))
        b.extend(f"{n} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(b)
    b.extend(f"xref\n0 {len(offsets)}\n".encode())
    b.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        b.extend(f"{offset:010d} 00000 n \n".encode())
    b.extend(f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n".encode())
    b.extend(f"startxref\n{xref}\n%%EOF\n".encode())
    return bytes(b)


def run():
    cases = [
        ("F0", "control", True),
        ("F1", "text-epub", False),
        ("F2", "text-pdf", False),
        ("F3", "compressed-mimetype", False),
        ("F4", "traversal", False),
        ("F5", "duplicate", False),
        ("F6", "missing-opf", False),
        ("F7", "bad-spine", False),
        ("F8", "bad-xref", False),
        ("F9", "expanded-budget", False),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="f001-smoke-317-") as d:
        epub = Path(d) / "book.epub"
        pdf = Path(d) / "book.pdf"
        for label, mode, expected_pass in cases:
            eb = b"not a zip" if mode == "text-epub" else epub_bytes(mode)
            pb = b"not a PDF" if mode == "text-pdf" else pdf_bytes()
            if mode == "bad-xref":
                pb = re.sub(rb"(?<=startxref\\n)\\d+(?=\\n%%EOF)", b"999999", pb)
            epub.write_bytes(eb)
            pdf.write_bytes(pb)
            before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (epub, pdf)]
            old_limit = mod.MAX_EPUB_UNCOMPRESSED
            try:
                if mode == "expanded-budget":
                    # Lower only the test's limit; does not exercise a 64 MiB file.
                    mod.MAX_EPUB_UNCOMPRESSED = 100
                result = mod.check_package(epub, pdf)
            finally:
                mod.MAX_EPUB_UNCOMPRESSED = old_limit
            after = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (epub, pdf)]
            observed_pass = result["smoke"] == "PASS"
            ok = (observed_pass == expected_pass
                  and result["release"] == "HOLD"
                  and result["readiness"] == "BLOCKED"
                  and result["publication_authorization"] == "ABSENT"
                  and result["full_conformance_verified"] is False
                  and before == after)
            results.append({"case": label, "mode": mode, "expected": "PASS" if expected_pass else "FAIL",
                            "observed": result["smoke"], "ok": ok, "issues": result["issues"],
                            "input_unchanged": before == after})
    summary = {"schema": "f001-smoke-test/v1", "planned": len(cases),
               "passed": sum(x["ok"] for x in results), "cases": results}
    print(json.dumps(summary, sort_keys=True, indent=2))
    if summary["passed"] != len(cases):
        raise SystemExit(1)


if __name__ == "__main__":
    run()
