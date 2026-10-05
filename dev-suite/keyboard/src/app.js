<script src="https://cdn.jsdelivr.net/npm/pyodide@0.26.4/pyodide.js"></script>
<script>
/* ---------- state ---------- */
const store={ get(k,d){ try{ const v=localStorage.getItem("ckt:"+k); return v?JSON.parse(v):d; }catch(e){ return d; } },
              set(k,v){ try{ localStorage.setItem("ckt:"+k,JSON.stringify(v)); }catch(e){} } };
let lines=store.get("lines",[""]), cur=store.get("cur",{l:0,c:0}), mine=store.get("mine",[]), kbName=store.get("kb","DSL");
let KB={}, USES={}, EXAMPLES={}, py=null, audits=[], fontPx=store.get("font",22);
let folded=store.get("folded",false), native=false, kScrollX=0;
let view=store.get("view","off"), dual=store.get("dual",false), pane="linear", ccur={b:0,c:0};
let links=store.get("links",[]), mode=store.get("mode","insert"), face=store.get("face",0), linkFrom=null;   // face: 0 key, 1 logic card, 2 examples
const chars=s=>Array.from(s);          // code points, so a glyph is one cell
const $=id=>document.getElementById(id);
const pal={}; function readPal(){ const s=getComputedStyle(document.documentElement); for(const k of ["paper","minor","major","ink","soft","node","ok","warn","sheet","key","line","hl"]) pal[k]=s.getPropertyValue("--"+k).trim(); }

/* ---------- substrate: Python if it runs, otherwise the same block read as data ---------- */
function fallbackParse(){
  const src=$("substrate").textContent;
  const grab=name=>{ const i=src.indexOf(name+" = {"); let d=0,j=i+name.length+3;
    for(;j<src.length;j++){ if(src[j]==="{") d++; else if(src[j]==="}"){ d--; if(!d) break; } }
    return JSON.parse(src.slice(i+name.length+3,j+1).replace(/,(\s*[}\]])/g,"$1")); };
  return {keyboards:grab("KEYBOARDS"), uses:grab("USES"), examples:grab("EXAMPLES")};
}
async function boot(){
  try{ const c=fallbackParse(); KB=c.keyboards; USES=c.uses; EXAMPLES=c.examples; }catch(e){ KB={DSL:["%","§","|","/"]}; }
  if(!KB[kbName]) kbName=Object.keys(KB)[0]; buildTabs(); layoutKeys(); drawAll();
  try{
    py=await loadPyodide(); py.runPython($("substrate").textContent);
    const c=JSON.parse(py.runPython("config()")); KB=c.keyboards; USES=c.uses; EXAMPLES=c.examples;
    $("st").textContent="Python "+py.runPython("import sys; sys.version.split()[0]"); $("dot").className="dot ok";
    if(!KB[kbName]) kbName=Object.keys(KB)[0]; buildTabs(); layoutKeys(); runAudit(); drawAll();
  }catch(e){ py=null; $("st").textContent="Python unavailable here: keys from the substrate as data"; $("dot").className="dot err"; console.warn(e); }
}
function runAudit(){ if(!py) { audits=[]; return; } py.globals.set("LINES_JSON",JSON.stringify(lines)); audits=JSON.parse(py.runPython("import json; audit(json.loads(LINES_JSON))")); }
function save(){ store.set("lines",lines); store.set("cur",cur); store.set("mine",mine); store.set("kb",kbName); store.set("font",fontPx); store.set("links",links); store.set("mode",mode); store.set("face",face); store.set("view",view); store.set("dual",dual); store.set("folded",folded); }

/* ---------- editing ---------- */
function ensureRow(l){ while(lines.length<=l) lines.push(""); }
const OPEN={"(":")","[":"]","{":"}","⟨":"⟩","⟦":"⟧","⌈":"⌉","⌊":"⌋","«":"»","‹":"›"}, CLOSE=Object.fromEntries(Object.entries(OPEN).map(([a,b])=>[b,a]));
function insert(text){
  if(pane==="compact"){ compactInsert(text); return; }
  if(mode==="insert"){ const row=chars(lines[cur.l]||"");
    if(CLOSE[text]&&row[cur.c]===text){ cur.c++; changed(false); return; }              // step over an auto-placed closer
    if(OPEN[text]){ placeAt(cur.l,cur.c,text+OPEN[text],true); cur.c--; changed(false); return; }  // pairs open empty: [│]
  }
  placeAt(cur.l,cur.c,text,mode==="insert"); }
function placeAt(l,c,text,shift){
  ensureRow(l); const row=chars(lines[l]); while(row.length<c) row.push(" "); const t=chars(text);
  if(shift) row.splice(c,0,...t); else t.forEach((ch,i)=>row[c+i]=ch);
  lines[l]=row.join("").replace(/\s+$/,""); cur={l,c:c+t.length}; changed(); }
