// GPT-owned offline synthetic two-ring test; preregistration Issue #395 before source commit and execution.
(function(){
const seeds=[11,23,47,89], glyphs=Array.from({length:27},(_,i)=>"glyph-"+String(i).padStart(2,"0"));
const sum=a=>a.reduce((s,x)=>s+x,0), l1=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);
function perm(seed){let a=Array.from({length:27},(_,i)=>i),x=seed>>>0;for(let i=26;i>0;i--){x=(1664525*x+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function run(seed,opt={}){
const {k=.16,reverse=.07,shuffle=false,phase=0,drift=0,zero=false,ticks=9}=opt;
let A=Array.from({length:27},(_,i)=>zero?0:1+((i*7+seed)%13)/17),B=Array(27).fill(0);
const initialA=A.slice(),initialB=B.slice(),before=sum(A)+sum(B),map=shuffle?perm(seed):Array.from({length:27},(_,i)=>i);
for(let t=0;t<ticks;t++){let na=A.slice(),nb=B.slice();for(let i=0;i<27;i++){
const j=map[i],theta=2*Math.PI*(t+i+phase+drift*t*t/27)/27,scale=.5+.5*Math.cos(theta);
const f=Math.min(A[i],A[i]*k*scale),b=Math.min(B[j],B[j]*reverse*scale);
na[i]+=b-f;nb[j]+=f-b;}A=na;B=nb;}
return {A,B,initialA,initialB,before,after:sum(A)+sum(B)};
}
function check(seed){
const base=run(seed),replay=run(seed),unc=run(seed,{k:0,reverse:0}),empty=run(seed,{zero:true}),one=run(seed,{reverse:0}),shuffle=run(seed,{shuffle:true}),phase=run(seed,{phase:7}),drift=run(seed,{drift:.73});
const tests={T1:glyphs.length===27&&new Set(glyphs).size===27,T2:Math.abs(base.before-base.after)<1e-9,T3:[...base.A,...base.B].every(x=>x>=-1e-12),T4:JSON.stringify(base)===JSON.stringify(replay),T5:l1(unc.A,unc.initialA)+l1(unc.B,unc.initialB)===0,T6:empty.after===0&&empty.A.every(x=>x===0)&&empty.B.every(x=>x===0),T7:l1(base.B,one.B)>1e-10,T8:l1(base.B,shuffle.B)>1e-10,T9:l1(base.B,phase.B)>1e-10,T10:l1(base.B,drift.B)>1e-10};
return {seed,tests,metrics:{mass_error:Math.abs(base.before-base.after),reverse_l1:l1(base.B,one.B),shuffle_l1:l1(base.B,shuffle.B),phase_l1:l1(base.B,phase.B),drift_l1:l1(base.B,drift.B),uncoupled_l1:l1(unc.A,unc.initialA)+l1(unc.B,unc.initialB)}};
}
return {protocol:"GPT-14Z-395",seeds,ticks:9,results:seeds.map(check)};
})()