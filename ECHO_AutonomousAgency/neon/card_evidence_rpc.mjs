/** Inert, policy-scoped MCP tools core for Neon card/evidence protocols.
 *
 * Pre-test threads:
 * NexusBoard: https://github.com/AGI144348Outlook/NexusBoard/issues/2
 * Echo: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/435
 *
 * This is an APPLICATION RPC HANDLER, not a deployed MCP HTTP endpoint.
 * Host MUST authenticate and bind context separately, check Origin/headers,
 * call authorizer at the final operation boundary, and implement MCP 2026-07-28
 * Streamable HTTP transport. No card or caller-provided headers grant rights.
 */
const ALLOWED = new Set([
  "catalog.card.get", "catalog.configuration.resolve", "catalog.card.propose",
  "evidence.node.get", "evidence.edge.trace", "evidence.edge.propose",
  "dictionary.lexical_path", "dictionary.network.compare",
]);
const PROPOSALS = new Set(["catalog.card.propose", "evidence.edge.propose"]);
const DICTIONARY = new Set(["dictionary.lexical_path", "dictionary.network.compare"]);

function error(id, code, message) {
  return {jsonrpc:"2.0", id, error:{code, message}};
}
function result(id, response) {
  return {jsonrpc:"2.0", id, result:response};
}
function validArguments(schema, args) {
  if (!args || typeof args !== "object" || Array.isArray(args)) return false;
  if (!schema || schema.type !== "object") return false;
  const names = Object.keys(args);
  if (names.some(k => !(k in schema.properties))) return false;
  if ((schema.required || []).some(k => !(k in args))) return false;
  for (const [key, value] of Object.entries(args)) {
    const spec = schema.properties[key];
    if (spec.type === "integer" &&
        (!Number.isInteger(value) || (spec.minimum !== undefined && value < spec.minimum)
          || (spec.maximum !== undefined && value > spec.maximum))) return false;
    if (spec.type === "string" && (typeof value !== "string" || !value.trim() || value.length > 256)) return false;
    if (spec.type === "object" && (!value || typeof value !== "object" || Array.isArray(value))) return false;
    if (spec.enum && !spec.enum.includes(value)) return false;
  }
  return true;
}
function isAdmitted(ctx, name) {
  const admitted = Array.isArray(ctx.admitted_words) ? ctx.admitted_words : [];
  return admitted.includes(name);
}
export function createCardEvidenceRpc(manifest, adapter, authorization) {
  if (!manifest || !Array.isArray(manifest.tools) || !adapter ||
      typeof authorization !== "function") throw new TypeError("trusted configuration required");
  const tools = new Map(manifest.tools.filter(t => ALLOWED.has(t.name)).map(t => [t.name, t]));
  return async function handle(rpc, trustedContext) {
    const id = rpc && Object.prototype.hasOwnProperty.call(rpc, "id") ? rpc.id : null;
    if (!trustedContext?.authenticated_principal || !trustedContext?.mission_id) {
      return error(id, -32001, "Unauthenticated or unscoped mission");
    }
    if (!rpc || rpc.jsonrpc !== "2.0" || typeof rpc.method !== "string") {
      return error(id, -32600, "Invalid request");
    }
    if (rpc.method === "tools/list") {
      const visible = [];
      for (const t of tools.values()) {
        if (await authorization(trustedContext, t.name, "discover")) {
          visible.push({name:t.name, description:t.title, inputSchema:t.inputSchema});
        }
      }
      return result(id, {tools:visible, ttlMs:0, cacheScope:"private"});
    }
    if (rpc.method === "resources/templates/list") {
      // Discovery is scoped too. Never enumerate actual card IDs or all seats.
      return result(id, {resourceTemplates:await authorization(
        trustedContext, "resources/templates/list", "discover"
      ) ? manifest.resourceTemplates : []});
    }
    if (rpc.method !== "tools/call") return error(id, -32601, "Method not found");
    const name=rpc.params?.name, args=rpc.params?.arguments;
    const tool=tools.get(name);
    if (!tool) return error(id, -32602, "Tool unavailable");
    if (!validArguments(tool.inputSchema, args)) return error(id, -32602, "Invalid tool arguments");
    if (!await authorization(trustedContext, name, "invoke")) {
      return error(id, -32003, "Tool not permitted for this mission or seat");
    }
    if (PROPOSALS.has(name) && !trustedContext.may_propose) {
      return error(id, -32003, "Proposal write requires separate proposal authorization");
    }
    if (DICTIONARY.has(name)) {
      if (manifest.dictionaryIntegrated !== true) return error(id, -32003, "Dictionary disabled");
      const words = name === "dictionary.lexical_path" ? [args.word] : [args.left,args.right];
      if (!words.every(word => isAdmitted(trustedContext, word))) {
        return error(id, -32003, "Dictionary word not admitted into this mission");
      }
    }
    const methodMap = {
      "catalog.card.get":"getCard", "catalog.configuration.resolve":"resolveConfiguration",
      "catalog.card.propose":"proposeCard", "evidence.node.get":"getNode",
      "evidence.edge.trace":"traceEdges", "evidence.edge.propose":"proposeEdge",
      "dictionary.lexical_path":"dictionaryPath",
      "dictionary.network.compare":"compareWords",
    };
    const method=methodMap[name];
    if (typeof adapter[method] !== "function") return error(id, -32603, "Tool adapter unavailable");
    try {
      const data=await adapter[method](args, trustedContext);
      return result(id, {content:[{type:"text",text:JSON.stringify(data)}], isError:false});
    } catch (_) {
      // Server logs may contain more, but never leak SQL or secret details to tools.
      return result(id, {content:[{type:"text",text:"Request rejected or unavailable"}],isError:true});
    }
  };
}
