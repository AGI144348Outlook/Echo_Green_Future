// GPT-only synthetic 27-seat 3-ring comparison; prereg Issue #423; node >=18
function model(seed,opt={}) {
 const n=27, theta=Array.from({length:3},(_,r)=>Array.from({length:n},(_,i)=>((seed*17+r*11+i*7)%101)/101*6.283185307179586+(opt.shift||0)));
 let m=Array.from({length:3},(_,r)=>Array.from({length:n},(_,i)=>1+((seed+r*7+i*3)%11)/20));
 const initial=m.map(a=>a.slice()), gain=opt.gain===undefined?.07:opt.gain;
 for(let t=0;t<12;t++){let next=m.map(a=>a.slice());
 for(let i=0;i<n;i++){let a=theta[0][i],b=theta[1][i],c=theta[2][i], affinity=opt.shuffle?((i*13+7)%27)/27:((i*7+seed)%27)/27;
 let w=opt.mode==="uncoupled"?0:gain*(.5+affinity);
 let flux=opt.mode==="triad"?w*Math.sin(b+c-2*a):w*(Math.sin(b-a)+Math.sin(c-a))/2;
 let amount=Math.max(-.035,Math.min(.035,flux))*(opt.boundary?1+.15*Math.sin(i):1);
 next[0][i]+=amount;next[1][i]-=amount/2;next[2][i]-=amount/2;
 }m=next;theta=theta.map((a,r)=>a.map((x,i)=>x+(opt.freq?r*.004:0)+.002*(r+1))); }
 return {ring:m,projection:m[0].map((x,i)=>x+m[1][i]+m[2][i]),initial};
}
function run() {
 const seeds=[11,23,37,53],rows=[];
 const l1=(a,b)=>a.flat(Infinity).reduce((s,v,i)=>s+Math.abs(v-b.flat(Infinity)[i]),0);
 const sum=a=>a.flat(Infinity).reduce((x,y)=>x+y,0);
 for(const seed of seeds){const p=model(seed,{mode:"pair"}),t=model(seed,{mode:"triad"}),u=model(seed,{mode:"uncoupled"}),shift=model(seed,{mode:"triad",shift:1.234}),zero=model(seed,{mode:"triad",gain:0}),sh=model(seed,{mode:"triad",shuffle:true}),fr=model(seed,{mode:"triad",freq:true}),bd=model(seed,{mode:"triad",boundary:true});
 const checks=[
 ["replay",l1(t.ring,model(seed,{mode:"triad"}).ring)===0],
 ["mass",Math.abs(sum(t.ring)-sum(t.initial))<1e-9],
 ["nonnegative",Math.min(...t.ring.flat())>=0],
 ["gauge",l1(t.ring,shift.ring)<1e-9],
 ["zero",l1(zero.ring,u.ring)<1e-9],
 ["nonpairwise",l1(t.ring,p.ring)>1e-6],
 ["shuffled",l1(t.ring,sh.ring)>1e-6],
 ["frequency",l1(t.ring,fr.ring)>1e-6],
 ["boundary",l1(t.ring,bd.ring)>1e-6],
 ["projection",l1(t.projection,u.projection)<1e-9 && l1(t.ring,u.ring)>1e-6]
 ];
 rows.push({seed,checks:Object.fromEntries(checks),metrics:{triad_pair_l1:l1(t.ring,p.ring),shuffle_l1:l1(t.ring,sh.ring),frequency_l1:l1(t.ring,fr.ring),boundary_l1:l1(t.ring,bd.ring),ring_uncoupled_l1:l1(t.ring,u.ring),projection_uncoupled_l1:l1(t.projection,u.projection),mass_error:Math.abs(sum(t.ring)-sum(t.initial))}});
 }return {test_types:10,seeds,pass:rows.reduce((s,r)=>s+Object.values(r.checks).filter(Boolean).length,0),total:40,rows};
}
console.log(JSON.stringify(run(),null,2));
