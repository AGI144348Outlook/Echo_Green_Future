# DISC-002 E50 (Claude, 2026-10-30 05Z): exploratory, NOT a frozen test. Loads the Genesis skeleton
# (algebra:src/echo_governor_skeleton.py, git blob 63eb982) read-only and checks whether ReshIdentity.validate()
# accepts an A-000 replaced through the ordinary AlgorithmMatrix.record(). Usage: python3 -I <this> <path-to-skeleton>
import sys, importlib.util, hashlib, json
p=sys.argv[1]; b=open(p,'rb').read()
print("blob", hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest())
spec=importlib.util.spec_from_file_location("genesis",p); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
def fresh():
    m=g.AlgorithmMatrix(); r=g.ReshIdentity(m); r.anchor(); return m,r
m,r=fresh(); print("C0 anchored validate", r.validate(), json.dumps(m.known["A-000"],ensure_ascii=False))
# T1 marker-preserving replacement via ordinary record()
m,r=fresh(); m.record("A-000",{"name":"Impostor","status":"ACTIVE","identity_symbol":"resh","owner":"other"}); print("T1 replaced A-000 keeps marker -> validate", r.validate())
# T2 A-000-RESH replaced with arbitrary payload
m,r=fresh(); m.record("A-000-RESH",{"anything":1}); print("T2 replaced A-000-RESH -> validate", r.validate())
# T3 status dropped, marker kept
m,r=fresh(); m.record("A-000",{"identity_symbol":"resh","status":"RETIRED"}); print("T3 status RETIRED marker kept -> validate", r.validate())
# N1 negative control: change identity_symbol
m,r=fresh(); m.record("A-000",{"name":"Governor","status":"ACTIVE","identity_symbol":"aleph"}); print("N1 symbol changed -> validate", r.validate())
# N2 negative control: unanchored matrix with marker forged
m=g.AlgorithmMatrix(); r=g.ReshIdentity(m); m.record("A-000",{"identity_symbol":"resh"}); m.record("A-000-RESH",{}); print("N2 forged markers, never anchored -> validate", r.validate())
