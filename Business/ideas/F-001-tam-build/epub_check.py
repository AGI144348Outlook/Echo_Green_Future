#!/usr/bin/env python3
"""F-001 candidate A, TAM shape: offline EPUB structure check (PROPOSED; Contract 000 §24-§25).

Checks the EPUB that build.py writes (<out-dir>/tam-draft.epub) for the
structural faults that make stores or readers reject a file, using only the
Python standard library (no epubcheck, no network):
  - `mimetype` is the first zip entry, stored uncompressed, text application/epub+zip
  - META-INF/container.xml exists and points at an OPF that exists
  - the OPF has dc:title, dc:language and dc:identifier, and the title is not a placeholder
  - every manifest item and every spine itemref resolves to a file in the zip
  - an EPUB 3 navigation document is declared (properties="nav")
  - every XHTML / XML file parses as XML
  - no remote resources (src/href to http(s)) inside content files
Prints PASS/FAIL/WARN lines, writes <out-dir>/epub-report.json, exits 1 on any FAIL.
It never edits the EPUB, uploads, sells or contacts anything. Passing this is not
a substitute for epubcheck or the store's own validator (UNVERIFIED until run).

Usage: python3 -I epub_check.py <out-dir> [file.epub]
"""
import hashlib, json, posixpath, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"c": "urn:oasis:names:tc:opendocument:xmlns:container",
      "opf": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/"}
PLACEHOLDER = re.compile(r"^\s*$|\[.*\]|untitled|tam-draft", re.I)
REMOTE = re.compile(rb"""(?:src|href)\s*=\s*["']https?://""", re.I)


def check(epub):
    res = []  # (level, message)
    ok = lambda c, m: res.append(("PASS" if c else "FAIL", m))
    z = zipfile.ZipFile(epub)
    infos = z.infolist(); names = set(z.namelist())
    first = infos[0] if infos else None
    ok(first is not None and first.filename == "mimetype", "mimetype is the first zip entry")
    ok(first is not None and first.compress_type == zipfile.ZIP_STORED, "mimetype stored uncompressed")
    ok("mimetype" in names and z.read("mimetype") == b"application/epub+zip", "mimetype content is application/epub+zip")
    if "META-INF/container.xml" not in names:
        ok(False, "META-INF/container.xml present"); return res, {}
    root = ET.fromstring(z.read("META-INF/container.xml"))
    rf = root.find(".//c:rootfile", NS)
    opf_path = rf.get("full-path") if rf is not None else None
    ok(opf_path in names, f"container points at an existing OPF ({opf_path})")
    if opf_path not in names:
        return res, {}
    opf = ET.fromstring(z.read(opf_path)); base = posixpath.dirname(opf_path)
    meta = {}
    for tag in ("title", "language", "identifier"):
        el = opf.find(f".//dc:{tag}", NS); meta[tag] = (el.text or "").strip() if el is not None else None
        ok(bool(meta[tag]), f"OPF has dc:{tag}")
    if meta.get("title"):
        res.append(("WARN" if PLACEHOLDER.search(meta["title"]) else "PASS",
                    f"title is not a placeholder ({meta['title']!r})"))
    items = {i.get("id"): i for i in opf.findall(".//opf:manifest/opf:item", NS)}
    missing = [i.get("href") for i in items.values() if posixpath.normpath(posixpath.join(base, i.get("href"))) not in names]
    ok(not missing, f"all {len(items)} manifest items exist" + (f"; missing {missing[:5]}" if missing else ""))
    spine = [r.get("idref") for r in opf.findall(".//opf:spine/opf:itemref", NS)]
    bad = [s for s in spine if s not in items]
    ok(spine and not bad, f"spine has {len(spine)} items, all in manifest" + (f"; bad {bad[:5]}" if bad else ""))
    ok(any("nav" in (i.get("properties") or "").split() for i in items.values()), "EPUB 3 nav document declared")
    unparsed, remote = [], []
    for n in sorted(names):
        if n.endswith((".xhtml", ".html", ".xml", ".opf", ".ncx")):
            try: ET.fromstring(z.read(n))
            except ET.ParseError as e: unparsed.append(f"{n}: {e}")
        if n.endswith((".xhtml", ".html", ".css")) and REMOTE.search(z.read(n)):
            remote.append(n)
    ok(not unparsed, "all XHTML/XML parse" + (f"; {unparsed[:3]}" if unparsed else ""))
    ok(not remote, "no remote resources in content" + (f"; {remote[:5]}" if remote else ""))
    info = {"opf": opf_path, "version": opf.get("version"), "metadata": meta,
            "manifest_items": len(items), "spine_items": len(spine), "zip_entries": len(names)}
    return res, info


def main(out, epub=None):
    out = Path(out).resolve(); epub = Path(epub) if epub else out / "tam-draft.epub"
    if not epub.exists():
        sys.exit("no EPUB found: run build.py with pandoc installed first")
    try:
        res, info = check(epub)
    except zipfile.BadZipFile:
        res, info = [("FAIL", "file is a readable zip")], {}
    for lvl, m in res: print(f"{lvl}  {m}")
    data = epub.read_bytes()
    report = {"file": epub.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
              "results": [{"level": l, "check": m} for l, m in res], **info}
    (out / "epub-report.json").write_text(json.dumps(report, indent=2))
    fails = sum(1 for l, _ in res if l == "FAIL")
    print(f"{fails} FAIL, {sum(1 for l, _ in res if l == 'WARN')} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
