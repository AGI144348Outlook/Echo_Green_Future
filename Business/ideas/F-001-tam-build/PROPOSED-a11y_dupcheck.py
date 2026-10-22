#!/usr/bin/env python3
"""F-001 §91 (PROPOSED; Contract 000 §24-§26, §89.3, §90.4). Not wired into build.py.

Read-only duplicate check for accessibility metadata in a built EPUB, so the
§89.3 case (pandoc 3.9 writes its own schema:* lines and F001_A11Y repeats one)
is caught by the build record, not only by Ace.

  python3 -I -B PROPOSED-a11y_dupcheck.py <book.epub> [<F001_A11Y file>]

Prints one JSON object (sorted keys):
  schema_props         {property: count} over every <meta property="schema:..."> in the OPF
  duplicates           properties whose (property, value) pair occurs more than once
  repeated_properties  properties occurring more than once at all (accessibilityFeature
                       legitimately repeats with different values, so this is information only)
  a11y_file_props      properties in the F001_A11Y file (only if given)
  already_written      a11y_file_props also present in the OPF more often than the file
                       holds them, i.e. written by pandoc as well (only if given)
  ok                   true when duplicates and already_written are both empty
Exit status 0 always (reporting only). Never edits either file.
"""
import json, re, sys, zipfile
from collections import Counter

META = re.compile(r'<meta\s+property="(schema:[A-Za-z]+)"[^>]*>([^<]*)</meta>')


def pairs(text):
    return [(p, v.strip()) for p, v in META.findall(text)]


def main(epub, a11y=None):
    with zipfile.ZipFile(epub) as z:
        opf = [n for n in z.namelist() if n.endswith(".opf")]
        text = z.read(opf[0]).decode("utf-8") if opf else ""
    got = pairs(text)
    props = Counter(p for p, _ in got)
    out = {
        "schema_props": dict(sorted(props.items())),
        "duplicates": sorted({pv[0] for pv, n in Counter(got).items() if n > 1}),
        "repeated_properties": sorted(p for p, n in props.items() if n > 1),
    }
    bad = list(out["duplicates"])
    if a11y:
        with open(a11y, encoding="utf-8") as f:
            mine = Counter(p for p, _ in pairs(f.read()))
        out["a11y_file_props"] = sorted(mine)
        out["already_written"] = sorted(p for p in mine if props.get(p, 0) > mine[p])
        bad += out["already_written"]
    out["ok"] = not bad
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    main(*sys.argv[1:])
