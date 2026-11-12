"""Echo-018: two distinct communication boundaries and a small algorithmic Echo runtime.

Human -> inbox (Vercel); Echo runtime (Render) -> MCP Memory OS -> Neon.
Only the Echo runtime may publish outbox records. No canned dialogue.
The experimental agent uses full NLTK WordNet and existing evidence relationships;
it is NOT the complete Governor/3³ neural wave system.
"""
import json
import os
import re
import hmac
import hashlib
import time
import threading
from dataclasses import dataclass

import requests
import psycopg
from psycopg.rows import dict_row
from flask import Flask, request, jsonify
from nltk.corpus import wordnet as wn

app = Flask(__name__)
PORT = int(os.environ.get("PORT", "10000"))
TOKEN = os.environ.get("ECHO_BRIDGE_TOKEN", "")
CONTACT_DATABASE = os.environ.get("ECHO_CONTACT_DATABASE_URL", "")
MIND_DATABASE = os.environ.get("ECHO_MIND_DATABASE_URL", "")
MODEL_ID = "echo-memory-transport-only"
WORKER_ID = os.environ.get("RENDER_SERVICE_ID", "render-echo-018")
HTTP = requests.Session()

def connect(url):
    if not url:
        raise RuntimeError("Required Neon database connection is not configured")
    return psycopg.connect(url, row_factory=dict_row, connect_timeout=12)

def bearer_ok():
    auth = request.headers.get("Authorization", "")
    provided = auth[7:] if auth.startswith("Bearer ") else ""
    return bool(TOKEN and provided and hmac.compare_digest(TOKEN, provided))

def json_error(message, status=400):
    return jsonify({"error": message}), status

MEMORY_TOOLS = [
    {"name":"dictionary.senses", "description":"Explore the full Princeton WordNet dictionary: definitions, senses, synonyms and semantic ancestry. No fixed word list.", "required":["word"]},
    {"name":"evidence.search", "description":"Discover Echo's live Neon evidence nodes by word or concept.", "required":["term"]},
    {"name":"evidence.trace", "description":"Explore typed evidence links to and from a selected source node.", "required":["node_id"]},
    {"name":"evidence.node.propose", "description":"Record a provisional evidence concept or observation, source attributed.", "required":["node_id","label","source_ref"]},
    {"name":"evidence.edge.propose", "description":"Propose a sourced, typed, provisional evidence link. Never promote facts.", "required":["edge_id","source_node","target_node","relation","source_ref"]},
    {"name":"catalog.card.get", "description":"Read exact revisioned catalog-box card with attribution.", "required":["card_id","revision"]},
    {"name":"catalog.card.propose", "description":"Create a new source-provenance-backed proposed lexical-context card.", "required":["card_id","title","body","source_ref"]},
    {"name":"mind.domains", "description":"Inspect the existing Echo Mind Domains in Neon.", "required":[]},
    {"name":"mind.box.get", "description":"Read a memory box using its persistent identifier.", "required":["box_id"]},
    {"name":"mind.box.put", "description":"Create a memory box holding a source-attributed observation; not a verified fact.", "required":["payload","provenance"]},
    {"name":"mind.tie.link", "description":"Make a directed, typed memory tie between existing boxes.", "required":["from_box","to_box","relation"]}
]

