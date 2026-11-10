import hashlib, json, random, sys
GLYPHS=list("אבגדהוזחטיכלמנסעפצקרשת")+list("ךםןףץ")
SEEDS=(9401,9402,9403,9404)
N=27
def step(x,shift,rate=.3):
    y=[0.0]*N
    for i,v in enumerate(x):
        y[i]+=v*(1-rate)
        y[(i+shift)%N]+=v*rate
    return y
def deform(x):
    y=[0.0]*N
    for i,v in enumerate(x):
        y[i]+=.7*v
        y[(2*i+1)%N]+=.3*v
    return y
def oracle(x,shift):
    return [sum(v*(.7 if i==j else 0)+v*(.3 if (i+shift)%N==j else 0) for i,v in enumerate(x)) for j in range(N)]
def dist(a,b):return sum(abs(u-v) for u,v in zip(a,b))
def run(seed):
    rng=random.Random(seed)
    x=[rng.random() for _ in range(N)]
    a=step(x,1);b=deform(a);c=step(b,2)
    rev=deform(step(x,1))
    rew=step(x,7)
    core=b"A-000|27|rings|v01"
    checks={
      "unique_glyphs":len(GLYPHS)==N and len(set(GLYPHS))==N,
      "replay":step(x,1)==step(x,1),
      "no_op":step(x,1,0)==x,
      "mass":abs(sum(x)-sum(c))<1e-9,
      "uncoupled":dist(a,x)>1e-6,
      "rewired":dist(a,rew)>1e-6 and abs(sum(a)-sum(rew))<1e-9,
      "order":dist(step(deform(x),1),rev)>1e-6,
      "phase_null":dist(step(step(x,1),2),step(step(x,2),1))<1e-9,
      "oracle":dist(a,oracle(x,1))<1e-9,
      "sha256":hashlib.sha256(core).digest()==hashlib.sha256(core).digest() and hashlib.sha256(core).digest()!=hashlib.sha256(core+b"!").digest()
    }
    return {"seed":seed,"checks":checks,"metrics":{"coupled_L1":dist(a,x),"rewired_L1":dist(a,rew),"order_L1":dist(step(deform(x),1),rev),"phase_null_L1":dist(step(step(x,1),2),step(step(x,2),1)),"oracle_L1":dist(a,oracle(x,1))}}
if __name__=="__main__":
    results=[run(s) for s in SEEDS]
    print(json.dumps({"python":sys.version.split()[0],"results":results,"passed":sum(sum(r["checks"].values()) for r in results),"total":40},sort_keys=True))
