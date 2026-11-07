// Echo-GPT noncanonical, bounded experimental portfolio, prereg Issue #333.
// Deterministic, no I/O, no network. runPortfolio() returns reproducible evidence.
function rng(seed){let x=seed>>>0;return ()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296}}
const SEEDS=[1109,2203,3301,4409],GLYPHS=Array.from({length:27},(_,i)=>i);
function arrivals(seed){let r=rng(seed),t=0;return Array.from({length:12},(_,i)=>{t+=1+Math.floor(r()*3);return {id:"g"+i,t,g:i%27}})}
function census(events){const ids=new Set(),errors=[];for(const e of events){if(ids.has(e.id))errors.push("duplicate");ids.add(e.id);if(!Number.isInteger(e.t)||e.t<0)errors.push("time");}return {ok:errors.length===0&&ids.size===12,errors,count:ids.size}}
function ring(seed,{n=3,coupled=false,shuffle=false,deform=false,noOp=false}={}){let r=rng(seed),phase=Array.from({length:n},()=>Math.floor(r()*27)),values=GLYPHS.map(i=>i+1);if(shuffle)values.reverse();let initial=phase.slice(),align=0,maxRadius=0;for(let tick=0;tick<32;tick++){if(!noOp){phase=phase.map((p,j)=>(p+1+(coupled?values[phase[(j+1)%n]]%3:0))%27)}align+=phase.filter((p,j)=>p===phase[(j+1)%n]).length;let radius=deform?1+0.1*Math.sin(tick+phase[0]):1;maxRadius=Math.max(maxRadius,radius)}return {phase,initial,align,maxRadius,stationary:phase.every((p,j)=>p===initial[j])}}
function project(){const a=GLYPHS.map(i=>[Math.floor(i/9),Math.floor(i/3)%3,i%3]);return {unique:new Set(a.map(v=>v.join(","))).size,bounded:a.every(v=>v.every(x=>x>=0&&x<3))}}
function served(events,dwell){let busy=0,count=0;for(const e of events){if(e.t>=busy){count++;busy=e.t+dwell}}return count}
function runPortfolio(){const rows=[];for(const seed of SEEDS){const a=arrivals(seed),b=arrivals(seed),r0=ring(seed,{noOp:true}),unc=ring(seed),cou=ring(seed,{coupled:true}),sh=ring(seed,{coupled:true,shuffle:true}),def=ring(seed,{deform:true}),p=project();const shifted=a.map(e=>({...e,t:e.t+7})),renamed=a.map(e=>({...e,id:"renamed_"+e.id}));const tests=[
["seeded-schedule-variation",JSON.stringify(a.map(e=>e.t))!==JSON.stringify(arrivals(seed+1).map(e=>e.t)),a.map(e=>e.t)],
["deterministic-replay",JSON.stringify(a)===JSON.stringify(b),null],
["independent-census",census(a).ok&& !census([...a,a[0]]).ok,census(a)],
["identity-renaming",census(renamed).ok&&renamed.every((e,i)=>e.t===a[i].t),null],
["time-translation",census(shifted).ok&&shifted.every((e,i)=>e.t-a[i].t===7),null],
["gematria-shuffle-control",sh.align!==undefined&&sh.phase.length===3,{coupled:cou.align,shuffled:sh.align}],
["coupled-uncoupled",unc.phase.length===cou.phase.length,{uncoupled:unc.align,coupled:cou.align}],
["stationary-no-op",r0.stationary,{initial:r0.initial,final:r0.phase}],
["geometry-boundary",p.unique===27&&p.bounded&&def.maxRadius<=1.10000001,{project:p,radius:def.maxRadius}],
["paired-dwell-intervention",served(a,4)<=served(a,2),{dwell2:served(a,2),dwell4:served(a,4)}]
];for(const [type,pass,evidence] of tests)rows.push({seed,type,status:pass?"PASS":"FAIL",evidence})}
return {protocol:"Issue #333, prospective amendment 6707269456",seeds:SEEDS,types:10,rows,summary:{pass:rows.filter(x=>x.status==="PASS").length,fail:rows.filter(x=>x.status==="FAIL").length},limitations:["Synthetic checks; gematria shuffle and coupling are descriptive controls, not superiority tests","3x3x3 is bijective coordinate projection, not spatial dynamics","Dwell changes throughput, not independently measured learning","Census is independent of ring state but shares input generator"]}}
