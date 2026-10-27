#!/usr/bin/env python3
"""PROPOSED read-only A-000/Resh witness prototype; NOT an identity authority.

Caller must keep the returned detached receipt outside AlgorithmMatrix and protect it
against replacement. No production code or frozen RC-R5 acceptance is changed.
"""
import copy
import hashlib
import json


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def snapshot(known):
    if not isinstance(known, dict):
        raise ValueError("matrix must be a dictionary")
    a, r = known.get("A-000"), known.get("A-000-RESH")
    if not isinstance(a, dict) or not isinstance(r, dict):
        raise ValueError("missing or malformed identity pair")
    if a.get("name") != "Governor" or a.get("status") != "ACTIVE":
        raise ValueError("A-000 lacks expected Governor identity")
    if (a.get("identity_symbol"), a.get("identity_glyph")) != ("resh", "ר"):
        raise ValueError("A-000 resh identity fields mismatch")
    if r.get("glyph") != "ר" or r.get("status") != "ACTIVE" or not isinstance(r.get("aliases"), list) or "A-000" not in r["aliases"]:
        raise ValueError("A-000-RESH alias mismatch")
    return copy.deepcopy({"A-000": a, "A-000-RESH": r})


def attest(known):
    state = snapshot(known)
    return {"schema": "a000-pair-candidate/v1", "sha256": hashlib.sha256(canonical(state)).hexdigest(),
            "detached_state": state}


def verify(known, receipt):
    if not isinstance(receipt, dict) or receipt.get("schema") != "a000-pair-candidate/v1":
        return False
    try:
        current = snapshot(known)
        detached = receipt["detached_state"]
        return (current == detached and
                hashlib.sha256(canonical(detached)).hexdigest() == receipt["sha256"])
    except (ValueError, KeyError, TypeError, OverflowError):
        return False
