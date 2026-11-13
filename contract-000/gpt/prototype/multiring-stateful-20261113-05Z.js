function experiment(seed,opt={}){
const N=27,pi=Math.PI, rnd=(s)=>{let x=s>>>0;return ()=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return x/4294967296}};
const rand=rnd(seed),phase=Array.from({length:N},()=>2*pi*rand()+(opt.shift||0)),omega=Array.from({length:N},(_,i)=>0.002*(i%7-3)),weights=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];if(opt.shuffle){let r=rnd(seed+991);for(let i=N-1;i>0;i--){let j=Math.floor(r()*(i+1));[weights[i],weights[j]]=[weights[j],weights[i]]}}
let matrix=Array.from({length:N},(_,i)=>i),warehouse=Array(N).fill(null),memory=Array(N).fill(0),events=0,maxOccupancy=0,history=[];
for(let t=0;t<16;t++){
if(opt.contact!==false&&[3,7,11].includes(t)){for(let i=0;i<N;i++){if((i+t)%4===0&&matrix[i]!==null&&warehouse[i]===null){warehouse[i]=matrix[i];matrix[i]=null;memory[i]=Math.sin(phase[i]);events++}}}
if([5,9,13].includes(t)){for(let i=0;i<N;i++)if(warehouse[i]!==null){matrix[i]=warehouse[i];warehouse[i]=null}}
maxOccupancy=Math.max(maxOccupancy,warehouse.filter(x=>x!==null).length);
const old=phase.slice();for(let i=0;i<N;i++){
const b=old[(i+1)%N],c=old[(i+2)%N],p=old[i];
const dyadic=Math.sin(b-p),triadic=Math.sin(b+c-2*p);
const influence=(opt.feedback===false||opt.sham)?0:0.015*memory[i];
phase[i]=p+(opt.uncoupled?0:0.025*(weights[i]/400)*(dyadic+(opt.triadic===false?0:0.5*triadic)))+influence+(opt.detune?omega[i]:0);
}history.push(phase.reduce((a,b)=>a+Math.cos(b),0)/N)}
return {phase,matrix,warehouse,memory,events,maxOccupancy,history}
}
if (typeof module !== 'undefined' && require.main === module) console.log(JSON.stringify([11,23,37,53].map(seed=>experiment(seed))));
