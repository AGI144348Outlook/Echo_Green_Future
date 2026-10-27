#!/usr/bin/env node
"use strict";
/** F-001 HOLD-only source coverage triage, not a claim verifier or release gate.
 * Use: node f001_source_coverage_probe_400.js <local-TAM-dir> <F-001-FULL-SENTENCE-QUEUE-388.json>
 * Inputs MUST be independently pinned before use. Output is candidate triage only.
 * The audit function below was executed on 8 pinned public source texts in Run400 V8.
 */
const audit = function audit(sources,queueIds){const triggers={certainty:/\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\b/i,percent:/\d+(\.\d+)?\s?%/,accuracy:/\b(accura(te|cy)|precision|precise(ly)?|correlat(es|ed|ion))\b/i,superlative:/\b(only|exactly|always|never|impossible)\b/i};const escaped=/\d+(?:\.\d+)?\s*\\%/;const unit=/\b\d+(?:\.\d+)?\s*(?:g|grams?|kg|cm|mm)\b/i;const assertion=/\b(?:is|was|were|are|became|acted|represents|demonstrates?|proves?|confirms?|enforced|yields?|predicts?|contains?|calibrated|calibration|functioned|served)\b/i;const baseline=[],escapes=[],unitNotBaseline=[],triage=[];for(const [name,content] of Object.entries(sources)){const ss=content.split(/(?<=[.!?])\s+|\n{2,}/).map(s=>s.trim()).filter(Boolean);for(let i=0;i<ss.length;i++){const s=ss[i],id=name+"#S"+(i+1),hits=Object.entries(triggers).filter(([,rx])=>rx.test(s)).map(([k])=>k);if(hits.length)baseline.push(id);if(escaped.test(s))escapes.push({id,baseline:hits.length>0,percent_trigger:hits.includes("percent"),in_queue:queueIds.has(id),excerpt:s.slice(0,260)});if(unit.test(s)&&!hits.length){unitNotBaseline.push(id);if(assertion.test(s)&&!queueIds.has(id))triage.push({id,excerpt:s.slice(0,220)})}}}return {baseline_count:baseline.length,escaped_percent:escapes,unit_without_baseline_count:unitNotBaseline.length,unit_assertion_triage_count:triage.length,unit_assertion_triage:triage,unreviewed_review_required:true,readiness:"HOLD"}};
if (typeof module !== "undefined") module.exports = {audit};
if (typeof require !== "undefined" && require.main === module) {
  const fs = require("node:fs"), path = require("node:path");
  if (process.argv.length !== 4) { console.error("usage: node f001_source_coverage_probe_400.js <TAM-dir> <queue.json>"); process.exit(2); }
  const dir = process.argv[2], queue = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
  const names = ["README.md","Article 1 Hacksilber","Article 2 Water Weight Computes","The Color Dyed and Dental Records","Article 5","Article 6","Article 10","Collective information"];
  const sources = Object.fromEntries(names.map(name => [name, fs.readFileSync(path.join(dir, name), "utf8")]));
  console.log(JSON.stringify(audit(sources, new Set(queue.cards.map(x => x.id))), null, 2));
}
