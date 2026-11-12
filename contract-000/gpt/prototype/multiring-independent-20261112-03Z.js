// Independent Echo-GPT experimental code; Issue #433 preregistered before execution.
function simulate(seed,mode="triad",opts={}){
const glyphs=Array.from("אבגדהוזחטיכלמנסעפצקרשתךםןףץ"),gems=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
let mass=Array.from({length:3},(_,r)=>Array.from({length:27},(_,i)=>1+.14*Math.sin(seed*.19+i*.61+r*.8)));
let phase=Array.from({length:3},(_,r)=>Array.from({length:27},(_,i)=>seed*.03+i*.17+r*.6+(opts.phaseShift||0)));
let base=mass.flat().reduce((s,v)=>s+v,0),gain=opts.gain??.07;
let radius=Array.from({length:27},(_,i)=>1+(opts.deform?.1*Math.sin(i*.3+seed):0));
for(let t=0;t<12;t++){
let next=mass.map(a=>a.slice());
for(let r=0;r<3;r++)for(let i=0;i<27;i++){
let j=(i+1)%27,k=(i+2)%27,affinity=(opts.shuffle?gems[(i*7+3)%27]:gems[i])/(gems[i]+400);
let phi=phase[r][i],psi=phase[(r+1)%3][j],omega=phase[(r+2)%3][k];
let coupling=mode==="triad"?Math.sin(psi+omega-2*phi):mode==="pair"?Math.sin(psi-phi):0;
let radiusFactor=opts.feedback?1+.5*(radius[i]-1):1;
let flux=gain*(.3+affinity)*coupling*Math.min(mass[r][i],mass[r][j])*.1*radiusFactor;
next[r][i]-=flux;next[r][j]+=flux;
}
mass=next;
phase=phase.map((a,r)=>a.map((v,i)=>v+.04*(1+(opts.commonFrequency||0))+.003*(r+1)*Math.sin(i+seed)+(opts.heterogeneous?.015*Math.sin(i*.71+r*1.3):0)));
}
return {glyphs,mass,base,total:mass.flat().reduce((s,v)=>s+v,0),radius,projection:Array.from({length:27},(_,i)=>mass.reduce((s,a)=>s+a[i],0))};
}
function runTests(){
let seeds=[11,23,37,53],rows=[];
for(const seed of seeds){
let a=simulate(seed),b=simulate(seed),p=simulate(seed,"pair"),z=simulate(seed,"triad",{gain:0}),u=simulate(seed,"none"),sh=simulate(seed,"triad",{shuffle:true}),fr=simulate(seed,"triad",{heterogeneous:true}),common=simulate(seed,"triad",{commonFrequency:.8}),rot=simulate(seed,"triad",{phaseShift:1.3}),de=simulate(seed,"triad",{deform:true}),feedback=simulate(seed,"triad",{deform:true,feedback:true});
let L=(x,y)=>x.mass.flat().reduce((s,v,i)=>s+Math.abs(v-y.mass.flat()[i]),0);
let target=Array.from({length:27},(_,i)=>3+.2*Math.sin(i*.37+seed*.13)),mae=x=>x.projection.reduce((s,v,i)=>s+Math.abs(v-target[i]),0)/27;
let tests={replay:L(a,b)<1e-12,identity:new Set(a.glyphs).size===27&&a.glyphs.length===27,nonnegative:Math.min(...a.mass.flat())>=0,conservation:Math.abs(a.total-a.base)<1e-9,zero_gain:L(z,u)<1e-12,common_phase:L(a,rot)<1e-9,triadic_pairwise:L(a,p)>1e-6,shuffled_affinity:L(a,sh)>1e-7,heterogeneous_frequency:L(a,fr)>1e-8&&L(a,common)<1e-8,boundary_feedback:L(de,feedback)>1e-8&&Number.isFinite(mae(a))&&Number.isFinite(mae(u))};
rows.push({seed,tests,l1_pair:L(a,p),l1_shuffle:L(a,sh),l1_heterogeneous:L(a,fr),l1_common_frequency:L(a,common),l1_boundary_feedback:L(de,feedback),mass_error:Math.abs(a.total-a.base),triad_mae:mae(a),uncoupled_mae:mae(u)});
}
return {seeds,rows,passed:rows.reduce((s,x)=>s+Object.values(x.tests).filter(Boolean).length,0),total:40};
}
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(runTests(),null,2)+"\n");
