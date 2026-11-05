"use strict";
// GPT-owned bounded synthetic run, seed 20261105. NOT canonical Echo.
const seed=20261105;
const glyphs=Array.from("אבגדהוזחטיכלמנסעפצקרשתךםןףץ");
const slots=["noun","adjective","anchor","verb","adverb","fused","forward","backward","question","join","split","relation","absence","turned","nested","catch","sense"];
function registry(){
 const hosts=glyphs.map((g,i)=>({glyph:g,pos:[Math.floor(i/9),Math.floor(i/3)%3,i%3],base:"ordinary:"+g}));
 const assignments=new Map(),active=new Set();
 function add(origin,host,component){if(!glyphs.includes(origin)||!glyphs.includes(host))throw Error("unknown");const key=origin+"|"+host+"|"+component;if(assignments.has(key))throw Error("duplicate");assignments.set(key,{origin,host,component});}
 for(let i=0;i<17;i++)add("פ",glyphs[i],slots[i]);
 add("ע",glyphs[0],"detect");add("ר",glyphs[0],"validate");add("צ",glyphs[1],"measure");
 function dispatch(origin,host,component){const key=origin+"|"+host+"|"+component;return active.has(origin)&&assignments.has(key)?{origin,host,component} : null;}
 return {hosts,assignments,active,add,dispatch};
}
function phase({coupled=true,shuffle=false,deform=false,kick=0}={}){
 let state=[.1,.3,.5], freq=[.01,.015,.02], weights=shuffle?[.2,.05]:[.05,.2];
 let boundary=1;
 for(let t=0;t<24;t++){if(t===0)state[0]+=kick;
 const next=state.map((v,i)=>v+freq[i]);
 if(coupled){next[1]+=weights[0]*Math.sin(state[0]-state[1]);next[2]+=weights[1]*Math.sin(state[1]-state[2]);}
 if(deform)boundary=Math.max(.8,Math.min(1.2,boundary+.002*Math.sin(t)));
 state=next.map(v=>((v%(2*Math.PI))+(2*Math.PI))%(2*Math.PI));
 }
 return {state,boundary};
}
function run(){
 const r=registry(),results=[];
 function check(id,condition,details){results.push({id,pass:!!condition,details});}
 check("T1_cube_bijection",r.hosts.length===27&&new Set(r.hosts.map(x=>x.pos.join(","))).size===27,{count:r.hosts.length});
 check("T2_inactive_pe",slots.every((s,i)=>r.dispatch("פ",glyphs[i],s)===null),{blocked:17});
 r.active.add("פ");
 check("T3_active_pe",slots.every((s,i)=>r.dispatch("פ",glyphs[i],s)?.component===s),{available:17});
 r.active.delete("פ");
 check("T4_deactivation",r.dispatch("פ",glyphs[0],slots[0])===null,{host:glyphs[0]});
 r.active.add("ע");
 check("T5_family_isolation",r.dispatch("ע",glyphs[0],"detect")!==null&&r.dispatch("ר",glyphs[0],"validate")===null&&r.dispatch("פ",glyphs[0],slots[0])===null,{});
 r.active.add("ר");
 check("T6_colocation",r.dispatch("ע",glyphs[0],"detect")!==null&&r.dispatch("ר",glyphs[0],"validate")!==null&&r.hosts[0].base==="ordinary:"+glyphs[0],{host:glyphs[0]});
 let rejected=false;try{r.add("ע",glyphs[0],"detect");}catch(e){rejected=e.message==="duplicate";}
 check("T7_collision",rejected&&r.assignments.size===20,{entries:r.assignments.size});
 const a=JSON.stringify(registry().hosts),b=JSON.stringify(registry().hosts);
 check("T8_replay",a===b&&r.hosts.length===27,{seed});
 const control=phase({coupled:false}),ablate=phase({coupled:false,kick:.3}),connected=phase({coupled:true}),intervention=phase({coupled:true,kick:.3});
 const delta=(a,b,i)=>Math.abs(Math.atan2(Math.sin(a.state[i]-b.state[i]),Math.cos(a.state[i]-b.state[i])));
 check("T9_causal_controls",delta(control,ablate,1)<1e-12&&delta(connected,intervention,1)>1e-8,{uncoupled_downstream:delta(control,ablate,1),coupled_downstream:delta(connected,intervention,1),upstream:delta(connected,intervention,0)});
 const shuffled=phase({coupled:true,shuffle:true}),deformed=phase({coupled:true,deform:true});
 check("T10_shuffled_deformation",delta(connected,shuffled,2)>1e-8&&deformed.boundary>=.8&&deformed.boundary<=1.2,{shuffled_node2_delta:delta(connected,shuffled,2),deformed_boundary:deformed.boundary,deformation_phase_delta:delta(connected,deformed,2)});
 return {seed,source:"gpt-owned-synthetic",tests:results,passed:results.filter(t=>t.pass).length,total:results.length};
}
if(typeof module!=="undefined")module.exports={run};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));