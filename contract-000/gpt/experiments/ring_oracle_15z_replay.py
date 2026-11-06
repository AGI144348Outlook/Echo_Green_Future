# GPT-only Issue #326 synthetic ring and queue diagnostic, Python 3 stdlib.
# Prospective tests posted before local execution. Reproduction requires the full
# local runner; this committed source is a minimal independent replay subset.
import random, json
SEEDS=(1106,1116,1124)
def grants(seed):
    rng=random.Random(seed)
    return [t for t in range(270) if rng.random()<0.57]
def queue(seed):
    pending=[]; ledger=[]; occupied=[0]*27; arrivals=grants(seed)
    for t in range(280):
        pending += [(j,a) for j,a in enumerate(arrivals) if a==t]
        for j,a in pending[:]:
            if t-a>=9:
                ledger.append(("expire",j,a,t)); pending.remove((j,a))
        for j,a in pending[:]:
            seat=j*7%27
            if occupied[seat]<=t:
                occupied[seat]=t+3;ledger.append(("accept",j,a,t));pending.remove((j,a));break
    return ledger
def ring(seed,k,coupled):
    phase=[(seed+i*7)%27 for i in range(k)]; speeds=[1,2,3,5][:k];out=[]
    for t in range(270):
        old=phase[:]
        phase=[(old[i]+speeds[i]+(int((old[(i-1)%k]-old[i])%27<9) if coupled else 0))%27 for i in range(k)]
        out.append(phase[0])
    return out
def loss(x,seed):
    return sum(min(abs(a-(seed*3+t*11)%27),27-abs(a-(seed*3+t*11)%27)) for t,a in enumerate(x))/len(x)
if __name__=="__main__":
    print(json.dumps({"seeds":{s:{"grants":len(grants(s)),"accepted":sum(x[0]=="accept" for x in queue(s))} for s in SEEDS},"loss":{m:loss(ring(1106,3,m=="coupled"),1106) for m in ("coupled","uncoupled")}},sort_keys=True))
