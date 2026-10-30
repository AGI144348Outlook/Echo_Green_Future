"use strict";
/* F-001 Run466: source-bound, HOLD-only tests. No network. */
function runSuite(api,texts,pins){
 const {buildReview,parseTsv,renderHtml,PINS}=api;
 const outcomes=[];
 function check(name,fn,refusal=false){
  try{const value=fn();outcomes.push({name,pass:!refusal&&Boolean(value),detail:String(value).slice(0,90)})}
  catch(e){outcomes.push({name,pass:refusal,detail:e.message.slice(0,100)})}
 }
 let html;
 check("pinned real data renders",()=>{html=buildReview(...texts,pins);return html.includes("82 editorial draft reviews")});
 check("repeat output byte-identical",()=>buildReview(...texts,pins)===html);
 check("all 82 occurrence IDs",()=>parseTsv(texts[0],"register").every(x=>html.includes(x.occurrence_id)));
 check("no remote requests",()=>!/(https?:\/\/|fetch\s*\(|XMLHttpRequest|<iframe|<img|<link)/i.test(html));
 check("draft-only export flags",()=>html.includes('authority:"NONE"')&&html.includes("publication_authorized:false")&&!html.includes('value="APPROVED"'));
 check("source text HTML escaped",()=>{const h=renderHtml([{id:"X",source:"x",sentence:"1",match:"LITERAL",section:"§1",preview:"</script><script>alert(1)</script>",proposal:"<img src=x onerror=alert(1)>",copy:""}]);return !h.includes("</script><script>alert(1)")&&!h.includes("<img src=x onerror")&&h.includes("\\u003cscript")});
 function mutate(k,fn){const x=[...texts];x[k]=fn(x[k]);return ()=>buildReview(...x,pins)}
 check("duplicate ID refused",mutate(0,t=>{const a=t.split("\n");a[2]=a[1];return a.join("\n")}),true);
 check("missing row refused",mutate(2,t=>{const a=t.trimEnd().split("\n");a.pop();return a.join("\n")+"\n"}),true);
 check("APPROVED intake refused",mutate(2,t=>t.replace("\tPENDING\t","\tAPPROVED\t")),true);
 check("release=true refused",mutate(2,t=>t.replace("\tfalse\n","\ttrue\n")),true);
 check("changed register pin refused",mutate(2,t=>t.replace(PINS.register,"a".repeat(40))),true);
 check("changed location pin refused",mutate(2,t=>t.replace(PINS.location,"a".repeat(40))),true);
 check("changed source pin refused",mutate(2,t=>t.replace("213bcfaf560dcc54fbb7ae79fad932e86b660357","a".repeat(40))),true);
 check("changed copy link refused",mutate(1,t=>t.replace("\tArticle 6#S4\t","\tArticle 6#S5\t")),true);
 check("approved register refused",mutate(0,t=>t.replace("PROPOSED_NOT_APPROVED","APPROVED")),true);
 check("row reordering refused",mutate(1,t=>{const a=t.split("\n");[a[1],a[2]]=[a[2],a[1]];return a.join("\n")}),true);
 check("changed header refused",mutate(0,t=>t.replace("proposal_section","proposal_state")),true);
 check("unverified input pins refused",()=>buildReview(...texts,{...pins,intake:"0".repeat(40)}),true);
 return {passed:outcomes.filter(x=>x.pass).length,total:outcomes.length,outcomes};
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto"),path=require("node:path");
 const args=process.argv.slice(2);
 if(args.length!==3){console.error("Usage: node test_f001_review_companion_466.js register.tsv locations.tsv intake.tsv");process.exit(2)}
 const api=require("./f001_review_companion_466.js");
 const data=args.map(x=>fs.readFileSync(x));
 const blob=b=>crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex");
 const pins={register:blob(data[0]),location:blob(data[1]),intake:blob(data[2])};
 const results=runSuite(api,data.map(x=>x.toString("utf8")),pins);
 console.log(JSON.stringify(results,null,2));
 if(results.passed!==results.total)process.exitCode=1;
}
