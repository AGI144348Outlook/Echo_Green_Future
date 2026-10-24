// F-001 Run 328 — public source-pinned editorial audit; read-only, no publication.
// Git blobs: A b62c970a660e0a6685b58db1ef121690daa4fce7; B 12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4
function audit(aText,bText) {
  const BASE=1370000n; // 13.7 grams at 1e-5 g resolution
  function micro(s){const p=s.split(".");if(p.length>2||!p[0].match(/^\d+$/)||p[1]&&!p[1].match(/^\d{1,5}$/))throw Error("invalid decimal: "+s);return BigInt(p[0])*100000n+BigInt((p[1]||"").padEnd(5,"0"));}
  function fmt(n){const neg=n<0n?"-":"";const v=n<0n?-n:n;return neg+(v/100000n).toString()+"."+(v%100000n).toString().padStart(5,"0").replace(/0+$/,"").padEnd(1,"0");}
  function pct(n){const neg=n<0n?"-":"+";const v=n<0n?-n:n;return neg+(v/100n).toString()+"."+(v%100n).toString().padStart(2,"0")+"%";}
  function roundEven(n,d){const sign=n<0n?-1n:1n;const v=n<0n?-n:n;let q=v/d;const r=v%d;if(2n*r>d||(2n*r===d&&q%2n===1n))q++;return sign*q;}
  function cents(n){const c=roundEven(n,1000n);return (c/100n).toString()+"."+(c%100n).toString().padStart(2,"0");}
  const aLines=aText.split(/\r?\n/).filter(l=>/\d+(?:\.\d+)?g\s/.test(l));
  const bLines=bText.split(/\r?\n/).filter(l=>/^\d+\s+\d+(?:\.\d+)?g\s/.test(l));
  if(aLines.length!==6||bLines.length!==8)throw Error("source row-count mismatch: A="+aLines.length+" B="+bLines.length);
  const a=aLines.map((line,i)=>{
    const m=line.match(/^(.+?)\s+(\d+(?:\.\d+)?)g\s+(\d+(?:\.\d+)?) Units? \(([^)]+)\)\s+([+-]?\d+(?:\.\d+)?\\%|<\d+(?:\.\d+)?\\%)\s+(.+)$/);
    if(!m)throw Error("unparsed A row "+(i+1)+": "+line);
    const u=micro(m[3])*8n/100000n;
    if(u*100000n!==micro(m[3])*8n)throw Error("unsupported A fraction");
    const exact=BASE*u/8n,obs=micro(m[2]),diff=obs-exact;
    const computed=roundEven(diff*10000n,exact);
    const raw=m[5].replace("\\%","%");
    const matches=raw.startsWith("<")?( (diff<0n?-diff:diff)*10000n < exact ):computed===BigInt(raw.replace("%",""))*100n; // overwritten for decimal parsing below
    const printedScaled=raw.startsWith("<")?null:roundEven(micro(raw.replace("%",""))*100n,100000n);
    const direct=raw.startsWith("<")?matches:computed===printedScaled;
    return {row:i+1,object:m[1],observed_mass_g:m[2],units:m[3],registry_sign:m[4],printed_deviation:raw,term:m[6],theoretical_mass_g:fmt(exact),computed_deviation:pct(computed),direct_match:direct};
  });
  const b=bLines.map((line,i)=>{
    const m=line.match(/^(\d+)\s+(\d+(?:\.\d+)?)g\s+(.+?)\s+(\d+\/\d+|\d+(?:\.\d+)?) Units?\s+(.+)$/);
    if(!m)throw Error("unparsed B row "+(i+1)+": "+line);
    const ratio=BigInt(m[1]),exact=BASE*ratio/16n,obs=micro(m[2]);
    const expectedUnits=ratio;const actualUnits=m[4].includes("/")?(()=>{let [n,d]=m[4].split("/").map(BigInt);return n*16n/d;})():micro(m[4])*16n/100000n;
    if(actualUnits!==expectedUnits)throw Error("B unit relation mismatch at row "+(i+1));
    const rounded=cents(exact);
    return {row:i+1,ratio:m[1],observed_mass_g:m[2],registry_sign:m[3],printed_unit_relation:m[4],printed_relation:m[5],theoretical_mass_g:fmt(exact),half_even_0_01g:rounded,rounded_match:m[2]===rounded,absolute_difference_g:fmt(obs>=exact?obs-exact:exact-obs)};
  });
  const gerahA=a.filter(x=>x.term.toLowerCase().includes("gerah")).map(x=>({row:x.row,units:x.units}));
  const gerahB=b.filter(x=>x.printed_relation.toLowerCase().includes("gerah")).map(x=>({row:x.row,units:x.printed_unit_relation}));
  if(gerahA.length!==1||gerahB.length!==1)throw Error("Gerah labels missing/ambiguous");
  const summary={a_rows:a.length,a_direct_matches:a.filter(x=>x.direct_match).length,b_rows:b.length,b_rounded_matches:b.filter(x=>x.rounded_match).length,gerah_A:gerahA,gerah_B:gerahB,gerah_unit_conflict:gerahA[0].units!==gerahB[0].units,rounding:"nearest 0.01g, ties-to-even",release:"HOLD",readiness:"BLOCKED"};
  return {summary,a,b};
}

if (typeof module !== "undefined") {
  module.exports={audit};
  if (require.main===module) {
    const fs=require("node:fs"), crypto=require("node:crypto");
    const paths=process.argv.slice(2);
    if(paths.length!==2)throw Error("usage: node F-001-PRECISION-AUDIT-328.js DATASET_A DATASET_B");
    const buf=paths.map(p=>fs.readFileSync(p));
    const blobSha=b=>crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\\0".replace("\\\\0","\\0"))).update(b).digest("hex");
    const want=["b62c970a660e0a6685b58db1ef121690daa4fce7","12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4"];
    buf.forEach((b,i)=>{if(blobSha(b)!==want[i])throw Error("source blob mismatch at "+i);});
    process.stdout.write(JSON.stringify(audit(buf[0].toString("utf8"),buf[1].toString("utf8")),null,2)+"\\n");
  }
}
