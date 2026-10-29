"use strict";
/* F-001 HOLD-only independent JS parity implementation of the Python claim_scan.py
 * Source Python: library-shared Business/ideas/F-001-tam-build/claim_scan.py
 * Git blob 31f3dcff486c4c8cc96d514eb425da86834d00c3.
 * This does NOT execute Python, authenticate historical claims or write files.
 * Pass an object mapping the eight exact TAM filenames to UTF-8 strings.
 */
const FILES = Object.freeze(["README.md","Article 1 Hacksilber",
  "Article 2 Water Weight Computes","The Color Dyed and Dental Records",
  "Article 5","Article 6","Article 10","Collective information"]);
const TRIGGERS = Object.freeze({
  certainty: /\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\b/i,
  percent: /\d+(\.\d+)?\s?%/i,
  accuracy: /\b(accura(te|cy)|precision|precise(ly)?|correlat(es|ed|ion))\b/i,
  superlative: /\b(only|exactly|always|never|impossible)\b/i
});
function sentences(text) {
  if (typeof text !== "string") throw Error("Source must be a UTF-8 text string");
  return text.split(/(?<=[.!?])\s+|\n{2,}/).map(s=>s.trim()).filter(Boolean);
}
function scanSources(sources) {
  const perFile={}, perTrigger={certainty:0,percent:0,accuracy:0,superlative:0};
  const rows=[];
  for (const file of FILES) {
    if (!Object.prototype.hasOwnProperty.call(sources,file)) throw Error("Missing source: "+file);
    let n=0;
    sentences(sources[file]).forEach((sentence,index)=>{
      const hits=Object.keys(TRIGGERS).filter(k=>TRIGGERS[k].test(sentence));
      if(hits.length){ n++; hits.forEach(k=>perTrigger[k]++);
        rows.push({file,sentence_no:index+1,triggers:hits.join(";"),sentence,status:""}); }
    });
    perFile[file]=n;
  }
  return {count:rows.length,perFile,perTrigger,rows};
}
function selfTests(){
  const samples=[["Proof! Plain text.",1],["Ordinary statement. Nothing unusual.",0],
    ["99% confident. Precisely measured.",2],["Never certain.",1]];
  return samples.map(([s,expected])=>({expected,actual:sentences(s).filter(x=>Object.values(TRIGGERS).some(r=>r.test(x))).length}));
}
if (typeof module !== "undefined") module.exports={FILES,TRIGGERS,sentences,scanSources,selfTests};
