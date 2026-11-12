"""GPT-only synthetic multiring controls; not canonical Echo. Issue #434 preregistration."""
import json, math, random
SEEDS=(11,23,37,53)
def model(seed, mode="triad", gain=.04, uniform=0., hetero=0., shuffled=False, boundary=True):
    rng=random.Random(seed)
    ids=tuple(range(27))
    affinity=list(range(27))
    if shuffled: rng.shuffle(affinity)
    mass=[[1.+rng.random()*.2 for _ in ids] for _ in range(3)]
    phase=[[rng.random()*6.283185307179586 for _ in ids] for _ in range(3)]
    start=sum(map(sum,mass))
    for t in range(8):
        for r in range(3):
            for i in ids:
                phase[r][i]+=.07+uniform+hetero*((i%5)-2)/5
        for r in range(3):
            for i in ids:
                j=(i+1)%27
                angle=phase[r][j]-phase[r][i]
                if mode=="triad":
                    angle+=.3*math.sin(phase[(r+1)%3][i]-phase[r][i])
                weight=1.+.2*math.sin(affinity[i]*.17)
                radius=1.+(.1*math.sin(phase[r][i]) if boundary else 0.)
                delta=gain*weight*radius*math.sin(angle)
                delta=max(-mass[r][j]*.1,min(mass[r][i]*.1,delta))
                mass[r][i]-=delta; mass[r][j]+=delta
    return ids,mass,start
def l1(a,b):
    return sum(abs(x-y) for ar,br in zip(a,b) for x,y in zip(ar,br))
def evaluate(seed):
    ids,a,initial=model(seed)
    _,replay,_=model(seed)
    _,noop,_=model(seed,gain=0)
    _,noop2,_=model(seed,gain=0,mode="pair",shuffled=True)
    _,uniform,_=model(seed,uniform=.25)
    _,hetero,_=model(seed,hetero=.25)
    _,pair,_=model(seed,mode="pair")
    _,shuffle,_=model(seed,shuffled=True)
    _,boundary,_=model(seed,boundary=False)
    d={"replay":l1(a,replay),"unique_ids":len(set(ids)),
       "conservation":abs(sum(map(sum,a))-initial),
       "min_mass":min(map(min,a)),"noop":l1(noop,noop2),
       "uniform":l1(a,uniform),"hetero":l1(a,hetero),
       "triad_pair":l1(a,pair),"shuffle":l1(a,shuffle),
       "boundary":l1(a,boundary)}
    checks={"replay":d["replay"]<1e-12,"unique_ids":d["unique_ids"]==27,
       "conservation":d["conservation"]<1e-10,"nonnegative":d["min_mass"]>=0,
       "noop":d["noop"]<1e-12,"uniform":d["uniform"]<1e-10,
       "hetero":d["hetero"]>1e-6,"triad_pair":d["triad_pair"]>1e-6,
       "shuffle":d["shuffle"]>1e-6,"boundary":d["boundary"]>1e-6}
    return {"seed":seed,"measurements":d,"checks":checks}
if __name__=="__main__":
    results=[evaluate(s) for s in SEEDS]
    print(json.dumps({"issue":434,"seeds":SEEDS,"results":results,
      "passed":sum(sum(x["checks"].values()) for x in results),
      "total":40},indent=2,sort_keys=True))
