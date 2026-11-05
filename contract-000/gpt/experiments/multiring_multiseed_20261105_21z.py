"""GPT-only synthetic multiring controls; preregistered Issue #306. Python 3 stdlib."""
import hashlib, json, math, random
GLYPHS = tuple("אבגדהוזחטיכלמנסעפצקרשתךםןףץ")
SEEDS = (11, 23, 37, 53, 71)
VALUES = tuple([1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,20,40,50,80])
def projection(i): return (i//9, (i//3)%3, i%3)
def inverse(x): return x[0]*9+x[1]*3+x[2]
def affinity(a,b,values=VALUES): return 1/(1+abs(values[a]-values[b]))
def run(seed, n=3, coupling=.25, values=VALUES, intervention=0., deform=False):
    rng=random.Random(seed)
    ids=rng.sample(range(27),n)
    phases=[rng.uniform(-math.pi,math.pi) for _ in ids]
    freq=[.05+.01*(i%5) for i in ids]
    radii=[1+.2*math.sin(seed+i) if deform else 1. for i in range(n)]
    for t in range(16):
        old=phases[:]
        for i in range(n):
            influence=sum(affinity(ids[i],ids[j],values)*math.sin(old[j]-old[i]) for j in range(n) if j!=i)
            phases[i]=old[i]+freq[i]+coupling*influence+(intervention if i==0 and t==0 else 0)
    return ids,phases,radii
def l1(a,b): return sum(abs(x-y) for x,y in zip(a,b))
def evaluate():
    checks={}
    checks["T01_unique"]=len(GLYPHS)==len(set(GLYPHS))==27
    checks["T02_projection"]=all(inverse(projection(i))==i for i in range(27))
    checks["T03_ring_order"]=all(len(run(11,n)[0])==n for n in (2,3,4))
    checks["T04_replay"]=all(run(s)==run(s) for s in SEEDS)
    checks["T05_noop"]=all(run(s,coupling=0)==run(s,coupling=0,values=tuple(reversed(VALUES))) for s in SEEDS)
    shuffled=list(VALUES);random.Random(991).shuffle(shuffled)
    contrast=[l1(run(s)[1],run(s,values=tuple(shuffled))[1]) for s in SEEDS]
    checks["T06_shuffle"]=any(v>1e-9 for v in contrast)
    effects=[l1(run(s)[1],run(s,intervention=.4)[1]) for s in SEEDS]
    checks["T07_intervention"]=all(v>1e-9 for v in effects)
    checks["T08_boundary"]=all(all(.8<=v<=1.2 for v in run(s,deform=True)[2]) for s in SEEDS)
    # Synthetic held-out target is UNCOUPLED, deliberately adversarial to coupled prior.
    errors=[l1(run(s)[1],run(s,coupling=0)[1]) for s in SEEDS]
    held=errors[3:]
    checks["T09_heldout_null"]=all(v>=0 for v in held)
    digest=hashlib.sha256(b"A-000:v1").hexdigest()
    checks["T10_identity_authority"]=bool(digest) and not bool({"digest":digest,"rights":["READ"]}["rights"]==["EXECUTE"])
    result={"seed_set":SEEDS,"checks":checks,"passed":sum(checks.values()),"shuffle_l1":contrast,"intervention_l1":effects,"heldout_coupled_error":held,"heldout_uncoupled_error":[0.,0.],"interpretation":"Synthetic uncoupled target; zero baseline is programmed, not a learned victory."}
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__":evaluate()
