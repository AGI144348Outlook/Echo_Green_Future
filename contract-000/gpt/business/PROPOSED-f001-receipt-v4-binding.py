#!/usr/bin/env python3
"""F-001 proposed HOLD-only cross-report receipt binding preflight (NOT a release gate).

Consumes the reports of separately executed receipt-v3 and v5-report-gate-v1.
Does not execute those tools, independently authenticate pins, or approve publishing.
Only an independently witnessed release process could change HOLD.
"""
import argparse
import json
import os
import re
import stat
import sys

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
V3_BLOB = "4aafb14298e901079428864bb57be28810bb226c"
V5_GATE_BLOB = "7556a83ff3923528b0be5d6c419a231285cee1d3"
V5_PARSER_BLOB = "f8c2b4b29f9fffb1bc3d65f4f1fdf56954b7a4f0"
ARTIFACTS = {"epub", "pdf", "dataset_a_csv", "dataset_b_csv"}
PIN_KEYS = {"schema", "source", "inputs", "scripts", "apply_order_blob", "applied_patches", "artifacts"}
RECEIPT_KEYS = PIN_KEYS | {"environment", "editorial", "release", "approved", "timothy_approval_reference"}
EDITORIAL_KEYS = {"release", "status", "source_pin_authenticated", "decision_reference_authenticated",
                  "dataset_a_sha256", "flagged_csv_lines"}
MANIFEST_KEYS = {"schema", "dataset_a_sha256", "v5_report_sha256", "v5_parser_blob",
                 "v5_gate_blob", "receipt_v3_blob", "publication_authorized"}
MAX_JSON = 1024 * 1024


def exact(obj, keys, label, issues):
    if not isinstance(obj, dict) or set(obj) != keys:
        issues.append(label + ": expected exact fields")
        return False
    return True


def digest(value, regex):
    return isinstance(value, str) and regex.fullmatch(value) is not None


