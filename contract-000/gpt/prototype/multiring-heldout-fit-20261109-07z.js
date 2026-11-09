/* GPT-only 07Z held-out portfolio. Prospective #367 comment 6734276577. Offline deterministic V8. */
return (()=>{"use strict";
const seeds=[3301,3302,3303,3304],results=[];
const rng=s=>()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296};
const mse=(a,b)=>a.reduce((s,v,i)=>s+(v-b[i])**2,0)/a.length;
const generate=(seed,n,mode)=>{let r=rng(seed),out=[];for(let i=0;i<n;i++){let x=2*r()-1,z=2*r()-1,e=.04*(2*r()-1);out.push({x,z,y:mode==="null"?e:.25*x+.65*z+e})}return out};
const fit=(rows,two)=>{let xx=0,zz=0,xz=0,xy=0,zy=0;for(let {x,z,y} of rows){xx+=x*x;zz+=z*z;xz+=x*z;xy+=x*y;zy+=z*y}let d=xx*zz-xz*xz;return two?[(xy*zz-zy*xz)/d,(zy*xx-xy*xz)/d]:[xy/xx,0]};
const predict=(rows,c,transform=(x,z)=>[x,z])=>rows.map(o=>{let [x,z]=transform(o.x,o.z);return c[0]*x+c[1]*z});
for(let seed of seeds){
 const train=generate(seed,128,"signal"),test=generate(seed+10000,64,"signal"),nullTrain=generate(seed+20000,128,"null"),nullTest=generate(seed+30000,64,"null");
 const c=fit(train,true),u=fit(train,false),cn=fit(nullTrain,true),y=test.map(o=>o.y),yn=nullTest.map(o=>o.y);
 const fitted=mse(y,predict(test,c)),zero=mse(y,test.map(()=>0)),unc=mse(y,predict(test,u)),shuffle=mse(y,test.map((o,i)=>c[0]*o.x+c[1]*test[(i+17)%test.length].z)),phase=mse(y,predict(test,c,(x,z)=>[x,-z])),detune=mse(y,predict(test,c,(x,z)=>[x,.5*z]));
 const nullFit=mse(yn,predict(nullTest,cn)),nullZero=mse(yn,nullTest.map(()=>0));
 const glyphs=Array.from({length:27},(_,i)=>"g"+String(i).padStart(2,"0")),cube=Array.from({length:27},(_,i)=>glyphs[i]),core=JSON.stringify({id:"A-000",v:1}),mutable={tick:0};mutable.tick++;
 const radius=Array.from({length:27},(_,i)=>1+.15*Math.sin((seed+i)/27));
 const tests={T1_two_order:[glyphs[2],glyphs[9]].join("|")==="g02|g09",T2_three_order:[glyphs[2],glyphs[9],glyphs[17]].join("|")==="g02|g09|g17",T3_projection:new Set(cube).size===27,T4_identity:core===JSON.stringify({id:"A-000",v:1})&&mutable.tick===1,T5_fit_zero:fitted<zero,T6_fit_uncoupled:fitted<unc,T7_shuffle:shuffle>fitted,T8_phase:phase>fitted,T9_detune:detune>fitted,T10_null_radius:radius.every(v=>v>=.85&&v<=1.15)&&nullFit<nullZero*.99===false};
 results.push({seed,coefficients:c.map(v=>+v.toFixed(5)),mse:{fitted,zero,unc,shuffle,phase,detune,nullFit,nullZero},tests});
}
return {version:"07z",seeds,train_size:128,test_size:64,results,passed:results.reduce((s,r)=>s+Object.values(r.tests).filter(Boolean).length,0),total:40,limitations:"Synthetic linear generator; training and test PRNG distinct but same model family; T4 structural only, T10 null margin criterion arbitrary; no semantic understanding or external causality established."};
})();