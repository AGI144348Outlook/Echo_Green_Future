import sys,json,hashlib,importlib.util
spec=importlib.util.spec_from_file_location("v15",sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
s="aébc".encode();h=hashlib.sha256(s).hexdigest()
ref={"occurrence_id":"O1","start":0,"end":1,"quote_sha256":hashlib.sha256(s[:1]).hexdigest()}
V=m.validate
r={
 "C1_empty_refs_review_ready":V("U1",[],s,h,evidence=["EB-SPAN"]),
 "C2_rights_rejected_still_review_ready":V("U1",[ref],s,h,rights="REJECTED",evidence=["EB-SPAN"]),
 "C3_tj_flag_string_false_accepted":V("U1",[ref],s,h,evidence=["EB-SPAN","EB-TJ"],authenticated_tj="false"),
 "C4_unit_none_accepted":V(None,[ref],s,h,evidence=["EB-SPAN"]),
 "C5_uppercase_sha_rejected":V("U1",[ref],s,h.upper(),evidence=["EB-SPAN"]),
 "C6_bytearray_source":V("U1",[ref],bytearray(s),h,evidence=["EB-SPAN"]),
}
print(json.dumps(r,sort_keys=True))
