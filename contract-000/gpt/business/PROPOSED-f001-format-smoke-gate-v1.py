#!/usr/bin/env python3
"""F-001 read-only EPUB/PDF format *smoke* gate, not a conformance validator.

Rejects obvious placeholder/corrupt containers. A PASS is NOT proof of a
readable, accessible, safe or independently authenticated ebook. Always HOLD.
Only standard-library modules; no network, build, publication or mutation.
"""
import io
import json
import os
from pathlib import PurePosixPath
import posixpath
import re
import stat
import sys
import xml.etree.ElementTree as ET
import zipfile

MAX_FILE = 64 * 1024 * 1024
MAX_EPUB_UNCOMPRESSED = 64 * 1024 * 1024
MAX_XML = 2 * 1024 * 1024
NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
NONBLOCK = getattr(os, "O_NONBLOCK", 0)
NS_CONTAINER = "{urn:oasis:names:tc:opendocument:xmlns:container}"
NS_OPF = "{http://www.idpf.org/2007/opf}"
NS_DC = "{http://purl.org/dc/elements/1.1/}"
NS_XHTML = "{http://www.w3.org/1999/xhtml}"


def bounded_file(path, limit=MAX_FILE):
    fd = os.open(path, os.O_RDONLY | NOFOLLOW | NONBLOCK)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
            raise ValueError("not bounded regular file")
        with os.fdopen(os.dup(fd), "rb") as f:
            data = f.read(limit + 1)
        after = os.fstat(fd)
        if len(data) > limit or len(data) != before.st_size:
            raise ValueError("file exceeds bound or changed size")
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
            before.st_ctime_ns) != (after.st_dev, after.st_ino, after.st_size,
                                     after.st_mtime_ns, after.st_ctime_ns):
            raise ValueError("file changed during read")
        return data
    finally:
        os.close(fd)


def safe_member(name):
    if not name or "\\" in name or "\x00" in name or name.startswith("/"):
        return False
    p = PurePosixPath(name)
    return all(x not in (".", "..") for x in name.split("/")) and not p.is_absolute()


def bounded_zip_read(z, name, limit=MAX_XML):
    info = z.getinfo(name)
    if info.file_size > limit:
        raise ValueError("XML member too large: " + name)
    with z.open(info) as f:
        data = f.read(limit + 1)
    if len(data) > limit or len(data) != info.file_size:
        raise ValueError("XML member exceeds bound: " + name)
    return data


def check_epub(data):
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
        with z:
            infos = z.infolist()
            if not infos:
                raise ValueError("empty EPUB ZIP")
            first = infos[0]
            if first.filename != "mimetype" or first.compress_type != zipfile.ZIP_STORED:
                raise ValueError("mimetype must be first and uncompressed")
            names = [i.filename for i in infos]
            if len(names) != len(set(names)):
                raise ValueError("duplicate EPUB ZIP member")
            if any(not safe_member(n) for n in names):
                raise ValueError("unsafe EPUB ZIP member path")
            if any(i.flag_bits & 1 for i in infos):
                raise ValueError("encrypted EPUB ZIP member")
            if sum(i.file_size for i in infos) > MAX_EPUB_UNCOMPRESSED:
                raise ValueError("EPUB expanded size exceeds bound")
            if bounded_zip_read(z, "mimetype", 64) != b"application/epub+zip":
                raise ValueError("wrong EPUB mimetype")
            container = ET.fromstring(bounded_zip_read(z, "META-INF/container.xml"))
            rootfiles = container.findall(".//" + NS_CONTAINER + "rootfile")
            if not rootfiles:
                raise ValueError("EPUB container lacks rootfile")
            opf_path = rootfiles[0].get("full-path")
            if not opf_path or not safe_member(opf_path) or opf_path not in names:
                raise ValueError("missing/unsafe EPUB OPF")
            if rootfiles[0].get("media-type") != "application/oebps-package+xml":
                raise ValueError("unexpected OPF media type")
            opf = ET.fromstring(bounded_zip_read(z, opf_path))
            if opf.tag != NS_OPF + "package":
                raise ValueError("invalid OPF package root")
            title = opf.find(".//" + NS_DC + "title")
            if title is None or not (title.text or "").strip():
                raise ValueError("OPF title absent")
            manifest = opf.find(NS_OPF + "manifest")
            spine = opf.find(NS_OPF + "spine")
            if manifest is None or spine is None:
                raise ValueError("missing OPF manifest/spine")
            ids = {x.get("id"): x for x in manifest.findall(NS_OPF + "item")}
            itemrefs = spine.findall(NS_OPF + "itemref")
            if not itemrefs:
                raise ValueError("empty OPF spine")
            for itemref in itemrefs:
                item = ids.get(itemref.get("idref"))
                if item is None or item.get("media-type") != "application/xhtml+xml":
                    raise ValueError("unresolved/non-XHTML spine item")
                href = item.get("href", "")
                if not href or href.startswith("/") or "#" in href or "?" in href:
                    raise ValueError("invalid XHTML href")
                target = posixpath.normpath(posixpath.join(posixpath.dirname(opf_path), href))
                if not safe_member(target) or target not in names:
                    raise ValueError("missing/unsafe spine XHTML")
                xhtml = ET.fromstring(bounded_zip_read(z, target))
                if xhtml.tag != NS_XHTML + "html":
                    raise ValueError("spine file is not XHTML")
                body = xhtml.find(NS_XHTML + "body")
                if body is None or not "".join(body.itertext()).strip():
                    raise ValueError("empty XHTML body")
            return {"ok": True, "spine_items": len(itemrefs), "title": title.text.strip()}
    except (zipfile.BadZipFile, KeyError, ET.ParseError, RuntimeError) as exc:
        raise ValueError("malformed EPUB: " + str(exc)) from exc


def check_pdf(data):
    if not re.match(rb"%PDF-[12]\.[0-9]", data[:8]):
        raise ValueError("PDF header missing")
    tail = data[-2048:]
    matches = list(re.finditer(rb"startxref\s+(\d+)\s+%%EOF\s*\Z", tail))
    if not matches:
        raise ValueError("PDF startxref/EOF missing")
    offset = int(matches[-1].group(1))
    if offset >= len(data):
        raise ValueError("PDF startxref out of range")
    obj = data[offset:offset + 256]
    if not (obj.startswith(b"xref") or
            (re.match(rb"\d+\s+\d+\s+obj\b", obj) and b"/XRef" in obj)):
        raise ValueError("PDF startxref target invalid")
    return {"ok": True, "startxref": offset}


def check_package(epub_path, pdf_path):
    issues = []
    info = {}
    for kind, path, checker in (("epub", epub_path, check_epub),
                                ("pdf", pdf_path, check_pdf)):
        try:
            info[kind] = checker(bounded_file(path))
        except (OSError, ValueError, TypeError, OverflowError) as exc:
            issues.append(kind + ": " + str(exc))
    return {"schema": "f001-format-smoke/v1",
            "smoke": "PASS" if not issues else "FAIL",
            "release": "HOLD", "readiness": "BLOCKED",
            "publication_authorization": "ABSENT",
            "full_conformance_verified": False,
            "issues": issues, "observations": info}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: format-smoke-gate-v1.py BOOK.epub BOOK.pdf")
    result = check_package(sys.argv[1], sys.argv[2])
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["smoke"] == "PASS" else 1)
