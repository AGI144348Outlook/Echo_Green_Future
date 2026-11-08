// Echo-GPT standalone synthetic portfolio 05Z; preregistration Issue #347. No external effects.
const seeds=[3301,3302,3303,3304], glyphs=Array.from({length:27},(_,i)=>i), anchor="A-000|RESH|v1";
function run(seed){
 const phase=(seed%97)/97, occupancy=glyphs.map((_,i)=>(i+seed%27)%27);
 const neighbors=i=>{let x=i%3,y=Math.floor(i/3)%3,z=Math.floor(i/9),o=[];for(const [a,b,c] of [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]){let X=x+a,Y=y+b,Z=z+c;if(X>=0&&X<3&&Y>=0&&Y<3&&Z>=0&&Z<3)o.push(X+3*Y+9*Z)}return o};
 const field=glyphs.map(i=>Math.sin((occupancy[i]+1)*.27+phase));
 const score=(variant, intervention=0)=>glyphs.map(i=>{let radius=1+.12*Math.sin(phase+i*.13);let v=field[i]*.12; if(variant==="noop")return 0;if(variant==="uncoupled")return v;let sum=neighbors(i).reduce((a,j)=>a+field[j]+(j===13?intervention:0),0);let c=variant==="reverse"?-.035:.035;if(variant==="shuffle")sum=neighbors(i).reduce((a,j)=>a+field[(j*11+7)%27],0);return v+c*sum/6*radius});
 const target=glyphs.map(i=>.12*Math.sin((i+1)*.27+phase*.7));
 const mse=a=>a.reduce((s,v,i)=>s+(v-target[i])**2,0)/27;
 const coupled=score("coupled"), uncoupled=score("uncoupled"), shuffled=score("shuffle"), noop=score("noop"), reverse=score("reverse");
 const t=[
 ["T1",new Set(glyphs).size===27],
 ["T2",JSON.stringify(score("coupled"))===JSON.stringify(score("coupled"))],
 ["T3",new Set(occupancy).size===27&&occupancy.every(x=>x>=0&&x<27)],
 ["T4",occupancy.slice(0,2).length===2&&occupancy[0]!==occupancy[1]],
 ["T5",occupancy.slice(0,3).length===3&&new Set(occupancy.slice(0,3)).size===3],
 ["T6",glyphs.every(i=>Math.abs(.12*Math.sin(phase+i*.13))<=.12+1e-12)],
 ["T7",anchor==="A-000|RESH|v1"],
 ["T8",Math.abs(score("coupled",.4)[12]-coupled[12])>1e-6&&Math.abs(score("coupled",.4)[0]-coupled[0])<1e-12],
 ["T9",Number.isFinite(mse(coupled))&&Number.isFinite(mse(uncoupled))],
 ["T10",[shuffled,noop,reverse].every(v=>Number.isFinite(mse(v)))]
 ];
 return {seed,checks:t,mse:{coupled:mse(coupled),uncoupled:mse(uncoupled),shuffled:mse(shuffled),noop:mse(noop),reverse:mse(reverse)},intervention:{neighbor:score("coupled",.4)[12]-coupled[12],far:score("coupled",.4)[0]-coupled[0]}};
}
JSON.stringify(seeds.map(run));