#!/usr/bin/env python3
"""Synthetic-only preregistered v579 gate harness. See Issue #258 BEFORE execution.
Usage: python3 -I -B F001-V579-SYNTHETIC-580.py F001-CLAIM-CHAIN-ALIGN-579.py
No real manuscript, network, publication, or source writes.
"""
import csv
import hashlib
import importlib.util
import json
import pathlib
import sys
import tempfile

def load_gate(path):
    spec = importlib.util.spec_from_file_location("f001_gate_579", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def make_fixture(gate, root, trigger=True):
    src, out = root / "source", root / "output"
    src.mkdir()
    out.mkdir()
    hashes = {}
    for name in gate.FILES:
        raw = b"Ordinary text without flagged words."
        if name == "README.md" and trigger:
            raw = b"This is proven."
        (src / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    rows = []
    per_file = {}
    per_trigger = {}
    for name in gate.FILES:
        count = 0
        if name == "README.md" and trigger:
            rows.append({"file": name, "sentence_no": "1", "triggers": "certainty",
                         "sentence": "This is proven.", "status": "sourced"})
            count = 1
            per_trigger["certainty"] = 1
        per_file[name] = count
    report = {"source_files": hashes, "per_file": per_file,
              "per_trigger": per_trigger, "rows": len(rows)}
    (out / "claims-report.json").write_text(json.dumps(report), encoding="utf-8")
    with (out / "claims.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=gate.COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return src, out

def run_case(gate, label, mutate=None, trigger=True, expect_fail=False):
    with tempfile.TemporaryDirectory(prefix="f001-v579-") as tmp:
        src, out = make_fixture(gate, pathlib.Path(tmp), trigger=trigger)
        if mutate:
            mutate(src, out)
        try:
            errors = gate.evaluate(src, out)
            actual_fail = bool(errors)
            detail = "; ".join(errors) if errors else "PASS alignment only"
        except Exception as exc:
            actual_fail = True
            detail = "UNHANDLED " + type(exc).__name__ + ": " + str(exc)
            print(label, "FAIL", detail)
            return False
        ok = actual_fail == expect_fail
        print(label, "PASS" if ok else "FAIL", detail)
        return ok

def rewrite_csv(out, change):
    path = out / "claims.csv"
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    change(rows)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file","sentence_no","triggers","sentence","status"])
        writer.writeheader()
        writer.writerows(rows)

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: harness <gate-file>")
    gate = load_gate(pathlib.Path(sys.argv[1]).resolve())
    checks = [
        run_case(gate, "P0 valid", expect_fail=False),
        run_case(gate, "F1 JSON array", lambda s,o: (o/"claims-report.json").write_text("[]"), expect_fail=True),
        run_case(gate, "F2 no triggers", trigger=False, expect_fail=True),
        run_case(gate, "F3 altered sentence", lambda s,o: rewrite_csv(o, lambda rows: rows[0].update(sentence="Forged.")), expect_fail=True),
        run_case(gate, "F4 missing source", lambda s,o: (s/"Article 5").unlink(), expect_fail=True),
        run_case(gate, "F5 invalid status", lambda s,o: rewrite_csv(o, lambda rows: rows[0].update(status="")), expect_fail=True),
    ]
    print("SUMMARY", sum(checks), "/", len(checks))
    return 0 if all(checks) else 1

if __name__ == "__main__":
    sys.exit(main())
