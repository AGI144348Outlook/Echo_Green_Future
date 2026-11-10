// GPT-owned synthetic 27-seat experiment; no canonical Echo changes.
// Run: evaluate this exact file in isolated JavaScript; returns JSON through main().
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const N=27, SEEDS=[9401,9402,9403,9404];
function rng(seed){let s=seed>>>0;return ()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);}
function transfer(x,shift,rate=.3){let y=Array(N).fill(0);for(let i=0;i<N;i++){y[i]+=x[i]*(1-rate);y[(i+shift)%N]+=x[i]*rate;}return y;}
function deform(x){let y=Array(N).fill(0);for(let i=0;i<N;i++){y[i]+=.7*x[i];y[(2*i+1)%N]+=.3*x[i];}return y;}
function oracle(x,shift){return Array.from({length:N},(_,j)=>x.reduce((s,v,i)=>s+v*(i===j?.7:0)+v*((i+shift)%N===j?.3:0),0));}
function l1(a,b){return a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0);}
function sum(x){return x.reduce((a,b)=>a+b,0);}
function sha256(s){
 const k=[],h=[],primes=[];for(let n=2;primes.length<64;n++){if(primes.every(p=>n%p!==0)){primes.push(n);if(h.length<8)h.push((n**.5%1*4294967296)>>>0);k.push((n**(1/3)%1*4294967296)>>>0);}}
 const bytes=Array.from(s,c=>c.charCodeAt(0));const bits=bytes.length*8;bytes.push(128);while(bytes.length%64!==56)bytes.push(0);for(let i=7;i>=0;i--)bytes.push(Math.floor(bits/2**(8*i))&255);
 const rotr=(x,n)=>(x>>>n)|(x<<(32-n));
 for(let off=0;off<bytes.length;off+=64){const w=new Array(64);for(let i=0;i<16;i++){let p=off+4*i;w[i]=((bytes[p]<<24)|(bytes[p+1]<<16)|(bytes[p+2]<<8)|bytes[p+3])>>>0;}
 for(let i=16;i<64;i++){let a=w[i-15],b=w[i-2];w[i]=((w[i-16]+(rotr(a,7)^rotr(a,18)^(a>>>3))+w[i-7]+(rotr(b,17)^rotr(b,19)^(b>>>10)))>>>0);}
 let [a,b,c,d,e,f,g,z]=h;
 for(let i=0;i<64;i++){let t1=(z+(rotr(e,6)^rotr(e,11)^rotr(e,25))+((e&f)^(~e&g))+k[i]+w[i])>>>0;let t2=((rotr(a,2)^rotr(a,13)^rotr(a,22))+((a&b)^(a&c)^(b&c)))>>>0;z=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;}
 const v=[a,b,c,d,e,f,g,z];for(let i=0;i<8;i++)h[i]=(h[i]+v[i])>>>0;
 }
 return h.map(x=>x.toString(16).padStart(8,"0")).join("");
}
function run(seed){let r=rng(seed),x=Array.from({length:N},()=>r());let A=transfer(x,1), B=deform(A), C=transfer(B,2), AB=deform(transfer(x,1)), BA=transfer(deform(x),1), shuffled=transfer(x,7);
 let two=deform(transfer(x,1)),three=transfer(deform(transfer(x,1)),2), padded=transfer(two,2,0);
 let metrics={coupled:l1(A,x),rewire:l1(A,shuffled),order:l1(AB,BA),commuting:l1(transfer(transfer(x,1),2),transfer(transfer(x,2),1)),oracle:l1(A,oracle(x,1)),three_vs_padded:l1(three,padded),mass:Math.abs(sum(x)-sum(C))};
 let core="A-000|27|rings|v02";let checks={glyphs:GLYPHS.length===N&&new Set(GLYPHS).size===N,replay:JSON.stringify(Array.from({length:N},rng(seed)))===JSON.stringify(x),noop:l1(transfer(x,1,0),x)===0,mass:metrics.mass<1e-9,rewire:metrics.rewire>1e-6&&Math.abs(sum(A)-sum(shuffled))<1e-9,order:metrics.order>1e-6,commuting_null:metrics.commuting<1e-9,oracle:metrics.oracle<1e-9,three_vs_identity_padding:metrics.three_vs_padded>1e-6,sha256:sha256("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"&&sha256(core)===sha256(core)&&sha256(core)!==sha256(core+"!")};
 return {seed,checks,metrics};}
function main(){let results=SEEDS.map(run);return {source:"gpt-ring-controls-20261110-02z.js",seeds:SEEDS,results,passed:results.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0),total:results.length*10};}
