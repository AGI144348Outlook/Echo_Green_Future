#!/usr/bin/env python3
"""DISC-002 E72 probe (Claude, 2026-11-05 14Z). Exploratory, not a frozen test.

Question (from ChatGPT 13Z, SOURCE-OBSERVED there): does Genesis's
governor_validate_and_deploy accept an A-000 entry whose identity is wrong,
as long as it has "name" and "status" == "ACTIVE"?

Method: extract ONLY that function's source (by ast) from the given file,
exec it with stub AlgorithmMatrix/SubAgentMatrix objects, and run it on a set
of A-000 variants. Nothing else in the source file is executed. A second,
PROPOSED validator that compares a pinned identity digest is run on the same
cases for contrast.

Usage: python3 -I DISC-002-a000-identity-e72-probe.py <path to echo_governor_skeleton.py>
(blob 63eb982989b4f3478d649430b555c8f4ba755c27 on branch algebra).
"""
import ast
import hashlib
import json
import sys


class StubMatrix:
    def __init__(self, known, regions):
        self.known = dict(known)
        self.regions = regions


class StubSubAgent:
    _n = 0

    def __init__(self, region_id, domain_words, parent, domain_weight):
        StubSubAgent._n += 1
        self.id = f"SA-{region_id}"


def load_function(path):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "governor_validate_and_deploy":
            mod = ast.Module(body=[node], type_ignores=[])
            ns = {"AlgorithmMatrix": StubMatrix, "SubAgentMatrix": StubSubAgent}
            exec(compile(mod, path, "exec"), ns)
            return ns["governor_validate_and_deploy"], node.lineno, node.end_lineno
    raise SystemExit("function not found")


def canon(entry):
    return hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()


GENUINE = {"name": "Governor", "status": "ACTIVE", "role": "self-index"}
PINNED = canon(GENUINE)  # PROPOSED: a pinned digest held outside the matrix


def proposed_validate(matrix):
    a = matrix.known.get("A-000")
    if not a:
        return "FAILED"
    return "OK" if canon(a) == PINNED else "FAILED"


REGIONS = {"R1": {"words": ["a", "b"]}}
TOOL = {"A-101": {"name": "tool", "status": "ACTIVE"}}
CASES = [
    ("C1 genuine A-000", {"A-000": GENUINE, **TOOL}),
    ("C2 impostor name", {"A-000": {"name": "IMPOSTOR", "status": "ACTIVE"}, **TOOL}),
    ("C3 empty name", {"A-000": {"name": "", "status": "ACTIVE"}, **TOOL}),
    ("C4 status not ACTIVE", {"A-000": {"name": "Governor", "status": "DORMANT"}, **TOOL}),
    ("C5 name missing", {"A-000": {"status": "ACTIVE"}, **TOOL}),
    ("C6 A-001 only, no A-101", {"A-000": GENUINE, "A-001": {"name": "t", "status": "ACTIVE"}}),
    ("C7 sub-agent entry reused as A-000",
     {"A-000": {"name": "SubAgent for R1", "status": "ACTIVE", "origin": "SELF-DEPLOYED",
                "domain_size": 2, "depth": 1}, **TOOL}),
]


def main():
    fn, a, b = load_function(sys.argv[1])
    print(f"function lines {a}-{b}")
    print("case | genesis status | proposed digest check")
    for label, known in CASES:
        m = StubMatrix(known, REGIONS)
        g = fn(m).get("status")
        p = proposed_validate(StubMatrix(known, REGIONS))
        print(f"{label} | {g} | {p}")


if __name__ == "__main__":
    main()
