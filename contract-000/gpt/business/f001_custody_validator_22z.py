"""F-001 GPT v15 synthetic custody gate; preregistered Issue #365. No release authority."""
import hashlib,re,json
SHA=re.compile(r"[0-9a-f]{64}\Z")
MACHINE={"EB-SPAN","EB-JOIN","EB-QUOTE"}
def validate(unit,refs,source,expected_sha,rights="HOLD",evidence=(),authenticated_tj=False):
    errors=[]
    if not isinstance(source,bytes):return {"errors":["BAD_SOURCE"],"state":"HOLD"}
    if not isinstance(expected_sha,str) or not SHA.fullmatch(expected_sha):errors.append("BAD_SOURCE_SHA")
    elif hashlib.sha256(source).hexdigest()!=expected_sha:errors.append("SOURCE_MISMATCH")
    if rights not in ("HOLD","APPROVED","REJECTED"):errors.append("BAD_RIGHTS")
    if not isinstance(refs,list):return {"errors":sorted(set(errors+["BAD_REFS"])),"state":"HOLD"}
    if not isinstance(evidence,(list,tuple)) or any(not isinstance(x,str) or x not in MACHINE|{"EB-TJ"} for x in evidence):errors.append("BAD_EVIDENCE")
    if "EB-TJ" in evidence and not authenticated_tj:errors.append("UNAUTHENTICATED_TJ")
    if authenticated_tj and "EB-TJ" not in evidence:errors.append("MISSING_TJ_RECEIPT")
    seen=set()
    for ref in refs:
        if not isinstance(ref,dict):errors.append("BAD_REF");continue
        occ=ref.get("occurrence_id")
        if not isinstance(occ,str) or not occ:errors.append("BAD_OCCURRENCE");continue
        key=(unit,occ)
        if key in seen:errors.append("DUPLICATE_JOIN")
        seen.add(key)
        a,b=ref.get("start"),ref.get("end")
        if type(a) is not int or type(b) is not int or a<0 or b<=a or b>len(source):errors.append("BAD_RANGE");continue
        try:source[:a].decode("utf-8");source[a:b].decode("utf-8")
        except UnicodeDecodeError:errors.append("BAD_UTF8");continue
        h=ref.get("quote_sha256")
        if not isinstance(h,str) or not SHA.fullmatch(h):errors.append("BAD_QUOTE_SHA")
        elif hashlib.sha256(source[a:b]).hexdigest()!=h:errors.append("QUOTE_MISMATCH")
    return {"errors":sorted(set(errors)),"state":"REVIEW_READY" if not errors and evidence and set(evidence)&MACHINE else "HOLD","release":"HOLD"}
def probes():
    s="aébc".encode(); h=hashlib.sha256(s).hexdigest()
    ref={"occurrence_id":"O1","start":0,"end":1,"quote_sha256":hashlib.sha256(s[:1]).hexdigest()}
    def has(code,refs=None,**kw):return code in validate("U1",[ref] if refs is None else refs,s,h,**kw)["errors"]
    checks={
      "valid_review":validate("U1",[ref],s,h,evidence=["EB-SPAN"])["state"]=="REVIEW_READY",
      "never_release":validate("U1",[ref],s,h,rights="APPROVED",evidence=["EB-SPAN","EB-TJ"],authenticated_tj=True)["release"]=="HOLD",
      "duplicate":has("DUPLICATE_JOIN",[ref,ref]),
      "boolean_range":has("BAD_RANGE",[dict(ref,start=True)]),
      "utf8_boundary":has("BAD_UTF8",[dict(ref,start=1,end=2)]),
      "quote_hash":has("BAD_QUOTE_SHA",[dict(ref,quote_sha256=None)]),
      "rights":has("BAD_RIGHTS",rights="APPROVED-OTHER"),
      "fake_tj":has("UNAUTHENTICATED_TJ",evidence=["EB-TJ"]),
      "unknown_evidence":has("BAD_EVIDENCE",evidence=["EB-UNKNOWN"]),
      "source_mutation":"SOURCE_MISMATCH" in validate("U1",[ref],s+b"x",h)["errors"],
      "missing_refs":"BAD_REFS" in validate("U1",None,s,h)["errors"],
      "missing_receipt":has("MISSING_TJ_RECEIPT",evidence=["EB-SPAN"],authenticated_tj=True)}
    return {"checks":checks,"passed":sum(checks.values()),"total":len(checks)}
if __name__=="__main__":print(json.dumps(probes(),sort_keys=True))