def memory_call(name, args):
    if name not in {t["name"] for t in MEMORY_TOOLS}:
        raise ValueError("Tool not discoverable")
    expected = next(t["required"] for t in MEMORY_TOOLS if t["name"] == name)
    if not isinstance(args, dict) or any(k not in args for k in expected):
        raise ValueError("Missing MCP tool arguments")
    if name == "dictionary.senses":
        word = str(args["word"]).strip().lower().replace(" ", "_")
        senses = wn.synsets(word)
        return {"word": word, "senses": [
            {"id":s.name(), "pos":s.pos(), "definition":s.definition(),
             "lemmas":[l.name() for l in s.lemmas()],
             "hypernyms":[h.name() for h in s.hypernyms()],
             "examples":list(s.examples())} for s in senses
        ], "source":"Princeton WordNet via NLTK", "admitted_new_words":0}
    if name.startswith("mind."):
        with connect(MIND_DATABASE) as con, con.cursor() as cur:
            if name == "mind.domains":
                cur.execute("SELECT domain_id,domain_key,label,domain_kind FROM echo_warehouse.mind_domains ORDER BY domain_id")
                return {"domains":cur.fetchall()}
            if name == "mind.box.get":
                cur.execute("SELECT box_id,generation,payload,provenance,accessibility,status FROM echo_warehouse.boxes WHERE box_id=%s",(int(args["box_id"]),))
                return {"box":cur.fetchone()}
            if name == "mind.box.put":
                payload = args["payload"]
                if not isinstance(payload,dict): raise ValueError("Memory payload must be object")
                source = str(args["provenance"])[:512]
                cur.execute("SELECT nextval('echo_warehouse.echo_contact_box_seq') AS id")
                num = cur.fetchone()["id"]
                cur.execute("INSERT INTO echo_warehouse.boxes(box_id,generation,payload,provenance) VALUES(%s,0,%s::jsonb,%s) RETURNING box_id",(num,json.dumps(payload),source))
                return {"box_id":cur.fetchone()["box_id"],"status":"observed_memory_not_verified_fact"}
            if name == "mind.tie.link":
                left,right=int(args["from_box"]),int(args["to_box"])
                if left == right: raise ValueError("Memory tie requires distinct boxes")
                rel = args["relation"]
                if not isinstance(rel,dict): raise ValueError("Relation must be object")
                cur.execute("SELECT nextval('echo_warehouse.echo_contact_tie_seq') AS id")
                eid=cur.fetchone()["id"]
                cur.execute("INSERT INTO echo_warehouse.ties(tie_id,from_box,to_box,relation) VALUES (%s,%s,%s,%s::jsonb) RETURNING tie_id",(eid,left,right,json.dumps(rel)))
                return {"tie_id":cur.fetchone()["tie_id"],"status":"memory_tie_created"}
    with connect(CONTACT_DATABASE) as con, con.cursor() as cur:
        if name == "evidence.search":
            term=str(args["term"])[:150].lower()
            cur.execute("SELECT node_id,node_kind,label,evidence_state FROM evidence_net.nodes WHERE lower(label) LIKE %s ORDER BY CASE WHEN lower(label)=%s THEN 0 ELSE 1 END,label LIMIT 30",("%"+term+"%",term))
            return {"nodes":cur.fetchall()}
        if name == "evidence.trace":
            node=str(args["node_id"])[:200]
            cur.execute("SELECT e.edge_id,e.source_node,e.target_node,e.relation_type,e.evidence_state,n.label AS target_label FROM evidence_net.edges e LEFT JOIN evidence_net.nodes n ON n.node_id=CASE WHEN e.source_node=%s THEN e.target_node ELSE e.source_node END WHERE e.source_node=%s OR e.target_node=%s ORDER BY e.edge_id LIMIT 80",(node,node,node))
            return {"edges":cur.fetchall()}
        if name == "evidence.node.propose":
            node=str(args["node_id"])[:160]
            cur.execute("INSERT INTO evidence_net.nodes(node_id,node_kind,label,details,attribution_ref,evidence_state) VALUES(%s,'observation',%s,%s::jsonb,%s,'provisional') ON CONFLICT DO NOTHING RETURNING node_id",(node,str(args["label"])[:200],json.dumps(args.get("details") or {}),str(args["source_ref"])[:500]))
            saved=cur.fetchone()
            return {"node_id":node,"created":bool(saved),"evidence_state":"provisional"}
        if name == "evidence.edge.propose":
            edge=str(args["edge_id"])[:160]
            cur.execute("INSERT INTO evidence_net.edges(edge_id,source_node,target_node,relation_type,relation_domain,evidence_state,source_ref) VALUES(%s,%s,%s,%s,'lexical','proposed',%s) ON CONFLICT DO NOTHING RETURNING edge_id",(edge,str(args["source_node"])[:200],str(args["target_node"])[:200],str(args["relation"])[:80],str(args["source_ref"])[:500]))
            saved=cur.fetchone()
            return {"edge_id":edge,"created":bool(saved),"evidence_state":"proposed"}
        if name == "catalog.card.get":
            cur.execute("SELECT card_id,revision,card_kind,title,body,provenance,review_state FROM card_protocol.card_revisions WHERE card_id=%s AND revision=%s",(str(args["card_id"]),int(args["revision"])))
            return {"card":cur.fetchone()}
        if name == "catalog.card.propose":
            card=str(args["card_id"])[:128]
            body=args["body"]
            if not isinstance(body,dict):raise ValueError("Card body must be object")
            cur.execute("INSERT INTO card_protocol.card_revisions(card_id,revision,card_kind,title,body,provenance,review_state) VALUES(%s,1,'lexical_context',%s,%s::jsonb,%s::jsonb,'proposed') ON CONFLICT DO NOTHING RETURNING card_id",(card,str(args["title"])[:200],json.dumps(body),json.dumps({"source":str(args["source_ref"]),"agent":MODEL_ID})))
            saved=cur.fetchone()
            return {"card_id":card,"revision":1,"created":bool(saved),"review_state":"proposed"}
    raise ValueError("Tool not implemented")

