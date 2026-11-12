"""F-001 inert receipt boundary; intentionally cannot authorize release.
Offline-only. No signature verifier or trust root is configured.
"""
import json
import hashlib
from pathlib import Path

class DuplicateKey(ValueError):
    pass

def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result

def hold(raw, root, now, seen=frozenset()):
    """Return (HOLD, reason), never PASS. No file writes."""
    try:
        obj = json.loads(raw, object_pairs_hook=unique_pairs)
        if not isinstance(obj, dict):
            return "HOLD", "not-object"
        required = ("issuer", "edition", "nonce", "expires", "artifact", "sha256", "editorial", "rights")
        if any(k not in obj for k in required):
            return "HOLD", "missing-field"
        if not isinstance(obj["issuer"], str) or not obj["issuer"].strip():
            return "HOLD", "issuer"
        if type(obj["expires"]) not in (int, float) or obj["expires"] <= now:
            return "HOLD", "expiry"
        if obj["nonce"] in seen:
            return "HOLD", "replay"
        if not isinstance(obj["rights"], list) or not obj["rights"] or any(x != "approved" for x in obj["rights"]):
            return "HOLD", "rights"
        if not isinstance(obj["editorial"], list) or not obj["editorial"] or any(x != "approved" for x in obj["editorial"]):
            return "HOLD", "editorial"
        base = Path(root).resolve(strict=True)
        file = (base / obj["artifact"]).resolve(strict=True)
        if not file.is_relative_to(base) or not file.is_file():
            return "HOLD", "path"
        digest = obj["sha256"]
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            return "HOLD", "digest-format"
        if hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            return "HOLD", "digest-mismatch"
        return "HOLD", "no-independent-trust-root"
    except (ValueError, TypeError, KeyError, OSError):
        return "HOLD", "invalid-evidence"
