# DISC-002 E51 (Claude, 2026-10-30 07Z): exploratory, NOT a frozen test. Loads the Genesis skeleton
# (genesis-documentary:src/echo_governor_skeleton.py, git blob 63eb982) read-only, in a scratch copy, and checks
# GPT 461/462 source claims about ReshIdentity.anchor()/validate() plus the PeCommunicator.open_exchanges re-anchor path.
# Usage: python3 -I <this> <path-to-skeleton>   (spawns 2 child processes for T3 with fixed PYTHONHASHSEED)
import sys, os, subprocess, importlib.util, hashlib, json, types
p=sys.argv[1]; b=open(p,'rb').read()
if len(sys.argv)>2 and sys.argv[2]=="T3child":
    spec=importlib.util.spec_from_file_location("genesis",p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    m=g.AlgorithmMatrix(); L=g.Lobby(m); L.agents["resh"]=g.WordAgent("resh",["head"],"TYPE","noun",m)
    g.ReshIdentity(m,L).anchor(); print(json.dumps(L.agents["resh"].definition_words)); sys.exit(0)
print("blob", hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest())
spec=importlib.util.spec_from_file_location("genesis",p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
def lobby_with(dw):
    m=g.AlgorithmMatrix(); L=g.Lobby(m)
    if dw is not ...: L.agents["resh"]=g.WordAgent("resh",dw,"TYPE","noun",m)
    return m,L
# T1 (GPT 462 N27 shape): malformed definition_words -> anchor raises after A-000/alias writes
m,L=lobby_with(None); r=g.ReshIdentity(m,L)
try: r.anchor(); err=None
except Exception as e: err=type(e).__name__
print("T1 anchor raised:", err, "| _anchored", r._anchored, "| validate", r.validate(),
      "| A-000.identity_symbol", m.known["A-000"].get("identity_symbol"), "| A-000-RESH present", "A-000-RESH" in m.known)
r2=g.ReshIdentity(m,L); print("T1b second ReshIdentity on same matrix, never anchored -> validate", r2.validate())
# T2 (GPT 461): _anchor_entry is the same dict object as the alias in known
m,L=lobby_with(["head"]); r=g.ReshIdentity(m,L); r.anchor()
same = r._anchor_entry is m.known["A-000-RESH"]; m.known["A-000-RESH"]["status"]="RETIRED"
print("T2 _anchor_entry is alias dict:", same, "| in-place edit seen through _anchor_entry:", r._anchor_entry["status"], "| validate", r.validate())
# T3 (GPT 461): definition_words order under two hash seeds
outs=[]
for seed in ("1","2"):
    env=dict(os.environ, PYTHONHASHSEED=seed)
    outs.append(json.loads(subprocess.run([sys.executable,"-I",__file__,p,"T3child"],env=env,capture_output=True,text=True,check=True).stdout))
print("T3 seed1", outs[0]); print("T3 seed2", outs[1]); print("T3 same list:", outs[0]==outs[1], "| same set:", set(outs[0])==set(outs[1]))
# T4 (GPT 461 N25 shape): Lobby configured but no resh agent -> anchored and valid, projection never checked
m,L=lobby_with(...); r=g.ReshIdentity(m,L); r.anchor(); print("T4 lobby without resh agent -> _anchored", r._anchored, "validate", r.validate())
# T5 (new): PeCommunicator.open_exchanges re-anchors when validate() is False (stub ayin returns no entities)
m,L=lobby_with(["head"]); r=g.ReshIdentity(m,L); r.anchor()
m.record("A-000",{"name":"Governor","status":"ACTIVE","identity_symbol":"aleph","owner":"other"})
print("T5 before: validate", r.validate(), json.dumps(m.known["A-000"],ensure_ascii=False))
ayin=types.SimpleNamespace(agentive_entities=lambda **k: [])
pe=g.PeCommunicator(m,L,r,ayin); out=pe.open_exchanges()
print("T5 after open_exchanges -> returned", out, "| validate", r.validate(), json.dumps(m.known["A-000"],ensure_ascii=False))
