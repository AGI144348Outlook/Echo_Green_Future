(function experiment(){
const seeds=[11,23,37,53], N=27, TAU=2*Math.PI;
const glyph=Array.from({length:N},(_,i)=>i);
const gem=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,20,40,50,80];
const xyz=i=>[Math.floor(i/9),Math.floor(i%9/3),i%3];
const inv=c=>9*c[0]+3*c[1]+c[2];
const run=(seed,mode)=>{
let state=seed>>>0; const rand=()=>((state=(Math.imul(state,1664525)+1013904223)>>>0)/4294967296);
let p=Array.from({length:N},()=>rand()*TAU),w=Array.from({length:N},()=>.02+.03*rand()),rad=Array(N).fill(1);
const g=mode==="shuffle"?gem.slice().reverse():gem;
for(let t=0;t<16;t++){const prev=p.slice();p=p.map((v,i)=>{
const j=(i+1)%N,k=(i+9)%N;
const pair=(mode==="zero"||mode==="uncoupled")?0:.09*Math.sin(prev[j]-v);
const tri=(mode==="triad")?.045*Math.sin(prev[j]+prev[k]-2*v):0;
const aff=(mode==="shuffle"?.015*g[i]/500:0);
return v+w[i]+pair+tri+aff;
});if(mode==="deform")rad=rad.map((v,i)=>Math.max(.85,Math.min(1.15,v+.01*Math.sin(p[i]))));}
return {p,rad};
};
const dist=(a,b)=>a.p.reduce((s,x,i)=>s+Math.abs(Math.atan2(Math.sin(x-b.p[i]),Math.cos(x-b.p[i]))),0)/N;
let rows=[];
for(const seed of seeds){
const zero=run(seed,"zero"),base=run(seed,"pair"),tri=run(seed,"triad"),sh=run(seed,"shuffle"),de=run(seed,"deform");
const checks=[
["unique27",new Set(glyph).size===27],
["projection27",glyph.every(i=>inv(xyz(i))===i)],
["ordered4",JSON.stringify([glyph[0],glyph[1],glyph[2],glyph[3]])==="[0,1,2,3]"],
["deterministic",JSON.stringify(base)===JSON.stringify(run(seed,"pair"))],
["noop",dist(zero,run(seed,"zero"))===0],
["uncoupled",dist(zero,run(seed,"uncoupled"))===0],
["pair-intervention",dist(base,zero)>0],
["triadic-ablation",dist(tri,base)>0],
["shuffled-affinity",dist(sh,base)>0],
["boundary",de.rad.every(x=>x>=.85&&x<=1.15)]
];rows.push({seed,checks:Object.fromEntries(checks),metrics:{pair_vs_zero:dist(base,zero),tri_vs_pair:dist(tri,base),shuffle_vs_pair:dist(sh,base),deform_min:Math.min(...de.rad),deform_max:Math.max(...de.rad)}});
}
return {rows,pass:rows.reduce((n,r)=>n+Object.values(r.checks).filter(Boolean).length,0),total:40};
})();
