"""F-001 N1/N2 experimental evidence gate. No publication authority."""
import hashlib
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def evaluate(record, manifest, receipt=None):
    errors=[]
    ev=record.get("evidence", [])
    if not ev: errors.append("N1_EMPTY_EVIDENCE")
    if record.get("machine_verified"): errors.append("N2_CALLER_ASSERTED_MACHINE_LABEL")
    if record.get("source_hash") != sha(manifest.get("source", "")): errors.append("SOURCE_HASH_MISMATCH")
    if record.get("quote_hash") != sha(manifest.get("quote", "")): errors.append("QUOTE_HASH_MISMATCH")
    if "rights" not in record: errors.append("RIGHTS_MISSING")
    elif record["rights"] != "cleared": errors.append("RIGHTS_NOT_CLEARED")
    if receipt is None: errors.append("EDITORIAL_RECEIPT_MISSING")
    elif receipt.get("trusted_source") != "independent_custodian": errors.append("EDITORIAL_RECEIPT_UNVERIFIED")
    elif receipt.get("digest") != sha(manifest.get("source", "") + "|" + manifest.get("quote", "")): errors.append("EDITORIAL_RECEIPT_FORGED")
    if len(ev) != len(set(ev)): errors.append("DUPLICATE_EVIDENCE_JOIN")
    return {"review": "REVIEW_READY" if not errors else "HOLD", "release": "HOLD", "errors": errors}