def mcp_request(payload):
    mid=payload.get("id")
    method=payload.get("method")
    if method=="initialize":
        return {"jsonrpc":"2.0","id":mid,"result":{"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"serverInfo":{"name":"echo-memory-os","version":"0.1.0"}}}
    if method=="tools/list":
        tools=[{"name":t["name"],"description":t["description"],"inputSchema":{"type":"object","properties":{k:{"type":"string"} for k in t["required"]},"required":t["required"]}} for t in MEMORY_TOOLS]
        return {"jsonrpc":"2.0","id":mid,"result":{"tools":tools}}
    if method=="tools/call":
        params=payload.get("params") or {}
        try:
            outcome=memory_call(params.get("name"),params.get("arguments") or {})
            return {"jsonrpc":"2.0","id":mid,"result":{"content":[{"type":"text","text":json.dumps(outcome,default=str)}]}}
        except Exception as err:
            app.logger.exception("echo_memory_tool_failed")
            return {"jsonrpc":"2.0","id":mid,"result":{"content":[{"type":"text","text":json.dumps({"error":type(err).__name__})}],"isError":True}}
    return {"jsonrpc":"2.0","id":mid,"error":{"code":-32601,"message":"method not found"}}

@app.post("/mcp/memory")
def memory_interface():
    if not bearer_ok(): return json_error("unauthorized",401)
    data=request.get_json(silent=True)
    if not isinstance(data,dict):return json_error("invalid JSON RPC")
    return jsonify(mcp_request(data))

def echo_tool(name,args):
    # The Echo runtime explicitly calls its distinct MCP interface over HTTP.
    url=f"http://127.0.0.1:{PORT}/mcp/memory"
    reply=HTTP.post(url,json={"jsonrpc":"2.0","id":int(time.monotonic_ns()%100000000),"method":"tools/call","params":{"name":name,"arguments":args}},headers={"Authorization":"Bearer "+TOKEN},timeout=25)
    reply.raise_for_status()
    data=reply.json()
    if data.get("result",{}).get("isError"):raise RuntimeError("Memory MCP tool returned error")
    return json.loads(data["result"]["content"][0]["text"])

# Echo-only communication boundary. A hosting adapter is not a speaker.
# The initial heuristic lexical composer was removed: the site and Render may
# not impersonate Echo before his actual autonomous Governor is connected.
@app.post("/echo/process")
def echo_process():
    if not bearer_ok():
        return json_error("unauthorized", 401)
    return jsonify({"status": "echo_runtime_not_connected",
                    "message": "No surrogate response is permitted; input remains pending.",
                    "outbox_written": False,
                    "runtime_required": "Echo autonomous algorithmic agent"}), 503

@app.get("/health")
def health():
    return jsonify({"service":"echo-018-runtime","status":"running","interfaces":{"human":"Vercel inbox / separate","memory":"POST /mcp/memory"},"scripted_dialogue":False,"full_governor_integrated":False,"may_speak_as_echo":False})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=PORT,threaded=True)
