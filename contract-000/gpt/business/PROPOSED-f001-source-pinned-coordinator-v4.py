#!/usr/bin/env python3
"""F-001 read-only, HOLD-only coordinator v4 PROPOSAL. Not a publication gate.

Runs fixed Git-blob-pinned receipt-v3, v5-report-gate-v1, and cross-report-v4
in sequence from checked temporary script snapshots (including nested v5 parser).
Caller pins are NOT independent authority. Linux/POSIX only; not a sandbox.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import subprocess
import sys
import tempfile

FIXED_BLOBS = {
    "receipt_v3": "4aafb14298e901079428864bb57be28810bb226c",
    "v5_gate": "7556a83ff3923528b0be5d6c419a231285cee1d3",
    "v4_binding": "848040fcfd7f73b1f65d0772c25bfcd6e9e1be56",
    "v5_parser": "f8c2b4b29f9fffb1bc3d65f4f1fdf56954b7a4f0",
}
MAX_JSON = 1_048_576
MAX_SCRIPT = 1_048_576
TIMEOUT = 5


def fail(reason, stages=None):
    return {"schema": "f001-source-pinned-coordinator/v4", "integrity": "FAIL",
            "release": "HOLD", "source_pin_authenticated": False,
            "approval_authenticated": False, "publication_authorization": "ABSENT",
            "issues": [str(reason)], "stages": stages or [],
            "readiness": "BLOCKED", "readiness_blockers": ["integrity_failure"],
            "editorial_status": "UNKNOWN", "format_accessibility_rights_verified": False}


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def canonical_path(value):
    """Reject lexical parent traversal before OS resolution; hand one checked path to children.

    This is not an atomic file-descriptor pin. Callers may still mutate files
    between preflight and child open; a trusted immutable artifact snapshot is
    required for stronger guarantees.
    """
    raw = Path(value)
    if ".." in raw.parts:
        raise ValueError("parent traversal component rejected")
    absolute = Path(os.path.abspath(raw))
    if os.path.realpath(absolute) != str(absolute):
        raise ValueError("symlink path component rejected")
    return absolute


def safe_file(path, root, limit, missing_ok=False):
    root = Path(os.path.abspath(root))
    path = Path(os.path.abspath(path))
    if path != root and root not in path.parents:
        raise ValueError("path escapes designated root")
    # Include the ancestors ABOVE the designated root, not just paths inside it.
    for ancestor in (root, *root.parents):
        if ancestor.is_symlink():
            raise ValueError("symlink ancestor of designated root")
    for part in (root, *(root / parent for parent in reversed(path.relative_to(root).parents) if parent != Path(".")), path):
        if part == Path('.'):
            continue
        if os.path.islink(part):
            raise ValueError("symlink path component")
    if missing_ok and not path.exists():
        return None
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("not a regular file")
        with os.fdopen(fd, "rb", closefd=False) as f:
            data = f.read(limit + 1)
        if len(data) > limit:
            raise ValueError("file exceeds bound")
        return data
    finally:
        os.close(fd)


def no_duplicates(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ValueError("duplicate JSON key")
        obj[k] = v
    return obj


def read_json(path, root):
    return json.loads(safe_file(path, root, MAX_JSON), object_pairs_hook=no_duplicates,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))


def child_limit():
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_JSON + 1, MAX_JSON + 1))


def run_script(script, argv, expected_blob, toolroot):
    """Execute the exact checked bytes, never the originally checked pathname.

    Re-open and re-hash immediately before staging. A replacement after the
    first coordinator preflight therefore fails rather than executing it.
    """
    data = safe_file(script, toolroot, MAX_SCRIPT)
    if git_blob(data) != expected_blob:
        raise ValueError("script changed before execution")
    with tempfile.TemporaryDirectory(prefix="f001-checked-script-") as sandbox:
        checked = Path(sandbox) / "reviewed.py"
        with os.fdopen(os.open(checked, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
            stream.write(data)
        with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            proc = subprocess.run([sys.executable, "-I", "-B", str(checked), *map(str, argv)],
                                  stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                  timeout=TIMEOUT, check=False, preexec_fn=child_limit)
            if out.tell() > MAX_JSON or err.tell() > MAX_JSON:
                raise ValueError("subprocess output exceeds bound")
            if proc.returncode < 0:
                raise ValueError("subprocess terminated by signal: " + str(proc.returncode))
            out.seek(0)
            raw = out.read(MAX_JSON + 1)
            return proc.returncode, json.loads(raw, object_pairs_hook=no_duplicates,
                                                parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))


def coordinate(a, expected_blobs=FIXED_BLOBS):
    stages = []
    try:
        root, toolroot = canonical_path(a.artifact_root), canonical_path(a.tool_root)
        # Never forward the original lexical pathname to a subprocess. In
        # particular, symlink/../x must not be checked as root/x and opened
        # by the child as an outside x (Claude's §118 V1 counterexample).
        for field in ("pins", "receipt", "binding_manifest", "v5_report", "disposition_record", *FIXED_BLOBS):
            setattr(a, field, canonical_path(getattr(a, field)))
        if not root.is_dir() or not toolroot.is_dir() or root.is_symlink() or toolroot.is_symlink():
            raise ValueError("artifact/tool root absent, symlinked or not directory")
        scripts = {key: Path(getattr(a, key)) for key in FIXED_BLOBS}
        for key, script in scripts.items():
            data = safe_file(script, toolroot, MAX_SCRIPT)
            if git_blob(data) != expected_blobs[key]:
                raise ValueError("unreviewed script blob: " + key)
        pins = read_json(a.pins, root)
        receipt = read_json(a.receipt, root)
        manifest = read_json(a.binding_manifest, root)
        if not all(isinstance(x, dict) for x in (pins, receipt, manifest)):
            raise ValueError("pin/receipt/manifest must be objects")
        if not isinstance(receipt.get("artifacts"), dict):
            raise ValueError("receipt artifact map invalid")
        art = receipt["artifacts"].get("dataset_a_csv", {})
        if not isinstance(art, dict) or not isinstance(art.get("path"), str):
            raise ValueError("Dataset A path absent")
        csv_path = canonical_path(root / art["path"])
        safe_file(csv_path, root, MAX_JSON)
        safe_file(a.v5_report, root, MAX_JSON)
        safe_file(a.disposition_record, root, MAX_JSON, missing_ok=True)
        expected_csv = pins["artifacts"]["dataset_a_csv"]["sha256"]
        expected_report = manifest["v5_report_sha256"]
        with tempfile.TemporaryDirectory(prefix="f001-coordinator-") as tmp:
            # Snapshot the nested parser as well; the gate must not execute its
            # mutable original pathname. The gate independently verifies this blob.
            parser_bytes = safe_file(scripts["v5_parser"], toolroot, MAX_SCRIPT)
            if git_blob(parser_bytes) != expected_blobs["v5_parser"]:
                raise ValueError("nested parser changed before execution")
            parser_copy = Path(tmp) / "v5_parser.py"
            with os.fdopen(os.open(parser_copy, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
                stream.write(parser_bytes)
            commands = [
                ("receipt_v3", ["--pins", a.pins, "--receipt", a.receipt, "--artifact-root", root]),
                ("v5_gate", ["--dataset-a", csv_path, "--disposition-record", a.disposition_record,
                             "--v5-script", parser_copy, "--report-json", a.v5_report,
                             "--expected-dataset-sha256", expected_csv,
                             "--expected-report-sha256", expected_report]),
            ]
            results = {}
            for name, args in commands:
                rc, result = run_script(scripts[name], args, expected_blobs[name], toolroot)
                if not isinstance(result, dict):
                    raise ValueError("subprocess stage output must be JSON object: " + name)
                stages.append({"stage": name, "exit": rc, "integrity": result.get("integrity")})
                if rc != 0 or result.get("integrity") != "PASS" or result.get("release") != "HOLD" or result.get("source_pin_authenticated") is not False or result.get("approval_authenticated") is not False or result.get("publication_authorization") != "ABSENT":
                    raise ValueError("upstream stage failed or claimed authority: " + name)
                results[name] = result
                (Path(tmp) / (name + ".json")).write_text(json.dumps(result))
            args = ["--pins", a.pins, "--receipt", a.receipt,
                    "--v3-result", Path(tmp) / "receipt_v3.json",
                    "--v5-result", Path(tmp) / "v5_gate.json",
                    "--binding-manifest", a.binding_manifest]
            rc, result = run_script(scripts["v4_binding"], args, expected_blobs["v4_binding"], toolroot)
            if not isinstance(result, dict):
                raise ValueError("subprocess stage output must be JSON object: v4_binding")
            stages.append({"stage": "v4_binding", "exit": rc, "integrity": result.get("integrity")})
            if rc != 0 or result.get("integrity") != "PASS" or result.get("release") != "HOLD" or result.get("source_pin_authenticated") is not False or result.get("approval_authenticated") is not False or result.get("publication_authorization") != "ABSENT":
                raise ValueError("binding failed or claimed authority")
        # Integrity consistency is not editorial or commercial release readiness.
        # A pending report is a valid integrity state but a visible blocker.
        editorial_status = results["v5_gate"].get("v5_status")
        if editorial_status not in ("PENDING", "RECORDED_UNAUTHENTICATED"):
            raise ValueError("unsupported editorial status in v5 gate")
        blockers = ["source_pin_not_independently_authenticated",
                    "artifact_format_accessibility_rights_unverified",
                    "timothy_publication_authorization_absent"]
        if editorial_status == "PENDING":
            blockers.insert(0, "editorial_dispositions_pending")
        else:
            blockers.insert(0, "editorial_decision_authority_unverified")
        return {"schema": "f001-source-pinned-coordinator/v4", "integrity": "PASS",
                "release": "HOLD", "source_pin_authenticated": False,
                "approval_authenticated": False, "publication_authorization": "ABSENT",
                "format_accessibility_rights_verified": False,
                "readiness": "BLOCKED", "readiness_blockers": blockers,
                "editorial_status": editorial_status,
                "issues": [], "stages": stages}
    except (OSError, ValueError, KeyError, TypeError, UnicodeError, json.JSONDecodeError,
            subprocess.TimeoutExpired, RecursionError, AttributeError, IndexError) as exc:
        return fail(exc, stages)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("artifact_root", "tool_root", "pins", "receipt", "binding_manifest",
                 "v5_report", "disposition_record", *FIXED_BLOBS):
        p.add_argument("--" + name.replace("_", "-"), required=True)
    result = coordinate(p.parse_args())  # no CLI override of reviewed source pins
    print(json.dumps(result, sort_keys=True))
    return 0 if result["integrity"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
