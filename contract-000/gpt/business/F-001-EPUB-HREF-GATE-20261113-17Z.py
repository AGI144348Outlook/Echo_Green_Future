#!/usr/bin/env python3
"""F-001 EPUB manifest containment gate, standalone DRAFT; no release certification.

Checks OPF href paths against ZIP members. Does not authenticate rights or certify
accessibility. No filesystem writes, network access, or dependency installation.
"""
from pathlib import PurePosixPath
from urllib.parse import unquote, urlsplit

def validate_opf_references(opf_name, manifest_items, archive_names):
    """Return canonical archive paths or raise ValueError (fail closed).

    manifest_items is an iterable of OPF <item> attribute dictionaries.
    All OPF referenced local resources must be present; remote, fragment-only,
    traversal, encoded traversal, absolute, query-bearing, duplicate and
    ambiguous paths are rejected.
    """
    names = list(archive_names)
    if len(names) != len(set(names)):
        raise ValueError("duplicate archive member")
    if any(not n or n.startswith("/") or "\\" in n or
           any(part in (".", "..", "") for part in n.split("/")) for n in names):
        raise ValueError("unsafe archive member")
    if opf_name not in names:
        raise ValueError("missing OPF")
    parent = PurePosixPath(opf_name).parent
    resolved = {}
    seen_ids = set()
    for item in manifest_items:
        identifier, href = item.get("id"), item.get("href")
        if not identifier or identifier in seen_ids or not href:
            raise ValueError("missing/duplicate manifest id or href")
        seen_ids.add(identifier)
        if any(ch in href for ch in ("\\", "\x00")):
            raise ValueError("unsafe href")
        parts = urlsplit(href)
        if parts.scheme or parts.netloc or parts.query or not parts.path:
            raise ValueError("external/ambiguous href")
        decoded = unquote(parts.path)
        if "%" in decoded or decoded.startswith("/") or "\\" in decoded:
            raise ValueError("absolute or double-encoded href")
        components = decoded.split("/")
        if any(c in ("", ".", "..") for c in components):
            raise ValueError("unsafe path component")
        target = str(parent.joinpath(*components))
        if target not in names:
            raise ValueError("missing manifest resource: " + target)
        resolved[identifier] = target
    if not resolved:
        raise ValueError("empty manifest")
    return resolved
