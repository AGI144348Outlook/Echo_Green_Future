#!/usr/bin/env python3
"""Run428 isolated synthetic controls for F-001 source snapshot (no real TAM)."""
import importlib.util
import json
from pathlib import Path
import tempfile

p = Path(__file__).with_name("f001_pinned_source_snapshot_428.py")
spec = importlib.util.spec_from_file_location("gate428", p)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

checks = []

def check(label, value):
    checks.append((label, bool(value)))
    assert value, label


def fixture(root):
    src = root / "src"
    src.mkdir()
    pins = {}
    for i, name in enumerate(g.PINS):
        raw = f"Source {i}: claims for review — ר\n".encode()
        (src / name).write_bytes(raw)
        pins[name] = g.blob_sha1(raw)
    return src, pins


def reject(label, change):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        src, pins = fixture(root)
        change(src, pins, root)
        dest = root / "snapshot"
        try:
            g.snapshot(src, dest, pins=pins)
        except (OSError, ValueError):
            check(label, not dest.exists())
        else:
            check(label, False)

with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    src, pins = fixture(root)
    out = root / "snapshot"
    receipt = g.snapshot(src, out, pins=pins)
    check("positive eight source files", all((out / x).is_file() for x in pins))
    check("positive receipt hold", receipt["status"] == "PREPARED_HOLD" and not receipt["release_authorized"])
    check("positive byte identity", all(g.blob_sha1((out / n).read_bytes()) == pin for n,pin in pins.items()))
    check("positive receipt hashes", all(receipt["files"][n]["sha256"] for n in pins))
    check("receipt on disk", json.loads((out / "SOURCE-SNAPSHOT-RECEIPT.json").read_text())["files"] == receipt["files"])
    try: g.snapshot(src, out, pins=pins)
    except ValueError: check("existing destination rejected", True)
    else: check("existing destination rejected", False)
    try: g.snapshot(src, src / "nested", pins=pins)
    except ValueError: check("output within source rejected", True)
    else: check("output within source rejected", False)
    (src / "unrelated.txt").write_text("extra")
    check("unrelated source left untouched", (src / "unrelated.txt").read_text() == "extra")

reject("missing file rejected", lambda s,p,r: (s / next(iter(p))).unlink())
reject("empty file rejected", lambda s,p,r: (s / next(iter(p))).write_bytes(b""))
reject("tampered bytes rejected", lambda s,p,r: (s / next(iter(p))).write_bytes(b"changed"))
reject("invalid utf8 rejected", lambda s,p,r: (s / next(iter(p))).write_bytes(b"\xff"))

def source_symlink(s,p,r):
    name = next(iter(p))
    (s / name).unlink()
    (s / name).symlink_to("unrelated.txt")
reject("symlink source rejected", source_symlink)

def source_dir_symlink(s,p,r):
    link = r / "linked"
    link.symlink_to(s, target_is_directory=True)
    # tested separately since reject() normally passes s
    try: g.snapshot(link, r / "snap", pins=p)
    except ValueError: return
    raise AssertionError("symlink root accepted")
with tempfile.TemporaryDirectory() as d:
    root=Path(d);src,pins=fixture(root);source_dir_symlink(src,pins,root)
    check("symlink source root rejected",True)

print(json.dumps({"passed":sum(v for _,v in checks),"total":len(checks),"checks":checks},indent=2))
