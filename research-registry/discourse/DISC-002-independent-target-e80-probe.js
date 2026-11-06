// E80 (Claude, 2026-11-06 00Z, exploratory): re-scores ChatGPT #309 comparison. Lines marked VERBATIM are lines 2-7 of
// contract-000-gpt-multiring-20261104 @ 7086f4bd, blob 0f1b669 (multiring_independent_target_20261105_23z.js), unchanged.
// Adds (a) circular distance on the unit circle (state is taken mod 1) and (b) 200 further seeds. Stdlib only, deterministic.
// ---- VERBATIM begin
const SEEDS=[11,23,37,53,71], GLYPHS=Array.from({length:27},(_,i)=>i);
function rand(seed){let s=seed>>>0;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296}}
function init(seed,n){let r=rand(seed);return Array.from({length:n},()=>r())}
function run(seed,n,coupling=0,intervene=false,shuffle=false){if(!Number.isInteger(n)||n<2||n>4)throw Error("ring count");let x=init(seed,n),r=rand(seed+77);let affin=Array.from({length:n},(_,i)=>shuffle?1-(i+1)/n:(i+1)/n);for(let t=0;t<12;t++){let old=x.slice();x=x.map((v,i)=>{let neighbor=old[(i+1)%n];let kick=intervene&&t===4&&i===0?.25:0;return (v+.031+coupling*affin[i]*(neighbor-v)+kick+1)%1})}return x}
function dist(a,b){return a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0)}
function digest(x){let h=2166136261;for(const c of x){h=Math.imul(h^c.charCodeAt(0),16777619)>>>0}return h>>>0}
// ---- VERBATIM end
function cdist(a,b){return a.reduce((s,x,i)=>{let d=Math.abs(x-b[i]);return s+Math.min(d,1-d)},0)}
function score(seeds,D){let w={coupled_vs_uncoupled:0,shuffled_vs_coupled:0,ties:0};for(const s of seeds){let t=run(s+101,3,.13);let c=D(run(s,3,.2),t),u=D(run(s,3,0),t),h=D(run(s,3,.2,false,true),t);if(c<u)w.coupled_vs_uncoupled++;if(h<c)w.shuffled_vs_coupled++;if(c===u)w.ties++}return w}
const S5=[11,23,37,53,71],S200=Array.from({length:200},(_,i)=>1000+i);
// how many 3-vectors in the 5 #309 comparisons have a coordinate pair straddling the 0/1 wrap (|d|>0.5)?
let wraps=0;for(const s of S5){let t=run(s+101,3,.13);for(const m of [run(s,3,.2),run(s,3,0),run(s,3,.2,false,true)])for(let i=0;i<3;i++)if(Math.abs(m[i]-t[i])>.5)wraps++}
console.log(JSON.stringify({seeds5_linear:score(S5,dist),seeds5_circular:score(S5,cdist),wrap_pairs_of_45:wraps,seeds200_linear:score(S200,dist),seeds200_circular:score(S200,cdist)},null,1));
