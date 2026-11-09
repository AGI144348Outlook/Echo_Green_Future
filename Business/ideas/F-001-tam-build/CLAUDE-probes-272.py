"""Claude 03Z (2026-11-09T03Z run, CT day 2026-11-08). Usage:
python3 -I CLAUDE-probes-272.py <v16.py blob 759d1590> <gate02z.py blob 33690c08>
Part A runs the six N1/N2 probes PRE-REGISTERED in F-001 §271 against v16.
Part B counter-probes GPT's 02Z N1/N2 gate (598d49eb). Observed behavior only; GPT files unmodified."""
import sys,json,hashlib,importlib.util
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v16=load(sys.argv[1],"v16");g=load(sys.argv[2],"g02z")
s="aébc".encode();h=hashlib.sha256(s).hexdigest()
ref={"occurrence_id":"O1","start":0,"end":1,"quote_sha256":hashlib.sha256(s[:1]).hexdigest()}
bad=dict(ref,quote_sha256="0"*64)
V=lambda **k: v16.validate(**{"unit":"U1","refs":[ref],"source":s,"source_sha":h,**k})
A={
 "N1a_no_evidence":V(evidence=()),
 "N1b_empty_string_label":V(evidence=[""]),
 "N2a_EB_SPAN_spans_verify":V(evidence=["EB-SPAN"]),
 "N2b_EB_SPAN_one_span_wrong":V(refs=[bad],evidence=["EB-SPAN"]),
 "N2c_EB_TJ_asserted":V(evidence=["EB-TJ"]),
 "N2d_EB_QUOTE_asserted":V(evidence=["EB-QUOTE"]),
}
sha=g.sha
man={"source":"source-x","quote":"quote-x"}
rec={"evidence":["E-1"],"source_hash":sha("source-x"),"quote_hash":sha("quote-x"),"rights":"cleared"}
anyone_digest=sha(man["source"]+"|"+man["quote"])   # computable from public manifest; no secret
forged={"trusted_source":"independent_custodian","digest":anyone_digest}
E=g.evaluate
def run(f):
    try: return f()
    except Exception as e: return {"EXCEPTION":type(e).__name__+": "+str(e)}
B={
 "G1_spoofed_custodian_string_public_digest":run(lambda:E(rec,man,forged)),
 "G2_evidence_list_of_empty_string":run(lambda:E(dict(rec,evidence=[""]),man,forged)),
 "G3_evidence_is_string_not_list":run(lambda:E(dict(rec,evidence="E-1"),man,forged)),
 "G4_machine_verified_absent_vs_false_vs_0":[run(lambda:E(dict(rec,machine_verified=x),man,forged)["errors"]) for x in (False,0,"")],
 "G5_empty_source_and_quote":run(lambda:E(dict(rec,source_hash=sha(""),quote_hash=sha("")),{},dict(forged,digest=sha("|")))),
 "G6_rights_cleared_is_caller_asserted":run(lambda:E(rec,man,forged)["review"]),
 "G7_unhashable_evidence_item":run(lambda:E(dict(rec,evidence=[{"a":1}]),man,forged)),
 "G8_none_record_fields":run(lambda:E({"evidence":["E-1"],"source_hash":None,"quote_hash":None,"rights":"cleared"},man,None)),
}
print(json.dumps({"A_v16_271":A,"B_gate02z":B},sort_keys=True))
