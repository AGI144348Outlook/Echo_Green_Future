"""F-001 custody validation v14: synthetic-only, fail closed. Preregistered Issue #357."""
import hashlib,re,json
SHA=re.compile(r"[0-9a-f]{64}\Z")
def validate(unit,refs,source_bytes,expected_source_sha,rights="HOLD",editorial="HOLD",approval_basis=""):
    errors=[]
    if not isinstance(source_bytes,bytes):return {"errors":["BAD_SOURCE_TYPE"],"release":"HOLD"}
    if not isinstance(expected_source_sha,str) or not SHA.fullmatch(expected_source_sha):errors.append("BAD_SHA256_FORMAT")
    elif hashlib.sha256(source_bytes).hexdigest()!=expected_source_sha:errors.append("SOURCE_HASH_MISMATCH")
    if rights not in ("HOLD","APPROVED","REJECTED"):errors.append("BAD_RIGHTS_DECISION")
    if editorial not in ("HOLD","APPROVED","REJECTED"):errors.append("BAD_EDITORIAL_DECISION")
    if not refs and rights!="HOLD":errors.append("ZERO_REFS_WITHOUT_HOLD")
    if editorial=="APPROVED" and (not approval_basis or approval_basis=="overlap-only"):errors.append("UNSUPPORTED_EDITORIAL_APPROVAL")
    seen=set()
    for ref in refs:
        if not isinstance(ref,dict):errors.append("BAD_REFERENCE");continue
        occ=ref.get("occurrence_id")
        if not isinstance(occ,str) or not occ:errors.append("BAD_OCCURRENCE");continue
        key=(unit,occ)
        if key in seen:errors.append("DUPLICATE_JOIN")
        seen.add(key)
        a,b=ref.get("start"),ref.get("end")
        if type(a) is not int or type(b) is not int or a<0 or b<=a or b>len(source_bytes):
            errors.append("BAD_RANGE");continue
        try:
            source_bytes[:a].decode("utf-8");source_bytes[a:b].decode("utf-8")
        except UnicodeDecodeError:errors.append("BAD_UTF8_BOUNDARY");continue
        digest=ref.get("quote_sha256")
        if not isinstance(digest,str) or not SHA.fullmatch(digest):
            errors.append("BAD_QUOTE_SHA256_FORMAT");continue
        if hashlib.sha256(source_bytes[a:b]).hexdigest()!=digest:errors.append("QUOTE_HASH_MISMATCH")
    return {"errors":sorted(set(errors)),"release":"HOLD"}
def run():
    s="aébc".encode();h=hashlib.sha256(s).hexdigest()
    ref={"occurrence_id":"O1","start":0,"end":1,"quote_sha256":hashlib.sha256(s[:1]).hexdigest()}
    cases={
    "positive":not validate("S",[ref],s,h)["errors"],
    "missing_hash":"BAD_QUOTE_SHA256_FORMAT" in validate("S",[dict(ref,quote_sha256=None)],s,h)["errors"],
    "bool_index":"BAD_RANGE" in validate("S",[dict(ref,start=False)],s,h)["errors"],
    "rights_prefix":"BAD_RIGHTS_DECISION" in validate("S",[ref],s,h,rights="HOLDOUT-APPROVED")["errors"],
    "empty_basis":"UNSUPPORTED_EDITORIAL_APPROVAL" in validate("S",[ref],s,h,editorial="APPROVED")["errors"],
    "utf8_split":"BAD_UTF8_BOUNDARY" in validate("S",[dict(ref,start=1,end=2)],s,h)["errors"],
    "duplicate":"DUPLICATE_JOIN" in validate("S",[ref,ref],s,h)["errors"],
    "mutated_source":"SOURCE_HASH_MISMATCH" in validate("S",[ref],s+b"x",h)["errors"],
    "uppercase":"BAD_SHA256_FORMAT" in validate("S",[ref],s,h.upper())["errors"],
    "zero_hold":not validate("S",[],s,h,rights="HOLD")["errors"]}
    return {"checks":cases,"passed":sum(cases.values()),"total":len(cases)}
if __name__=="__main__":print(json.dumps(run(),sort_keys=True))
