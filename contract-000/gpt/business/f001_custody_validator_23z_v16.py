"""F-001 v16: synthetic custody REVIEW gate, NEVER release authority. Issue #366."""
import hashlib, json, re
HEX = re.compile(r"[0-9a-f]{64}\Z")
MACHINE = {"EB-SPAN","EB-JOIN","EB-QUOTE"}
def validate(unit, refs, source, source_sha, rights="HOLD", evidence=(), receipt=None):
    err=[]
    def add(x): err.append(x)
    if not isinstance(unit,str) or not unit.strip(): add("BAD_UNIT")
    if not isinstance(source,bytes): add("BAD_SOURCE"); source=b""
    if not isinstance(source_sha,str) or not HEX.fullmatch(source_sha): add("BAD_SOURCE_SHA")
    elif hashlib.sha256(source).hexdigest()!=source_sha: add("SOURCE_MISMATCH")
    if rights not in ("HOLD","APPROVED","REJECTED"): add("BAD_RIGHTS")
    if rights=="REJECTED": add("RIGHTS_REJECTED")
    if not isinstance(evidence,(list,tuple)) or any(not isinstance(x,str) or x not in MACHINE|{"EB-TJ"} for x in evidence): add("BAD_EVIDENCE"); evidence=()
    if "EB-TJ" in evidence: add("TJ_UNVERIFIED") # No server-side receipt verifier in this pure function.
    if receipt is not None: add("UNVERIFIED_RECEIPT") # Never trust caller-provided claims.
    if not isinstance(refs,list): add("BAD_REFS"); refs=[]
    if not refs: add("EMPTY_REFS")
    seen=set()
    for ref in refs:
        if not isinstance(ref,dict): add("BAD_REF"); continue
        occ=ref.get("occurrence_id")
        if not isinstance(occ,str) or not occ: add("BAD_OCCURRENCE"); continue
        key=(unit,occ)
        if key in seen: add("DUPLICATE_JOIN")
        seen.add(key)
        a,b=ref.get("start"),ref.get("end")
        if type(a)!=int or type(b)!=int or a<0 or b<=a or b>len(source): add("BAD_RANGE"); continue
        try: source[:a].decode("utf-8"); source[a:b].decode("utf-8")
        except UnicodeDecodeError: add("BAD_UTF8"); continue
        h=ref.get("quote_sha256")
        if not isinstance(h,str) or not HEX.fullmatch(h): add("BAD_QUOTE_SHA")
        elif hashlib.sha256(source[a:b]).hexdigest()!=h: add("QUOTE_MISMATCH")
    return {"errors":sorted(set(err)), "state":"REVIEW_READY" if not err and set(evidence)&MACHINE else "HOLD", "release":"HOLD"}
def probes():
    src="aébc".encode(); sha=hashlib.sha256(src).hexdigest()
    ref={"occurrence_id":"O1","start":0,"end":1,"quote_sha256":hashlib.sha256(src[:1]).hexdigest()}
    def gate(**kw):
        p={"unit":"U1","refs":[ref],"source":src,"source_sha":sha,"evidence":["EB-SPAN"]}
        p.update(kw); return validate(**p)
    tests={
      "valid_review":gate()["state"]=="REVIEW_READY",
      "empty_refs":gate(refs=[])["state"]=="HOLD",
      "rejected_rights":gate(rights="REJECTED")["state"]=="HOLD",
      "invalid_unit":gate(unit=None)["state"]=="HOLD",
      "forged_authority":gate(evidence=["EB-SPAN","EB-TJ"],receipt={"authenticated_tj":"false"})["state"]=="HOLD",
      "duplicate_join":"DUPLICATE_JOIN" in gate(refs=[ref,ref])["errors"],
      "utf8_boundary":"BAD_UTF8" in gate(refs=[dict(ref,start=1,end=2)])["errors"],
      "quote_mismatch":"QUOTE_MISMATCH" in gate(refs=[dict(ref,quote_sha256="0"*64)])["errors"],
      "source_mismatch":"SOURCE_MISMATCH" in gate(source=src+b"x")["errors"],
      "schema_consistency":all(set(gate(**x))=={"errors","state","release"} and gate(**x)["release"]=="HOLD" for x in ({},{"refs":None},{"source":None},{"evidence":None}))
    }
    return {"tests":tests,"passed":sum(tests.values()),"total":len(tests)}
if __name__=="__main__": print(json.dumps(probes(),sort_keys=True))
