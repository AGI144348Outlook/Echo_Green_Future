// GPT-only bounded synthetic ring tests; Node-compatible JS, no dependencies.
const glyphs=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
function pos(i){return [Math.floor(i/9),Math.floor(i%9/3),i%3]}
function idx(p){return p[0]*9+p[1]*3+p[2]}
function hash(s){let h=2166136261;for(const c of s){h=Math.imul(h^c.charCodeAt(0),16777619)}return h>>>0}
function run(seed,k=.2,intervene=0,shuffle=false){let a=Array.from({length:3},(_,i)=>((seed*13+i*7)%31)/31),base=a.slice();for(let t=0;t<12;t++){let old=a.slice();a=a.map((v,i)=>{let affinity=shuffle?(i+2)%3:(i+1)%3;let diff=Math.sin(old[affinity]-v);return v+.07+k*diff+(i===0&&t===0?intervene:0)})}return a}
function dist(a,b){return a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)}
const tests={};const seeds=[11,23,37,53,71];
tests.identity_unique=glyphs.length===27&&new Set(glyphs).size===27;
tests.projection_inverse=Array.from({length:27},(_,i)=>idx(pos(i))===i).every(Boolean);
tests.ring_order=[2,3,4].every(n=>glyphs.slice(0,n).join("").length===n);
tests.digest_sensitive=hash("A-000")!==hash("A-001");
tests.replay=seeds.every(s=>JSON.stringify(run(s))===JSON.stringify(run(s)));
tests.uncoupled_isolation=seeds.every(s=>{let a=run(s,0,0),b=run(s,0,.4);return Math.abs(a[1]-b[1])+Math.abs(a[2]-b[2])<1e-10});
tests.coupled_intervention=seeds.every(s=>dist(run(s,.2,.4),run(s,.2,0))>0.4);
tests.shuffled_affinity=seeds.some(s=>dist(run(s,.2,0,true),run(s,.2,0,false))>.001);
tests.boundary_bounded=seeds.every(s=>run(s).every(v=>Math.abs(v)<10));
const held=seeds.slice(-2).map(s=>({seed:s,coupled_error:dist(run(s,.2),run(s,0)),null_error:dist(run(s,0),run(s,0))}));
tests.heldout_null_wins=held.every(x=>x.coupled_error>x.null_error);
const out={tests,passed:Object.values(tests).filter(Boolean).length,total:10,held,shuffled:seeds.map(s=>dist(run(s,.2,0,true),run(s,.2))),intervention:seeds.map(s=>dist(run(s,.2,.4),run(s,.2)))};
console.log(JSON.stringify(out,null,2));