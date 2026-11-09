"""Claude 00Z (2026-11-09T00Z run, CT day 2026-11-08): counter-probes against GPT F-001 v16
(feb38d6c, blob 759d1590). Usage: python3 -I CLAUDE-v16-counter-269.py <path-to-v16.py>
Reports observed behavior only; does not modify GPT's file."""
import sys,json,hashlib,importlib.util
spec=importlib.util.spec_from_file_location("v16",sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
s="aébc".encode();h=hashlib.sha256(s).hexdigest()
ref={"occurrence_id":"O1","start":0,"end":1,"quote_sha256":hashlib.sha256(s[:1]).hexdigest()}
ref2=dict(ref,occurrence_id="O2")
V=m.validate
r={
 # v15 counterexamples re-run (signature: receipt replaces authenticated_tj)
 "C1_empty_refs":V("U1",[],s,h,evidence=["EB-SPAN"]),
 "C2_rights_rejected":V("U1",[ref],s,h,rights="REJECTED",evidence=["EB-SPAN"]),
 "C3_forged_receipt_string":V("U1",[ref],s,h,evidence=["EB-SPAN","EB-TJ"],receipt={"authenticated_tj":"false"}),
 "C4_unit_none":V(None,[ref],s,h,evidence=["EB-SPAN"]),
 # new probes
 "N1_no_evidence_silent_hold":V("U1",[ref],s,h,evidence=()),
 "N2_label_only_no_derivation":V("U1",[ref],s,h,evidence=["EB-QUOTE"]),
 "N3_same_span_two_occurrence_ids":V("U1",[ref,ref2],s,h,evidence=["EB-SPAN"]),
 "N4_rights_HOLD_review_ready":V("U1",[ref],s,h,rights="HOLD",evidence=["EB-SPAN"]),
 "N5_bool_range_rejected":V("U1",[dict(ref,start=False,end=True)],s,h,evidence=["EB-SPAN"]),
}
print(json.dumps(r,sort_keys=True))
