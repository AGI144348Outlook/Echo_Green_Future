// KS Recess visual playback: recorded-operation sample, not live Echo agency.
const panel=document.createElement('section');panel.className='window';panel.style.cssText='position:relative;z-index:2;margin-top:12px;padding:12px;background:white;max-width:760px';
panel.innerHTML='<header><strong>Echo · KS Recess Visual Test</strong><span id="recessStatus">Ready · sample replay</span></header><p>Recorded KS Recess operation examples. Replay is not autonomous operation generation.</p><button id="recessPlay">Play</button> <button id="recessPause">Pause</button> <button id="recessReset">Reset</button><label>Speed <input id="recessSpeed" type="range" min="1" max="10" value="4"></label><div style="overflow:auto;max-width:100%"><svg id="recessStage" viewBox="500 100 800 760" style="width:100%;min-width:340px;height:auto;background-color:#fff;background-image:linear-gradient(#e2e8f0 1px,transparent 1px),linear-gradient(90deg,#e2e8f0 1px,transparent 1px);background-size:40px 40px;border:1px solid #94a3b8"></svg></div><pre id="recessEvent" style="white-space:pre-wrap"></pre>';
document.querySelector('#desktop').append(panel);
const q=s=>panel.querySelector(s), ns='http://www.w3.org/2000/svg';
const operations=[
{op:'PRESENTIATE',id:'entity',word:'entity',x:600,y:316,r:30,theta:0},
{op:'PRESENTIATE',id:'cast',word:'cast',x:700,y:724,r:30,theta:0},
{op:'PRESENTIATE',id:'complex',word:'complex',x:700,y:453,r:30,theta:0},
{op:'PRESENTIATE',id:'branch',word:'branch',x:800,y:479,r:30,theta:0},
{op:'PRESENTIATE',id:'discipline',word:'discipline',x:900,y:656,r:30,theta:0},
{op:'PRESENTIATE',id:'division',word:'division',x:900,y:563,r:30,theta:0},
{op:'PRESENTIATE',id:'unit',word:'unit',x:1000,y:180,r:30,theta:0},
{op:'PRESENTIATE',id:'time',word:'time',x:1100,y:277,r:30,theta:0},
{op:'ROTATE',id:'division',theta:4.5492,segment:8},
{op:'SET_SIZE',id:'division',r:37},
{op:'MOVE',id:'complex',x:844.1,y:587},
{op:'ALIGN',a:'division',b:'complex',kind:'visual_sample'},
{op:'SET_GROUP',group:'set1',members:['complex','division']}
];
const nodes=new Map(),relations=[];let index=0,timer=null;
function svg(tag,attributes={}){const el=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attributes))el.setAttribute(k,String(v));return el}
function render(){const stage=q('#recessStage');stage.replaceChildren();for(const rel of relations){const a=nodes.get(rel.a),b=nodes.get(rel.b);if(a&&b)stage.append(svg('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,stroke:'#0f766e','stroke-width':2,'stroke-dasharray':'6 4'}))}
for(const node of nodes.values()){const g=svg('g',{transform:`translate(${node.x} ${node.y}) rotate(${(node.theta||0)*180/Math.PI})`});g.append(svg('circle',{r:node.r,fill:node.group?'#ccfbf1':'#dbeafe',stroke:'#2563eb','stroke-width':2}));g.append(svg('line',{x1:0,y1:0,x2:node.r,y2:0,stroke:'#1d4ed8','stroke-width':3}));stage.append(g);const text=svg('text',{x:node.x,y:node.y+node.r+17,'text-anchor':'middle','font-size':14,fill:'#0f172a'});text.textContent=node.word;stage.append(text)}}
function apply(op){if(op.op==='PRESENTIATE')nodes.set(op.id,{...op});else if(['MOVE','ROTATE','SET_SIZE'].includes(op.op)){const n=nodes.get(op.id);if(n){if(op.op==='MOVE'){n.x=op.x;n.y=op.y}else if(op.op==='ROTATE')n.theta=op.theta;else n.r=op.r}}else if(op.op==='ALIGN')relations.push(op);else if(op.op==='SET_GROUP')for(const id of op.members){const n=nodes.get(id);if(n)n.group=op.group}render();q('#recessEvent').textContent=`Step ${index+1}/${operations.length} · ${JSON.stringify(op)}`;q('#recessStatus').textContent=`Replay ${index+1}/${operations.length}`}
function stop(){if(timer!==null)clearTimeout(timer);timer=null}
function step(){if(index>=operations.length){stop();q('#recessStatus').textContent='Replay complete';return}apply(operations[index++]);timer=setTimeout(step,Math.max(80,1100-Number(q('#recessSpeed').value)*100))}
q('#recessPlay').onclick=()=>{if(timer===null)step()};
q('#recessPause').onclick=stop;
q('#recessReset').onclick=()=>{stop();index=0;nodes.clear();relations.length=0;render();q('#recessStatus').textContent='Ready · sample replay';q('#recessEvent').textContent=''};
render();
