// F-001 inert release evidence schema validator. Does NOT verify evidence authenticity.
// Preregistered in issue #441; not permission to publish.
function verify(m) {
 const fail=[];
 const required=["project_id","artifact_kind","verify_mode","delivered_sha256","source_ref","licence_basis","licence_notice_sha256","rights_route","rights_open","editorial_open","decisions_ref","accessibility_report_ref","listing_sample_parity_ref","release_receipt_ref","release_issuer","editorial_receipt","timothy_authorized"];
 for(const k of required)if(!Object.prototype.hasOwnProperty.call(m,k))fail.push("missing:"+k);
 if(m.project_id!=="F-001")fail.push("project_id");
 if(!["pdf","epub"].includes(m.artifact_kind))fail.push("artifact_kind");
 if(!["delivered_hash_only","rebuild_compare"].includes(m.verify_mode))fail.push("verify_mode");
 if(m.artifact_kind==="epub"&&m.verify_mode!=="rebuild_compare")fail.push("epub_requires_rebuild_compare");
 if(m.artifact_kind==="pdf"&&m.verify_mode!=="delivered_hash_only")fail.push("pdf_requires_delivered_hash_only");
 const hex=x=>typeof x==="string"&&/^[0-9a-f]{64}$/.test(x);
 if(!hex(m.delivered_sha256))fail.push("delivered_sha256");
 if(!hex(m.licence_notice_sha256))fail.push("licence_notice_sha256");
 if(m.verify_mode==="rebuild_compare"&&(!hex(m.rebuild_sha256)||m.rebuild_sha256!==m.delivered_sha256))fail.push("rebuild_sha256");
 if(m.verify_mode==="delivered_hash_only"&&m.rebuild_sha256!==null)fail.push("rebuild_must_be_null");
 for(const k of ["source_ref","licence_basis","rights_route","decisions_ref","accessibility_report_ref","listing_sample_parity_ref","release_receipt_ref","release_issuer","editorial_receipt"])if(typeof m[k]!=="string"||!m[k].trim())fail.push(k);
 if(m.rights_open!==0)fail.push("rights_open");
 if(m.editorial_open!==0)fail.push("editorial_open");
 if(m.timothy_authorized!==true)fail.push("authorization");
 return {admit:fail.length===0,fail};
}
const example={
  "project_id": "F-001",
  "artifact_kind": "pdf",
  "verify_mode": "delivered_hash_only",
  "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "rebuild_sha256": null,
  "source_ref": "source",
  "licence_basis": "documented",
  "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "rights_route": "verified",
  "rights_open": 0,
  "editorial_open": 0,
  "decisions_ref": "signed",
  "accessibility_report_ref": "report",
  "listing_sample_parity_ref": "parity",
  "release_receipt_ref": "receipt",
  "release_issuer": "authorized",
  "editorial_receipt": "editor",
  "timothy_authorized": true
};
const cases=[
  [
    "complete_synthetic",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    true
  ],
  [
    "missing_license",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    false
  ],
  [
    "open_rights",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 70,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    false
  ],
  [
    "open_editorial",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 82,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    false
  ],
  [
    "missing_authority",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": false
    },
    false
  ],
  [
    "pdf_rebuild_mismatch",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    false
  ],
  [
    "epub_without_rebuild",
    {
      "project_id": "F-001",
      "artifact_kind": "epub",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    false
  ],
  [
    "epub_rebuild_match",
    {
      "project_id": "F-001",
      "artifact_kind": "epub",
      "verify_mode": "rebuild_compare",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    true
  ],
  [
    "invalid_hash",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "not-a-hash",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    false
  ],
  [
    "missing_release_issuer",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "",
      "editorial_receipt": "editor",
      "timothy_authorized": true
    },
    false
  ],
  [
    "missing_editorial_receipt",
    {
      "project_id": "F-001",
      "artifact_kind": "pdf",
      "verify_mode": "delivered_hash_only",
      "delivered_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "rebuild_sha256": null,
      "source_ref": "source",
      "licence_basis": "documented",
      "licence_notice_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "rights_route": "verified",
      "rights_open": 0,
      "editorial_open": 0,
      "decisions_ref": "signed",
      "accessibility_report_ref": "report",
      "listing_sample_parity_ref": "parity",
      "release_receipt_ref": "receipt",
      "release_issuer": "authorized",
      "editorial_receipt": "",
      "timothy_authorized": true
    },
    false
  ]
];
const results=cases.map(([name,m,expected])=>({name,expected,actual:verify(m).admit,fail:verify(m).fail}));
console.log(JSON.stringify(results,null,2));
if(results.some(x=>x.expected!==x.actual))process.exitCode=1;
