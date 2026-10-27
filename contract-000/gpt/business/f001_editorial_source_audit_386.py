#!/usr/bin/env python3
"""F-001 HOLD-only, offline source-anchored editorial preview audit.
Usage: python3 -I -B f001_editorial_source_audit_386.py QUEUE.json PINNED_SOURCE_DIR
Never changes input, never publishes, and never approves editorial claims.
"""
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]


def normalize(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


def audit(queue, root):
    root = Path(root)
    errors, files, rows, seen = [], {}, [], set()
    if queue.get("project") != "F-001" or queue.get("status") != "HOLD" or queue.get("release_authorized") is not False:
        errors.append("queue must remain F-001 HOLD with release_authorized=false")
    cards = queue.get("cards", [])
    if not isinstance(cards, list):
        cards = []
        errors.append("cards must be a list")
    for c in cards:
        ident, name = c.get("id"), c.get("source_file")
        if not isinstance(ident, str) or ident in seen:
            errors.append(f"duplicate or malformed card ID: {ident}")
            continue
        seen.add(ident)
        if not isinstance(name, str) or Path(name).name != name or name in ("", ".", ".."):
            errors.append(f"unsafe source name for {ident}")
            continue
        if c.get("review_status") != "UNREVIEWED":
            errors.append(f"editorial status changed: {ident}")
        if name not in files:
            p = root / name
            if p.is_symlink() or not p.is_file():
                files[name] = (None, None)
                errors.append(f"missing/symlink source: {name}")
            else:
                raw = p.read_bytes()
                try:
                    files[name] = (git_blob(raw), sentences(raw.decode("utf-8")))
                except UnicodeDecodeError:
                    files[name] = (None, None)
                    errors.append(f"invalid UTF-8: {name}")
        sha, sents = files[name]
        if sha != c.get("source_blob_sha"):
            errors.append(f"source blob mismatch: {ident}")
            continue
        n = c.get("sentence_no")
        if not isinstance(n, int) or isinstance(n, bool) or n < 1 or n > len(sents):
            errors.append(f"sentence number invalid: {ident}")
            continue
        full = sents[n - 1]
        excerpt = c.get("excerpt")
        if not isinstance(excerpt, str) or not full.startswith(excerpt):
            errors.append(f"excerpt is not source prefix: {ident}")
            continue
        rows.append({"id": ident, "source_file": name, "source_blob_sha": sha,
                     "sentence_no": n, "excerpt_is_truncated": len(full) > len(excerpt),
                     "excerpt_chars": len(excerpt), "full_sentence_chars": len(full),
                     "full_sentence_sha256": hashlib.sha256(full.encode()).hexdigest(),
                     "normalized_full_sha256": hashlib.sha256(normalize(full).encode()).hexdigest(),
                     "review_status": "UNREVIEWED"})
    if queue.get("card_count") != len(cards) or queue.get("unreviewed_count") != len(cards):
        errors.append("queue card count/unreviewed count mismatch")
    groups = defaultdict(list)
    for row in rows:
        groups[row["normalized_full_sha256"]].append(row["id"])
    duplicate_groups = [ids for ids in groups.values() if len(ids) > 1]
    return {"project": "F-001", "status": "HOLD", "release_authorized": False,
            "source_files": len(files), "cards_seen": len(cards), "cards_verified": len(rows),
            "exact_full_sentence_cards": sum(not x["excerpt_is_truncated"] for x in rows),
            "truncated_preview_cards": sum(x["excerpt_is_truncated"] for x in rows),
            "unique_full_sentences": len(groups), "duplicate_groups": duplicate_groups,
            "errors": errors, "verified": not errors and len(rows) == len(cards), "rows": rows}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    result = audit(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")), sys.argv[2])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["verified"] else 2)
