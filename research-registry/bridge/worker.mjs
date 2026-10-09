// Stage 0 inert Cloudflare Worker shell.
// Not deployed. No GitHub access, model calls, cron work, or secret reads.
// Intended for a separately approved deployment to a participant-owned Worker.
const VERSION = "0.0.1-inert";
const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status,
  headers: {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "x-content-type-options": "nosniff",
  },
});
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/health") {
      return json({
        service: "echo-bot-bridge",
        status: "inert",
        version: VERSION,
        timestamp: new Date().toISOString(),
      });
    }
    return json({ error: "not_found" }, 404);
  },
  async scheduled(_event, _env, _ctx) {
    // Intentionally no-op. Do not enable real work before approved gates.
    return;
  },
};
