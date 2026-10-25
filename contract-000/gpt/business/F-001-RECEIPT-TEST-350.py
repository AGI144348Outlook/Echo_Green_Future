#!/usr/bin/env python3
"""F-001 Run 350 prospective receipt-shape test harness (synthetic only).

Pre-registered: Echo_Green_Future Issue #53, comment 6399246110.
Run only in a disposable local environment with the exact Run 350 caller
present; never publishes, pays, launches CI, or touches shared content.
Usage: python3 -I -B F-001-RECEIPT-TEST-350.py /abs/path/F-001-STAGE-SESSION-350.py
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

PIN_CALLER_BLOB = "722e84897a7bbac700054c15d4e1d8af64eb2aa8"


def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("expected exact absolute Run 350 caller path")
    source = Path(sys.argv[1])
    if not source.is_absolute() or not source.is_file():
        raise SystemExit("caller must be an absolute existing file")
    raw = source.read_bytes()
    if blob_sha(raw) != PIN_CALLER_BLOB:
        raise SystemExit("caller blob mismatch; no tests run")
    spec = importlib.util.spec_from_file_location("f001_run350_caller", source)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # __name__ != '__main__': no caller main()
    stage = "/private/stages/f001-candidate-abc"
    base = {
        "stage_consistency": "PASS", "release": "HOLD", "stage": stage,
        "output_hashes": {
            "dataset-a.csv": {"sha256": mod.EXPECTED_CSV_SHA256["dataset-a.csv"], "bytes": 584},
            "dataset-b.csv": {"sha256": mod.EXPECTED_CSV_SHA256["dataset-b.csv"], "bytes": 723},
            "dataset-check.json": {"sha256": "a" * 64, "bytes": 250},
        },
    }
    cases = [
        ("valid", lambda d: None, True),
        ("missing_root_key", lambda d: d.pop("release"), False),
        ("extra_root_key", lambda d: d.update(unexpected="yes"), False),
        ("wrong_stage", lambda d: d.update(stage="/other"), False),
        ("missing_output", lambda d: d["output_hashes"].pop("dataset-a.csv"), False),
        ("extra_output", lambda d: d["output_hashes"].update(extra={"sha256": "a"*64, "bytes": 2}), False),
        ("malformed_digest", lambda d: d["output_hashes"]["dataset-check.json"].update(sha256="x"*64), False),
        ("uppercase_digest", lambda d: d["output_hashes"]["dataset-check.json"].update(sha256="A"*64), False),
        ("bool_size", lambda d: d["output_hashes"]["dataset-check.json"].update(bytes=True), False),
        ("zero_size", lambda d: d["output_hashes"]["dataset-check.json"].update(bytes=0), False),
        ("negative_size", lambda d: d["output_hashes"]["dataset-check.json"].update(bytes=-1), False),
        ("oversize", lambda d: d["output_hashes"]["dataset-check.json"].update(bytes=5_000_001), False),
        ("wrong_csv_pin", lambda d: d["output_hashes"]["dataset-a.csv"].update(sha256="a"*64), False),
        ("unexpected_release", lambda d: d.update(release="READY"), False),
        ("extra_output_field", lambda d: d["output_hashes"]["dataset-a.csv"].update(approved=True), False),
        ("missing_output_field", lambda d: d["output_hashes"]["dataset-a.csv"].pop("bytes"), False),
    ]
    results = []
    for name, change, expected_accept in cases:
        sample = copy.deepcopy(base)
        change(sample)
        try:
            output = mod.validate_receipt_shape(sample, stage)
            accepted = output is sample["output_hashes"]
        except ValueError:
            accepted = False
        results.append({"case": name, "pass": accepted == expected_accept,
                        "accepted": accepted, "expected_accept": expected_accept})
    print(json.dumps({"project": "F-001", "release": "HOLD",
                      "caller_blob": PIN_CALLER_BLOB,
                      "passed": sum(r["pass"] for r in results),
                      "total": len(results), "results": results}, sort_keys=True))
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
