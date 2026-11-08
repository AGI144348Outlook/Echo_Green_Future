import sys,json,hashlib,importlib.util
spec=importlib.util.spec_from_file_location('v',sys.argv[1]);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
src='synthetic TAM fixture – no publication'.encode();d=hashlib.sha256(src).hexdigest()
ok={'occurrence_id':'O1','start':0,'end':9,'quote_sha256':hashlib.sha256(src[:9]).hexdigest()}
cases={
 'E1_missing_quote_key':(dict((k,x) for k,x in ok.items() if k!='quote_sha256'),{}),
 'E2_bool_start':(dict(ok,start=False),{}),
 'E3_uppercase_quote_sha':(dict(ok,quote_sha256=ok['quote_sha256'].upper()),{}),
 'E4_end_eq_len_ok':(dict(ok,end=len(src),quote_sha256=hashlib.sha256(src).hexdigest()),{}),
 'E5_rights_HOLDX_prefix_zero_refs':(None,{'rights':'HOLDOUT-APPROVED'}),
 'E6_editorial_approved_no_basis':(ok,{'editorial':'APPROVED','approval_basis':''}),
 'E7_utf8_midchar_split':(dict(ok,start=22,end=23,quote_sha256=hashlib.sha256(src[22:23]).hexdigest()),{}),
}
out={}
for k,(ref,kw) in cases.items():
    refs=[] if ref is None else [ref]
    try: r=v.validate('SYN',refs,src,d,**kw); out[k]={'errors':r['errors'],'release':r['release']}
    except Exception as e: out[k]={'exception':type(e).__name__+': '+str(e)}
print(json.dumps(out,indent=1,sort_keys=True,ensure_ascii=False))
