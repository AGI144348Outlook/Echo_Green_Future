// GPT inert shell v0.0.2. Binding detection only; no inference or outbound calls.
const respond=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store","x-content-type-options":"nosniff"}});
export default {
  async fetch(request,env) {
    const url=new URL(request.url);
    if(request.method==="GET" && url.pathname==="/health") return respond({service:"echo-bot-stage0-inert",status:"inert",version:"0.0.2-inert",ai_binding:typeof env?.AI?.run==="function",timestamp:new Date().toISOString()});
    if(request.method==="GET" && url.pathname==="/think") {
      // No inference yet. Stable, schema-limited probe for the GitHub writing bridge.
      return respond({schema:"contract-000-think/v0",service:"echo-bot-stage0-inert",status:"inert",action:"no-op",ai_binding:typeof env?.AI?.run==="function"});
    }
    return respond({error:"not_found"},404);
  },
  async scheduled() { /* Deliberate no-op. */ }
};
