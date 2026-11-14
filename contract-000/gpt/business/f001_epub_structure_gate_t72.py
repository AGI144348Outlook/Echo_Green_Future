"""F-001 independent EPUB structural gate — GPT-owned draft, UNTESTED.

Pure stdlib, no file writes or network. Not a publication certificate.
Caller must separately verify rights, accessibility, PDF, and authorization.
"""
from pathlib import PurePosixPath
from zipfile import ZipFile, BadZipFile
from xml.etree import ElementTree as ET

CONTAINER_NS = "{urn:oasis:names:tc:opendocument:xmlns:container}"
OPF_NS = "{http://www.idpf.org/2007/opf}"
XML_NS = "{http://www.w3.org/XML/1998/namespace}"

class EPUBGateError(ValueError):
    pass

def safe_member(name):
    if not name or "\\" in name or name.startswith("/") or "%" in name:
        raise EPUBGateError("unsafe archive reference")
    parts = name.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise EPUBGateError("unsafe path segment")
    return name

def validate_epub(path):
    """Return minimal evidence after checking container, OPF, manifest and spine."""
    try:
        with ZipFile(path) as z:
            names = z.namelist()
            if len(names) != len(set(names)):
                raise EPUBGateError("duplicate ZIP members")
            for name in names:
                safe_member(name.rstrip("/") if name.endswith("/") else name)
            files = {n for n in names if not n.endswith("/")}
            if "mimetype" not in files or z.read("mimetype") != b"application/epub+zip":
                raise EPUBGateError("invalid EPUB mimetype")
            if "META-INF/container.xml" not in files:
                raise EPUBGateError("missing container.xml")
            container = ET.fromstring(z.read("META-INF/container.xml"))
            roots = container.findall(".//" + CONTAINER_NS + "rootfile")
            if len(roots) != 1:
                raise EPUBGateError("expected exactly one rootfile")
            opf_path = safe_member(roots[0].get("full-path", ""))
            if opf_path not in files:
                raise EPUBGateError("missing OPF")
            opf = ET.fromstring(z.read(opf_path))
            manifest = opf.find(OPF_NS + "manifest")
            spine = opf.find(OPF_NS + "spine")
            if manifest is None or spine is None:
                raise EPUBGateError("missing manifest or spine")
            base = opf_path.rpartition("/")[0]
            ids = {}
            for item in manifest.findall(OPF_NS + "item"):
                ident, href = item.get("id"), item.get("href")
                if not ident or ident in ids or not href or "#" in href or "?" in href:
                    raise EPUBGateError("ambiguous manifest item")
                rel = safe_member(href)
                full = safe_member((base + "/" if base else "") + rel)
                if full not in files:
                    raise EPUBGateError("manifest resource missing")
                ids[ident] = full
            refs = [i.get("idref") for i in spine.findall(OPF_NS + "itemref")]
            if not refs or any(ref not in ids for ref in refs):
                raise EPUBGateError("invalid spine reference")
            return {"opf": opf_path, "manifest_items": len(ids), "spine_items": len(refs), "status": "STRUCTURE_ONLY"}
    except (BadZipFile, ET.ParseError, KeyError) as exc:
        raise EPUBGateError("malformed EPUB structure") from exc
