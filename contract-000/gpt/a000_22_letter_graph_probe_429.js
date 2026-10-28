/** Run429 isolated source-transcribed 22-letter A-000 graph probe.
 * Input: exact genesis-documentary/src/alphabet_data.py, blob
 * 3ec8330646880e69dd9dd74b35f79fd58409af0e.
 * Models WordAgent reference regex, Lobby orientation/additive ties and
 * ReshIdentity.anchor list update; NOT the full Genesis runtime or frozen test.
 * Call probe(alphabetText); result includes all assertion labels.
 */
function probe(alphabetText) {
  const block=alphabetText.split("HEBREW_ALPHABET = [")[1]?.split("LATIN_ALPHABET =")[0];
  if (!block) throw Error("Hebrew alphabet source not found");
  const entries=[...block.matchAll(/\{"name":\s*"([^"]+)"[\s\S]*?"properties":\s*\[([\s\S]*?)\]\s*\}/g)]
    .map(m=>({name:m[1],props:[...m[2].matchAll(/"([^"]*)"/g)].map(x=>x[1])}));
  const agents=new Map(entries.map(x=>[x.name,{word:x.name,defs:[...x.props],
    raw:x.props.join(" "),score:0.9,confirmed:true,ties:new Set()}]));
  const graph=new Map(), checks=[];
  const check=(name,ok)=>{checks.push({name,pass:!!ok});if(!ok)throw Error("FAIL "+name)};
  const refs=a=>new Set((a.defs.join(" ").toLowerCase().match(/[a-z']+/g)||[])
    .filter(x=>x!==a.word && x.length>1));
  function orient() {
    if ([...agents.values()].some(a=>!a.confirmed))throw Error("unconfirmed");
    const discovered=[...agents].map(([name,a])=>[name,refs(a)]);
    for(const [name,words] of discovered)for(const w of words)if(w!==name&&agents.has(w)){
      const key=[name,w].sort().join("|");
      graph.set(key,(graph.get(key)||0)+1);
      agents.get(name).ties.add(w);agents.get(w).ties.add(name);
    }
    return graph.size;
  }
  check("22 source letters",entries.length===22&&agents.size===22);
  check("no initial cross-letter name tokens",![...agents.values()].some(a=>[...refs(a)].some(w=>agents.has(w))));
  check("initial orientation zero edges",orient()===0);
  const resh=agents.get("resh"),raw=resh.raw,score=resh.score;
  resh.defs=[...new Set([...resh.defs,"governor","indexing","algorithm","identity","matrix","aleph","ayin","pe"])];
  check("anchor adds three letter references",["aleph","ayin","pe"].every(w=>refs(resh).has(w)));
  check("anchor leaves graph unchanged",graph.size===0&&resh.ties.size===0);
  check("first explicit orientation 3 edges",orient()===3);
  check("first strengths one",[...graph.values()].every(v=>v===1));
  check("resh adjacency three",resh.ties.size===3&&["aleph","ayin","pe"].every(w=>resh.ties.has(w)));
  check("second orientation 3 unique edges",orient()===3);
  check("second strengths two",[...graph.values()].every(v=>v===2));
  check("adjacency set hides strength duplication",resh.ties.size===3);
  check("raw definition unchanged",resh.raw===raw&&!raw.includes("aleph"));
  check("generality unchanged",resh.score===score&&score===0.9);
  return {scope:"isolated source-transcribed JS, not full Genesis",letters:entries.length,
    passed:checks.length,total:checks.length,post_anchor_edges:0,after_first:3,
    after_second_weights:[...graph.values()].sort(),checks};
}
if(typeof module!=="undefined"&&module.exports)module.exports={probe};
