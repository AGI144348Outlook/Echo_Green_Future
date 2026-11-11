// Echo-GPT synthetic multiring controlled portfolio, 2026-11-11 20Z. No external I/O.
(function(){
const seeds=[11,23,37,53],out=[];
const l1=(a,b)=>a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0);
function run(seed,mode="pair",opts={}){
let state=Array.from({length:3},(_,r)=>Array.from({length:27},(_,i)=>1+((seed+7*i+11*r)%17)/17));
let phase=Array.from({length:3},(_,r)=>0.17*r+0.01*seed+(opts.shift||0));
const initial=state.flat(),total=initial.reduce((a,b)=>a+b,0);
const aff=opts.shuffle?[2,0,1]:[0,1,2];
for(let t=0;t<8;t++){
let next=state.map(row=>row.slice());
for(let i=0;i<27;i++){
const g=mode==="none"?0:0.016;
const p=(r,s)=>Math.sin(phase[s]-phase[r]+0.03*(aff[s]-aff[r]));
const tri=(r,s,u)=>Math.sin(phase[s]+phase[u]-2*phase[r]+0.03*(aff[s]+aff[u]-2*aff[r]));
const d01=g*(mode==="triad"?tri(0,1,2):p(0,1))*(state[0][i]+state[1][i])/2;
const d12=g*(mode==="triad"?tri(1,2,0):p(1,2))*(state[1][i]+state[2][i])/2;
next[0][i]-=d01;next[1][i]+=d01-d12;next[2][i]+=d12;
}
state=next;
}
if(opts.local){state[0][7]-=0.05;state[1][7]+=0.05;}
return {flat:state.flat(),projection:Array.from({length:27},(_,i)=>state[0][i]+state[1][i]+state[2][i]),total,initial};
}
for(const seed of seeds){
const pair=run(seed),tri=run(seed,"triad"),none=run(seed,"none"),shift=run(seed,"pair",{shift:1.23}),shuffle=run(seed,"pair",{shuffle:true}),local=run(seed,"pair",{local:true}),zero=run(seed,"none",{shuffle:true});
const replay=run(seed);
const mae=(x,y)=>l1(x,y)/x.length;
const checks={
replay:l1(pair.flat,replay.flat)<1e-12,
projection27:pair.projection.length===27,
nonnegative:Math.min(...tri.flat)>0,
mass:Math.abs(tri.flat.reduce((a,b)=>a+b,0)-tri.total)<1e-9,
commonPhase:l1(pair.flat,shift.flat)<1e-9,
triadVsPair:l1(pair.flat,tri.flat)>1e-5,
zeroGain:l1(none.flat,zero.flat)<1e-12,
shuffledAffinity:l1(pair.flat,shuffle.flat)>1e-5,
localIntervention:l1(pair.flat,local.flat)>0.09,
holdoutMAE: Number.isFinite(mae(tri.flat,none.initial)) && Number.isFinite(mae(none.flat,none.initial))
};
out.push({seed,checks,metrics:{triad_pair_l1:l1(tri.flat,pair.flat),shuffled_l1:l1(pair.flat,shuffle.flat),local_l1:l1(pair.flat,local.flat),aggregate_l1:l1(pair.projection,tri.projection),triad_mae:mae(tri.flat,none.initial),uncoupled_mae:mae(none.flat,none.initial),mass_error:Math.abs(tri.flat.reduce((a,b)=>a+b,0)-tri.total)}});
}
return {experiment:"echo-gpt-multiring-20z",seeds,types:10,results:out,passed:out.reduce((s,o)=>s+Object.values(o.checks).filter(Boolean).length,0),total:40};
})()