def check_binding(pins, receipt, v3, v5, manifest):
    """Pure cross-report consistency checker; upstream tools must independently check bytes."""
    issues = []
    exact(pins, PIN_KEYS, "pins", issues)
    exact(receipt, RECEIPT_KEYS, "receipt", issues)
    exact(manifest, MANIFEST_KEYS, "binding manifest", issues)
    if not all(isinstance(x, dict) for x in (pins, receipt, v3, v5, manifest)):
        return result(["all five inputs must be JSON objects"] + issues)
    if pins.get("schema") != "f001-pins/v1" or receipt.get("schema") != "f001-receipt/v1":
        issues.append("source schemas unsupported")
    if manifest.get("schema") != "f001-receipt-v4-binding/v1":
        issues.append("binding schema unsupported")
    if pins.get("source") != receipt.get("source"):
        issues.append("source mismatch")
    exact(pins.get("source"), {"repository", "commit"}, "source", issues)
    src = pins.get("source") if isinstance(pins.get("source"), dict) else {}
    if src.get("repository") != "AGI144348Outlook/The-TAM-protocol" or not digest(src.get("commit"), HEX40):
        issues.append("source identifier invalid")
    for key in ("inputs", "scripts", "apply_order_blob", "applied_patches"):
        if pins.get(key) != receipt.get(key):
            issues.append(key + " mismatch")
    for name in ("inputs", "scripts"):
        values = pins.get(name)
        if not isinstance(values, dict) or not values or any(not isinstance(k, str) or not k or not digest(v, HEX40) for k, v in values.items()):
            issues.append(name + " invalid Git blob map")
    if not digest(pins.get("apply_order_blob"), HEX40):
        issues.append("apply-order pin invalid")
    patches = pins.get("applied_patches")
    if not isinstance(patches, dict) or any(not isinstance(k, str) or not digest(v, HEX64) for k, v in patches.items()):
        issues.append("patch digests invalid")
    if (not isinstance(pins.get("scripts"), dict) or
        pins["scripts"].get("PROPOSED-f001-disposition-binding-v5.py") != V5_PARSER_BLOB):
        issues.append("audited v5 parser pin mismatch")
    if (manifest.get("v5_parser_blob") != V5_PARSER_BLOB or
        manifest.get("receipt_v3_blob") != V3_BLOB or
        not isinstance(manifest.get("v5_gate_blob"), str) or
        manifest["v5_gate_blob"] != V5_GATE_BLOB):
        issues.append("reviewed verifier/parser blob mismatch")
    if manifest.get("publication_authorized") is not False:
        issues.append("publication authority must remain absent")
    if not digest(manifest.get("v5_report_sha256"), HEX64):
        issues.append("v5 report digest malformed")
    pin_art = pins.get("artifacts")
    rec_art = receipt.get("artifacts")
    if not isinstance(pin_art, dict) or set(pin_art) != ARTIFACTS or not isinstance(rec_art, dict) or set(rec_art) != ARTIFACTS:
        issues.append("exact four-artifact maps required")
        pin_art, rec_art = {}, {}
    for name in sorted(ARTIFACTS):
        p, r = pin_art.get(name), rec_art.get(name)
        if not exact(p, {"sha256", "size"}, "pin " + name, issues):
            continue
        if not exact(r, {"path", "sha256", "size"}, "receipt " + name, issues):
            continue
        if (not digest(p.get("sha256"), HEX64) or type(p.get("size")) is not int or p["size"] < 0
            or not isinstance(r.get("path"), str) or not r["path"]
            or r.get("sha256") != p["sha256"] or type(r.get("size")) is not int or r["size"] != p["size"]):
            issues.append(name + ": invalid or inconsistent artifact metadata")
    exact(receipt.get("environment"), {"platform", "python_version", "build_output_realpath"}, "environment", issues)
    ed = receipt.get("editorial")
    exact(ed, EDITORIAL_KEYS, "editorial", issues)
    if not isinstance(ed, dict):
        ed = {}
    if (ed.get("release") != "HOLD" or ed.get("status") != "PENDING" or
        ed.get("source_pin_authenticated") is not False or ed.get("decision_reference_authenticated") is not False):
        issues.append("editorial may only assert PENDING/HOLD, unauthenticated")
    lines = ed.get("flagged_csv_lines")
    if (not isinstance(lines, list) or any(type(n) is not int for n in lines)
        or lines != sorted(set(lines)) or lines != [6, 7]):
        issues.append("Dataset A flags must be exact [6,7] until reviewed")
    if (receipt.get("release") != "HOLD" or receipt.get("approved") is not False
        or receipt.get("timothy_approval_reference") is not None):
        issues.append("receipt falsely asserts approval")
    a_pin = pin_art.get("dataset_a_csv") if isinstance(pin_art, dict) else None
    a_sha = a_pin.get("sha256") if isinstance(a_pin, dict) else None
    if (not digest(a_sha, HEX64) or ed.get("dataset_a_sha256") != a_sha or
        manifest.get("dataset_a_sha256") != a_sha):
        issues.append("Dataset A digest differs across receipt/pin/binding")
    if (v3.get("schema") != "f001-receipt-verification/v3" or v3.get("integrity") != "PASS" or
        v3.get("release") != "HOLD" or v3.get("source_pin_authenticated") is not False or
        v3.get("approval_authenticated") is not False or v3.get("publication_authorization") != "ABSENT" or
        v3.get("format_accessibility_rights_verified") is not False or v3.get("issues") != []):
        issues.append("upstream receipt-v3 did not pass safely")
    checked = v3.get("artifacts_checked")
    if (not isinstance(checked, list) or len(checked) != 4 or
        {x.get("artifact") for x in checked if isinstance(x, dict)} != ARTIFACTS):
        issues.append("v3 did not report all four distinct artifacts")
    else:
        for item in checked:
            if not isinstance(item, dict):
                issues.append("v3 measured artifact entry not object")
                continue
            p = pin_art.get(item["artifact"], {})
            if item.get("sha256") != p.get("sha256") or type(item.get("bytes")) is not int or item.get("bytes") != p.get("size"):
                issues.append("v3 measured artifact mismatch: " + item["artifact"])
    if (v5.get("schema") != "f001-v5-report-gate/v1" or v5.get("integrity") != "PASS" or
        v5.get("release") != "HOLD" or v5.get("source_pin_authenticated") is not False or
        v5.get("approval_authenticated") is not False or v5.get("publication_authorization") != "ABSENT" or
        v5.get("issues") != []):
        issues.append("upstream v5 report gate did not pass safely")
    if (v5.get("dataset_a_sha256") != a_sha or
        v5.get("dataset_a_sha256") != manifest.get("dataset_a_sha256") or
        v5.get("v5_report_sha256") != manifest.get("v5_report_sha256")):
        issues.append("v5 source/report digest not bound to four-artifact receipt")
    if v5.get("flagged_csv_lines") != lines or v5.get("v5_status") not in ("PENDING", "RECORDED_UNAUTHENTICATED"):
        issues.append("v5 flags/status disagree with receipt")
    return result(issues)


def result(issues):
    return {"schema": "f001-receipt-v4-binding/v1", "integrity": "FAIL" if issues else "PASS",
            "release": "HOLD", "source_pin_authenticated": False, "approval_authenticated": False,
            "publication_authorization": "ABSENT", "format_accessibility_rights_verified": False,
            "issues": issues}


def no_dupes(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key: " + key)
        out[key] = value
    return out


def read_json(path):
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("not regular file")
        with os.fdopen(fd, "rb", closefd=False) as fh:
            raw = fh.read(MAX_JSON + 1)
        if len(raw) > MAX_JSON:
            raise ValueError("JSON exceeds 1 MiB")
        return json.loads(raw.decode("utf-8"), object_pairs_hook=no_dupes,
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
    finally:
        os.close(fd)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    for key in ("pins", "receipt", "v3_result", "v5_result", "binding_manifest"):
        p.add_argument("--" + key.replace("_", "-"), required=True)
    a = p.parse_args(argv)
    try:
        output = check_binding(*(read_json(getattr(a, k)) for k in
                                 ("pins", "receipt", "v3_result", "v5_result", "binding_manifest")))
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError, OverflowError) as exc:
        output = result(["input invalid: " + str(exc)])
    print(json.dumps(output, sort_keys=True))
    return 0 if output["integrity"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