function newline(){ const row=chars(lines[cur.l]); lines[cur.l]=row.slice(0,cur.c).join(""); lines.splice(cur.l+1,0,row.slice(cur.c).join("")); cur={l:cur.l+1,c:0}; changed(); }
function backspace(){
  if(pane==="compact"){ compactBack(); return; }
  { const row=chars(lines[cur.l]||""); if(mode==="insert"&&cur.c>0&&OPEN[row[cur.c-1]]&&row[cur.c]===OPEN[row[cur.c-1]]){ row.splice(cur.c-1,2); lines[cur.l]=row.join(""); cur.c--; changed(); return; } }
  if(cur.c>0){ const row=chars(lines[cur.l]); row.splice(cur.c-1,1); lines[cur.l]=row.join(""); cur.c--; }
  else if(cur.l>0){ const prev=chars(lines[cur.l-1]).length; lines[cur.l-1]+=lines[cur.l]; lines.splice(cur.l,1); cur={l:cur.l-1,c:prev}; }
  changed(); }
function move(d){ const len=chars(lines[cur.l]).length;
  if(d<0){ if(cur.c>0) cur.c--; else if(cur.l>0){ cur.l--; cur.c=chars(lines[cur.l]).length; } }
  else { if(cur.c<len) cur.c++; else if(cur.l<lines.length-1){ cur.l++; cur.c=0; } } changed(false); }
function changed(content=true){ if(content) runAudit(); keepCursorVisible(); save(); drawTerm(); drawCompact(); }

/* ---------- terminal: a grid of cells with numbered lines ---------- */
const tc=$("tc"), tctx=tc.getContext("2d"); let TW=0,TH=0,DPR=1, scroll={x:0,y:0};
const cellW=()=>Math.round(fontPx*0.82), cellH=()=>Math.round(fontPx*1.45), gutter=()=>Math.max(3,String(lines.length).length)*cellW()*0.7+34;
function sizeTerm(){ const r=$("term").getBoundingClientRect(); DPR=Math.min(devicePixelRatio||1,3); TW=r.width; TH=r.height; tc.width=TW*DPR; tc.height=TH*DPR; }
function keepCursorVisible(){ const ch=cellH(), cw=cellW(), y=cur.l*ch, x=cur.c*cw;
  if(y<scroll.y) scroll.y=y; if(y+ch>scroll.y+TH-8) scroll.y=y+ch-TH+8;
  const vis=TW-gutter()-8; if(x<scroll.x) scroll.x=Math.max(0,x-cw*2); if(x+cw>scroll.x+vis) scroll.x=x+cw*3-vis; }
