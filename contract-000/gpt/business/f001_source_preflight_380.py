#!/usr/bin/env python3
"""HOLD-only, read-only F-001 source preflight for original claim_scan.py.
Usage: python f001_source_preflight_380.py <pinned-TAM-source-directory>
       python f001_source_preflight_380.py --self-test
All eight files must match exact Git blob SHA and size. Never authorizes release.
"""
import hashlib, json, sys, tempfile
from pathlib import Path

PINS = {
    "README.md": ("213bcfaf560dcc54fbb7ae79fad932e86b660357", 2561),
    "Article 1 Hacksilber": ("237bd3335abdcc0f0465817dffe01ad6eaa86055", 2345),
    "Article 2 Water Weight Computes": ("ec657c3fa0f70da9686fb1ae52983d28f77c6c4c", 2535),
    "The Color Dyed and Dental Records": ("b525ad60ab37cb2d72ea43c40ba687b0fe2a348d", 2974),
    "Article 5": ("c8c1bf617c0d81389f6c2408ed975131695857ff", 3969),
    "Article 6": ("662d745f0b9b41236d1053cdbaa9351f7c020dd0", 3210),
    "Article 10": ("e82be564872f636662652d34dcb8d3437559f84f", 812),
    "Collective information": ("710ad3cd4feeae7bafa329d7437a78df4c40cfa8", 33708),
}

def blob_sha(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()

def check(root, pins=PINS):
    root = Path(root)
    results = []
    for name, (sha, size) in pins.items():
        path = root / name
        if path.is_symlink():
            results.append({"file": name, "state": "SYMLINK_REJECTED"})
            continue
        if not path.is_file():
            results.append({"file": name, "state": "MISSING"})
            continue
        raw = path.read_bytes()
        ok = len(raw) == size and blob_sha(raw) == sha
        results.append({"file": name, "state": "MATCH" if ok else "MISMATCH",
                        "actual_sha": blob_sha(raw), "actual_size": len(raw)})
    return {"status": "PASS" if all(x["state"] == "MATCH" for x in results) else "HOLD",
            "files": results, "count": len(results)}

def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        pins = {"one": (blob_sha(b"abc"), 3), "two": (blob_sha(b"xyz"), 3)}
        (p / "one").write_bytes(b"abc")
        missing = check(p, pins)
        (p / "two").write_bytes(b"bad")
        altered = check(p, pins)
        (p / "two").write_bytes(b"xyz")
        good = check(p, pins)
        (p / "two").unlink()
        (p / "two").symlink_to("one")
        linked = check(p, pins)
        checks = {
            "missing_fails": missing["status"] == "HOLD" and missing["files"][1]["state"] == "MISSING",
            "changed_blob_fails": altered["status"] == "HOLD" and altered["files"][1]["state"] == "MISMATCH",
            "all_match_passes": good["status"] == "PASS",
            "symlink_fails": linked["status"] == "HOLD" and linked["files"][1]["state"] == "SYMLINK_REJECTED",
        }
        print(json.dumps({"checks": checks, "passed": sum(checks.values()), "total": len(checks)}, indent=2))
        return all(checks.values())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == "--self-test":
        raise SystemExit(0 if self_test() else 1)
    report = check(sys.argv[1])
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 2)
