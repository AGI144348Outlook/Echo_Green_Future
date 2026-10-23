#!/usr/bin/env python3
"""F-001 read-only four-artifact integrity receipt checker. PROPOSAL, NOT release approval.

Two JSON files are compared but neither is an authenticated trust anchor.
Exit 0: internally consistent and bytes match, still HOLD. Exit 1: integrity FAIL.
Exit 64: usage error. No publication-ready state is emitted by this program.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

ARTIFACTS = ("epub", "pdf", "dataset_a_csv", "dataset_b_csv")
REQUIRED_SCRIPTS = ("build.py", "build_pdf.py", "rebuild_datasets.py", "claim_scan.py",
                    "listing_check.py", "epub_check.py", "PROPOSED-f001-disposition-binding-v5.py")
LIMITS = {"epub": 50 * 1024 * 1024, "pdf": 50 * 1024 * 1024,
          "dataset_a_csv": 1024 * 1024, "dataset_b_csv": 1024 * 1024}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_JSON = 1024 * 1024


def duplicates_forbidden(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key: " + key)
        obj[key] = value
    return obj


def no_constant(value):
    raise ValueError("nonfinite JSON constant: " + value)


def read_regular(path, limit):
    """Reject symlink final component, FIFOs/devices and unbounded reads.
    Caller also checks parent components; this is not a concurrent-swap proof.
    """
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("not a regular file")
        with os.fdopen(fd, "rb", closefd=False) as fh:
            data = fh.read(limit + 1)
        if len(data) > limit:
            raise ValueError("exceeds byte limit")
        return data
    finally:
        os.close(fd)


def load_json(path):
    raw = read_regular(path, MAX_JSON)
    return json.loads(raw.decode("utf-8"), object_pairs_hook=duplicates_forbidden,
                      parse_constant=no_constant)


def valid_sha(value, regex):
    return isinstance(value, str) and regex.fullmatch(value) is not None


def check_sha_map(obj, label, issues, required=()):
    if not isinstance(obj, dict) or not obj:
        issues.append(label + " must be a nonempty object")
        return
    for key, sha in obj.items():
        if not isinstance(key, str) or not key or not valid_sha(sha, HEX40):
            issues.append(label + " contains invalid Git blob pin")
            break
    for key in required:
        if key not in obj:
            issues.append(label + " missing required script: " + key)


def safe_artifact_path(root, rel):
    if not isinstance(rel, str) or not rel or "\\" in rel or "\x00" in rel:
        raise ValueError("unsafe artifact path")
    path = Path(rel)
    if path.is_absolute() or any(part in (".", "..", "") for part in path.parts):
        raise ValueError("unsafe artifact path")
    cur = root
    for part in path.parts:
        cur = cur / part
        mode = os.lstat(cur).st_mode
        if stat.S_ISLNK(mode):
            raise ValueError("symlink path component")
    if not stat.S_ISREG(os.lstat(cur).st_mode):
        raise ValueError("not a regular artifact")
    return cur


def verify(pins, receipt, root):
    issues, checked = [], []
    if not isinstance(pins, dict) or not isinstance(receipt, dict):
        return ["pin manifest and receipt must be JSON objects"], checked
    if pins.get("schema") != "f001-pins/v1" or receipt.get("schema") != "f001-receipt/v1":
        issues.append("schema mismatch")
    source = pins.get("source")
    if (not isinstance(source, dict) or
        source.get("repository") != "AGI144348Outlook/The-TAM-protocol" or
        not valid_sha(source.get("commit"), HEX40)):
        issues.append("invalid independent source identifier")
    if receipt.get("source") != source:
        issues.append("source pin differs between manifest and receipt")
    for field in ("inputs", "scripts"):
        check_sha_map(pins.get(field), "pin " + field, issues,
                      REQUIRED_SCRIPTS if field == "scripts" else ())
        if receipt.get(field) != pins.get(field):
            issues.append(field + " provenance mismatch")
    if not valid_sha(pins.get("apply_order_blob"), HEX40):
        issues.append("missing/invalid APPLY-ORDER.md pin")
    if receipt.get("apply_order_blob") != pins.get("apply_order_blob"):
        issues.append("apply order mismatch")
    patches = pins.get("applied_patches")
    if not isinstance(patches, dict):
        issues.append("applied_patches must be a map (empty allowed for draft)")
    elif any(not isinstance(k, str) or not valid_sha(v, HEX64) for k, v in patches.items()):
        issues.append("invalid applied patch digest")
    if receipt.get("applied_patches") != patches:
        issues.append("applied patch provenance mismatch")
    env = receipt.get("environment")
    if not isinstance(env, dict) or any(not isinstance(env.get(k), str) or not env[k]
                                       for k in ("platform", "python_version", "build_output_realpath")):
        issues.append("missing build environment fields")
    pinned = pins.get("artifacts")
    delivered = receipt.get("artifacts")
    if not isinstance(pinned, dict) or set(pinned) != set(ARTIFACTS):
        issues.append("pin manifest must specify exactly four artifacts")
        pinned = {}
    if not isinstance(delivered, dict) or set(delivered) != set(ARTIFACTS):
        issues.append("receipt must specify exactly four artifacts")
        delivered = {}
    for key in ARTIFACTS:
        pin, item = pinned.get(key), delivered.get(key)
        if not isinstance(pin, dict) or not isinstance(item, dict):
            issues.append(key + ": missing pin or receipt record")
            continue
        sha, size = pin.get("sha256"), pin.get("size")
        if not valid_sha(sha, HEX64) or type(size) is not int or size < 0 or size > LIMITS[key]:
            issues.append(key + ": invalid pinned hash or size")
            continue
        if item.get("sha256") != sha or item.get("size") != size:
            issues.append(key + ": self-reported digest/size differs from pin")
        try:
            file_path = safe_artifact_path(root, item.get("path"))
            data = read_regular(file_path, LIMITS[key])
            measured = hashlib.sha256(data).hexdigest()
            checked.append({"artifact": key, "bytes": len(data), "sha256": measured})
            if len(data) != size or measured != sha:
                issues.append(key + ": artifact bytes differ from pinned hash/size")
        except (OSError, ValueError) as exc:
            issues.append(key + ": unreadable/unsafe artifact (" + str(exc) + ")")
    editorial = receipt.get("editorial")
    if not isinstance(editorial, dict):
        issues.append("editorial disposition report missing")
    else:
        if editorial.get("release") != "HOLD" or editorial.get("status") not in (
                "PENDING", "RECORDED_UNAUTHENTICATED", "NO_FLAGGED_ROWS"):
            issues.append("editorial report has invalid status/release")
        if editorial.get("source_pin_authenticated") is not False or editorial.get("decision_reference_authenticated") is not False:
            issues.append("editorial report asserts unverified authentication")
        if editorial.get("dataset_a_sha256") != (pinned.get("dataset_a_csv") or {}).get("sha256"):
            issues.append("editorial report not bound to pinned Dataset A")
        if editorial.get("flagged_csv_lines") != [6, 7]:
            issues.append("F-001 unresolved Dataset A lines 6 and 7 must remain flagged")
    if receipt.get("release") != "HOLD" or receipt.get("approved") is not False or receipt.get("timothy_approval_reference") is not None:
        issues.append("candidate receipt asserts publication/approval without authentication")
    return issues, checked


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pins", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args(argv)
    issues, checked = [], []
    try:
        root = Path(args.artifact_root).resolve(strict=True)
        if not root.is_dir():
            raise ValueError("artifact root is not a directory")
        pins, receipt = load_json(args.pins), load_json(args.receipt)
        issues, checked = verify(pins, receipt, root)
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError, OverflowError) as exc:
        issues = ["input invalid: " + str(exc)]
    result = {"schema": "f001-receipt-verification/v1", "integrity": "FAIL" if issues else "PASS",
              "release": "HOLD", "source_pin_authenticated": False,
              "approval_authenticated": False, "publication_authorization": "ABSENT",
              "format_accessibility_rights_verified": False,
              "issues": issues, "artifacts_checked": checked}
    print(json.dumps(result, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
