// Inert Stage 0 bot shell. No model, GitHub, KV, or outbound network access.
const respond=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store","x-content-type-options":"nosniff"}});
export default {
  async fetch(request) {
    const url=new URL(request.url);
    if(request.method==="GET" && url.pathname==="/health") return respond({service:"echo-bot-stage0-inert",status:"inert",version:"0.0.1",timestamp:new Date().toISOString()});
    return respond({error:"not_found"},404);
  },
  async scheduled() { /* Deliberate no-op; no autonomous activity. */ }
};