function drawTerm(){
  const ctx=tctx, ch=cellH(), cw=cellW(), g=gutter(); ctx.setTransform(DPR,0,0,DPR,0,0);
  ctx.fillStyle=pal.paper; ctx.fillRect(0,0,TW,TH);
  const first=Math.max(0,Math.floor(scroll.y/ch)), last=Math.min(lines.length-1,Math.ceil((scroll.y+TH)/ch));
  // grid
  ctx.strokeStyle=pal.minor; ctx.lineWidth=1; ctx.beginPath();
  for(let x=g-(scroll.x%cw);x<TW;x+=cw){ ctx.moveTo(Math.round(x)+.5,0); ctx.lineTo(Math.round(x)+.5,TH); }
  for(let y=-(scroll.y%ch);y<TH;y+=ch){ ctx.moveTo(g,Math.round(y)+.5); ctx.lineTo(TW,Math.round(y)+.5); } ctx.stroke();
  // current line band
  const cy=cur.l*ch-scroll.y; ctx.fillStyle=pal.hl; ctx.fillRect(0,cy,TW,ch);
  // % view: invariant positions are frame, changing positions are operation
  if(view!=="off"){ for(let l=first;l<=last;l++){ const m=invMask(lines[l]); m.forEach((inv,i)=>{ if(view==="frame"?inv:!inv){ const x=g+i*cw-scroll.x;
        ctx.fillStyle=view==="frame"?"rgba(47,143,91,.18)":"rgba(192,138,30,.22)"; ctx.fillRect(x,l*ch-scroll.y,cw,ch); } }); } }
  // text
  ctx.save(); ctx.beginPath(); ctx.rect(g,0,TW-g,TH); ctx.clip();
  ctx.font=`500 ${fontPx}px ui-monospace,"SF Mono",Menlo,Consolas,"Noto Sans Mono",monospace`; ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillStyle=pal.ink;
  for(let l=first;l<=last;l++){ const y=l*ch-scroll.y+ch/2; chars(lines[l]).forEach((c,i)=>{ const x=g+i*cw-scroll.x+cw/2; if(x>g-cw&&x<TW+cw) ctx.fillText(c,x,y); }); }
  // links between symbols: the mind map drawn over the grid
  const ctr=(p)=>({x:g+p.c*cw-scroll.x+cw/2,y:p.l*ch-scroll.y+ch/2});
  ctx.strokeStyle=pal.node; ctx.fillStyle=pal.node; ctx.lineWidth=1.6;
  for(const k of links){ const a=ctr(k.a), b=ctr(k.b), ang=Math.atan2(b.y-a.y,b.x-a.x), rr=Math.min(cw,ch)*0.42;
    const ax=a.x+Math.cos(ang)*rr, ay=a.y+Math.sin(ang)*rr, bx=b.x-Math.cos(ang)*rr, by=b.y-Math.sin(ang)*rr;
    ctx.beginPath(); ctx.moveTo(ax,ay); ctx.lineTo(bx,by); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(bx,by); ctx.lineTo(bx-8*Math.cos(ang-0.45),by-8*Math.sin(ang-0.45)); ctx.lineTo(bx-8*Math.cos(ang+0.45),by-8*Math.sin(ang+0.45)); ctx.closePath(); ctx.fill(); }
  if(linkFrom){ const a=ctr(linkFrom); ctx.strokeStyle=pal.ok; ctx.lineWidth=2.5; ctx.strokeRect(a.x-cw/2+1,a.y-ch/2+1,cw-2,ch-2); }
  // cursor: a bar between cells when inserting, a cell box when placing
  const cx=g+cur.c*cw-scroll.x;
  if(mode==="insert"){ ctx.fillStyle=pal.node; ctx.fillRect(cx-1,cy+3,2.5,ch-6); } else if(mode==="place"){ ctx.strokeStyle=pal.node; ctx.lineWidth=2; ctx.strokeRect(cx+1,cy+1,cw-2,ch-2); }
  ctx.restore();
  // gutter: line numbers and audit marks
  ctx.fillStyle=pal.sheet; ctx.fillRect(0,0,g,TH); ctx.strokeStyle=pal.major; ctx.beginPath(); ctx.moveTo(g+.5,0); ctx.lineTo(g+.5,TH); ctx.stroke();
  ctx.font=`500 ${Math.max(11,fontPx*0.55)}px ui-monospace,Menlo,monospace`; ctx.textAlign="right";
  for(let l=first;l<=last;l++){ const y=l*ch-scroll.y+ch/2; ctx.fillStyle=l===cur.l?pal.ink:pal.soft; ctx.fillText(String(l+1),g-18,y);
    const a=audits[l]; if(a&&!a.empty){ ctx.fillStyle=a.ok?pal.ok:a.pending?pal.soft:pal.warn; ctx.textAlign="center"; ctx.fillText(a.ok?"✓":a.pending?"·":"!",g-8,y); ctx.textAlign="right"; } }
  $("pos").textContent=`Ln ${cur.l+1}, Col ${cur.c+1}`;
}
let tp=null;
tc.addEventListener("pointerdown",e=>{ tc.setPointerCapture(e.pointerId); tp={x:e.clientX,y:e.clientY,sx:scroll.x,sy:scroll.y,moved:false}; });
tc.addEventListener("pointermove",e=>{ if(!tp) return; const dx=e.clientX-tp.x, dy=e.clientY-tp.y; if(Math.hypot(dx,dy)>6) tp.moved=true;
  if(tp.moved){ scroll.x=Math.max(0,tp.sx-dx); scroll.y=Math.max(0,Math.min(Math.max(0,lines.length*cellH()-TH+cellH()),tp.sy-dy)); drawTerm(); } });
function cellAt(clientX,clientY,round){ const r=tc.getBoundingClientRect(), x=clientX-r.left, y=clientY-r.top;
  const l=Math.max(0,Math.floor((y+scroll.y)/cellH())), f=(x-gutter()+scroll.x)/cellW(); return {l,c:Math.max(0,round?Math.round(f):Math.floor(f)),x,y}; }
const symAt=(l,c)=>(chars(lines[l]||"")[c]||" ").trim();
tc.addEventListener("pointerup",e=>{ if(tp&&!tp.moved){ const hitc=cellAt(e.clientX,e.clientY,mode==="insert"), {l,c,x}=hitc;
    if(mode==="link"){ const cc=cellAt(e.clientX,e.clientY,false); if(!symAt(cc.l,cc.c)){ toast("Link mode: tap a symbol"); tp=null; return; }
      if(!linkFrom){ linkFrom={l:cc.l,c:cc.c}; toast("Now tap the symbol to link to"); }
      else if(linkFrom.l===cc.l&&linkFrom.c===cc.c){ linkFrom=null; toast("Link cancelled"); }
      else { const i=links.findIndex(k=>k.a.l===linkFrom.l&&k.a.c===linkFrom.c&&k.b.l===cc.l&&k.b.c===cc.c);
        if(i>=0){ links.splice(i,1); toast("Link removed"); } else { links.push({a:linkFrom,b:{l:cc.l,c:cc.c}}); toast("Linked"); } linkFrom=null; save(); }
      drawTerm(); tp=null; return; }
    cur={l,c:mode==="insert"?Math.min(c,chars(lines[l]||"").length):c}; ensureRow(l); changed(false);
    const a=audits[l]; if(a&&!a.ok&&!a.empty&&x<gutter()) toast(`Line ${l+1}: ${a.why}`); } tp=null; });

