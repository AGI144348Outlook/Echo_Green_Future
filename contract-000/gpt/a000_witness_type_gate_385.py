#!/usr/bin/env python3
"""PROPOSED A-000 detached witness comparison hardening; synthetic-only.

This changes only comparison semantics, NOT issuance, custody, revocation,
rollback protection, canonical identity policy, or the production Governor.
"""
import hashlib
import hmac
from a000_detached_witness_384 import canonical, snapshot


def verify_strict(known, receipt):
    if not isinstance(receipt, dict) or receipt.get("schema") != "a000-pair-candidate/v1":
        return False
    try:
        current_bytes = canonical(snapshot(known))
        receipt_bytes = canonical(receipt["detached_state"])
        digest = hashlib.sha256(receipt_bytes).hexdigest()
        return (hmac.compare_digest(current_bytes, receipt_bytes)
                and hmac.compare_digest(digest, receipt["sha256"]))
    except (ValueError, KeyError, TypeError, OverflowError):
        return False
