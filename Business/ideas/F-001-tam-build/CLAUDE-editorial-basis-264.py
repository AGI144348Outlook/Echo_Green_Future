"""F-001 §264 (Claude 19Z): executable form of the §263 PROPOSED editorial-basis rule.
Synthetic fixtures only; no TAM text. Expected codes are written below BEFORE the first run.
Proposal, not adopted: field names and the code list are ChatGPT's schema / Timothy's decision.
Rule: editorial=APPROVED needs basis = list of {code, blob}; codes subset of VOCAB;
EB-TJ present; >=1 machine code; each machine code has a 7..40 hex blob; EB-TJ has no blob
and may not be written by an agent (writer != 'timothy' -> EB_TJ_NOT_BY_AGENT).
Machine codes without EB-TJ -> REVIEW_READY (not an error, not APPROVED). HOLD needs no basis."""
import json, hashlib, sys, re

VOCAB = {"EB-SPAN", "EB-JOIN", "EB-QUOTE", "EB-TJ"}
HEX = re.compile(r"^[0-9a-f]{7,40}$")

def check(row):
    if not isinstance(row, dict):
        return ["ROW_NOT_OBJECT"]
    ed = row.get("editorial")
    if ed == "HOLD":
        return ["OK_HOLD"]
    if ed != "APPROVED":
        return ["BAD_EDITORIAL_DECISION"]
    basis = row.get("basis")
    if not isinstance(basis, list) or not basis:
        return ["BASIS_NOT_LIST"]
    errs, codes = [], []
    for b in basis:
        if not isinstance(b, dict) or not isinstance(b.get("code"), str):
            errs.append("BASIS_ITEM_MALFORMED"); continue
        c = b["code"]; codes.append(c)
        if c not in VOCAB:
            errs.append("BASIS_CODE_UNKNOWN")
        elif c == "EB-TJ":
            if b.get("writer") != "timothy":
                errs.append("EB_TJ_NOT_BY_AGENT")
        elif not (isinstance(b.get("blob"), str) and HEX.match(b["blob"])):
            errs.append("MACHINE_CODE_NO_BLOB")
    if errs:
        return sorted(set(errs))
    machine = [c for c in codes if c != "EB-TJ"]
    if not machine:
        return ["NO_MACHINE_CODE"]
    if "EB-TJ" not in codes:
        return ["REVIEW_READY"]
    return ["OK_APPROVED"]

S, J = {"code": "EB-SPAN", "blob": "81e48b0e"}, {"code": "EB-JOIN", "blob": "efa621d4"}
TJ = {"code": "EB-TJ", "writer": "timothy"}
CASES = [  # (id, row, expected) -- written before first run
    ("B1", {"editorial": "APPROVED", "basis": "anything"}, ["BASIS_NOT_LIST"]),  # v14 P1 free text
    ("B2", {"editorial": "APPROVED", "basis": [S, TJ]}, ["OK_APPROVED"]),
    ("B3", {"editorial": "APPROVED", "basis": [S, J]}, ["REVIEW_READY"]),
    ("B4", {"editorial": "APPROVED", "basis": [TJ]}, ["NO_MACHINE_CODE"]),
    ("B5", {"editorial": "APPROVED", "basis": [S, {"code": "EB-TJ", "writer": "claude"}]}, ["EB_TJ_NOT_BY_AGENT"]),
    ("B6", {"editorial": "APPROVED", "basis": [{"code": "EB-SPAN"}, TJ]}, ["MACHINE_CODE_NO_BLOB"]),
    ("B7", {"editorial": "APPROVED", "basis": [{"code": "EB-VIBES", "blob": "abcdef1"}, TJ]}, ["BASIS_CODE_UNKNOWN"]),
    ("B8", {"editorial": "HOLD"}, ["OK_HOLD"]),
    ("B9", {"editorial": "APPROVED", "basis": [{"code": "EB-SPAN", "blob": "81E48B0E"}, TJ]}, ["MACHINE_CODE_NO_BLOB"]),
    ("B10", {"editorial": "approved", "basis": [S, TJ]}, ["BAD_EDITORIAL_DECISION"]),
    ("B11", {"editorial": "APPROVED", "basis": [S, 7, TJ]}, ["BASIS_ITEM_MALFORMED"]),
    ("B12", None, ["ROW_NOT_OBJECT"]),
]

def main():
    res = []
    for cid, row, exp in CASES:
        got = check(row)
        res.append({"id": cid, "expected": exp, "got": got, "match": got == exp})
    out = {"section": "264", "cases": res,
           "matched": sum(r["match"] for r in res), "total": len(res)}
    text = json.dumps(out, sort_keys=True, indent=1) + "\n"
    sys.stdout.write(text)
    sys.stdout.write("sha256=" + hashlib.sha256(text.encode()).hexdigest() + "\n")

if __name__ == "__main__":
    main()
