# DISC-002 01Z exploratory check (Claude, 2026-11-08). NOT pre-registered; not part of E115. Run: python3 -I -B this.py <dir holding unmodified echo_governor_skeleton.py blob 63eb982>
import sys, types; sys.path.insert(0, sys.argv[1])
import echo_governor_skeleton as g
class M: pass
# case A: A-000 absent before anchor
m=M(); m.known={}
r=g.ReshIdentity(m); r.anchor()
print("A absent-before: validate=",r.validate(),"A-000 keys=",sorted(m.known["A-000"]))
# case B: alias entry replaced by arbitrary value after anchor
m=M(); m.known={"A-000":{"name":"Governor","status":"ACTIVE"}}
r=g.ReshIdentity(m); r.anchor(); m.known["A-000-RESH"]="x"
print("B alias replaced by 'x': validate=",r.validate())
# case C: A-000 replaced wholesale with only identity_symbol
m.known["A-000"]={"identity_symbol":"resh"}
print("C A-000 replaced {identity_symbol}: validate=",r.validate())
# case D: real AlgorithmMatrix
try:
    am=g.AlgorithmMatrix(); before=am.known["A-000"]; r=g.ReshIdentity(am); r.anchor()
    print("D real matrix: same dict object mutated in place =", am.known["A-000"] is before, "validate=",r.validate())
except Exception as e: print("D error",type(e).__name__,e)
