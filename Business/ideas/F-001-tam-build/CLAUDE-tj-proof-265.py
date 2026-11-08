"""F-001 §265 (Claude 20Z): PROPOSED proof shape for EB-TJ (Timothy's editorial sign-off).
§264 limit: a row's writer="timothy" is self-reported. Observed 20Z (SOURCE-OBSERVED, GitHub REST):
Claude's comment 6725739559 and ChatGPT's Issue #362 both show user.login=AGI144348Outlook;
they differ only in performed_via_github_app (claude / chatgpt-codex-connector). Commit author
fields are free text (main 8402a45b: author 'Timothy', unsigned) and prove nothing.
Proposal: EB-TJ cites proof={kind:'issue_comment', id}; the comment record must have
user.login == OWNER and performed_via_github_app == null (posted directly, not through an app),
and its body must name the row id. Fixtures below are the field values only (no comment text,
no personal data); expected codes were written before the first run. Fails closed.
Limit: a personal token used by a script also shows app == null; this narrows, not closes, forgery."""
import json, hashlib

OWNER = "AGI144348Outlook"

def check(eb_tj, records):
    p = eb_tj.get("proof") if isinstance(eb_tj, dict) else None
    if not isinstance(p, dict):
        return "NO_PROOF"
    if p.get("kind") == "commit":
        return "COMMIT_AUTHOR_NOT_PROOF"
    if p.get("kind") != "issue_comment":
        return "PROOF_KIND_UNKNOWN"
    r = records.get(p.get("id"))
    if r is None:
        return "PROOF_NOT_FOUND"
    if r.get("login") != OWNER:
        return "NOT_OWNER"
    if r.get("app") is not None:
        return "POSTED_VIA_APP"
    if eb_tj.get("row") not in r.get("names_rows", []):
        return "ROW_NOT_NAMED"
    return "OK_TJ"

# observed field values (20Z) + synthetic records S1..S3
RECORDS = {
    6725739559: {"login": OWNER, "app": "claude", "names_rows": ["R1"]},          # real: Claude 19Z #13 note
    "issue-362": {"login": OWNER, "app": "chatgpt-codex-connector", "names_rows": ["R1"]},  # real: GPT #362
    "S1": {"login": OWNER, "app": None, "names_rows": ["R1"]},
    "S2": {"login": "someone-else", "app": None, "names_rows": ["R1"]},
    "S3": {"login": OWNER, "app": None, "names_rows": ["R2"]},
}
FIXTURES = [
    ("T1 real Claude comment cited", {"row": "R1", "proof": {"kind": "issue_comment", "id": 6725739559}}, "POSTED_VIA_APP"),
    ("T2 real GPT issue cited", {"row": "R1", "proof": {"kind": "issue_comment", "id": "issue-362"}}, "POSTED_VIA_APP"),
    ("T3 direct owner comment naming row", {"row": "R1", "proof": {"kind": "issue_comment", "id": "S1"}}, "OK_TJ"),
    ("T4 other login", {"row": "R1", "proof": {"kind": "issue_comment", "id": "S2"}}, "NOT_OWNER"),
    ("T5 comment names other row", {"row": "R1", "proof": {"kind": "issue_comment", "id": "S3"}}, "ROW_NOT_NAMED"),
    ("T6 commit 8402a45b cited", {"row": "R1", "proof": {"kind": "commit", "id": "8402a45b"}}, "COMMIT_AUTHOR_NOT_PROOF"),
    ("T7 no proof (writer field only)", {"row": "R1", "writer": "timothy"}, "NO_PROOF"),
    ("T8 unknown comment id", {"row": "R1", "proof": {"kind": "issue_comment", "id": 1}}, "PROOF_NOT_FOUND"),
    ("T9 unknown kind", {"row": "R1", "proof": {"kind": "email", "id": "x"}}, "PROOF_KIND_UNKNOWN"),
]
out = []
for name, row, exp in FIXTURES:
    got = check(row, RECORDS)
    out.append({"fixture": name, "expected": exp, "got": got, "match": got == exp})
res = {"script": "CLAUDE-tj-proof-265.py", "matched": sum(o["match"] for o in out), "total": len(out), "results": out}
s = json.dumps(res, indent=1, sort_keys=True)
print(s)
