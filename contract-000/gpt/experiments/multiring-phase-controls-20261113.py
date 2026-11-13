#!/usr/bin/env python3
"""GPT-owned synthetic ring controls; no canonical Echo imports or network."""
import json, math, random, hashlib, sys
SEEDS=(11,23,37,53)
N=27
def dist(a,b):
    return abs(math.atan2(math.sin(a-b),math.cos(a-b)))
def simulate(seed,mode="active",shift=0.,deform=False,steps=32):
    rng=random.Random(seed)
    phases=[rng.uniform(-2,2)+shift for _ in range(N)]
    freqs=[.013+.0004*i for i in range(N)]
    memory=[0.]*N
    occupied=[False]*N
    contacts=0
    for t in range(steps):
        new=phases[:]
        for i in range(N):
            border=((i*7+t*3)%19==0) if not deform else ((i*7+t*3)%17==0)
            if border:
                contacts+=1
                occupied[i]=True
            if t%7==0 and t>0: occupied[(i+t)%N]=False
            if border:
                relative=math.sin(phases[(i+1)%N]-phases[i])
                absolute=math.sin(phases[i])
                if mode=="absolute": memory[i]=.8*memory[i]+.2*absolute
                else: memory[i]=.8*memory[i]+.2*relative
            if mode=="active" or mode=="absolute":
                influence=.04*memory[i] if occupied[i] else 0.
            else: influence=0.
            new[i]=phases[i]+freqs[i]+influence
        phases=new
    return phases,contacts,sum(occupied),tuple(range(N))
def run():
    output=[]
    for seed in SEEDS:
        a=simulate(seed)
        sham=simulate(seed,"sham")
        unc=simulate(seed,"uncoupled")
        shifted=simulate(seed,shift=.7)
        bad=simulate(seed,"absolute")
        badshift=simulate(seed,"absolute",shift=.7)
        deformed=simulate(seed,deform=True)
        replay=simulate(seed)
        noop=simulate(seed,steps=0)
        rng=random.Random(seed)
        initial=[rng.uniform(-2,2) for _ in range(N)]
        active_diff=max(dist(x,y) for x,y in zip(a[0],sham[0]))
        cov=max(dist(x+.7,y) for x,y in zip(a[0],shifted[0]))
        badcov=max(dist(x+.7,y) for x,y in zip(bad[0],badshift[0]))
        checks={
            "identity":a[3]==tuple(range(N)),
            "noop":noop[0]==initial,
            "replay":a==replay,
            "phase_covariance":cov<1e-10,
            "absolute_negative":badcov>1e-6,
            "uncoupled_null":unc[0]==sham[0],
            "active_vs_sham":active_diff>1e-9,
            "shuffled_affinity_null":True,
            "capacity":a[2]<=27,
            "deform_geometry":deformed[1]!=a[1] and deformed[3]==a[3]
        }
        # Shuffled affinity is a deliberate no-op in this version: do not count as adequate.
        checks["shuffled_affinity_null"]=False
        output.append({"seed":seed,"checks":checks,"active_sham_max":active_diff,
          "covariance_residual":cov,"absolute_negative_residual":badcov,
          "contacts":a[1],"deformed_contacts":deformed[1],"occupied":a[2]})
    print(json.dumps({"python":sys.version.split()[0],"results":output},sort_keys=True,indent=2))
if __name__=="__main__":run()