/* ---------- keyboard: keys drawn on a canvas, switchable ---------- */
const kc=$("kc"), kctx=kc.getContext("2d"); let KW=0,KH=0, keyRects=[], kScroll=0, kContent=0;
function current(){ return kbName==="Mine"?mine:(KB[kbName]||[]); }
function buildTabs(){ const t=$("tabs"); t.innerHTML=""; for(const name of [...Object.keys(KB),"Mine"]){ const b=document.createElement("button");
  b.className="tab"; b.type="button"; b.textContent=name==="Mine"?"★ Mine":name; b.setAttribute("aria-pressed",String(name===kbName));
  b.onclick=()=>{ kbName=name; kScroll=0; buildTabs(); layoutKeys(); drawKeys(); save(); }; t.appendChild(b); } }
function sizeKeys(){ const r=$("keys").getBoundingClientRect(); KW=r.width; KH=r.height; kc.width=KW*DPR; kc.height=KH*DPR; }
function strip(){ return folded||native; }
function layoutKeys(){ if(strip()){ const keys=current(), gap=6, h=46; let x=gap; keyRects=keys.map(k=>{ const w=Math.max(42,chars(k).length*13+20); const r={k,span:1,x,y:6,w,h}; x+=w+gap; return r; }); kContent=x; return; }
  const keys=current(), cols=face?(KW<420?2:KW<700?3:4):(KW<420?8:KW<700?10:14), gap=6, w=(KW-gap*(cols+1))/cols, h=face?74:Math.min(54,Math.max(42,w*1.05)); keyRects=[];
  keys.forEach((k,i)=>{ const span=!face&&chars(k).length>2?2:1; keyRects.push({k,span}); });
  let col=0,row=0; for(const r of keyRects){ if(col+r.span>cols){ col=0; row++; } r.x=gap+col*(w+gap); r.y=gap+row*(h+gap); r.w=w*r.span+gap*(r.span-1); r.h=h; col+=r.span; }
  kContent=(row+1)*(h+gap)+gap; }
function drawKeys(){
  const ctx=kctx; ctx.setTransform(DPR,0,0,DPR,0,0); ctx.fillStyle=pal.sheet; ctx.fillRect(0,0,KW,KH);
  if(!keyRects.length){ ctx.fillStyle=pal.soft; ctx.font="14px system-ui"; ctx.textAlign="center"; ctx.fillText(kbName==="Mine"?"Empty. Hold any key on another keyboard and choose Add to ★ Mine.":"No keys.",KW/2,KH/2); return; }
  const sx=strip()?kScrollX:0;
  for(const r0 of keyRects){ const r=sx?{...r0,x:r0.x-sx}:r0; if(sx&&(r.x>KW||r.x+r.w<0)) continue; const y=r.y-(strip()?0:kScroll); if(y>KH||y+r.h<0) continue;
    ctx.fillStyle=r0===pressed?pal.hl:pal.key; ctx.strokeStyle=pal.line; ctx.lineWidth=1; ctx.beginPath();
    ctx.roundRect?ctx.roundRect(r.x,y,r.w,r.h,7):ctx.rect(r.x,y,r.w,r.h); ctx.fill(); ctx.stroke();
    const n=chars(r.k).length;
    if(face){ // face 1: the logic card (its uses); face 2: the card turned over again (examples to try)
      ctx.fillStyle=face===2?pal.ok:pal.node; ctx.font=`600 ${n<=2?20:13}px ui-monospace,Menlo,monospace`; ctx.textAlign="left"; ctx.textBaseline="top"; ctx.fillText(r.k,r.x+8,y+6);
      if(face===2){ ctx.fillStyle=pal.soft; ctx.font="11px system-ui,sans-serif"; ctx.textAlign="right"; ctx.fillText("try",r.x+r.w-8,y+8); ctx.textAlign="left"; }
      ctx.fillStyle=pal.ink;
      if(face===1){ ctx.font="12.5px system-ui,sans-serif"; wrapIn(ctx,(USES[r.k]||["no use recorded yet"]).join("; "),r.x+8,y+(n<=2?30:24),r.w-14,15,3); }
      else { ctx.font="13px ui-monospace,Menlo,monospace"; (EXAMPLES[r.k]||["(no example yet)"]).slice(0,3).forEach((ex,j)=>{ ctx.fillText(ex.length>26?ex.slice(0,25)+"…":ex,r.x+8,y+(n<=2?30:24)+j*15); }); }
      continue; }
    const fs=n<=1?Math.min(26,r.h*0.5):n<=2?Math.min(20,r.h*0.4):Math.min(16,r.w/(n*0.62));
    ctx.fillStyle=pal.ink; ctx.font=`500 ${fs}px ui-monospace,"SF Mono",Menlo,"Noto Sans Mono",monospace`; ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(r.k,r.x+r.w/2,y+r.h/2+1); }
  if(!strip()&&kContent>KH){ const bar=KH*KH/kContent, top=kScroll/(kContent-KH)*(KH-bar); ctx.fillStyle=pal.major; ctx.fillRect(KW-3,top,2,bar); }
}
function wrapIn(ctx,t,x,y,max,lh,maxLines){ const words=t.split(" "); let line="",n=0;
  for(let i=0;i<words.length;i++){ const tt=line?line+" "+words[i]:words[i];
    if(ctx.measureText(tt).width>max&&line){ n++; if(n===maxLines){ ctx.fillText(line.replace(/.$/,"")+"…",x,y); return; } ctx.fillText(line,x,y); y+=lh; line=words[i]; } else line=tt; }
  if(line) ctx.fillText(line,x,y); }
