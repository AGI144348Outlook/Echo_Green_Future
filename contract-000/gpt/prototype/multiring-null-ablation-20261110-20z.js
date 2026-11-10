// GPT-only offline synthetic experiment. Prospectively registered Issue #401.
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const VALUES=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const SEEDS=[11,23,47,89],N=27;
const initial=seed=>Array.from({length:2},()=>Array.from({length:N},(_,i)=>({id:GLYPHS[i],mass:(1+((i*7+seed)%17)/17)/2})));
const total=a=>a.flat().reduce((s,x)=>s+x.mass,0);
const l1=(a,b)=>a.flat().reduce((s,x,i)=>s+Math.abs(x.mass-b.flat()[i].mass),0);
function permutation(seed){let a=VALUES.slice(),x=seed>>>0;for(let i=N-1;i>0;i--){x=(1664525*x+1013904223)>>>0;let j=x%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}
function simulate(seed,{gain=.12,uncoupled=false,values=VALUES,gate=true,phase=0,knock=-1,frequency=1}={}){
 const a=initial(seed),before=total(a),labels=a.map(row=>row.map(x=>x.id));
 for(let t=0;t<9;t++){if(uncoupled)continue;
  for(let r=0;r<2;r++)for(let i=0;i<N;i++){if(i===knock)continue;
   let j=(i+Math.floor(values[i]/10)+Math.floor(t*frequency)+phase)%N;if(j===knock)continue;
   const radius=1+.18*Math.sin((i+t+phase)*Math.PI/13.5);if(gate&&radius>1.07)continue;
   let moved=a[r][i].mass*gain*(.5+.5*Math.sin((t+phase+i)*Math.PI/27)**2);
   a[r][i].mass-=moved;a[1-r][j].mass+=moved;
  }
 }
 return {a,before,after:total(a),min:Math.min(...a.flat().map(x=>x.mass)),identity:a.every((row,r)=>row.every((x,i)=>x.id===labels[r][i]))};
}
function run(){let rows=[];for(const seed of SEEDS){
 const b=simulate(seed),re=simulate(seed),noop=simulate(seed,{gain:0}),unc=simulate(seed,{uncoupled:true});
 const nulls=[1,2,3,4].map(k=>l1(b.a,simulate(seed,{values:permutation(seed+k*101)}).a));
 const phase=l1(b.a,simulate(seed,{phase:7}).a),gate=l1(b.a,simulate(seed,{gate:false}).a);
 const zero=l1(b.a,simulate(seed,{values:Array(N).fill(0)}).a),knock=l1(b.a,simulate(seed,{knock:0}).a),freq=l1(b.a,simulate(seed,{frequency:1.3}).a);
 const tests=[["T1 deterministic replay",JSON.stringify(b.a)===JSON.stringify(re.a)],["T2 persistent 27 glyph identities",b.identity&&new Set(GLYPHS).size===27],["T3 mass conservation",Math.abs(b.after-b.before)<1e-9],["T4 nonnegative mass",b.min>=0],["T5 zero-gain no-op",l1(noop.a,initial(seed))<1e-9],["T6 strict uncoupled equality",l1(unc.a,initial(seed))<1e-9],["T7 four seeded permutation controls",nulls.every(x=>Number.isFinite(x)&&x>1e-9)],["T8 boundary gate contrast",gate>1e-9],["T9 phase contrast",phase>1e-9],["T10 affinity knockout and frequency contrasts",[zero,knock,freq].every(x=>x>1e-9)]];
 rows.push({seed,massError:b.after-b.before,nulls,phase,gate,zero,knock,freq,tests});}
 return {protocol:"issue-401",seeds:SEEDS,passed:rows.flatMap(x=>x.tests).filter(x=>x[1]).length,total:40,rows};}
if(typeof module!=="undefined")module.exports={run,simulate,initial,permutation};