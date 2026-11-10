// GPT-only synthetic controlled experiment; preregistered Issue #400.
const GLYPHS=[..."אבגדהוזחטיכלמנסעפצקרשתךםןףץ"];
const VALUES=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90];
const SEEDS=[11,23,47,89],N=27;
const initial=seed=>Array.from({length:2},(_,r)=>Array.from({length:N},(_,i)=>({id:GLYPHS[i],mass:(1+((i*7+seed)%17)/17)/2})));
const total=a=>a.flat().reduce((s,x)=>s+x.mass,0);
const l1=(a,b)=>a.flat().reduce((s,x,i)=>s+Math.abs(x.mass-b.flat()[i].mass),0);
function simulate(seed,{gain=.12,uncoupled=false,shuffle=false,gate=true,phase=0,knock=-1}={}){
 const a=initial(seed),before=total(a),labels=a.map(r=>r.map(x=>x.id));
 const v=shuffle?VALUES.map((_,i)=>VALUES[(i*11+3)%N]):VALUES;
 for(let t=0;t<9;t++){
  if(uncoupled)continue;
  for(let r=0;r<2;r++)for(let i=0;i<N;i++){
   if(i===knock)continue;
   let j=(i+Math.floor(v[i]/10)+t+phase)%N;
   if(j===knock)continue;
   const radius=1+.18*Math.sin((i+t+phase)*Math.PI/13.5);
   if(gate&&radius>1.07)continue;
   let moved=a[r][i].mass*gain*(.5+.5*Math.sin((t+phase+i)*Math.PI/27)**2);
   a[r][i].mass-=moved;a[1-r][j].mass+=moved;
  }
 }
 return {a,before,after:total(a),min:Math.min(...a.flat().map(x=>x.mass)),identity:a.every((row,r)=>row.every((x,i)=>x.id===labels[r][i]))};
}
function run(){
 let rows=[];
 for(let seed of SEEDS){
  const b=simulate(seed),repeat=simulate(seed),noop=simulate(seed,{gain:0}),unc=simulate(seed,{uncoupled:true}),sh=simulate(seed,{shuffle:true}),open=simulate(seed,{gate:false}),ph=simulate(seed,{phase:7}),ko=simulate(seed,{knock:0});
  const differences={gematriaShuffle:l1(b.a,sh.a),boundaryGate:l1(b.a,open.a),phase:l1(b.a,ph.a),knockout:l1(b.a,ko.a)};
  const tests=[
   ["T1 replay",JSON.stringify(b.a)===JSON.stringify(repeat.a)],
   ["T2 identity",b.identity&&new Set(GLYPHS).size===27],
   ["T3 conservation",Math.abs(b.after-b.before)<1e-9],
   ["T4 nonnegative",b.min>=0],
   ["T5 zero-gain no-op",l1(noop.a,initial(seed))<1e-9],
   ["T6 uncoupled equality",l1(unc.a,initial(seed))<1e-9],
   ["T7 gematria shuffle",differences.gematriaShuffle>1e-9],
   ["T8 causal boundary gate",differences.boundaryGate>1e-9],
   ["T9 phase contrast",differences.phase>1e-9],
   ["T10 knockout",differences.knockout>1e-9]
  ];rows.push({seed,differences,massError:b.after-b.before,tests});
 }
 return {protocol:"issue-400",seeds:SEEDS,passed:rows.flatMap(x=>x.tests).filter(x=>x[1]).length,total:40,rows};
}
if(typeof module!=="undefined")module.exports={run,simulate,initial,GLYPHS,VALUES};