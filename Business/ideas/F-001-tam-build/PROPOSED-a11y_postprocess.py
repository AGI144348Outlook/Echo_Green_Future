#!/usr/bin/env python3
"""F-001 §89 (PROPOSED; Contract 000 §24-§26, §86-§88). Not wired into build.py.

Exact, standalone form of the post-process §87.2 described in prose and §88.3
proposed, so that any receipt hash made with it can be re-checked from the record.

  python3 -I -B PROPOSED-a11y_postprocess.py <in.epub> <out.epub>

Copies every zip member in its original order, reusing each member's own
ZipInfo (same name, date_time, compress_type, create_system, create_version),
as build.py's F001_A11Y step does with dst.writestr(info, data). Two guarded edits:
  1. content OPF: add xml:lang (value from dc:language) to <package> only if absent
  2. nav.xhtml: add role="doc-toc" to <nav epub:type="toc"> only if no role is present
If neither applies (e.g. a pandoc 3.9 build), the output is byte-identical to the input.
Prints a JSON line saying which edits applied. Never edits the input file.
"""
import json, re, sys, zipfile


def main(src, dst):
    applied = {"package_xml_lang": False, "toc_nav_role": False}
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename.endswith(".opf"):
                t = data.decode("utf-8")
                m = re.search(r"<package\b[^>]*>", t)
                lang = re.search(r"<dc:language>([^<]+)</dc:language>", t)
                if m and lang and not re.search(r"\bxml:lang=", m.group(0)):
                    t = t[:m.start()] + m.group(0).replace("<package", '<package xml:lang="%s"' % lang.group(1).strip(), 1) + t[m.end():]
                    data = t.encode("utf-8")
                    applied["package_xml_lang"] = True
            elif info.filename.endswith("nav.xhtml"):
                t = data.decode("utf-8")
                t2 = re.sub(r'<nav epub:type="toc"(?![^>]*\brole=)', '<nav epub:type="toc" role="doc-toc"', t, count=1)
                if t2 != t:
                    data = t2.encode("utf-8")
                    applied["toc_nav_role"] = True
            zout.writestr(info, data)
    print(json.dumps(applied, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] == sys.argv[2]:
        sys.exit("usage: PROPOSED-a11y_postprocess.py <in.epub> <out.epub> (different paths)")
    main(sys.argv[1], sys.argv[2])
