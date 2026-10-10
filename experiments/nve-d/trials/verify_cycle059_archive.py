#!/usr/bin/env python3
"""Verify a downloaded Cycle 059 ZIP. Standard-library-only, read-only."""
import hashlib
import io
import json
import sys
import zipfile

def digest(data):
    return hashlib.sha256(data).hexdigest()

def verify(archive):
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC mismatch")
        manifest = json.loads(z.read("MANIFEST059.json"))
        assert manifest["cycle"] == "NVE-D-HOURLY-059"
        for item in manifest["files"]:
            data = z.read(item["name"])
            assert len(data) == item["bytes"]
            assert digest(data) == item["sha256"], item["name"]
        ledger = z.read("ledger059.jsonl")
        fixture = z.read("fixture-ledger059.jsonl")
        assert digest(ledger) == "b5d96c138f840319af612a6adf37378a68d1f8797e8b4da8ec492e13cee32b99"
        records = ledger.splitlines(keepends=True)
        fixtures = fixture.splitlines(keepends=True)
        assert len(records) == 60 and len(fixtures) == 180
        for n in range(10, 61, 10):
            checkpoint = json.loads(z.read(f"checkpoint_{n:04d}.json"))
            assert checkpoint["records"] == n
            assert digest(b"".join(records[:n])) == checkpoint["sha256"]
        for n in range(20, 181, 20):
            checkpoint = json.loads(z.read(f"fixture-checkpoint_{n:04d}.json"))
            assert checkpoint["records"] == n
            assert digest(b"".join(fixtures[:n])) == checkpoint["ledger_sha256"]
        print(json.dumps({"evaluation": "=", "manifest_files": len(manifest["files"]), "predictive_records": 60, "fixture_records": 180, "checkpoints": 15}))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python verify_cycle059_archive.py NVE-D-HOURLY-059-artifacts.zip")
    verify(sys.argv[1])
