"use strict";
/* F-001 Run403, HOLD-only editorial proposal generator.
 * node f001_editorial_proposals_403.js <coverage-packet-401.json> <exact-group-map-402.json>
 * This is draft reviewer support, not source verification, editorial approval or release.
 */
const PROPOSALS=[
  [
    "G001",
    "Cross-cultural standardization",
    "Reframe the universal 13.7g trade standard as a hypothesis explored by this notebook, not an established archaeological fact.",
    "Independently dated weight catalogs from both regions, mass distributions, chronologies and evidence of transmission."
  ],
  [
    "G004",
    "Hoard inventory",
    "Attribute the five-jug/over-26kg claim to a verified excavation inventory or label these numbers unverified.",
    "Primary excavation publication, findspot inventory, vessel counts, original units and aggregate mass."
  ],
  [
    "G005",
    "Arithmetic versus causation",
    "Separate 13.7/2 = 6.85 and 13.7/4 = 3.425 arithmetic from the unsupported claim that silver was deliberately cut to these values.",
    "Individual measured fragment masses, precision, competing weight bases, null model and rounding rationale for displayed 3.42g."
  ],
  [
    "G009",
    "Astronomical prediction",
    "Reframe the claimed perfect lunar prediction as a proposed experiment, not a demonstrated result.",
    "Clock geometry, flow rate, timing calibration, lunar ephemeris, dates, error bars and held-out predictions."
  ],
  [
    "G011",
    "Historical trade enforcement",
    "Label the indigo/silver one-to-one registry rule as speculative reconstruction, not an attested historical transaction.",
    "Contemporaneous trade records, units, commodity quantities/quality, currency and independent provenance."
  ],
  [
    "G020",
    "Geodetic evidence table",
    "Mark the grid-pointer table as a proposed research diagram pending verification of every coordinate and artifact association.",
    "Coordinate datum, source for each artifact, geodesic method, uncertainty, and repair of the Markdown table split by the sentence scanner."
  ],
  [
    "G027",
    "Gravity and measurement",
    "Frame salt-dome balance differences as a testable physical hypothesis, not demonstrated ancient calibration.",
    "Quantified gravity difference, instrument sensitivity, controls, and historical evidence; distinguish mass from weight."
  ],
  [
    "G033",
    "Electromagnetic shielding",
    "Qualify or remove the salt-dome shielding and millennia-long metric-purity preservation claim pending physical evidence.",
    "Proposed shielding mechanism, corrosion chemistry, measurable preservation endpoint, environmental controls and independent source."
  ]
];
function validate(packet,groups){
 if(!packet||!groups||packet.project!=="F-001"||groups.project!=="F-001"||packet.status!=="HOLD / NOT LAUNCH-READY"||groups.status!==packet.status||packet.release_authorized!==false||groups.release_authorized!==false)throw Error("HOLD guard");
 if(packet.items.length!==37||groups.groups.length!==34||groups.occurrence_count!==37||groups.human_approved_count!==0||packet.human_approved_count!==0)throw Error("count/approval guard");
 if(groups.source_packet_blob!=="dfa28a6a750967a2bb600e56a6e962117890478b"||packet.source_commit!==groups.source_commit)throw Error("source pin guard");
 const map=new Map(packet.items.map(x=>[x.id,x]));if(map.size!==37)throw Error("duplicate source ID");
 const seen=new Set();
 for(const group of groups.groups){
  if(seen.has(group.group_id))throw Error("duplicate group ID");seen.add(group.group_id);
  if(group.human_review_status!=="UNREVIEWED"||group.editorial_disposition!==null||group.release_authorized!==false||group.rights_clearance!==null)throw Error("group decision/release guard");
  for(const r of group.source_refs){
   const x=map.get(r.id);
   if(!x||!group.occurrence_ids.includes(r.id)||x.full_sentence!==group.full_sentence||x.source_blob_sha!==r.blob_sha||packet.source_pins[r.file]!==r.blob_sha||x.source_commit!==r.source_commit||x.human_review_status!=="UNREVIEWED"||x.editorial_disposition!==null||x.rights_clearance!==null)throw Error("source binding");
  }
 }
 if(PROPOSALS.length!==8||PROPOSALS.some(row=>!seen.has(row[0])))throw Error("proposal IDs");
 return true;
}
function build(packet,groups){
 validate(packet,groups);
 return {format:"f001-hold-editorial-proposals-v1",project:"F-001",run:403,status:"HOLD / NOT LAUNCH-READY",release_authorized:false,source_packet_blob:groups.source_packet_blob,source_group_blob:"32dfe75589a031de46c28145fe993122ee2ca0f2",source_commit:packet.source_commit,proposal_count:8,human_approved_count:0,scope:"ChatGPT draft reviewer suggestions only; no historical truth, rights, editorial approval or publication asserted.",items:PROPOSALS.map(([id,topic,suggested_treatment,evidence_required])=>{const group=groups.groups.find(x=>x.group_id===id);return {group_id:id,source_refs:group.source_refs,original_sentence:group.full_sentence,topic,suggested_treatment,evidence_required,human_review_status:"UNREVIEWED",editorial_disposition:null,independent_evidence:null,rights_clearance:null,reviewer:null,release_authorized:false};})};
}
if(typeof module!=="undefined"&&module.exports){module.exports={build,validate};if(require.main===module){const fs=require("fs");if(process.argv.length!==4)throw Error("usage: node generator packet.json groups.json");process.stdout.write(JSON.stringify(build(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2)+"\n");}}
