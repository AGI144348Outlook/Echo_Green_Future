"""GPT-only offline F-001 release-gate draft. UNTESTED. Never release authority."""
def inspect_manifest(m):
    if not isinstance(m, dict): return ("HOLD", ["MANIFEST_TYPE"])
    required = ("source_sha256", "editorial_receipts", "rights_receipts", "issuer_verified_external", "pdf_sha256", "epub_sha256", "accessibility_qa", "android_qa", "timothy_release_approval")
    failures = ["MISSING_"+key.upper() for key in required if key not in m]
    def digest(s):
        return isinstance(s,str) and len(s)==64 and all(c in "0123456789abcdef" for c in s)
    for key in ("source_sha256","pdf_sha256","epub_sha256"):
        if key in m and not digest(m[key]): failures.append("INVALID_"+key.upper())
    for key in ("issuer_verified_external","accessibility_qa","android_qa","timothy_release_approval"):
        if key in m and m[key] is not True: failures.append("NOT_APPROVED_"+key.upper())
    for key,count in (("editorial_receipts",82),("rights_receipts",70)):
        if key in m:
            v=m[key]
            if not isinstance(v,list) or len(v)!=count or not all(isinstance(x,dict) and x.get("approved") is True and isinstance(x.get("id"),str) for x in v) or len({x["id"] for x in v if isinstance(x,dict) and isinstance(x.get("id"),str)})!=count:
                failures.append("INCOMPLETE_"+key.upper())
    # Boolean issuer flag is not independently authenticated authority.
    if "issuer_verified_external" in m: failures.append("EXTERNAL_AUTHENTICATION_UNVERIFIED")
    return ("HOLD", failures or ["INDEPENDENT_AUTHORITY_REQUIRED"])
