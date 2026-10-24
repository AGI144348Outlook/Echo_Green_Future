#!/usr/bin/env python3
"""Run 320 preregistered C0-C6 tests, pretest GitHub Issue #39.

Synthetic artifacts only. This script intentionally checks a known false positive
in C6 and NEVER changes a release decision from HOLD/BLOCKED.
"""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zipfile

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "PROPOSED-f001-dual-format-preflight-v1.py"
SMOKE = ROOT / "PROPOSED-f001-format-smoke-gate-v1.py"
SUPP = ROOT / "PROPOSED-f001-format-supplement-v2.py"
BASE = ROOT / "PROPOSED-f001-test-format-smoke-v1.py"
spec = importlib.util.spec_from_file_location("f001_run317_fixture", BASE)
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)


def epub_nfc_collision():
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("mimetype", fixtures.MIMETYPE, compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", fixtures.CONTAINER)
        z.writestr("OPS/package.opf", fixtures.OPF)
        z.writestr("OPS/chapter.xhtml", fixtures.XHTML)
        z.writestr("OPS/caf\u00e9.xhtml", fixtures.XHTML)
        z.writestr("OPS/cafe\u0301.xhtml", fixtures.XHTML)
    return out.getvalue()


def spoof_pdf():
    # Text markers exist but no actual PDF indirect-object/xref table graph.
    content = (b"%PDF-1.4\n% marker spoof, not a real PDF\n"
               b"stream\n1 0 obj\n2 0 obj\n3 0 obj\n"
               b"/Type /Catalog\n/Type /Pages\n/Type /Page\n/Root 1 0 R\nendstream\n")
    pos = len(content)
    return content + b"xref\n0 1\n0000000000 65535 f \ntrailer\n<< /Root 1 0 R >>\n" + f"startxref\n{pos}\n%%EOF\n".encode()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    expected = {"C0": "PASS", "C1": "FAIL", "C2": "FAIL", "C3": "FAIL",
                "C4": "FAIL", "C5": "FAIL", "C6": "PASS"}
    observations = []
    with tempfile.TemporaryDirectory(prefix="f001-run320-") as d:
        root = Path(d)
        for label in expected:
            sub = root / label
            sub.mkdir()
            for p in (SRC, SMOKE, SUPP):
                shutil.copyfile(p, sub / p.name)
            epub = sub / "book.epub"
            pdf = sub / "book.pdf"
            epub.write_bytes(fixtures.epub_bytes("missing-opf" if label == "C1" else "control")
                             if label != "C2" else epub_nfc_collision())
            pdf.write_bytes(fixtures.pdf_bytes() if label != "C6" else spoof_pdf())
            if label == "C3":
                pdf.write_bytes(re.sub(rb"(?<=startxref\n)\d+(?=\n%%EOF)", b"999999", pdf.read_bytes()))
            if label == "C4":
                epub.rename(sub / "actual.epub")
                epub.symlink_to("actual.epub")
            if label == "C5":
                with (sub / SUPP.name).open("ab") as f:
                    f.write(b"\nprint('TAMPER_EXECUTED')\n")
            tracked = [p for p in sub.iterdir() if p.is_file() and not p.is_symlink()]
            before = {p.name: sha(p) for p in tracked}
            cp = subprocess.run([sys.executable, "-I", "-B", str(sub / SRC.name),
                                 str(epub), str(pdf)], capture_output=True, text=True,
                                timeout=25, check=False)
            try:
                result = json.loads(cp.stdout)
                parsed = True
            except Exception:
                result, parsed = {}, False
            after = {p.name: sha(p) for p in tracked}
            status = result.get("composition")
            ok = (parsed and status == expected[label] and
                  result.get("release") == "HOLD" and
                  result.get("readiness") == "BLOCKED" and
                  result.get("publication_authorization") == "ABSENT" and
                  result.get("full_conformance_verified") is False and
                  before == after and "TAMPER_EXECUTED" not in cp.stdout and
                  cp.returncode == (0 if status == "PASS" else 1))
            observations.append({"case": label, "expected": expected[label],
                                 "observed": status, "ok": ok, "exit": cp.returncode,
                                 "inputs_unchanged": before == after,
                                 "epub_sha256": before.get("book.epub", before.get("actual.epub")),
                                 "pdf_sha256": before.get("book.pdf"),
                                 "issues": result.get("issues", []),
                                 "gate_statuses": {k:v.get("status") for k,v in result.get("gate_results",{}).items()},
                                 "stderr": cp.stderr[-350:]})
    output = {"schema": "f001-dual-format-tests/v1", "pretest_issue": 39,
              "python": sys.version, "planned": len(expected),
              "passed": sum(o["ok"] for o in observations), "cases": observations}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["passed"] == len(expected) else 1


if __name__ == "__main__":
    raise SystemExit(run())
