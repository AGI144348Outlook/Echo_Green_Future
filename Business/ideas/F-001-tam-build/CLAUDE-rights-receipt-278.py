# F-001 §278 (Claude 09Z): rights-receipt shape check for one class or unit decision. Synthetic fixtures only;
# reads RIGHTS-CLASSES-277.tsv for class names; reads no TAM text; no network; prints to stdout only.
import sys, json, csv
CLASSES = {r["class"] for r in csv.DictReader((l for l in open(sys.argv[1]) if not l.startswith("#")), delimiter="\t")}
REQ = ["scope", "target", "source_file_blob", "decision", "decided_by", "channel", "mixed_content_checked"]
def status(rc):
    miss = [k for k in REQ if k not in rc]
    if miss: return "INVALID_RECEIPT:missing=" + ",".join(miss)
    if rc["scope"] not in ("class", "unit"): return "INVALID_RECEIPT:scope"
    if rc["scope"] == "class" and rc["target"] not in CLASSES: return "INVALID_RECEIPT:unknown_class"
    if rc["decision"] not in ("CLEAR", "REJECT"): return "INVALID_RECEIPT:decision"
    if rc["decision"] == "REJECT": return "RIGHTS_REJECTED"   # a rejection is accepted from any well-formed receipt (fail-closed side)
    if rc["decided_by"] != "Timothy": return "RIGHTS_UNVERIFIED:not_timothy"
    if rc["scope"] == "class" and rc["mixed_content_checked"] is not True: return "RIGHTS_UNVERIFIED:mixed_content_unchecked"
    if rc["channel"] != "EB-TJ-verified": return "CLASS_CLEARED_PENDING_RECORD" if rc["scope"] == "class" else "UNIT_CLEARED_PENDING_RECORD"
    return "RIGHTS_OK_CANDIDATE"   # still not release: Timothy's A1-A5 and release approval remain separate
base = {"scope": "class", "target": "Article 5", "source_file_blob": "0"*40, "decision": "CLEAR", "decided_by": "Timothy", "channel": "issue-comment", "mixed_content_checked": True}
F = {
 "R0_well_formed_class_clear_unverified_channel": dict(base),
 "R1_missing_blob": {k: v for k, v in base.items() if k != "source_file_blob"},
 "R2_decided_by_agent": dict(base, decided_by="ChatGPT"),
 "R3_class_clear_mixed_unchecked": dict(base, mixed_content_checked=False),
 "R4_unknown_class": dict(base, target="Article 99"),
 "R5_reject_by_anyone": dict(base, decision="REJECT", decided_by="Claude"),
 "R6_verified_channel": dict(base, channel="EB-TJ-verified"),
 "R7_string_true_not_bool": dict(base, mixed_content_checked="true"),
}
print(json.dumps({k: status(v) for k, v in F.items()}, sort_keys=True))
