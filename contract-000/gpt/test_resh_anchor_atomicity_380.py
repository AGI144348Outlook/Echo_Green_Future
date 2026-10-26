#!/usr/bin/env python3
"""RC-R5 exploratory atomicity characterization, read-only.
Usage: python test_resh_anchor_atomicity_380.py <full-genesis-source.py>
Requires pinned Genesis blob; no test is frozen and no code is patched.
"""
import ast
import hashlib
import json
import sys
from pathlib import Path

PIN = "63eb982989b4f3478d649430b555c8f4ba755c27"

def run(path):
    raw = Path(path).read_bytes()
    sha = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    if sha != PIN:
        raise ValueError(f"Genesis blob mismatch: {sha} != {PIN}")
    tree = ast.parse(raw.decode("utf-8"))
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "ReshIdentity"]
    if len(classes) != 1:
        raise ValueError("Expected exactly one ReshIdentity class")
    scope = {}
    exec(compile(ast.fix_missing_locations(ast.Module(body=classes, type_ignores=[])), str(path), "exec"), scope)
    ReshIdentity = scope["ReshIdentity"]
    class Matrix:
        def __init__(self):
            self.known = {"A-000": {"name": "Governor", "status": "ACTIVE"}}
    class FailingAgent:
        @property
        def definition_words(self):
            raise RuntimeError("injected agent-read failure")
        @definition_words.setter
        def definition_words(self, value):
            raise RuntimeError("injected agent-write failure")
    class Lobby:
        def __init__(self):
            self.agents = {"resh": FailingAgent()}
    matrix = Matrix()
    identity = ReshIdentity(matrix, Lobby())
    exceptions = []
    try:
        identity.anchor()
    except RuntimeError as e:
        exceptions.append(str(e))
    checks = {
        "injected_exception_observed": len(exceptions) == 1,
        "a000_mutated_after_exception": matrix.known["A-000"].get("identity_symbol") == "resh",
        "alias_written_after_exception": "A-000-RESH" in matrix.known,
        "anchored_flag_still_false": identity._anchored is False,
        "validate_false_after_exception": identity.validate() is False,
        "anchor_reference_unset": identity._anchor_entry is None,
    }
    identity.hebrew_lobby = None
    identity.anchor()
    checks.update({
        "retry_anchored_true": identity._anchored is True,
        "retry_validates_true": identity.validate() is True,
        "no_failure_audit_field": not any("failure" in k for k in matrix.known["A-000-RESH"]),
    })
    print(json.dumps({"source_sha": sha, "method": "AST-extracted exact ReshIdentity with stubs",
                      "checks": checks, "passed": sum(checks.values()), "total": len(checks),
                      "exceptions": exceptions}, indent=2))
    return all(checks.values())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raise SystemExit(0 if run(sys.argv[1]) else 1)
