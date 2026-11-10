// GPT-only bounded multiring experiment; Issue #394 preregistered before execution.
(function(){
const seeds=[11,23,47,89], glyphs=Array.from({length:27},(_,i)=>"glyph-"+String(i).padStart(2,"0"));
const total=a=>a.reduce((s,x)=>s+x,0), l1=(a,b)=>a.reduce((s,x,i)=>s+Math.abs(x-b[i]),0);
function perm(seed){let a=Array.from({length:27},(_,i)=>i),x=seed>>>0;for(let i=26;i>0;i--){x=(1664525*x+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function run(seed,opt={}){
 const {k=.16,reverse=.07,shuffle=false,phase=0,knockout=-1,zero=false}=opt;
 let A=Array.from({length:27},(_,i)=>zero?0:1+((i*7+seed)%13)/17), B=Array(27).fill(0), map=shuffle?perm(seed):Array.from({length:27},(_,i)=>i);
 const before=total(A)+total(B),initialA=A.slice(),initialB=B.slice();
 for(let t=0;t<27;t++){let nextA=A.slice(),nextB=B.slice();for(let i=0;i<27;i++){if(i===knockout)continue;let j=map[i],scale=0.5+0.5*Math.cos(2*Math.PI*(t+i+phase)/27),forward=Math.min(A[i],A[i]*k*scale),back=Math.min(B[j],B[j]*reverse*scale);nextA[i]+=-forward+back;nextB[j]+=forward-back}A=nextA;B=nextB}
 return {A,B,before,after:total(A)+total(B),initialA,initialB};
}
function check(seed){
 let base=run(seed),replay=run(seed),uncoupled=run(seed,{k:0,reverse:0}),empty=run(seed,{zero:true}),oneway=run(seed,{reverse:0}),shuffled=run(seed,{shuffle:true}),shift=run(seed,{phase:7}),knock=run(seed,{knockout:3});
 let values=[...base.A,...base.B];
 return {seed,tests:{
 T1:glyphs.length===27&&new Set(glyphs).size===27,
 T2:Math.abs(base.before-base.after)<1e-9,
 T3:values.every(x=>x>=-1e-12),
 T4:JSON.stringify(base)===JSON.stringify(replay),
 T5:l1(uncoupled.A,uncoupled.initialA)===0&&l1(uncoupled.B,uncoupled.initialB)===0,
 T6:empty.after===0&&empty.A.every(x=>x===0)&&empty.B.every(x=>x===0),
 T7:l1(base.A,oneway.A)+l1(base.B,oneway.B)>1e-10,
 T8:l1(base.B,shuffled.B)>1e-10,
 T9:l1(base.B,shift.B)>1e-10,
 T10:l1(base.B,knock.B)>1e-10
 },metrics:{mass_error:Math.abs(base.before-base.after),reverse_l1:l1(base.B,oneway.B),shuffle_l1:l1(base.B,shuffled.B),phase_l1:l1(base.B,shift.B),knockout_l1:l1(base.B,knock.B),uncoupled_initial_l1:l1(uncoupled.A,uncoupled.initialA)+l1(uncoupled.B,uncoupled.initialB)}};
}
return {protocol:"GPT-13Z-394",seeds,results:seeds.map(check)};
})()