let kp=null, pressed=null, holdTimer=null;
function keyAt(x,y){ if(strip()){ const X=x+kScrollX; return keyRects.find(r=>X>=r.x&&X<=r.x+r.w&&y>=r.y&&y<=r.y+r.h); }
  return keyRects.find(r=>x>=r.x&&x<=r.x+r.w&&y+kScroll>=r.y&&y+kScroll<=r.y+r.h); }
kc.addEventListener("pointerdown",e=>{ kc.setPointerCapture(e.pointerId); const b=kc.getBoundingClientRect(), x=e.clientX-b.left, y=e.clientY-b.top;
  kp={x:e.clientX,y:e.clientY,s:kScroll,sx:kScrollX,moved:false,held:false}; pressed=keyAt(x,y); kp.cand=pressed; drawKeys();
  clearTimeout(holdTimer); holdTimer=setTimeout(()=>{ if(kp&&!kp.moved&&pressed){ kp.held=true; showInfo(pressed.k); } },480); });
const ghost=$("ghost");
kc.addEventListener("pointermove",e=>{ if(!kp) return; const dy=e.clientY-kp.y, top=kc.getBoundingClientRect().top;
  if(kp.cand&&!kp.drag&&e.clientY<top-4){ kp.drag=kp.cand.k; kp.moved=true; pressed=null; kScroll=kp.s; drawKeys(); clearTimeout(holdTimer); ghost.textContent=kp.drag; ghost.style.display="block"; }
  if(kp.drag){ ghost.style.left=e.clientX+"px"; ghost.style.top=e.clientY+"px"; return; }
  const dx=e.clientX-kp.x;
  if(strip()){ if(Math.abs(dx)>8){ kp.moved=true; pressed=null; clearTimeout(holdTimer); } if(kp.moved){ kScrollX=Math.max(0,Math.min(Math.max(0,kContent-KW),kp.sx-dx)); drawKeys(); } return; }
  if(Math.abs(dy)>8){ kp.moved=true; pressed=null; clearTimeout(holdTimer); }
  if(kp.moved){ kScroll=Math.max(0,Math.min(Math.max(0,kContent-KH),kp.s-dy)); drawKeys(); } });
kc.addEventListener("pointerup",e=>{ clearTimeout(holdTimer);
  if(kp&&kp.drag){ ghost.style.display="none"; const tr=tc.getBoundingClientRect();
    if(e.clientY>=tr.top&&e.clientY<=tr.bottom&&e.clientX>=tr.left+gutter()){ const {l,c}=cellAt(e.clientX,e.clientY,false); placeAt(l,c,kp.drag,false); toast(`Dropped ${kp.drag} at Ln ${l+1}, Col ${c+1}`); } }
  else if(kp&&!kp.moved&&!kp.held&&pressed){ if(face===2){ const ex=(EXAMPLES[pressed.k]||[pressed.k])[0]; insert(ex); toast("Typed an example of "+pressed.k); } else insert(pressed.k); }
  pressed=null; kp=null; drawKeys(); });
kc.addEventListener("pointercancel",()=>{ ghost.style.display="none"; clearTimeout(holdTimer); pressed=null; kp=null; drawKeys(); });

