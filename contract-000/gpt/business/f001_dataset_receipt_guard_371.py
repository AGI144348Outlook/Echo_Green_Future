#!/usr/bin/env python3
"""F-001 HOLD-only verifier for exact, publicly pinned TAM dataset rebuild outputs.

This is a supplemental byte/shape gate, not an editorial, rights, or publication
approval. It checks one known builder and two known public source inputs.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

SOURCE = {
    "Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)": "48437f58ee74a9a0226d901d1291b6c104764648fe7760ebbc91b74b6ba6a302",
    "Dataset_B_Binary_Matrix.md": "bc16da657b19317e110cdcf4159a9118aa89f2cfc4f8183e7e3f1d94f2eb3b81",
}
OUTPUT = {
    "dataset-a.csv": ("d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2", 6),
    "dataset-b.csv": ("fecd151b5b7393fc69975a0b323e02c5f306eb1fd49bedc2901f849001e8afc5", 8),
    "dataset-check.json": ("036a85e5fe3b372c6ada0e0851f3463fd6da3e5d6ab825972cb454085f85dde4", None),
}


class HoldGateError(ValueError):
    pass


def _read(root, name):
    p = root / name
    if p.is_symlink() or not p.is_file():
        raise HoldGateError(f"missing, symlinked or nonregular file: {name}")
    if p.stat().st_size > 1_000_000:
        raise HoldGateError(f"oversized file: {name}")
    return p.read_bytes()


def _pairs(items):
    obj = {}
    for k, v in items:
        if k in obj:
            raise HoldGateError("duplicate JSON key")
        obj[k] = v
    return obj


def _bad_constant(value):
    raise HoldGateError(f"nonfinite JSON value: {value}")


def verify(source_dir, output_dir):
    src, out = Path(source_dir), Path(output_dir)
    if src.is_symlink() or out.is_symlink() or not src.is_dir() or not out.is_dir():
        raise HoldGateError("source/output directory missing or symlinked")
    source_bytes = {}
    for name, expected in SOURCE.items():
        b = _read(src, name)
        if hashlib.sha256(b).hexdigest() != expected:
            raise HoldGateError(f"source SHA-256 mismatch: {name}")
        source_bytes[name] = b
    output_bytes = {}
    for name, (expected, _) in OUTPUT.items():
        b = _read(out, name)
        if hashlib.sha256(b).hexdigest() != expected:
            raise HoldGateError(f"output SHA-256 mismatch: {name}")
        output_bytes[name] = b
    try:
        report = json.loads(output_bytes["dataset-check.json"].decode("utf-8"),
                            object_pairs_hook=_pairs, parse_constant=_bad_constant)
    except (UnicodeError, ValueError) as e:
        raise HoldGateError(f"invalid report: {e}") from e
    if report.get("base_g_per_unit") != 13.7 or set(report.get("files", {})) != {"A", "B"}:
        raise HoldGateError("unexpected report structure")
    for key, name, n in [("A", list(SOURCE)[0], 6), ("B", list(SOURCE)[1], 8)]:
        entry = report["files"][key]
        if entry.get("rows") != n or entry.get("rejected") != [] or entry.get("sha256") != hashlib.sha256(source_bytes[name]).hexdigest():
            raise HoldGateError(f"incomplete source acceptance: {key}")
    for name, (_, n) in OUTPUT.items():
        if n is None:
            continue
        try:
            csv_rows = list(csv.reader(io.StringIO(output_bytes[name].decode("utf-8")), strict=True))
        except (UnicodeError, csv.Error) as e:
            raise HoldGateError(f"invalid CSV {name}: {e}") from e
        if len(csv_rows) != n + 1 or len(set(map(len, csv_rows))) != 1:
            raise HoldGateError(f"unexpected CSV row count/width: {name}")
    return {"status": "VERIFIED_FOR_REVIEW", "release_authorized": False,
            "source_sha256": {k: hashlib.sha256(v).hexdigest() for k, v in source_bytes.items()},
            "output_sha256": {k: hashlib.sha256(v).hexdigest() for k, v in output_bytes.items()},
            "rows": {"A": 6, "B": 8},
            "editorial_flags": ["Dataset A Silver Droplet deviation", "Dataset A Small Scrap deviation", "Gerah label conflict"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source_dir")
    ap.add_argument("output_dir")
    args = ap.parse_args()
    try:
        print(json.dumps(verify(args.source_dir, args.output_dir), indent=2, sort_keys=True))
    except (HoldGateError, OSError, KeyError, TypeError) as e:
        ap.exit(2, f"HOLD: {e}\n")


if __name__ == "__main__":
    main()
