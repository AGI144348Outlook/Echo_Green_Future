// GPT-only synthetic multiring experiment; Issue #399 preregistered before execution.
const seeds=[11,23,47,89], N=27, steps=9;
function init(seed){let a=Array.from({length:N},(_,i)=>1+((seed+i*7)%13)/20), b=Array.from({length:N},(_,i)=>1+((seed+i*11)%17)/20);return {a,b,ids:Array.from({length:N},(_,i)=>"glyph-"+i)}}
function simulate(seed,mode="base"){let s=init(seed),start=s.a.concat(s.b).reduce((x,y)=>x+y,0);let rng=seed>>>0;const rand=()=>{rng=(Math.imul(1664525,rng)+1013904223)>>>0;return rng/4294967296};let perm=Array.from({length:N},(_,i)=>i);if(mode==="shuffle")for(let i=N-1;i>0;i--){let j=Math.floor(rand()*(i+1));[perm[i],perm[j]]=[perm[j],perm[i]]};let radius=Array.from({length:N},(_,i)=>1);for(let t=0;t<steps;t++){let da=Array(N).fill(0),db=Array(N).fill(0);for(let i=0;i<N;i++){let j=mode==="shuffle"?perm[i]:i;if(mode==="phase")j=(i+7+t)%N;let affinity=mode==="gematria"?1+(((i%9)+1)*((j%9)+1)%7)/10:1;let gain=(mode==="noop"||mode==="uncoupled")?0:0.035*affinity;if(mode==="knockout"&&i===0)gain=0;let transfer=Math.min(s.a[i],s.a[i]*gain);da[i]-=transfer;db[j]+=transfer;let back=Math.min(s.b[j],s.b[j]*gain*0.6);db[j]-=back;da[i]+=back;if(mode==="deform")radius[i]=1+0.15*Math.sin((i+t)*Math.PI/13.5)}for(let i=0;i<N;i++){s.a[i]+=da[i];s.b[i]+=db[i]}}return {...s,radius,total:s.a.concat(s.b).reduce((x,y)=>x+y,0),start}}
const L1=(x,y)=>x.reduce((z,v,i)=>z+Math.abs(v-y[i]),0);
function run(){let results=[];for(let seed of seeds){let base=simulate(seed), initial=init(seed), noop=simulate(seed,"noop"),unc=simulate(seed,"uncoupled"),sh=simulate(seed,"shuffle"),gem=simulate(seed,"gematria"),phase=simulate(seed,"phase"),def=simulate(seed,"deform"),ko=simulate(seed,"knockout");let tests=[
["T1_ids",base.ids.length===N&&new Set(base.ids).size===N],
["T2_replay",JSON.stringify(base)===JSON.stringify(simulate(seed))],
["T3_noop",L1(noop.a,initial.a)+L1(noop.b,initial.b)<1e-12],
["T4_uncoupled",L1(unc.a,initial.a)+L1(unc.b,initial.b)<1e-12],
["T5_mass",Math.abs(base.total-base.start)<1e-9&&Math.min(...base.a,...base.b)>=0],
["T6_shuffle",L1(base.b,sh.b)>1e-8],
["T7_gematria",L1(base.b,gem.b)>1e-8],
["T8_phase",L1(base.b,phase.b)>1e-8],
["T9_deform",def.radius.every(r=>r>=0.85&&r<=1.15)],
["T10_knockout",L1(base.b,ko.b)>1e-8]];
results.push({seed,tests,metrics:{mass_error:base.total-base.start,shuffle:L1(base.b,sh.b),gematria:L1(base.b,gem.b),phase:L1(base.b,phase.b),knockout:L1(base.b,ko.b),deform_min:Math.min(...def.radius),deform_max:Math.max(...def.radius)}})}return results}
