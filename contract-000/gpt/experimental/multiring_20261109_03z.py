"""GPT-only bounded toy multiring experiment. No canonical Echo dependency."""
import hashlib, json, math, random
SEEDS=(3301,3302,3303,3304)
GLYPHS=tuple("אבגדהוזחטיכלמנסעפצקרשת")+("ך","ם","ן","ף","ץ")
assert len(GLYPHS)==27
def compose(indices): return "".join(GLYPHS[i] for i in indices)
def project(indices): return [((i//9),(i//3)%3,i%3) for i in indices]
def digest(core): return hashlib.sha256(json.dumps(core,sort_keys=True).encode()).hexdigest()
def signal(x,neighbor,phase=0.,freq=1.,affinity=1.,boundary=1.,coupled=True):
    return x + (0.08*neighbor*math.cos(phase*freq)*affinity*boundary if coupled else 0.)
def frozen_target(seed):
    r=random.Random(seed+910000)
    return [(r.random()-.5)*.7 for _ in range(27)]
def run(seed):
    rng=random.Random(seed)
    ids=list(range(27));rng.shuffle(ids)
    values=[rng.uniform(-1,1) for _ in range(27)]
    results={}
    results["T1_two_ring_order"]=compose(ids[:2])==GLYPHS[ids[0]]+GLYPHS[ids[1]]
    results["T2_three_ring_order"]=compose(ids[:3])==GLYPHS[ids[0]]+GLYPHS[ids[1]]+GLYPHS[ids[2]]
    coords=project(ids)
    results["T3_projection_bijection"]=len(set(coords))==27 and all(0<=v<3 for p in coords for v in p)
    core={"id":"A-000","version":1};shell={"status":"draft"}
    before=digest(core);shell["status"]="mutated"
    results["T4_core_shell_separation"]=digest(core)==before and digest({**core,**shell})!=before
    x,n=.2,.4
    results["T5_neighbor_effect"]=abs((signal(x,n+.4)-signal(x,n))-.032)<1e-10
    results["T6_distant_null"]=signal(x,n)==signal(x,n) and signal(x,n,coupled=False)==signal(x,n+.4,coupled=False)
    results["T7_affinity_shuffle_effect"]=abs(signal(x,n,affinity=1.2)-signal(x,n,affinity=.8))>1e-6
    results["T8_phase_reversal"]=abs(signal(x,n,phase=0)-signal(x,n,phase=math.pi))>.05
    results["T9_frequency_detuning"]=abs(signal(x,n,phase=1,freq=1)-signal(x,n,phase=1,freq=2))>.02
    results["T10_boundary_response"]=abs(signal(x,n,boundary=.4)-signal(x,n,boundary=1))>.01
    target=frozen_target(seed)
    aff=[1+.1*((i%5)-2) for i in range(27)]
    sh=aff[:];random.Random(seed+1).shuffle(sh)
    pred={
      "coupled":[signal(values[i],values[(i-1)%27],phase=.3,affinity=aff[i]) for i in range(27)],
      "shuffled":[signal(values[i],values[(i-1)%27],phase=.3,affinity=sh[i]) for i in range(27)],
      "uncoupled":[signal(values[i],values[(i-1)%27],coupled=False) for i in range(27)],
      "no_op":[values[i] for i in range(27)],
      "zero":[0. for _ in range(27)]
    }
    mse={k:sum((v-target[i])**2 for i,v in enumerate(arr))/27 for k,arr in pred.items()}
    return {"seed":seed,"checks":results,"mse":mse}
if __name__=="__main__":
    print(json.dumps({"schema":"gpt-multiring-v1","results":[run(s) for s in SEEDS]},sort_keys=True))
