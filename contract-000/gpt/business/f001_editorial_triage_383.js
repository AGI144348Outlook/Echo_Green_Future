"use strict";
/* F-001 editorial triage; review-only, never authorizes publication. */
function buildQueue(input) {
  if (!input || input.project !== "F-001" || input.status !== "HOLD" ||
      input.release_authorized !== false || input.reviewed_count !== 0)
    throw Error("F-001 HOLD provenance required");
  const sources=input.sources;
  if (!Array.isArray(sources) || sources.length!==8) throw Error("eight source pins required");
  const sourceMap=new Map();
  for (const s of sources) {
    if (!s.file || !/^[a-f0-9]{40}$/.test(s.blob_sha) || sourceMap.has(s.file))
      throw Error("invalid source pin");
    sourceMap.set(s.file,s);
  }
  if (!Array.isArray(input.baseline) || input.baseline.length!==42 ||
      !Array.isArray(input.supplemental) || input.supplemental.length!==3)
    throw Error("expected 42+3 candidates");
  const seen=new Set(), cards=[];
  for (const [group,records] of [["baseline",input.baseline],["supplemental",input.supplemental]]) {
    for (const rec of records) {
      const source=sourceMap.get(rec.file);
      if (!source || rec.source_blob_sha!==source.blob_sha ||
          !Number.isInteger(rec.sentence_no) || rec.sentence_no<1 ||
          rec.sentence_no>source.sentences ||
          rec.id!==rec.file+"#S"+rec.sentence_no || seen.has(rec.id) ||
          typeof rec.excerpt!=="string" || !rec.excerpt.trim() ||
          rec.review_status!=="UNREVIEWED")
        throw Error("invalid candidate: "+String(rec.id));
      seen.add(rec.id);
      const t=rec.excerpt;
      const flags=[];
      if (/\\?%|\b(?:percent|percentage|correlation|accuracy|deviation)\b/i.test(t))
        flags.push("quantitative-verification");
      if (/\b(?:prove[sd]?|proving|demonstrat\w*|confirm\w*|establish\w*|invariant|locked)\b/i.test(t))
        flags.push("certainty-or-inference");
      if (/\b(?:first|most|least|only|never|always|world|universal|unprecedented)\b/i.test(t))
        flags.push("comparative-or-superlative");
      if (/\b(?:because|therefore|forcing|caus\w*|led to|resulted in)\b/i.test(t))
        flags.push("causal-claim");
      if (/\b(?:BCE|CE|century|millennium|ancient|historic\w*)\b/i.test(t))
        flags.push("historical-context");
      if (!flags.length) flags.push("general-source-support");
      const priority=flags.includes("quantitative-verification") ||
        flags.includes("certainty-or-inference") ||
        flags.includes("causal-claim") ? "P1" : "P2";
      cards.push({
        id:rec.id, source_file:rec.file, source_blob_sha:rec.source_blob_sha,
        source_commit:input.source_commit, sentence_no:rec.sentence_no,
        excerpt:rec.excerpt, detection_group:group,
        detection_triggers:group==="baseline"?rec.triggers:[rec.extra_trigger],
        review_priority:priority, heuristic_flags:flags,
        reviewer_question:"What independent primary evidence supports this exact claim, and should the wording be qualified, cited, corrected or removed?",
        review_status:"UNREVIEWED", editorial_disposition:null,
        evidence_reference:null, reviewer:null, rights_clearance:null
      });
    }
  }
  if(cards.length!==45)throw Error("not 45 candidates");
  const byFile={};
  for(const c of cards)byFile[c.source_file]=(byFile[c.source_file]||0)+1;
  return {project:"F-001",status:"HOLD",release_authorized:false,
    source_repo:input.source_repo,source_commit:input.source_commit,
    source_tree:input.source_tree,source_inventory_blob:"d9e36400b90cf534f9914c1c42b39d17f6d8a7fc",
    card_count:cards.length,baseline_count:42,supplemental_count:3,
    unreviewed_count:cards.length,source_counts:byFile,
    disclaimer:"Heuristic flags and questions are NOT factual findings or editorial dispositions.",
    cards};
}
if(typeof module!=="undefined")module.exports={buildQueue};
if(typeof require!=="undefined" && typeof process!=="undefined" &&
    require.main===module) {
  const fs=require("fs");
  if(process.argv.length!==3)throw Error("usage: node f001_editorial_triage_383.js input.json");
  process.stdout.write(JSON.stringify(buildQueue(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2)+"\n");
}
