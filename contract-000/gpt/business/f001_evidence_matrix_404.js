/* F-001 HOLD-only, read-only evidence-planning matrix generator.
   Input: Run403 F-001-EDITORIAL-PROPOSALS-403.json. No approval or external evidence.
   Usage: node f001_evidence_matrix_404.js <proposals.json> [output.json]
*/
"use strict";
const PLANS={
G001:["cross-cultural standard","Obtain independently dated Indus and Levant weight catalogs; define unit classification, sample selection, chronology, and alternative standards.","Do independently sourced mass distributions and dates support a shared 13.7g unit better than separate local standards?","Compare distributions against multiple candidate units and controls; report uncertainty and exclusions."],
G004:["excavation inventory","Locate original Eshtemoa excavation inventory with vessel and aggregate mass measurements; cite page, edition and unit conversions.","Do primary find records actually establish five jugs and more than 26kg, rather than a later retelling?","Reconcile counts and total mass against original itemized inventory."],
G005:["arithmetic versus historical intention","Collect measured fragment masses and analytical precision; distinguish arithmetic fractions from observed archaeological cutting practices.","Could 13.7g fractions fit only because a base was selected after seeing the data?","Compare 13.7/2=6.85 and 13.7/4=3.425 with raw measurements, alternative bases and null distribution; state rounding rule."],
G009:["astronomical prediction","Specify water-clock dimensions, rate stability, dates, calibration and independent lunar ephemeris before examining results.","Would held-out eclipse or lunar-event predictions be no better than a simple calendar baseline?","Pre-register out-of-sample dates, prediction error and baseline comparisons."],
G011:["historical exchange rule","Find contemporaneous indigo/silver contracts, accounting units and independent provenance for the asserted one-to-one registry rule.","Do attested transactions show variable units, prices or no such registry?","Compare units of mass, value, commodity grade and conversion assumptions before any 1:1 statement."],
G020:["geodetic artifact network","Verify each site coordinate, datum, artifact provenance and proposed link; rebuild table from complete source context.","Do coordinate uncertainty, alternate geodesics or unattested artifacts remove the apparent grid relationship?","Compute geodesic distances with declared earth model, uncertainty and a comparison/null set."],
G027:["gravity and instrument sensitivity","Define what a salt-dome experiment would measure and whether an ancient balance could resolve the effect.","Is the expected gravity-induced weight change below measurement resolution, or unrelated to an ancient calibration practice?","Distinguish invariant mass from local weight; calculate expected delta and instrument uncertainty."],
G033:["electromagnetic and corrosion mechanism","Define proposed shielding and metal-preservation mechanism; seek physical tests and independently sourced archaeological observations.","Does salt-dome burial fail to attenuate the relevant fields or fail to preserve metal relative to controls?","Specify field strength/frequency, corrosion controls, measured endpoints and time scales."]
};
function makeEvidenceMatrix(input){
 if(!input || input.project!=="F-001" || !Array.isArray(input.items)) throw Error("Invalid F-001 source packet");
 return {format:"f001-hold-evidence-plan-v1",project:"F-001",run:404,source_packet_blob:"bff79b23d2d7a4ad79edae0ad55254c773d59223",source_commit:input.source_commit,status:"HOLD / NOT LAUNCH-READY",release_authorized:false,
 scope:"Proposed evidence/falsification work plan only; no claims externally verified, no editorial/rights decisions or release authority.",
 items:input.items.map(p=>{const plan=PLANS[p.group_id];if(!plan)throw Error("Unexpected group "+p.group_id);return {group_id:p.group_id,source_refs:p.source_refs,original_sentence:p.original_sentence,proposed_treatment:p.suggested_treatment,claim_type:plan[0],evidence_plan:plan[1],falsification_question:plan[2],quantitative_or_control_check:plan[3],editorial_review_status:"UNREVIEWED",independent_evidence_status:"NOT COLLECTED",rights_status:"UNCLEARED",reviewer:null,release_authorized:false}})};
}
function validateEvidenceMatrix(input,m){
 const e=[];if(m?.project!=="F-001"||m?.status!=="HOLD / NOT LAUNCH-READY"||m?.release_authorized!==false)e.push("HOLD release status");
 if(m?.source_packet_blob!=="bff79b23d2d7a4ad79edae0ad55254c773d59223"||m?.source_commit!==input?.source_commit)e.push("source packet pin");
 if(!Array.isArray(input?.items)||!Array.isArray(m?.items)||m.items.length!==input.items.length||m.items.length!==8){e.push("row count");return e;}
 const seen=new Set();const lookup=new Map(input.items.map(p=>[p.group_id,p]));
 for(const r of m.items){const p=lookup.get(r.group_id);if(!p||seen.has(r.group_id)){e.push("group mismatch/duplicate");continue;}seen.add(r.group_id);
 if(JSON.stringify(r.source_refs)!==JSON.stringify(p.source_refs)||r.original_sentence!==p.original_sentence||r.proposed_treatment!==p.suggested_treatment)e.push("source binding "+r.group_id);
 for(const k of ["claim_type","evidence_plan","falsification_question","quantitative_or_control_check"])if(typeof r[k]!=="string"||r[k].trim().length<15)e.push("plan missing "+r.group_id+" "+k);
 if(r.editorial_review_status!=="UNREVIEWED"||r.independent_evidence_status!=="NOT COLLECTED"||r.rights_status!=="UNCLEARED"||r.reviewer!==null||r.release_authorized!==false)e.push("unauthorized decision "+r.group_id);
 }
 return e;
}
if(typeof module!=="undefined")module.exports={makeEvidenceMatrix,validateEvidenceMatrix};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),input=JSON.parse(fs.readFileSync(process.argv[2],"utf8")),m=makeEvidenceMatrix(input),errors=validateEvidenceMatrix(input,m);
 if(errors.length){console.error(JSON.stringify(errors));process.exit(1);}
 const json=JSON.stringify(m,null,2)+"\n";
 if(process.argv[3])fs.writeFileSync(process.argv[3],json);else process.stdout.write(json);
}
