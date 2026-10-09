/* ---------- Grammar: Legend v0.1 tagger + recursive structure parser ---------- */
const G=(function(){
const L=s=>new Set(s.split(" "));
const ANC=L("the a an my your his her its our their each every any another this that these those whose");
const DEIX=L("this that these those here there other another");
const TIMEANC=L("now then today tomorrow yesterday tonight");
const PRON=L("i me you he him she it we us they them myself yourself himself herself itself ourselves themselves someone something somebody anyone anything anybody everyone everything everybody one mine yours hers ours theirs");
const QUANT=L("some all few many much several most more less fewer both enough various certain");
const QW=L("who whom whose what which where when why how");
const PF=L("up to into onto toward towards at on in upon with by for over under across through along around about against between among beside near past within behind beyond above below inside outside via per during throughout without");
const PB=L("down from of off out away since back except");
const AND=L("and both plus"), OR=L("or either nor but yet");
const REL=L("same different like as than unlike alike");
const NEG=L("not no never none nothing nobody neither nowhere n't");
const BE=L("be am is are was were been being 's 're 'm");
const HAVE=L("have has had having 've 'd"), DO=L("do does did");
const MODAL=L("will would shall should can could may might must ought 'll");
const COPULA=L("be am is are was were been being become becomes became seem seems seemed remain remains remained");
const LINKING=L("look looks looked feel feels felt sound sounds sounded taste tastes smell smells appear appears appeared grow grows grew get gets got turn turns turned stay stays stayed");
const OC=L("make makes made call calls called name names named consider considers considered elect elected keep keeps kept find finds found leave leaves left render rendered paint painted");
const SUBS=L("because although though if unless while whereas whether so");
const SUBPREP=L("before after since until till once");
const IRR={went:"go",gone:"go",ran:"run",made:"make",took:"take",taken:"take",saw:"see",seen:"see",was:"be",were:"be",been:"be",had:"have",did:"do",done:"do",said:"say",got:"get",gotten:"get",gave:"give",given:"give",came:"come",knew:"know",known:"know",thought:"think",told:"tell",found:"find",left:"leave",felt:"feel",brought:"bring",began:"begin",begun:"begin",kept:"keep",held:"hold",wrote:"write",written:"write",stood:"stand",heard:"hear",meant:"mean",met:"meet",paid:"pay",sat:"sit",spoke:"speak",spoken:"speak",lay:"lie",led:"lead",grew:"grow",grown:"grow",lost:"lose",fell:"fall",fallen:"fall",sent:"send",built:"build",understood:"understand",drew:"draw",drawn:"draw",broke:"break",broken:"break",spent:"spend",rose:"rise",risen:"rise",drove:"drive",driven:"drive",bought:"buy",wore:"wear",worn:"wear",chose:"choose",chosen:"choose",sought:"seek",threw:"throw",thrown:"throw",caught:"catch",won:"win",forgot:"forget",forgotten:"forget",hung:"hang",shook:"shake",stole:"steal",stolen:"steal",struck:"strike",swam:"swim",sang:"sing",sung:"sing",rang:"ring",drank:"drink",drunk:"drink",fought:"fight",fed:"feed",fled:"flee",flew:"fly",flown:"fly",froze:"freeze",frozen:"freeze",hid:"hide",hidden:"hide",bit:"bite",bitten:"bite",blew:"blow",blown:"blow",bore:"bear",born:"bear",bent:"bend",bound:"bind",dug:"dig",laid:"lay",lent:"lend",lit:"light",rode:"ride",ridden:"ride",shone:"shine",shot:"shoot",slid:"slide",slept:"sleep",spun:"spin",sprang:"spring",stuck:"stick",swept:"sweep",swore:"swear",swung:"swing",taught:"teach",tore:"tear",torn:"tear",wept:"weep",woke:"wake",wound:"wind",ate:"eat",eaten:"eat",men:"man",women:"woman",children:"child",feet:"foot",teeth:"tooth",mice:"mouse",people:"person",better:"good",best:"good",worse:"bad",worst:"bad",has:"have",does:"do",is:"be",are:"be",am:"be"};
let look=()=>null; // word -> {poss,pos,rank,up}
let glyphCatch=()=>"";
function lemmas(w){const o=[w];if(IRR[w])o.push(IRR[w]);
  const add=x=>{if(x&&x.length>1&&!o.includes(x))o.push(x)};
  if(/ies$/.test(w))add(w.slice(0,-3)+"y"); if(/ied$/.test(w))add(w.slice(0,-3)+"y");
  if(/es$/.test(w))add(w.slice(0,-2)); if(/s$/.test(w)&&!/ss$/.test(w))add(w.slice(0,-1));
  if(/ed$/.test(w)){add(w.slice(0,-2));add(w.slice(0,-1));if(/(.)\1ed$/.test(w))add(w.slice(0,-3))}
  if(/ing$/.test(w)){add(w.slice(0,-3));add(w.slice(0,-3)+"e");if(/(.)\1ing$/.test(w))add(w.slice(0,-4))}
  if(/er$/.test(w)){add(w.slice(0,-2));add(w.slice(0,-1))} if(/est$/.test(w)){add(w.slice(0,-3));add(w.slice(0,-2))}
  if(/ly$/.test(w)){add(w.slice(0,-2));if(/ily$/.test(w))add(w.slice(0,-3)+"y")}
  return o}
function cands(w){
  const own=look(w); const set=new Set(own&&own.poss?own.poss.split(""):own?[own.pos[0]]:[]); let lem=own?w:null;
  for(const l of lemmas(w).slice(1)){const e=look(l);if(!e)continue;const p=e.poss||e.pos[0];
    if(/s$/.test(w)&&!IRR[w]){if(p.includes("n"))set.add("n");if(p.includes("v"))set.add("v")}
    else if(/(ed|ing)$/.test(w)||IRR[w]){if(p.includes("v"))set.add("v");if(/^(men|women|children|feet|teeth|mice|people)$/.test(w)&&p.includes("n"))set.add("n")}
    else if(/(er|est)$/.test(w)){if(p.includes("a"))set.add("a")}
    else if(/ly$/.test(w)){if(p.includes("a"))set.add("r")}
    if(!lem&&(set.size))lem=l}
  if(!set.size){ // guess from shape
    if(/ly$/.test(w))set.add("r");else if(/(ed|ing)$/.test(w))set.add("v");else if(/(ous|ful|ive|al|able|ible|ic|less|ish|ary|ent|ant)$/.test(w))set.add("a");else set.add("n")}
  return {set,lem:lem||(IRR[w]||w)}}
function tokenize(s){return (s.toLowerCase().replace(/[“”"’]/g,m=>m==="’"?"'":" ").replace(/\bcan't\b/g,"can n't").replace(/\bwon't\b/g,"will n't").replace(/n't\b/g," n't").replace(/'(ll|re|ve|m|d)\b/g," '$1").replace(/\b(it|he|she|that|there|what|who|where|here|how)'s\b/g,"$1 's").match(/[a-z0-9]+(?:[-'][a-z0-9]+)*|'[a-z]+|[,;:.!?]/g)||[])}
const NOUNISH=t=>t&&(t.k==="N"||t.k==="PRON");
function tag(sentence){
  const ws=tokenize(sentence); const T=ws.map(w=>({w,k:null}));
  const peekC=i=>i<ws.length&&/^[a-z]/.test(ws[i])?closedKind(i)||("c:"+[...cands(ws[i]).set].join("")):"";
  function closedKind(i){const w=ws[i];
    if(BE.has(w)||HAVE.has(w)||DO.has(w)||MODAL.has(w))return"AUX";
    if(NEG.has(w))return"NEG"; if(AND.has(w))return"AND"; if(OR.has(w))return"OR";
    if(PRON.has(w))return"PRON"; if(ANC.has(w)||TIMEANC.has(w))return"ANC"; if(PF.has(w))return"PF"; if(PB.has(w))return"PB";
    if(REL.has(w))return"REL"; if(QW.has(w))return"Q"; if(SUBS.has(w))return"SUB"; if(QUANT.has(w))return"ADJ"; return null}
  let clauseHasV=false;
  for(let i=0;i<T.length;i++){const t=T[i],w=t.w,prev=T[i-1],nx=ws[i+1]||"",nxk=peekC(i+1);
    if(/^[,;:.!?]$/.test(w)){t.k="P";if(w!==",")clauseHasV=false;continue}
    if(/^\d/.test(w)){t.k="ADJ";continue}
    if(/[a-z]('s|s')$/.test(w)&&!PRON.has(w)){t.k="ANC";t.poss=1;t.lem=w.replace(/('s|')$/,"");continue}
    if(QW.has(w)){t.k=(i===0||(prev&&prev.k==="P"))?"Q":"SUB";clauseHasV=false;continue}
    if(w==="that"){const nk=peekC(i+1);
      if(prev&&(prev.k==="V"||prev.k==="AUX"||prev.k==="N")&&(nk==="PRON"||ANC.has(nx)||/c:.*n/.test(nk))&&i>0){t.k="SUB";clauseHasV=false;continue}
      t.k=/c:[^v]*n/.test(nk)&&!/v/.test(nk.split(":")[1]||"")?"ANC":"N";if(t.k==="N")t.deix=1;continue}
    if(w==="to"){const c=peekC(i+1);if(/^c:.*v/.test(c)&&!ANC.has(nx)){t.k="INF";clauseHasV=false;continue}t.k="PF";continue}
    if(DEIX.has(w)){const nk=peekC(i+1);if(/^c:/.test(nk)&&/[na]/.test(nk)&&!(nk.includes("v")&&prev&&NOUNISH(prev))){t.k="ANC"}else{t.k="N";t.deix=1}continue}
    if(TIMEANC.has(w)){t.k="TIME";t.time=1;continue}
    if(w==="her"||w==="his"){t.k=/^c:.*[na]/.test(nxk)?"ANC":"PRON";continue}
    if(ANC.has(w)){t.k="ANC";continue}
    if(PRON.has(w)){t.k="PRON";continue}
    if(QUANT.has(w)){t.k=/^c:.*[na]|ANC|ADJ/.test(nxk)?"ADJ":"N";continue}
    if(NEG.has(w)){t.k="NEG";continue}
    if(BE.has(w)||HAVE.has(w)||DO.has(w)||MODAL.has(w)){t.k="AUX";clauseHasV=true;continue}
    if(SUBS.has(w)&&w!=="so"){t.k="SUB";clauseHasV=false;continue}
    if(SUBPREP.has(w)){const rest=ws.slice(i+1,i+6);const hasV=rest.some((x,j)=>BE.has(x)||HAVE.has(x)||DO.has(x)||MODAL.has(x)||(j>0&&/c:.*v/.test(peekC(i+1+j))&&!/n/.test(peekC(i+1+j))));
      t.k=hasV&&(PRON.has(nx)||ANC.has(nx))?"SUB":"PF";if(t.k==="SUB")clauseHasV=false;continue}
    if(AND.has(w)){t.k="AND";continue} if(OR.has(w)){t.k="OR";continue}
    if(REL.has(w)){if(prev&&prev.k==="ANC"){t.k="ADJ";t.rel=1}else t.k="REL";continue}
    if(PF.has(w)){t.k="PF";continue} if(PB.has(w)){t.k="PB";continue}
    const {set,lem}=cands(w); t.lem=lem; t.amb=set.size>1; const has=c=>set.has(c);
    let pj=i-1;while(T[pj]&&(T[pj].k==="ADV"||T[pj].k==="TIME"))pj--;const pk=T[pj]?T[pj].k:null; const nN=/^c:.*n/.test(nxk), nA=/^c:.*a/.test(nxk);
    let k=null;
    if(set.size===1)k={n:"N",v:"V",a:"ADJ",r:"ADV"}[[...set][0]];
    else if(has("r")&&/ly$/.test(w))k="ADV";
    else if(pk==="INF"||pk==="AUX"&&has("v")&&(/(ed|ing|en)$/.test(w)||!/^(be|am|is|are|was|were|been|being)$/.test(prev.w))||(pk==="NEG"&&has("v")&&T[i-2]&&T[i-2].k==="AUX"))k="V";
    else if(pk==="AUX"&&/^(be|am|is|are|was|were|been|being)$/.test(prev.w)&&has("v")&&/(ed|ing|en)$/.test(w))k="V";
    else if(pk==="ANC"||pk==="ADJ"||pk==="PF"||pk==="PB"||pk==="REL")k=has("a")&&(nN||nA)&&!(has("n")&&!nN)?"ADJ":has("n")?"N":has("a")?"ADJ":"V";
    else if((pk==="PRON"||pk==="N"||pk==="SUB"||pk==="Q")&&has("v")&&!clauseHasV)k="V";
    else if((i===0||pj<0)&&has("v")&&(/^(ANC|PRON|PF|PB|REL)$/.test(nxk)||nxk==="ADJ"&&(IRR[w]||/(ed|t)$/.test(w))))k="V";
    else if(pk==="NEG"&&has("v"))k="V";
    else if(has("a")&&nN&&!has("v"))k="ADJ";
    else if((pk==="V"||pk==="AUX")&&has("a")&&!nN)k="ADJ";
    else if((pk==="N"||pk==="PRON")&&clauseHasV&&has("a")&&!nN)k="ADJ";
    else if((pk==="V"||pk==="AUX")&&has("r")&&!has("n"))k="ADV";
    else if(has("n"))k="N"; else if(has("a"))k="ADJ"; else if(has("v"))k="V"; else k="ADV";
    t.k=k; if(k==="V")clauseHasV=true;
  }
  // a trailing ANC with no noun becomes a state (e.g. "I like that")
  T.forEach((t,i)=>{if(t.k==="ANC"&&!t.time&&!(T[i+1]&&/N|ADJ|ANC/.test(T[i+1].k))){t.k="N";t.deix=1}});
  return T.filter(t=>t.k!=="P"||t.w===","||t.w===";");
}
/* ---- constituents ---- */
function chunk(T){const C=[];let i=0;
  while(i<T.length){const t=T[i];
    if(t.k==="ANC"||t.k==="ADJ"||t.k==="N"||t.k==="PRON"){const np={type:"NP",anc:[],adj:[],n:[]};
      while(i<T.length&&T[i].k==="ANC"){np.anc.push(T[i]);i++}
      while(i<T.length&&(T[i].k==="ADJ"||T[i].k==="ADV"&&T[i+1]&&T[i+1].k==="ADJ")){np.adj.push(T[i]);i++}
      while(i<T.length&&(T[i].k==="N"||T[i].k==="PRON")){if(T[i].k==="PRON"&&np.n.length)break;np.n.push(T[i]);i++;if(np.n[np.n.length-1].k==="PRON")break}
      if(!np.n.length&&np.adj.length&&!np.anc.length){C.push({type:"ADJP",adj:np.adj});continue}
      C.push(np);continue}
    if(t.k==="AUX"||t.k==="V"||(t.k==="ADV"&&T[i+1]&&(T[i+1].k==="V"||T[i+1].k==="AUX"))){const vg={type:"VG",aux:[],v:[],adv:[],neg:[],seq:[]};
      while(i<T.length&&/AUX|V|ADV|NEG/.test(T[i].k)){const x=T[i];
        if(x.k==="ADV"&&!(vg.v.length===0||T[i+1]&&/V|AUX/.test(T[i+1].k))&&vg.v.length){ if(!(T[i+1]&&/V|AUX/.test(T[i+1].k)))break}
        if(x.k==="V"&&vg.v.length&&!(T[i-1]&&/AUX|NEG|ADV/.test(T[i-1].k)))break;
        vg.seq.push(x);(x.k==="AUX"?vg.aux:x.k==="V"?vg.v:x.k==="ADV"?vg.adv:vg.neg).push(x);i++}
      const lastAux=vg.aux[vg.aux.length-1];
      vg.passive=!!(vg.v.length&&vg.aux.some(a=>/^(be|am|is|are|was|were|been|being|get|got)$/.test(a.w))&&/(ed|en|wn|t)$/.test(vg.v[vg.v.length-1].w)&&!/ing$/.test(vg.v[vg.v.length-1].w));
      const head=(vg.v[vg.v.length-1]||lastAux||{}).w||"";
      vg.copula=!vg.v.length?COPULA.has(head):COPULA.has(head)||LINKING.has(head);
      vg.head=head; C.push(vg);continue}
    if(t.k==="PF"||t.k==="PB"){C.push({type:"PREP",t});i++;continue}
    if(t.k==="SUB"||t.k==="INF"){ // embedded clause: to the next comma/semicolon or end
      let j=i+1;const relv=t.k==="SUB"&&/^(who|which|that|whom|whose)$/.test(t.w)&&C.length&&C[C.length-1].type==="NP";let seenV=false,afterV=false;
      while(j<T.length&&T[j].k!=="P"){const x=T[j];if(relv&&/^(V|AUX)$/.test(x.k)){if(afterV)break;seenV=true}else if(seenV&&x.k!=="NEG"&&x.k!=="ADV")afterV=true;j++}C.push({type:"EMB",t,body:T.slice(i+1,j)});i=j;continue}
    C.push({type:t.k,t});i++}
  return C}
const sup=t=>{const g=glyphCatch(t.lem||t.w,t.k);return g?"^"+g:""};
const W=t=>t.rel?"}"+t.w+sup(t)+"{":t.w+sup(t);
function rNP(np){let s=np.n.map(W).join(" ");s=s?"["+s+"]":"";
  const ra=np.adj.filter(a=>a.rel),pa=np.adj.filter(a=>!a.rel);
  if(pa.length)s="{"+pa.map(a=>a.k==="ADV"?"<"+W(a)+">":W(a)).join(" ")+(s?" "+s:"")+"}";
  if(ra.length)s=ra.map(W).join(" ")+(s?" "+s:"");
  if(np.anc.length)s="|"+np.anc.map(W).join(" ")+(s?" "+s:"")+"|";return s}
function rVG(vg){const neg=vg.neg.length?" ]"+vg.neg.map(W).join(" ")+"[":"";
  const core=[...vg.aux,...vg.v].map(W).join(" ");const adv=vg.adv.map(W).join(" ");
  if(vg.passive)return (adv?"<"+adv+" ":"")+")"+core+"("+neg;
  return (adv?"<"+adv+" ":"(")+core+")"+neg}
function parse(sentence,maxDepth=6){const T=tag(sentence);return clause(T,0,maxDepth)}
function clause(T,depth,maxDepth){
  const C=chunk(T);const parts=[];const emb=[];let pat="",subj=false,verb=null,objs=0,q=false,ex=false;
  const vi=C.findIndex(c=>c.type==="VG");
  C.forEach((c,ci)=>{
    if(c.type==="NP"){parts.push(rNP(c));
      if(vi<0||ci<vi){if(!subj){if(c.n.length===1&&c.n[0].w==="there"&&C[ci+1]&&C[ci+1].type==="VG"&&COPULA.has(C[ci+1].head)){ex=true;pat+="∃"}else pat+="S";subj=true}}
      else if(C[ci-1]&&C[ci-1].type==="PREP"){}
      else if(ex&&objs===0){pat+="S";objs++}
      else if(verb&&verb.copula){pat+="C"}
      else if(verb&&objs===1&&OC.has(verb.head)&&C[ci-1]&&C[ci-1].type==="NP"){pat+="C"}
      else {pat+="O";objs++}}
    else if(c.type==="ADJP"){parts.push("{"+c.adj.map(W).join(" ")+"}");if(verb)pat+="C"}
    else if(c.type==="VG"){parts.push(rVG(c));if(!verb){verb=c;pat+=c.passive?"Vᵖ":"V"}}
    else if(c.type==="PREP"){parts.push(c.t.k==="PF"?"/"+W(c.t)+"/":"\\"+W(c.t)+"\\");if(verb&&!pat.endsWith("A"))pat+="A";if(!verb&&!pat)pat+="";}
    else if(c.type==="EMB"){const opener=c.t.k==="INF"?"/"+c.t.w+"/":">"+c.t.w+"<";
      if(depth+1<=maxDepth&&c.body.length){const sub=clause(c.body,depth+1,maxDepth);parts.push(opener+"⟨"+sub.notation+"⟩");emb.push(sub.pattern)}
      else parts.push(opener+"⟨"+c.body.map(W).join(" ")+"⟩")}
    else if(c.type==="Q"){parts.push(">"+W(c.t)+"<");q=true}
    else if(c.type==="ADV"){parts.push("<"+W(c.t)+">");if(verb&&!pat.endsWith("A"))pat+="A"}
    else if(c.type==="TIME"){parts.push("|"+W(c.t)+"|");if(verb&&!pat.endsWith("A"))pat+="A"}
    else if(c.type==="AND")parts.push("/"+W(c.t)+"\\");
    else if(c.type==="OR")parts.push("\\"+W(c.t)+"/");
    else if(c.type==="REL")parts.push("}"+W(c.t)+"{");
    else if(c.type==="NEG")parts.push("]"+W(c.t)+"[");
    else if(c.type==="P"){}
    else parts.push(W(c.t));
  });
  if(!verb){pat=C.some(c=>c.type==="NP")?"∅NP":"∅"} else if(!subj&&!q)pat=(depth?"":"!")+pat; // ! = imperative at top level
  if(q)pat="Q:"+pat;
  const pattern=pat+(emb.length?"⟨"+emb.join("·")+"⟩":"");
  return {notation:parts.join(" "),pattern,core:pat,emb,tokens:T.map(t=>({w:t.w,k:t.k,lem:t.lem}))}
}
const LEGEND=[["[•]","Noun","a state (operator or operand)","1 · innermost"],["{•}","Adjective","property of a state","2 · wraps the state"],["|•|","Anchor","this/that, here/there, now; articles and possessives","3 · outermost"],
  ["(•)","Verb","an operation","1"],["<•>","Adverb","magnitude or effect of an operation","2"],["<•)","Fused","magnitude opening into an operation: left mark modifies, right mark is the head","mixed"],
  ["/•/","Preposition, forward","D.O → I.O (to, into, for, with…)","joins"],["\\•\\","Preposition, backward","I.O ← D.O (from, of, off, out…)","joins"],
  [">•<","Interrogative","the empty slot (?), also opens a nested clause","fills any slot"],["/•\\","Pair, join","and, both","joins"],["\\•/","Pair, split","or, either, nor, but","joins"],
  ["}•{","Relation","same, different, like, as, than","joins"],["]•[","Absence","no, not, none, never","replaces [•]"],[")•(","Turned operation","passive or reflexive","replaces (•)"],
  ["⟨…⟩","Nested clause","an embedded clause, parsed again one level deeper","recursion"],["^x","Catch","glyph cards that catch this word","superscript"],["ⁿ","Sense","sense number on any slot","superscript"]];
const PATTERNS={S:"subject",V:"operation (verb)",Vᵖ:"turned operation (passive)",O:"object",C:"complement",A:"adverbial","∃":"existential there",Q:"question","!":"imperative (no subject)","∅":"fragment, no operation","⟨⟩":"nested clause patterns"};
return {tag,parse,tokenize,cands,setLookup:f=>look=f,setCatch:f=>glyphCatch=f,LEGEND,PATTERNS};
})();
if(typeof module!=="undefined")module.exports=G;
