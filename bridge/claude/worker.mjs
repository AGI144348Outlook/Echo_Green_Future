// echo-bot-claude, Stage 0 inert Worker (Contract 000 §17, BOT-COORDINATION.md).
// Inert by design: reports whether the Workers AI binding is present but never calls it;
// no model calls, no GitHub access, no secret reads, no cron work.
// Owner: Claude. Deployed only through the bridge with participant = claude.
const SERVICE = "echo-bot-claude";
const VERSION = "0.0.2-inert";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
    },
  });

export default {
  async fetch(request, env = {}) {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      if (request.method !== "GET" && request.method !== "HEAD") {
        return json({ error: "method_not_allowed" }, 405);
      }
      return json({
        service: SERVICE,
        status: "inert",
        version: VERSION,
        ai_binding: typeof env.AI?.run === "function",
        timestamp: new Date().toISOString(),
      });
    }
    return json({ error: "not_found" }, 404);
  },

  async scheduled() {
    // Intentionally a no-op until Timothy approves real work (Contract 000 §14, §17).
  },
};
