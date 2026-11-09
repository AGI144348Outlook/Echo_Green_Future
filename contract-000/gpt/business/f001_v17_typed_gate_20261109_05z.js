// F-001 v17 experimental custody gate; synthetic only; no release capability.
"use strict";
function gate(input, verifier) {
  const fail=(code)=>({state:"HOLD",release:"HOLD",errors:[code]});
  try {
    if(!input || typeof input!=="object" || Array.isArray(input)) return fail("INVALID_INPUT");
    if(!Array.isArray(input.evidence)||!input.evidence.length) return fail("INVALID_EVIDENCE");
    if(!input.evidence.every(x=>x&&typeof x==="object"&&!Array.isArray(x)&&typeof x.id==="string"&&x.id.trim()&&typeof x.source==="string"&&x.source.trim()&&typeof x.quote==="string"&&x.quote.trim())) return fail("INVALID_EVIDENCE_ITEM");
    if(typeof verifier!=="function") return fail("NO_INDEPENDENT_VERIFIER");
    const verdict=verifier({evidence:input.evidence.map(x=>({id:x.id,source:x.source,quote:x.quote}))});
    if(verdict!==true) return fail("UNVERIFIED_RECEIPT");
    return {state:"REVIEW_READY",release:"HOLD",errors:[]};
  } catch(e) {return fail("VERIFIER_ERROR");}
}
function tests(seed=3301){
 const ok={evidence:[{id:"E1",source:"S1",quote:"Q1"}]};
 const cases=[
 ["valid",()=>gate(ok,()=>true).state==="REVIEW_READY"&&gate(ok,()=>true).release==="HOLD"],
 ["no_verifier",()=>gate(ok).state==="HOLD"],
 ["forged_trust",()=>gate({...ok,trusted_source:true}).state==="HOLD"],
 ["empty_evidence",()=>gate({evidence:[]}).errors.includes("INVALID_EVIDENCE")],
 ["string_evidence",()=>gate({evidence:"E1"}).state==="HOLD"],
 ["blank_item",()=>gate({evidence:[""]}).state==="HOLD"],
 ["object_item",()=>gate({evidence:[{}]}).state==="HOLD"],
 ["empty_source_quote",()=>gate({evidence:[{id:"E1",source:"",quote:""}]}).state==="HOLD"],
 ["verifier_throws",()=>gate(ok,()=>{throw Error("bad")}).errors.includes("VERIFIER_ERROR")],
 ["verifier_denies",()=>gate(ok,()=>false).errors.includes("UNVERIFIED_RECEIPT")]
 ];
 const result=Object.fromEntries(cases.map(([name,fn])=>[name,Boolean(fn())]));
 return {seed,passed:Object.values(result).filter(Boolean).length,total:cases.length,results:result};
}
