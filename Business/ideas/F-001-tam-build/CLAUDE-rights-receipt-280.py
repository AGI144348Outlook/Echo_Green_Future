# F-001 §280 (Claude 11Z): rights-receipt shape v2 + nonce ledger, PRE-REGISTERED (predictions below, pushed before first run).
# v2 adds schema_version, issued_at, expires_at, nonce (§279) and requires the EXACT key set (DISC-002 e118 lesson).
# The expected schema version and "now" come from the HOST argument, never from the receipt (A10).
# Ledger admission is copy-check-swap with nonce reuse refused (DISC-002 e119, A11/A12 PROPOSED).
# Best status is SHAPE_VALID_CHANNEL_CLAIMED: shape only, never authentication or RIGHTS_OK (A8; §279 wording note).
# Synthetic fixtures only; reads RIGHTS-CLASSES-277.tsv for class names; reads no TAM text; no network; stdout only.
# Usage: python3 -I -B CLAUDE-rights-receipt-280.py RIGHTS-CLASSES-277.tsv
import sys, json, csv, copy
from datetime import datetime
CLASSES = {r["class"] for r in csv.DictReader((l for l in open(sys.argv[1]) if not l.startswith("#")), delimiter="\t")}
HOST = {"schema_version": "rights-receipt-v2", "now": "2026-11-09T11:00:00+00:00"}   # protected side (stand-in)
KEYS = {"schema_version", "scope", "target", "source_file_blob", "decision", "decided_by", "channel",
        "mixed_content_checked", "issued_at", "expires_at", "nonce"}
def ts(s):
    try: d = datetime.fromisoformat(s)
    except (TypeError, ValueError): return None
    return d if d.tzinfo else None
def shape(rc, host):
    if not isinstance(rc, dict): return "INVALID_RECEIPT:type"
    if KEYS - set(rc): return "INVALID_RECEIPT:missing=" + ",".join(sorted(KEYS - set(rc)))
    if set(rc) - KEYS: return "INVALID_RECEIPT:extra=" + ",".join(sorted(set(rc) - KEYS))
    if rc["schema_version"] != host["schema_version"]: return "INVALID_RECEIPT:schema_version"
    if rc["scope"] not in ("class", "unit"): return "INVALID_RECEIPT:scope"
    if rc["scope"] == "class" and rc["target"] not in CLASSES: return "INVALID_RECEIPT:unknown_class"
    if rc["decision"] not in ("CLEAR", "REJECT"): return "INVALID_RECEIPT:decision"
    if not (isinstance(rc["nonce"], str) and len(rc["nonce"]) >= 16): return "INVALID_RECEIPT:nonce"
    i, e, now = ts(rc["issued_at"]), ts(rc["expires_at"]), ts(host["now"])
    if i is None or e is None or not i < e: return "INVALID_RECEIPT:time"
    if not i <= now < e: return "EXPIRED_OR_FUTURE"
    if rc["decision"] == "REJECT": return "RIGHTS_REJECTED"   # rejection accepted from any well-formed receipt (fail-closed side)
    if rc["decided_by"] != "Timothy": return "RIGHTS_UNVERIFIED:not_timothy"
    if rc["scope"] == "class" and rc["mixed_content_checked"] is not True: return "RIGHTS_UNVERIFIED:mixed_content_unchecked"
    return "SHAPE_VALID_CHANNEL_CLAIMED"   # channel is a claimed string until Timothy names the trust root (EB-TJ, §270)
def admit(ledger, rc, host, crash=False):   # copy-check-swap; returns (new_ledger, outcome)
    st = shape(rc, host)
    if st.startswith("INVALID") or st == "EXPIRED_OR_FUTURE": return ledger, st + "|NOT_RECORDED"
    if rc["nonce"] in ledger["nonces"]: return ledger, "NONCE_REUSED|NOT_RECORDED"
    shadow = copy.deepcopy(ledger); shadow["nonces"].append(rc["nonce"]); shadow["rows"].append([rc["target"], st])
    if crash: return ledger, "CRASH|ROLLED_BACK"   # injected before the swap
    return shadow, st + "|RECORDED"
base = {"schema_version": "rights-receipt-v2", "scope": "class", "target": "Article 5", "source_file_blob": "0" * 40,
        "decision": "CLEAR", "decided_by": "Timothy", "channel": "issue-comment", "mixed_content_checked": True,
        "issued_at": "2026-11-09T10:00:00+00:00", "expires_at": "2026-11-10T10:00:00+00:00", "nonce": "synthetic-nonce-0001"}
F = [
 ("V0_well_formed", dict(base), False),
 ("V1_replay_same_nonce", dict(base), False),
 ("V2_missing_nonce", {k: v for k, v in base.items() if k != "nonce"}, False),
 ("V3_extra_key_rights_ok", dict(base, nonce="synthetic-nonce-0003", rights_ok=True), False),
 ("V4_unpinned_schema_v3", dict(base, schema_version="rights-receipt-v3", nonce="synthetic-nonce-0004"), False),
 ("V5_expired", dict(base, issued_at="2026-11-01T00:00:00+00:00", expires_at="2026-11-02T00:00:00+00:00", nonce="synthetic-nonce-0005"), False),
 ("V6_naive_timestamp", dict(base, issued_at="2026-11-09T10:00:00", nonce="synthetic-nonce-0006"), False),
 ("V7_reject_by_agent", dict(base, decision="REJECT", decided_by="Claude", nonce="synthetic-nonce-0007"), False),
 ("V8_crash_before_swap", dict(base, nonce="synthetic-nonce-0008"), True),
 ("V9_after_crash_same_nonce", dict(base, nonce="synthetic-nonce-0008"), False),
]
PRED = {"V0_well_formed": "SHAPE_VALID_CHANNEL_CLAIMED|RECORDED", "V1_replay_same_nonce": "NONCE_REUSED|NOT_RECORDED",
        "V2_missing_nonce": "INVALID_RECEIPT:missing=nonce|NOT_RECORDED", "V3_extra_key_rights_ok": "INVALID_RECEIPT:extra=rights_ok|NOT_RECORDED",
        "V4_unpinned_schema_v3": "INVALID_RECEIPT:schema_version|NOT_RECORDED", "V5_expired": "EXPIRED_OR_FUTURE|NOT_RECORDED",
        "V6_naive_timestamp": "INVALID_RECEIPT:time|NOT_RECORDED", "V7_reject_by_agent": "RIGHTS_REJECTED|RECORDED",
        "V8_crash_before_swap": "CRASH|ROLLED_BACK", "V9_after_crash_same_nonce": "SHAPE_VALID_CHANNEL_CLAIMED|RECORDED"}
ledger = {"nonces": [], "rows": []}; out = {}
for name, rc, crash in F:
    ledger, out[name] = admit(ledger, rc, HOST, crash)
res = {"outcomes": out, "match": {k: out[k] == PRED[k] for k in PRED}, "final_ledger": ledger}
res["matched"] = sum(res["match"].values()); res["of"] = len(PRED)
print(json.dumps(res, sort_keys=True))