/* ---------- hold a key: its identity, classical logics, and ★ Mine ---------- */
function esc(t){ return String(t).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
function showInfo(k){
  let ids;
  if(py){ py.globals.set("KEY",k); ids=JSON.parse(py.runPython("json.dumps(identity(KEY))")); }
  else ids=chars(k).map(c=>({ch:c,cp:"U+"+c.codePointAt(0).toString(16).toUpperCase().padStart(4,"0"),name:"(names need Python)",cat:""}));
  const inMine=mine.includes(k), uses=USES[k]||[], exs=EXAMPLES[k]||[];
  $("info").innerHTML=`<span class="g">${esc(k)}</span><h2>${ids.map(i=>esc(i.name)).join(" + ")}</h2><p>${ids.map(i=>i.cp+(i.cat?", "+i.cat:"")).join("  ")}</p>
    ${uses.length?`<ul>${uses.map(u=>`<li>${esc(u)}</li>`).join("")}</ul>`:`<p style="clear:both;padding-top:8px">No uses recorded yet: add them to USES in the substrate.</p>`}
    ${exs.length?`<p style="clear:both;padding-top:10px;color:var(--ink);font-weight:600">Try it</p><div class="acts" style="margin-top:4px">${exs.map((x,i)=>`<button class="btn ex" data-i="${i}" style="font-family:ui-monospace,Menlo,monospace">${esc(x)}</button>`).join("")}</div>`:""}
    <div class="acts"><button class="btn" id="iIns">Type it</button><button class="btn" id="iMine">${inMine?"Remove from ★ Mine":"Add to ★ Mine"}</button><button class="btn" id="iClose">Close</button></div>`;
  $("info").classList.add("open");
  $("iIns").onclick=()=>{ insert(k); $("info").classList.remove("open"); };
  document.querySelectorAll("#info .ex").forEach(b=>b.onclick=()=>{ insert(exs[+b.dataset.i]); $("info").classList.remove("open"); toast("Typed the example: now change it and practise"); });
  $("iMine").onclick=()=>{ mine=inMine?mine.filter(x=>x!==k):[...mine,k]; save(); if(kbName==="Mine"){ layoutKeys(); drawKeys(); } showInfo(k); };
  $("iClose").onclick=()=>$("info").classList.remove("open");
}

/* ---------- % invariants: mirror inversion (frame stays, operation changes) ---------- */
const MIR={"(":")",")":"(","[":"]","]":"[","{":"}","}":"{","<":">",">":"<","/":"\\","\\":"/","⟨":"⟩","⟩":"⟨"};
function invMask(s){ const c=chars(s||""), r=c.slice().reverse().map(x=>MIR[x]||x); return c.map((x,i)=>x===r[i]); }
const VIEWS={off:"◫",frame:"◫ Frame",operation:"◫ Operation"};
$("view").onclick=()=>{ view=view==="off"?"frame":view==="frame"?"operation":"off"; $("view").textContent=VIEWS[view]; save(); drawTerm();
  toast(view==="off"?"Highlighting off":view==="frame"?"Frame: what % leaves unchanged":"Operation: what % changes"); };

/* ---------- dual display: linear lines above, the same blocks compacted below ---------- */
function blocksOf(ls){ const out=[]; let cur=[]; ls.forEach((l,i)=>{ if(l.trim()) cur.push(i); else if(cur.length){ out.push(cur); cur=[]; } }); if(cur.length) out.push(cur); return out; }
function compactLines(ls){ // join with the hinge rule (drop the token a line shares with the one before), then drop joint slashes
  let s=ls[0]||""; for(const n of ls.slice(1)){ let k=Math.min(s.length,n.length); while(k>0&&!s.endsWith(n.slice(0,k))) k--; s+=n.slice(k); }
  return s.replace(/\/(?=[\[\{\(])/g,"").replace(/([\]\}\)])\//g,"$1"); }
function expandLine(s){ // compact → linear, one line per level, each line beginning with the token the last one ended on
  let t=s, framed=false; if(t.startsWith(".|")&&t.endsWith("|.")&&t.length>3){ framed=true; t=t.slice(2,-2); }
  const opens=[], closes=[]; let i=0; const strip=x=>x.replace(/^_+/,""), rstrip=x=>x.replace(/_+$/,"");
  t=strip(rstrip(t));
  while(true){ const m=t.match(/^_*([\[\{\(])/); if(!m) break; const o=m[1], cl=OPEN[o]; const end=t.lastIndexOf(cl); if(end<0) return [s];
    opens.push(o); closes.unshift(cl); t=rstrip(strip(t.slice(m[0].length,end))); const tail=t; i++; if(i>12) break; }
  if(!opens.length) return [s];
  if(/[\[\]\{\}\(\)]/.test(t)) return [s];        // siblings or deeper structure: keep it on one line
  const out=[]; let hinge=framed?"|":"";
  if(framed) out.push(".|");
  opens.forEach((o,k)=>{ if(k<opens.length-1||true){ if(k===opens.length-1) return; out.push(hinge+"__/"+o); hinge="/"+o; } });
  const last=opens[opens.length-1]; out.push(hinge+"__/"+last); hinge="/"+last;
  out.push(hinge+"__"+t+"__"+closes[0]+"/"); closes.slice(1).forEach(c=>out.push("/__"+c+"/"));
  if(framed){ out.push("/__|"); out.push("|."); }
  return out; }
const cc=$("cc"), cctx=cc.getContext("2d"); let CW=0,CH=0, cscroll=0;
function sizeCompact(){ const r=$("compact").getBoundingClientRect(); CW=r.width; CH=r.height; cc.width=CW*DPR; cc.height=CH*DPR; }
function compactRows(){ return blocksOf(lines).map(b=>({b,text:compactLines(b.map(i=>lines[i]))})); }
function drawCompact(){ if(!dual||!CW) return; const ctx=cctx, ch=cellH(), cw=cellW(), g=gutter(); ctx.setTransform(DPR,0,0,DPR,0,0);
  ctx.fillStyle=pal.paper; ctx.fillRect(0,0,CW,CH); const rows=compactRows();
  ctx.strokeStyle=pal.minor; ctx.beginPath(); for(let x=g;x<CW;x+=cw){ ctx.moveTo(Math.round(x)+.5,0); ctx.lineTo(Math.round(x)+.5,CH); } for(let y=0;y<CH;y+=ch){ ctx.moveTo(g,y+.5); ctx.lineTo(CW,y+.5); } ctx.stroke();
  rows.forEach((r,k)=>{ const y=k*ch-cscroll; if(pane==="compact"&&k===ccur.b){ ctx.fillStyle=pal.hl; ctx.fillRect(0,y,CW,ch); }
    ctx.font=`500 ${fontPx}px ui-monospace,"SF Mono",Menlo,monospace`; ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillStyle=pal.ink;
    chars(r.text).forEach((c,i)=>ctx.fillText(c,g+i*cw+cw/2,y+ch/2));
    ctx.fillStyle=pal.soft; ctx.font=`${Math.max(10,fontPx*0.45)}px ui-monospace,monospace`; ctx.textAlign="right";
    ctx.fillText(r.b.length>1?`${r.b[0]+1}–${r.b[r.b.length-1]+1}`:`${r.b[0]+1}`,g-6,y+ch/2); });
  if(pane==="compact"){ const y=ccur.b*ch-cscroll, x=g+ccur.c*cw; ctx.fillStyle=pal.node; ctx.fillRect(x-1,y+3,2.5,ch-6); }
  ctx.strokeStyle=pal.major; ctx.beginPath(); ctx.moveTo(g+.5,0); ctx.lineTo(g+.5,CH); ctx.stroke(); }
function applyCompact(k,text){ const rows=compactRows(), r=rows[k]; if(!r) return; const exp=expandLine(text);
  lines.splice(r.b[0],r.b.length,...exp); changed(); }
function compactInsert(t){ const rows=compactRows(), r=rows[ccur.b]; if(!r){ pane="linear"; insert(t); return; }
  const c=chars(r.text); let add=t, back=0; if(OPEN[t]&&mode==="insert"){ add=t+OPEN[t]; back=1; }
  c.splice(ccur.c,0,...chars(add)); ccur.c+=chars(add).length-back; applyCompact(ccur.b,c.join("")); }
function compactBack(){ const r=compactRows()[ccur.b]; if(!r||ccur.c<=0) return; const c=chars(r.text); c.splice(ccur.c-1,1); ccur.c--; applyCompact(ccur.b,c.join("")); }
cc.addEventListener("pointerup",e=>{ const b=cc.getBoundingClientRect(), y=e.clientY-b.top, x=e.clientX-b.left, rows=compactRows();
  const k=Math.floor((y+cscroll)/cellH()); if(!rows[k]){ pane="linear"; drawAll(); return; }
  pane="compact"; ccur={b:k,c:Math.max(0,Math.min(chars(rows[k].text).length,Math.round((x-gutter())/cellW())))}; drawAll(); toast("Editing the compact line: the linear pane follows"); });
tc.addEventListener("pointerdown",()=>{ if(pane!=="linear"){ pane="linear"; drawCompact(); } });
$("dual").onclick=()=>{ dual=!dual; document.body.classList.toggle("dual",dual); pane="linear"; save(); resize(); toast(dual?"Dual display: linear above, compact below":"Single display"); };

/* ---------- terminal modes: Insert (text lines), Place (drop anywhere), Link (connect symbols) ---------- */
const MODES={insert:"✎ Insert",place:"▣ Place",link:"⟋ Link"};
function setMode(m){ mode=m; linkFrom=null; $("mode").textContent=MODES[m]; save(); drawTerm();
  toast(m==="insert"?"Insert: typing shifts the line":m==="place"?"Place: keys drop into the cell, nothing shifts":"Link: tap one symbol, then another"); }
$("mode").onclick=()=>setMode(mode==="insert"?"place":mode==="place"?"link":"insert");
/* ---------- control row ---------- */
$("kSwitch").onclick=()=>{ const names=[...Object.keys(KB),"Mine"]; kbName=names[(names.indexOf(kbName)+1)%names.length]; kScroll=0; buildTabs(); layoutKeys(); drawKeys(); save();
  const t=[...document.querySelectorAll(".tab")].find(b=>b.getAttribute("aria-pressed")==="true"); if(t) t.scrollIntoView({inline:"center",block:"nearest"}); };
$("kSpace").onclick=()=>insert(" ");
function setFold(v){ folded=v; document.body.classList.toggle("folded",folded); $("kFold").textContent=folded?"▴":"▾"; $("kFold").setAttribute("aria-pressed",String(folded)); kScrollX=0; save(); resize(); }
$("kFold").onclick=()=>setFold(!folded);
/* your phone's keyboard, for words: a hidden field catches what you type and drops it into the grid */
const nat=$("native"); let composing=false; const SENT=" ";
function natFlush(){ const v=nat.value; if(v.length>1) insert(v.slice(1)); else if(v.length===0) backspace(); nat.value=SENT; }
nat.value=SENT;
nat.addEventListener("compositionstart",()=>composing=true);
nat.addEventListener("compositionend",()=>{ composing=false; natFlush(); });
nat.addEventListener("input",()=>{ if(!composing) natFlush(); });
nat.addEventListener("keydown",e=>{ if(e.key==="Enter"){ e.preventDefault(); natFlush(); newline(); } else if(e.key==="Backspace"&&nat.value===SENT&&!composing){ e.preventDefault(); backspace(); }
  else if(e.key==="ArrowLeft"){ e.preventDefault(); move(-1); } else if(e.key==="ArrowRight"){ e.preventDefault(); move(1); } });
function endNative(){ native=false; document.body.classList.remove("native"); $("kNative").setAttribute("aria-pressed","false"); resize(); }
let natExit=false;
nat.addEventListener("blur",()=>{ if(!native) return; setTimeout(()=>{ if(native&&(natExit||document.activeElement!==nat)){ natExit=false; if(document.activeElement!==nat) endNative(); } },300); });
[kc,tc].forEach(el=>el.addEventListener("mousedown",e=>{ if(native) e.preventDefault(); }));
$("kNative").addEventListener("pointerdown",e=>e.preventDefault());
$("kNative").onclick=()=>{ if(native){ natExit=true; nat.blur(); endNative(); return; } native=true; document.body.classList.add("native"); $("kNative").setAttribute("aria-pressed","true"); kScrollX=0; resize(); nat.value=SENT; nat.focus(); toast("Your keyboard: type words; symbols stay in the strip above it"); };
// keep the hidden field focused while typing natively, even after tapping the grid or a symbol
["kSpace","kBack","kEnter","kLeft","kRight","kSwitch","kFlip"].forEach(id=>$(id).addEventListener("pointerdown",e=>{ if(native) e.preventDefault(); }));
kc.addEventListener("pointerup",()=>{ if(native) setTimeout(()=>nat.focus(),0); });
tc.addEventListener("pointerup",()=>{ if(native) setTimeout(()=>nat.focus(),0); });
const FACES=["Keys","Logic cards: their uses","Examples: tap one to try it"];
$("kFlip").onclick=()=>{ face=(face+1)%3; $("kFlip").textContent=face===2?"-%":"%"; kScroll=0; layoutKeys(); drawKeys(); save(); toast(FACES[face]); }; $("kBack").onclick=backspace; $("kEnter").onclick=newline;
$("kLeft").onclick=()=>move(-1); $("kRight").onclick=()=>move(1);
$("kMenu").onclick=()=>{ $("info").innerHTML=`<h2>Terminal</h2><p>${lines.length} lines, ${links.length} links. Lines with a ✓ close every bracket they open; a ! marks one that doesn't (tap the number to see why). Checks run in Python.</p>
  <div class="acts"><button class="btn" id="mCopy">Copy all, with line numbers</button><button class="btn" id="mPlain">Copy text only</button>
  <button class="btn" id="mLinks">Clear links (${links.length})</button><button class="btn" id="mBig">Bigger cells</button><button class="btn" id="mSmall">Smaller cells</button><button class="btn" id="mClear">Clear terminal</button><button class="btn" id="mClose">Close</button></div>`;
  $("info").classList.add("open");
  const copy=t=>navigator.clipboard?navigator.clipboard.writeText(t).then(()=>toast("Copied"),()=>toast("Copy is blocked here")):toast("Copy is blocked here");
  $("mCopy").onclick=()=>copy(lines.map((l,i)=>String(i+1).padStart(String(lines.length).length," ")+"  "+l).join("\n"));
  $("mPlain").onclick=()=>copy(lines.join("\n"));
  $("mLinks").onclick=()=>{ links=[]; linkFrom=null; save(); drawTerm(); $("info").classList.remove("open"); };
  $("mBig").onclick=()=>{ fontPx=Math.min(40,fontPx+3); save(); keepCursorVisible(); drawTerm(); };
  $("mSmall").onclick=()=>{ fontPx=Math.max(12,fontPx-3); save(); keepCursorVisible(); drawTerm(); };
  $("mClear").onclick=()=>{ if(confirm("Clear every line and link?")){ lines=[""]; links=[]; cur={l:0,c:0}; changed(); $("info").classList.remove("open"); } };
  $("mClose").onclick=()=>$("info").classList.remove("open"); };
let toastT=null; function toast(m){ $("st").dataset.keep=$("st").dataset.keep||$("st").textContent; $("st").textContent=m; clearTimeout(toastT); toastT=setTimeout(()=>{ $("st").textContent=$("st").dataset.keep; delete $("st").dataset.keep; },2200); }

/* ---------- start ---------- */
function drawAll(){ drawTerm(); drawKeys(); drawCompact(); }
function resize(){ sizeTerm(); sizeKeys(); if(dual) sizeCompact(); layoutKeys(); drawAll(); }
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>{ readPal(); drawAll(); });
if(window.visualViewport) visualViewport.addEventListener("resize",()=>{ document.body.style.height=visualViewport.height+"px"; resize(); });
addEventListener("resize",resize); readPal(); document.body.classList.toggle("folded",folded); $("kFold").textContent=folded?"▴":"▾"; $("kFold").setAttribute("aria-pressed",String(folded));
$("mode").textContent=MODES[mode]; $("view").textContent=VIEWS[view]; document.body.classList.toggle("dual",dual); $("kFlip").textContent=face===2?"-%":"%"; resize(); boot();
</script>
</body>
</html>
