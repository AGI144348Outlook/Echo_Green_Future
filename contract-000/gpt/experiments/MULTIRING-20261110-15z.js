// GPT-owned independent offline simulation; prospective Issue #396 before any execution.
(function () {
"use strict";
const seeds=[11,23,47,89], ids=Array.from({length:27},(_,i)=>"glyph-"+String(i).padStart(2,"0"));
const sum=a=>a.reduce((s,v)=>s+v,0), l1=(a,b)=>a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0);
function permutation(seed){let p=Array.from({length:27},(_,i)=>i),x=seed>>>0;for(let i=26;i>0;i--){x=(Math.imul(x,1664525)+1013904223)>>>0;let j=x%(i+1);[p[i],p[j]]=[p[j],p[i]];}return p;}
function run(seed,{ticks=9,k=.16,reverse=.07,phase=0,freq=1,shuffle=false,empty=false}={}){
let A=Array.from({length:27},(_,i)=>empty?0:1+((i*7+seed)%13)/17), B=Array(27).fill(0);
const initialA=A.slice(),initialB=B.slice(),before=sum(A)+sum(B),map=shuffle?permutation(seed):Array.from({length:27},(_,i)=>i);
for(let t=0;t<ticks;t++){let na=A.slice(),nb=B.slice();for(let i=0;i<27;i++){
const j=map[i],angle=2*Math.PI*(freq*t+i+phase)/27,weight=.5+.5*Math.cos(angle);
const f=Math.min(A[i],A[i]*k*weight),b=Math.min(B[j],B[j]*reverse*weight);
na[i]+=b-f;nb[j]+=f-b;
}A=na;B=nb;}
return {A,B,initialA,initialB,before,after:sum(A)+sum(B)};
}
function check(seed){
const b9=run(seed),b27=run(seed,{ticks:27}),b54=run(seed,{ticks:54}),replay=run(seed);
const unc=run(seed,{k:0,reverse:0}),empty=run(seed,{empty:true}),p9=run(seed,{phase:7}),p27=run(seed,{ticks:27,phase:7}),p54=run(seed,{ticks:54,phase:7});
const freq=run(seed,{freq:1.13}),shuffled=run(seed,{shuffle:true}),noreverse=run(seed,{reverse:0});
const phase9=l1(b9.B,p9.B),phase27=l1(b27.B,p27.B),phase54=l1(b54.B,p54.B);
const freqL1=l1(b9.B,freq.B),shuffleL1=l1(b9.B,shuffled.B),reverseL1=l1(b9.B,noreverse.B);
const err=Math.max(...[b9,b27,b54,p9,p27,p54,freq,shuffled,noreverse,unc,empty].map(x=>Math.abs(x.after-x.before)));
const tests={
T1:ids.length===27&&new Set(ids).size===27,
T2:err<1e-9,
T3:[b9,b27,b54,p9,p27,p54,freq,shuffled,noreverse,unc,empty].every(x=>[...x.A,...x.B].every(v=>v>=-1e-12)),
T4:JSON.stringify(b9)===JSON.stringify(replay),
T5:l1(unc.A,unc.initialA)+l1(unc.B,unc.initialB)===0,
T6:empty.after===0&&empty.A.every(v=>v===0)&&empty.B.every(v=>v===0),
T7:[phase9,phase27,phase54].every(Number.isFinite),
T8:freqL1>1e-10,
T9:shuffleL1>1e-10,
T10:reverseL1>1e-10
};
return {seed,tests,metrics:{max_mass_error:err,phase9,phase27,phase54,freq_l1:freqL1,shuffle_l1:shuffleL1,reverse_l1:reverseL1}};
}
return {protocol:"GPT-15Z-396",seeds,results:seeds.map(check)};
})()