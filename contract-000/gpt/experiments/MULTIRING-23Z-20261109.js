// GPT-only synthetic multiring experiment. Issue #380 preregistered before execution.
// Reproduce: invoke runEchoGpt23() in a JavaScript runtime with crypto.subtle SHA-256.
async function runEchoGpt23() {
 const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
 const n=27, seeds=[10001,10002,10003,10004], eps=1e-9;
 const sum=a=>a.reduce((x,y)=>x+y,0);
 const l1=(a,b)=>sum(a.map((x,i)=>Math.abs(x-b[i])));
 const permA=i=>(i+1)%n;
 const permB=i=>(i*2)%n; // 2 coprime with 27
 const permC=i=>(i+9+(i%3))%n; // non-bijective allowed; mass preserved
 const step=(a,p,g=.37)=>{let b=a.map(x=>x*(1-g));for(let i=0;i<n;i++)b[p(i)]+=g*a[i];return b;};
 const oracle=(a,p,g=.37)=>Array.from({length:n},(_,j)=>a[j]*(1-g)+g*sum(a.map((x,i)=>p(i)===j?x:0)));
 const run=(a,ops)=>ops.reduce((v,p)=>step(v,p),a);
 const rng=seed=>{let x=seed>>>0;return ()=>{x=(1664525*x+1013904223)>>>0;return x/4294967296;}};
 const hex=bytes=>Array.from(bytes,b=>b.toString(16).padStart(2,"0")).join("");
 const digest=async s=>{if(!globalThis.crypto?.subtle)throw Error("SHA-256 unavailable");return hex(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(s))));};
 const core=JSON.stringify({version:"gpt23",glyphs,operators:["A","B","C"],seats:n});
 const hash=await digest(core),hash2=await digest(core),mut=await digest(core+"!");
 let rows=[];
 for(const seed of seeds){let random=rng(seed),v=Array.from({length:n},()=>random());let z=Array(n).fill(0),id=i=>i;
 let abc=run(v,[permA,permB,permC]),aba=run(v,[permA,permB,permA]),cba=run(v,[permC,permB,permA]),rewired=run(v,[permA,permB,i=>(i+5)%n]);
 let conditions=[
 glyphs.length===27&&new Set(glyphs).size===27,
 l1(abc,run(v,[permA,permB,permC]))===0,
 l1(run(z,[permA,permB,permC]),z)===0,
 l1(step(v,id,0),v)===0,
 Math.abs(sum(abc)-sum(v))<eps,
 l1(abc,aba)>eps,
 l1(abc,cba)>eps,
 l1(abc,rewired)>eps,
 l1(step(v,permC),oracle(v,permC))<eps,
 hash===hash2&&hash!==mut&&hash.length===64];
 rows.push({seed,conditions,metrics:{matched:l1(abc,aba),reverse:l1(abc,cba),rewired:l1(abc,rewired),oracle:l1(step(v,permC),oracle(v,permC)),mass:Math.abs(sum(abc)-sum(v))}});}
 return {source:"GPT-23Z",seeds,hash,rows,pass:rows.reduce((s,r)=>s+r.conditions.filter(Boolean).length,0),total:40};
}
