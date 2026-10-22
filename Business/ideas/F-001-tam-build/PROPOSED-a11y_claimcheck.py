#!/usr/bin/env python3
"""F-001 §92 (PROPOSED, read-only): do the EPUB's schema:accessibilityFeature claims
match its content?  Contract 000 §24-§25; not wired into build.py.

Ace and PROPOSED-a11y_dupcheck.py check form. This checks a few claims against the
built XHTML, so the editor sees which claims are supported, vacuous (nothing to
apply them to) or unsupported, before any listing (§89.3.3).

  alternativeText       images (<img>, <svg>, <image>) in content documents:
                        0 -> vacuous; any <img> without alt -> unsupported
  tableOfContents       nav document has a toc nav with >= 1 link -> supported
  structuralNavigation  >= 1 <h1>-<h6> in content documents -> supported
  anything else         editor (not machine-checkable here, e.g. readingOrder)

Also reports accessMode vs images (a 'visual' mode with 0 images, or images with
no 'visual' mode, is flagged for the editor) and the table count (information).
It opens the EPUB read-only and writes nothing. Prints one JSON line; exit 1 only
when a claim is unsupported.

Usage: python3 -I claimcheck.py <book.epub>
"""
import json, re, sys, zipfile
import xml.etree.ElementTree as ET

OPF_NS = "{http://www.idpf.org/2007/opf}"
X = "{http://www.w3.org/1999/xhtml}"
EPUB_TYPE = "{http://www.idpf.org/2007/ops}type"


def main(path):
    z = zipfile.ZipFile(path)
    container = ET.fromstring(z.read("META-INF/container.xml"))
    opf_path = next(e.get("full-path") for e in container.iter() if e.get("full-path"))
    base = opf_path.rsplit("/", 1)[0] + "/" if "/" in opf_path else ""
    opf = ET.fromstring(z.read(opf_path))
    meta = {}
    for m in opf.iter(OPF_NS + "meta"):
        p = m.get("property") or ""
        if p.startswith("schema:"):
            meta.setdefault(p[7:], []).append((m.text or "").strip())
    items = {i.get("id"): i for i in opf.iter(OPF_NS + "item")}
    spine = [items[r.get("idref")].get("href") for r in opf.iter(OPF_NS + "itemref")]
    nav_href = next((i.get("href") for i in items.values() if "nav" in (i.get("properties") or "").split()), None)

    imgs = imgs_no_alt = svgs = headings = tables = 0
    for href in spine:
        doc = ET.fromstring(z.read(base + href))
        for e in doc.iter():
            tag = e.tag
            if tag == X + "img":
                imgs += 1
                imgs_no_alt += e.get("alt") is None
            elif tag in ("{http://www.w3.org/2000/svg}svg", "{http://www.w3.org/2000/svg}image"):
                svgs += 1
            elif re.fullmatch(re.escape(X) + r"h[1-6]", tag):
                headings += 1
            elif tag == X + "table":
                tables += 1
    toc_links = 0
    if nav_href:
        nav = ET.fromstring(z.read(base + nav_href))
        for n in nav.iter(X + "nav"):
            if "toc" in (n.get(EPUB_TYPE) or "").split():
                toc_links += sum(1 for _ in n.iter(X + "a"))

    images = imgs + svgs
    claims = {}
    for f in meta.get("accessibilityFeature", []):
        if f == "alternativeText":
            claims[f] = "vacuous" if images == 0 else ("unsupported" if imgs_no_alt else "supported")
        elif f == "tableOfContents":
            claims[f] = "supported" if toc_links else "unsupported"
        elif f == "structuralNavigation":
            claims[f] = "supported" if headings else "unsupported"
        else:
            claims[f] = "editor"
    modes = meta.get("accessMode", [])
    mode_notes = []
    if images and "visual" not in modes and modes:
        mode_notes.append("images present but accessMode lacks visual")
    if not images and "visual" in modes:
        mode_notes.append("accessMode visual with 0 images")
    out = {
        "epub": path.rsplit("/", 1)[-1],
        "content": {"spine_docs": len(spine), "images": images, "img_without_alt": imgs_no_alt,
                    "headings": headings, "tables": tables, "toc_links": toc_links},
        "accessMode": modes,
        "claims": claims,
        "accessMode_notes": mode_notes,
        "needs_editor": sorted(k for k, v in claims.items() if v in ("vacuous", "editor")) + mode_notes,
        "ok": not any(v == "unsupported" for v in claims.values()),
    }
    print(json.dumps(out, sort_keys=True))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
