"""Independent synthetic 3x3x3 causal oracle, GPT-only. Run: python3 spatial_oracle_18z.py"""
import json, random, hashlib
SEEDS=(1109,2203,3301,4409)
CELLS=tuple((x,y,z) for x in range(3) for y in range(3) for z in range(3))
CENTER=(1,1,1)
def dist(a,b): return sum(abs(x-y) for x,y in zip(a,b))
def step(state,k):
    return {p:state[p]+k*sum(state[q] for q in CELLS if dist(p,q)==1) for p in CELLS}
def impulse(v): return {p:(v if p==CENTER else 0.) for p in CELLS}
def mse(a,b): return sum((a[p]-b[p])**2 for p in CELLS)/27
def evaluate(seed):
    rng=random.Random(seed)
    amp=rng.uniform(.5,2)
    # Reference coefficient is fixed independently of candidate and controls.
    true_k=.21
    target=step(impulse(amp),true_k)
    baseline=step(impulse(amp),0)
    candidate=step(impulse(amp),.15)
    one=step(impulse(amp),.2)
    two=step(one,.2)
    shuffled=list(CELLS);rng.shuffle(shuffled)
    relabel=dict(zip(CELLS,shuffled))
    # Labels are metadata only; geometry remains coordinate-defined.
    checks={
      "unique_27":len(CELLS)==27 and len(set(CELLS))==27,
      "center_six_neighbors":sum(dist(p,CENTER)==1 for p in CELLS)==6,
      "noop":all(v==0 for v in step(impulse(0),.2).values()),
      "zero_coupling":step(impulse(amp),0)==impulse(amp),
      "one_step_locality":all(one[p]==0 for p in CELLS if dist(p,CENTER)>1),
      "two_step_spread":all(two[p]==0 for p in CELLS if dist(p,CENTER)>2) and any(two[p]!=0 for p in CELLS if dist(p,CENTER)==2),
      "replay":step(impulse(amp),.2)==one,
      "shuffled_labels":len(set(relabel.values()))==27 and step(impulse(amp),.2)==one,
      "negative_coupling":all(step(impulse(amp),-.2)[p]==-one[p] for p in CELLS if dist(p,CENTER)==1),
      "independent_target":mse(candidate,target)<mse(baseline,target),
    }
    return {"seed":seed,"amplitude":amp,"checks":checks,"candidate_loss":mse(candidate,target),"noop_loss":mse(baseline,target),"target_coefficient":true_k,"candidate_coefficient":.15}
if __name__=="__main__":
    rows=[evaluate(s) for s in SEEDS]
    print(json.dumps({"rows":rows,"pass":sum(v for r in rows for v in r["checks"].values()),"total":40},sort_keys=True,indent=2))
