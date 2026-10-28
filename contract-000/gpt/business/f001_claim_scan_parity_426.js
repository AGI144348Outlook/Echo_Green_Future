/* F-001 Run426: dependency-free, read-only JS parity candidate for the Python
 * claim_scan.py (library-shared Git blob 31f3dcff486c4c8cc96d514eb425da86834d00c3).
 * This is NOT execution of the original Python scanner. No editorial adjudication.
 * Node: require this file, then globalThis.F001ClaimScan426.scan(sources,pins).
 * sources[name] = {content: exact UTF-8 text, sha: Git blob SHA}; pins[name] = Git blob SHA.
 */
(function (root) {
  "use strict";
  const FILES = ["README.md", "Article 1 Hacksilber", "Article 2 Water Weight Computes",
    "The Color Dyed and Dental Records", "Article 5", "Article 6", "Article 10",
    "Collective information"];
  const RX = {
    certainty: /\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\b/i,
    percent: /\d+(\.\d+)?\s?%/i,
    accuracy: /\b(accura(te|cy)|precision|precise(ly)?|correlat(es|ed|ion))\b/i,
    superlative: /\b(only|exactly|always|never|impossible)\b/i
  };
  function utf8(str) {
    const b = [];
    for (const ch of str) {
      const cp = ch.codePointAt(0);
      if (cp < 128) b.push(cp);
      else if (cp < 2048) b.push(192 | (cp >> 6), 128 | (cp & 63));
      else if (cp < 65536) b.push(224 | (cp >> 12), 128 | ((cp >> 6) & 63), 128 | (cp & 63));
      else b.push(240 | (cp >> 18), 128 | ((cp >> 12) & 63), 128 | ((cp >> 6) & 63), 128 | (cp & 63));
    }
    return b;
  }
  function sha1(bytes) {
    const a = bytes.slice(), bitLen = a.length * 8;
    a.push(128);
    while (a.length % 64 !== 56) a.push(0);
    const hi = Math.floor(bitLen / 4294967296), lo = bitLen >>> 0;
    for (const n of [hi, lo]) for (let i = 3; i >= 0; i--) a.push((n >>> (i * 8)) & 255);
    let h0=0x67452301,h1=0xefcdab89,h2=0x98badcfe,h3=0x10325476,h4=0xc3d2e1f0;
    const rol=(v,n)=>(v<<n)|(v>>>(32-n));
    for(let offset=0;offset<a.length;offset+=64){
      const w=new Array(80);
      for(let i=0;i<16;i++){const k=offset+i*4;w[i]=((a[k]<<24)|(a[k+1]<<16)|(a[k+2]<<8)|a[k+3])>>>0;}
      for(let i=16;i<80;i++)w[i]=rol(w[i-3]^w[i-8]^w[i-14]^w[i-16],1)>>>0;
      let A=h0,B=h1,C=h2,D=h3,E=h4;
      for(let i=0;i<80;i++){
        let f,k;
        if(i<20){f=(B&C)|((~B)&D);k=0x5a827999;}
        else if(i<40){f=B^C^D;k=0x6ed9eba1;}
        else if(i<60){f=(B&C)|(B&D)|(C&D);k=0x8f1bbcdc;}
        else {f=B^C^D;k=0xca62c1d6;}
        const t=(rol(A,5)+f+E+k+w[i])>>>0;
        E=D;D=C;C=rol(B,30)>>>0;B=A;A=t;
      }
      h0=(h0+A)>>>0;h1=(h1+B)>>>0;h2=(h2+C)>>>0;h3=(h3+D)>>>0;h4=(h4+E)>>>0;
    }
    return [h0,h1,h2,h3,h4].map(n=>n.toString(16).padStart(8,"0")).join("");
  }
  function blobSha(content) {
    const bytes=utf8(content);
    return sha1(utf8("blob "+bytes.length+"\0").concat(bytes));
  }
  function sentences(text) {
    return text.split(/(?<=[.!?])\s+|\n{2,}/u).map(s=>s.trim()).filter(Boolean);
  }
  function scan(sources,pins) {
    if(!sources||!pins) throw Error("source bytes and independent Git blob pins required");
    const rows=[],per_file={},per_trigger={certainty:0,percent:0,accuracy:0,superlative:0},source_blobs={};
    for(const name of FILES){
      const f=sources[name],pin=pins[name];
      if(!f||typeof f.content!=="string"||typeof f.sha!=="string"||!pin)throw Error("missing source/pin: "+name);
      const actual=blobSha(f.content);
      if(actual!==pin||f.sha!==pin)throw Error("Git blob mismatch: "+name);
      source_blobs[name]=pin;
      let count=0;
      const ss=sentences(f.content);
      for(let i=0;i<ss.length;i++){
        const hits=Object.keys(RX).filter(k=>RX[k].test(ss[i]));
        if(hits.length){
          rows.push({file:name,sentence_no:i+1,triggers:hits.join(";"),sentence:ss[i],status:""});
          count++; for(const h of hits)per_trigger[h]++;
        }
      }
      per_file[name]=count;
    }
    if(Object.keys(sources).some(n=>!FILES.includes(n)))throw Error("unexpected source file");
    return {schema:"f001-claim-scan-js-parity-candidate/v1",
      original_python_scanner_blob:"31f3dcff486c4c8cc96d514eb425da86834d00c3",
      source_repository:"AGI144348Outlook/The-TAM-protocol",source_blobs,
      rows_count:rows.length,per_file,per_trigger,rows,
      editorial_disposition:"UNREVIEWED",release_status:"HOLD / NOT LAUNCH-READY",
      limitations:"JS transcription; original Python not executed; Unicode regex semantics may differ; candidate detection is not claim verification."};
  }
  function verify(manifest,sources,pins) {
    const expected=scan(sources,pins);
    if(JSON.stringify(expected)!==JSON.stringify(manifest))throw Error("manifest differs from recomputed source-pinned candidate inventory");
    return true;
  }
  root.F001ClaimScan426={FILES,blobSha,sha1,utf8,sentences,scan,verify};
})(globalThis);
