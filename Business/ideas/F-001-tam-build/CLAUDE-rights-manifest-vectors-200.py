# F-001 §200 (Claude, 2026-11-06 00Z): PROPOSED acceptance vectors for a rights-manifest validator (ChatGPT 23Z "next:
# rights manifest validator against approved source list"). Reference rules = §198 crosswalk. SYNTHETIC rows only:
# no manuscript text, no real passage ids, no decision on any real passage. Stdlib, deterministic. Not legal advice.
import json, re
APPROVED = {"a" * 40}  # stand-in for "approved source list": full 40-hex blob ids pinned by Timothy (none approved yet)
BASIS = {"own", "third-party-permission", "third-party-public-domain", "unsure"}
DECISION = {"ACCEPT", "HOLD", "REJECT"}
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?Z$")
def validate(r):
    """Returns (verdict, reason). verdict: VALID-ACCEPT | VALID-HOLD | VALID-REJECT | INVALID. Fail closed."""
    need = ["passage_id", "source_blob_sha", "source_range", "rights_basis", "evidence_reference", "reviewer", "decision", "reviewed_at"]
    for k in need:
        if k not in r: return "INVALID", f"missing {k}"
    if not re.fullmatch(r"[0-9a-f]{40}", r["source_blob_sha"]): return "INVALID", "blob not full 40-hex"
    if r["source_blob_sha"] not in APPROVED: return "INVALID", "blob not on approved source list"
    if not re.fullmatch(r"\d+:\d+\+\d+", r["source_range"]): return "INVALID", "range must be line:col+chars (no text)"
    if r["rights_basis"] not in BASIS: return "INVALID", "unknown rights_basis (no fair-use value exists)"
    if r["decision"] not in DECISION: return "INVALID", "unknown decision"
    if r["decision"] == "HOLD": return "VALID-HOLD", "default"
    if not TS.match(r["reviewed_at"] or ""): return "INVALID", "decided row needs UTC reviewed_at"
    if r["decision"] == "ACCEPT":
        if r["reviewer"] != "timothy": return "INVALID", "only Timothy can ACCEPT"
        if r["rights_basis"] == "unsure": return "INVALID", "unsure is always HOLD"
        if not r["evidence_reference"]: return "INVALID", "ACCEPT needs an evidence pointer"
        return "VALID-ACCEPT", "ok"
    return "VALID-REJECT", "ok"
B = {"passage_id": "synthetic:1:1", "source_blob_sha": "a" * 40, "source_range": "1:1+10", "rights_basis": "own",
     "evidence_reference": "", "reviewer": "", "decision": "HOLD", "reviewed_at": ""}
def v(**kw): r = dict(B); r.update(kw); return r
CASES = [  # (name, row, expected verdict)
 ("default hold", v(), "VALID-HOLD"),
 ("missing field", {k: x for k, x in B.items() if k != "rights_basis"}, "INVALID"),
 ("7-hex blob", v(source_blob_sha="aaaaaaa"), "INVALID"),
 ("blob not approved", v(source_blob_sha="b" * 40), "INVALID"),
 ("quoted text in range", v(source_range="some quoted words"), "INVALID"),
 ("fair-use basis", v(rights_basis="fair-use"), "INVALID"),
 ("AI reviewer accepts", v(decision="ACCEPT", reviewer="claude", evidence_reference="commit x", reviewed_at="2026-11-06T00:00Z"), "INVALID"),
 ("unsure accepted", v(decision="ACCEPT", reviewer="timothy", rights_basis="unsure", evidence_reference="note", reviewed_at="2026-11-06T00:00Z"), "INVALID"),
 ("accept without evidence", v(decision="ACCEPT", reviewer="timothy", reviewed_at="2026-11-06T00:00Z"), "INVALID"),
 ("accept without timestamp", v(decision="ACCEPT", reviewer="timothy", evidence_reference="note"), "INVALID"),
 ("valid accept", v(decision="ACCEPT", reviewer="timothy", evidence_reference="note", reviewed_at="2026-11-06T00:00Z"), "VALID-ACCEPT"),
 ("valid reject by Claude", v(decision="REJECT", reviewer="claude", rights_basis="unsure", reviewed_at="2026-11-06T00:00Z"), "VALID-REJECT"),
]
out = [{"case": n, "expected": e, "got": validate(r)[0], "reason": validate(r)[1]} for n, r, e in CASES]
print(json.dumps({"pass": sum(o["expected"] == o["got"] for o in out), "total": len(out), "cases": out}, indent=1))
