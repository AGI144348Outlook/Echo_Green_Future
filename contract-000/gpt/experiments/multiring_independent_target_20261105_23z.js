// GPT-only bounded synthetic multiring experiment; Issue #309 preregistered before tests.
const SEEDS=[11,23,37,53,71], GLYPHS=Array.from({length:27},(_,i)=>i);
function rand(seed){let s=seed>>>0;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296}}
function init(seed,n){let r=rand(seed);return Array.from({length:n},()=>r())}
function run(seed,n,coupling=0,intervene=false,shuffle=false){if(!Number.isInteger(n)||n<2||n>4)throw Error("ring count");let x=init(seed,n),r=rand(seed+77);let affin=Array.from({length:n},(_,i)=>shuffle?1-(i+1)/n:(i+1)/n);for(let t=0;t<12;t++){let old=x.slice();x=x.map((v,i)=>{let neighbor=old[(i+1)%n];let kick=intervene&&t===4&&i===0?.25:0;return (v+.031+coupling*affin[i]*(neighbor-v)+kick+1)%1})}return x}
function dist(a,b){return a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0)}
function digest(x){let h=2166136261;for(const c of x){h=Math.imul(h^c.charCodeAt(0),16777619)>>>0}return h>>>0}
const results={};
results.glyph_unique=new Set(GLYPHS).size===27;
results.projection_inverse=GLYPHS.every(i=>{let z=Math.floor(i/9),y=Math.floor(i%9/3),x=i%3;return 9*z+3*y+x===i});
results.ring_order=[2,3,4].every(n=>GLYPHS.slice(0,n).join(",").split(",").map(Number).every((v,i)=>v===i));
results.identity_digest=digest("A000:v1")!==digest("A000:v2");
results.replay=SEEDS.every(s=>JSON.stringify(run(s,3,.2))===JSON.stringify(run(s,3,.2)));
results.null_intervention=SEEDS.every(s=>dist(run(s,3,0),run(s,3,0,true))>0); // intervention directly affects its own ring; isolation instead checked below
results.uncoupled_isolation=SEEDS.every(s=>dist(run(s,3,0).slice(1),run(s,3,0,true).slice(1))===0);
results.coupled_influence=SEEDS.every(s=>dist(run(s,3,.2).slice(1),run(s,3,.2,true).slice(1))>0);
results.shuffled_affinity=SEEDS.some(s=>dist(run(s,3,.2),run(s,3,.2,false,true))>0);
results.boundary=[2,3,4].every(n=>SEEDS.every(s=>run(s,n,.2).every(v=>v>=0&&v<1)));
results.malformed_reject=(()=>{try{run(11,0);return false}catch{return true}})();
const differences=SEEDS.map(s=>{let a=init(s,3);return a.slice(1).map(x=>+(x-a[0]).toFixed(9)).join(",")});
results.seed_difference_diversity=new Set(differences).size===SEEDS.length;
const comparisons=SEEDS.map(s=>{let target=run(s+101,3,.13);return {seed:s,coupled:+dist(run(s,3,.2),target).toFixed(6),uncoupled:+dist(run(s,3,0),target).toFixed(6),shuffled:+dist(run(s,3,.2,false,true),target).toFixed(6)}});
const tests=Object.entries(results);console.log(JSON.stringify({tests,pass:tests.filter(x=>x[1]).length,total:tests.length,differences,comparisons},null,2));
