#!/usr/bin/env python3
"""F-001 HOLD-only, read-only duplicate sentence context comparator.
PRE-TEST: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/60
Requires exact local pinned TAM source bytes; never downloads or writes to source.
This is not claim-scanner replay, editorial approval, or a release gate.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PINS = {
    "Article 6": "662d745f0b9b41236d1053cdbaa9351f7c020dd0",
    "Article 10": "e82be564872f636662652d34dcb8d3437559f84f",
    "Collective information": "710ad3cd4feeae7bafa329d7437a78df4c40cfa8",
}
PAIRS = [
    ("Article 6", 4, "Collective information", 153),
    ("Article 6", 23, "Collective information", 172),
    ("Article 6", 29, "Collective information", 178),
    ("Article 10", 3, "Collective information", 293),
    ("Article 10", 4, "Collective information", 294),
    ("Article 10", 5, "Collective information", 295),
    ("Article 10", 8, "Collective information", 298),
]


def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def sentences(text):
    """Exact Python sentence splitter from shared F-001 claim_scan.py blob 31f3dcff."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]


def normalize_neighbor(s):
    """For context comparison ONLY; do not normalize source or claim text."""
    return " ".join(re.sub("[\u200b-\u200d\ufeff]", "", s).split())


def compare_pair(a, ai, b, bi):
    if not isinstance(ai, int) or not isinstance(bi, int) or not 1 <= ai <= len(a) or not 1 <= bi <= len(b):
        raise ValueError("invalid sentence index")
    left, right = a[ai-1], b[bi-1]
    if left != right:
        raise ValueError("duplicate source sentences differ")
    pa, pb = a[ai-2] if ai > 1 else "", b[bi-2] if bi > 1 else ""
    na, nb = a[ai] if ai < len(a) else "", b[bi] if bi < len(b) else ""
    return {
        "same_sentence": True,
        "raw_previous_equal": pa == pb,
        "raw_next_equal": na == nb,
        "normalized_previous_equal": normalize_neighbor(pa) == normalize_neighbor(pb),
        "normalized_next_equal": normalize_neighbor(na) == normalize_neighbor(nb),
        "left_has_next": ai < len(a),
        "right_has_next": bi < len(b),
    }


def compare_sources(root, pins=PINS, pairs=PAIRS):
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("missing/linked source directory")
    source = {}
    for name, expected in pins.items():
        if name in ("", ".", "..") or "/" in name or "\\" in name:
            raise ValueError("unsafe source path")
        p = root / name
        if p.is_symlink() or not p.is_file():
            raise ValueError("missing/linked source: " + name)
        raw = p.read_bytes()
        if git_blob_sha(raw) != expected:
            raise ValueError("source blob mismatch: " + name)
        source[name] = sentences(raw.decode("utf-8", "replace"))
    out = []
    for a, ai, b, bi in pairs:
        if a not in source or b not in source:
            raise ValueError("unpinned pair source")
        out.append({"left": f"{a}#S{ai}", "right": f"{b}#S{bi}", **compare_pair(source[a], ai, source[b], bi)})
    return {"project": "F-001", "status": "HOLD", "release_authorized": False,
            "source_pins": pins, "pair_count": len(out), "pairs": out}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 -I -B f001_duplicate_context_387.py <pinned-tam-source-dir>")
    try:
        print(json.dumps(compare_sources(sys.argv[1]), indent=2))
    except (ValueError, OSError) as exc:
        sys.exit("HOLD / source verification failed: " + str(exc))
