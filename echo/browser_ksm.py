"""Browser-live KSM Recess adapter. Pure stdlib; canonical Registry only."""
import json
from echo.kernel import skeleton as K
from echo.matrix.registry import Registry
from echo.canvas.ks_recess import KSRecess

reg=Registry(); km=K.AlgorithmMatrix()
for w,e in reg.canonical.items(): km.index_dictionary_entry(w,e["def"],pos="noun",category="registry")
lobby=K.Lobby(km); lobby.populate(); lobby.run_orientation(); lobby.matrix=km
raw=lobby.compute_generality_scores() or {}
gscore={w:raw.get(w,0.0) for w in reg.canonical}

def relate(a,b):
    d=reg.ancestors(a).get(b)
    if d:return ("is_a",d)
    d=reg.ancestors(b).get(a)
    if d:return ("includes",d)
    return None
def speak(u,kind,v):
    r=relate(u,v)
    if not r or r[0]!=kind:return None
    text=f"{u.capitalize()} {'is a' if kind=='is_a' else 'includes'} {v}."
    return {"english":text,"emel":f"{u} {kind} {v}","audits":"registry semantic: PASS"}
def define(w): return reg.resolve(w)["def"]

rec=KSRecess(K,lobby,gscore,relate,speak,define)
started=False

def _turn():
    rec.turn+=1
    arm=rec.matrix.bandit_select("canvas",["INTRODUCE","ALIGN","CONTAIN","MANIFOLD"])
    ops=[]; say=[]
    ok,why=getattr(rec,arm.lower())(ops,say)
    rec.matrix.record_outcome(arm,"canvas",ok)
    return {"turn":rec.turn,"arm":arm,"ok":ok,"reason":why,"ops":ops,"say":say}

def boot():
    global started
    if not started:
        ops=[]; rec.presentiate(ops,"entity",600,"canonical Registry root")
        started=True
        return json.dumps({"status":"ready","words":reg.all_words(),"ops":ops,
          "echo":{"arm":"START","reason":"KSM Recess initialized from the canonical Registry."}})
    return json.dumps({"status":"ready","words":reg.all_words(),"ops":[]})

def presentiate(word):
    global started
    if not started: json.loads(boot())
    w=reg.key(word)
    if not reg.has(w):
        return json.dumps({"ok":False,"gap":reg.resolve(w),"ops":[],"echo":{"arm":"GAP","reason":f"'{w}' is not yet indexed; Echo will not invent its meaning."}})
    if w in rec.planes:
        return json.dumps({"ok":True,"ops":[],"echo":{"arm":"IDENTIFY","reason":f"{w} is already present on the KSM Canvas."}})
    ops=[]; rec.turn+=1; rec.presentiate(ops,w,600,f"Tim presentiated canonical resident {w}")
    live=_turn()
    return json.dumps({"ok":True,"ops":ops+live["ops"],"echo":live,"resident":reg.resolve(w)})

def turn():
    global started
    if not started: json.loads(boot())
    return json.dumps({"ok":True,"ops":_turn()["ops"],"echo":_turn()})
