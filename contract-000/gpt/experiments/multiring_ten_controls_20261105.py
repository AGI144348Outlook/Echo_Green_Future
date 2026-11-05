#!/usr/bin/env python3
"""GPT-only synthetic multiring controls. No canonical Echo imports."""
import json, random, math
SEED=20261105
GLYPHS=list("אבגדהוזחטיכלמנסעפצקרשת")+list("ךםןףץ")
VALUES=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90]
def project(i): return (i%3,(i//3)%3,i//9)
def select(n,seed=SEED): return [GLYPHS[i] for i in random.Random(seed).sample(range(27),n)]
def affinity(a,b): return int(max(a,b)%min(a,b)==0)
def update(x,values=VALUES,coupling=1):
    return [round((v+coupling*sum(affinity(values[i],values[j])*x[j] for j in range(len(x)) if i!=j)/len(x)),8) for i,v in enumerate(x)]
def deformation(phase): return 1+0.2*math.sin(phase)
def run():
    x=[(i+1)/27 for i in range(27)]
    shuffled=VALUES[:]; random.Random(SEED).shuffle(shuffled)
    a=update(x); b=update(x,shuffled)
    checks={
      "T01_unique_glyphs":len(GLYPHS)==27 and len(set(GLYPHS))==27,
      "T02_projection_bijection":len({project(i) for i in range(27)})==27,
      "T03_two_ring":len(select(2))==2,
      "T04_three_ring":len(select(3))==3,
      "T05_four_ring":len(select(4))==4,
      "T06_seed_replay":select(4)==select(4),
      "T07_noop":update(x,coupling=0)==[round(v,8) for v in x],
      "T08_shuffled_numeric_contrast":a!=b,
      "T09_intervention_effect":update([x[0]+1]+x[1:])!=a,
      "T10_deformation_bounds":all(0.8-1e-9<=deformation(k/10)<=1.2+1e-9 for k in range(100))
    }
    return {"seed":SEED,"checks":checks,"pass_count":sum(checks.values()),"total":len(checks),"affinity_3_9":affinity(3,9),"affinity_2_3":affinity(2,3),"coupled_delta_l1":round(sum(abs(u-v) for u,v in zip(a,x)),6),"shuffled_delta_l1":round(sum(abs(u-v) for u,v in zip(a,b)),6),"limits":"synthetic numerical topology, not semantic learning"}
if __name__=="__main__": print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
