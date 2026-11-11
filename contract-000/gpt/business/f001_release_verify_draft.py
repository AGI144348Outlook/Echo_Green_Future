#!/usr/bin/env python3
"""F-001 draft fail-closed evidence verifier. NOT TESTED; never authorizes publication."""
import csv, hashlib, json, pathlib, sys
REQUIRED=("manifest.json","book.pdf","book.epub","editorial.csv","rights.csv","qa.json","approvals.json")
def pairs_unique(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise ValueError("duplicate JSON key: "+k)
        d[k]=v
    return d
def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=pairs_unique)
def verify(root):
    root=pathlib.Path(root).resolve(strict=True)
    if not root.is_dir(): raise ValueError("candidate is not directory")
    for name in REQUIRED:
        p=root/name
        if p.is_symlink() or not p.is_file() or p.resolve(strict=True).parent!=root:
            raise ValueError("missing/unsafe artifact: "+name)
    manifest=load_json(root/"manifest.json")
    hashes=manifest.get("sha256")
    if not isinstance(hashes,dict) or set(hashes)!=(set(REQUIRED)-{"manifest.json"}):
        raise ValueError("manifest must hash every evidence artifact")
    for name,digest in hashes.items():
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("bad sha256 syntax")
        actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
        if actual!=digest: raise ValueError("sha256 mismatch: "+name)
    for name,expected in (("editorial.csv",82),("rights.csv",70)):
        with (root/name).open(newline="",encoding="utf-8-sig") as f:
            rows=list(csv.DictReader(f))
        if len(rows)!=expected or any(not x.get("item_id") or not x.get("decision") or not x.get("evidence_ref") for x in rows):
            raise ValueError("incomplete "+name)
        if len({x["item_id"] for x in rows})!=expected: raise ValueError("duplicate item_id")
    qa=load_json(root/"qa.json")
    approvals=load_json(root/"approvals.json")
    if not isinstance(qa,dict) or not isinstance(approvals,dict):
        raise ValueError("invalid QA or approval object")
    # No independent trust-root verifier is implemented. Never treat self-supplied approvals as authority.
    return {"status":"HOLD","reason":"independent issuer authorization not implemented","hashes_verified":True}
if __name__=="__main__":
    try:
        result=verify(sys.argv[1]);print(json.dumps(result,sort_keys=True));sys.exit(2)
    except Exception as exc:
        print(json.dumps({"status":"HOLD","reason":str(exc)}));sys.exit(2)
