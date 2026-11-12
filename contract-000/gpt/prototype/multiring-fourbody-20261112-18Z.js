function rng(seed){let x=seed>>>0;return ()=>{x=(1664525*x+1013904223)>>>0;return x/4294967296}}

function initial(seed){const R=rng(seed);return Array.from({length:27},(_,i)=>({id:i,phase:R()*Math.PI*2,weight:1,radius:1,aff:(i%9+1)}))}

function model(seed,opts={}){const a=initial(seed),R=rng(seed+777);let perm=Array.from({length:27},(_,i)=>i);if(opts.shuffle){for(let i=26;i>0;i--){const j=Math.floor(R()*(i+1));[perm[i],perm[j]]=[perm[j],perm[i]]}}let p=a.map(x=>x.phase+(opts.shift||0)),radius=a.map(x=>x.radius);const rings=opts.rings||3;const strength=opts.strength===undefined?0.025:opts.strength;for(let t=0;t<16;t++){const q=p.map((v,i)=>{const b=p[(i+1)%27],c=p[(i+2)%27],d=p[(i+3)%27];const pair=Math.sin(b-v);const tri=Math.sin(b+c-2*v);const four=Math.sin(b+c+d-3*v);const affinity=(perm[i]%9+1)/9;const term=pair+(rings>=3?0.6*tri:0)+(rings>=4?0.35*four:0);return v+strength*affinity*term+(opts.detune?0.0005*(i%5-2):0)});p=q;if(opts.deform)radius=radius.map((v,i)=>Math.max(0.8,Math.min(1.2,v+0.003*Math.sin(p[i]-p[(i+1)%27]))))}return {ids:a.map(x=>x.id),weights:a.map(x=>x.weight),phase:p,radius}}

function delta(a,b){return a.phase.reduce((s,x,i)=>s+Math.abs(Math.sin((x-b.phase[i])/2)),0)}

function test(seed){const base=model(seed),again=model(seed),no=model(seed,{strength:0}),orig=initial(seed),unc=model(seed,{strength:0,rings:4}),shuffle=model(seed,{shuffle:true}),pair=model(seed,{rings:2}),four=model(seed,{rings:4}),shift=model(seed,{shift:0.9}),deform=model(seed,{deform:true});const checks=[
["unique_ids",new Set(base.ids).size===27],
["inverse_3cube",base.ids.every(i=>{let x=Math.floor(i/9),y=Math.floor(i/3)%3,z=i%3;return x*9+y*3+z===i})],
["deterministic_replay",JSON.stringify(base)===JSON.stringify(again)],
["no_op_null",no.phase.every((x,i)=>x===orig[i].phase)],
["uncoupled_null",unc.phase.every((x,i)=>x===orig[i].phase)],
["shuffled_affinity",delta(base,shuffle)>1e-8],
["triadic_pairwise",delta(base,pair)>1e-8],
["four_vs_three",delta(base,four)>1e-8],
["phase_shift_symmetry",Math.max(...base.phase.map((x,i)=>Math.abs(Math.sin((shift.phase[i]-x-0.9)/2))))<1e-12],
["boundary_and_mass",deform.radius.every(x=>x>=0.8&&x<=1.2)&&deform.weights.reduce((a,b)=>a+b,0)===27]
];return {seed,checks,metrics:{shuffle:delta(base,shuffle),triadic:delta(base,pair),four:delta(base,four),phaseError:Math.max(...base.phase.map((x,i)=>Math.abs(Math.sin((shift.phase[i]-x-0.9)/2))))}}}

if (typeof module !== 'undefined' && require.main === module) console.log(JSON.stringify([11,23,37,53].map(test),null,2));
