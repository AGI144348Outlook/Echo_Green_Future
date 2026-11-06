"""F-001 TAM Protocol ebook rights gate. DRAFT ONLY; NOT TESTED.
Input JSON: {"passages":[{"passage_id","source_id","immutable_digest",
"rights_basis","rights_evidence_ref","reviewer","reviewed_at",
"permitted_scope","decision"}]}.
All fields must be nonempty strings; decision exactly ALLOW; duplicate passage IDs fail.
An ALLOW record is NOT proof of ownership: human verification and explicit
Timothy publication approval remain mandatory independent gates.
Usage (after preregistration for any repository test): python f001_rights_gate_v1.py manifest.json
"""
import json,sys
REQUIRED=("passage_id","source_id","immutable_digest","rights_basis",
          "rights_evidence_ref","reviewer","reviewed_at","permitted_scope","decision")
def validate(document):
    errors=[]
    rows=document.get("passages") if isinstance(document,dict) else None
    if not isinstance(rows,list) or not rows:
        return ["passages must be a nonempty list"]
    seen=set()
    for i,row in enumerate(rows):
        if not isinstance(row,dict):
            errors.append(f"{i}: not an object");continue
        for key in REQUIRED:
            if not isinstance(row.get(key),str) or not row[key].strip():
                errors.append(f"{i}: missing {key}")
        ident=row.get("passage_id")
        if ident in seen:errors.append(f"{i}: duplicate passage_id")
        seen.add(ident)
        if row.get("decision")!="ALLOW":errors.append(f"{i}: not explicitly ALLOW")
        if row.get("permitted_scope") not in ("ebook-pdf","ebook-epub","ebook-pdf-and-epub"):
            errors.append(f"{i}: unsupported publication scope")
    return errors
if __name__=="__main__":
    errors=validate(json.load(open(sys.argv[1],encoding="utf-8")))
    print(json.dumps({"status":"HOLD" if errors else "MANIFEST_STRUCTURALLY_COMPLETE_NOT_RIGHTS_CLEARED","errors":errors}))
    sys.exit(1 if errors else 0)
