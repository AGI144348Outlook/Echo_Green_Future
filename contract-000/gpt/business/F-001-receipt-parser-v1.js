// GPT-only F-001 strict synthetic receipt parser; NOT a signature verifier.
function accept(body){
  if(typeof body!=="string"||!/^\{[\x20-\x7e]*\}$/.test(body))return false;
  let pairs;try{pairs=JSON.parse(body)}catch{return false}
  if(!pairs||Array.isArray(pairs)||typeof pairs!=="object")return false;
  const keys=["decision","evidence_blob","expires_at","issued_at","issuer","nonce","unit","v"];
  if(Object.keys(pairs).length!==8||keys.some(k=>!Object.hasOwn(pairs,k)))return false;
  if(JSON.stringify(pairs)!==body)return false; // canonical bytes; duplicate keys and spacing rejected
  if(Object.keys(pairs).join(",")!==keys.join(","))return false;
  if(pairs.v!==1||typeof pairs.v!=="number"||!Number.isInteger(pairs.v))return false;
  if(!["ACCEPT","REJECT"].includes(pairs.decision))return false;
  if(!/^[0-9a-f]{40}$/.test(pairs.evidence_blob)||!/^[0-9a-f]{32}$/.test(pairs.nonce))return false;
  if(!/^[a-z0-9-]+$/.test(pairs.issuer)||!/^[A-Za-z0-9-]+$/.test(pairs.unit))return false;
  const iso=/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
  if(!iso.test(pairs.issued_at)||!iso.test(pairs.expires_at))return false;
  const a=Date.parse(pairs.issued_at),b=Date.parse(pairs.expires_at);
  if(!Number.isFinite(a)||!Number.isFinite(b)||new Date(a).toISOString().replace(".000Z","Z")!==pairs.issued_at||new Date(b).toISOString().replace(".000Z","Z")!==pairs.expires_at)return false;
  return b>a&&b-a<=30*86400000;
}
if(typeof module!=="undefined")module.exports={accept};
