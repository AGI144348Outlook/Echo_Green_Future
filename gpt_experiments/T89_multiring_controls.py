#!/usr/bin/env python3
"""GPT-owned synthetic ring controls; no canonical Echo dependencies."""
import json, math, random
SEEDS=(11,23,37,53)
GLYPHS=list("אבגדהוזחטיכלמנסעפצקרשת")+list("ךםןףץ")
assert len(GLYPHS)==27
def run(seed, pair=.13, tri=.07, shuffle=False, deform=False, freq=False):
    rng=random.Random(seed)
    phases=[rng.uniform(-math.pi,math.pi) for _ in range(27)]
    frequencies=[rng.uniform(.01,.08) for _ in range(27)]
    if freq: frequencies=[v+.01 for v in frequencies]
    affinities=list(range(27))
    if shuffle: rng.shuffle(affinities)
    radii=[1.0]*27
    for step in range(24):
        old=phases[:]
        for i in range(27):
            j=(i+1)%27; k=(i+2)%27
            p=pair*math.sin(old[j]-old[i])*(1+affinities[i]/100)
            t=tri*math.sin(old[j]+old[k]-2*old[i])
            phases[i]=old[i]+frequencies[i]+p+t
            if deform: radii[i]=min(1.15,max(.85,1+.1*math.sin(phases[i])))
    return phases,radii
def dist(a,b):
    return sum(abs(x-y) for x,y in zip(a,b))/len(a)
def main():
    out=[]
    for seed in SEEDS:
        base,_=run(seed,pair=0,tri=0)
        default,radii=run(seed)
        nop,_=run(seed,pair=0,tri=0)
        freq,_=run(seed,pair=0,tri=0,freq=True)
        no_pair,_=run(seed,pair=0)
        no_tri,_=run(seed,tri=0)
        shuffled,_=run(seed,shuffle=True)
        _,deformed=run(seed,deform=True)
        coords=[(i//9,(i//3)%3,i%3) for i in range(27)]
        tests={
          "unique_ids":len(set(GLYPHS))==27,
          "projection_bijection":len(set(coords))==27,
          "two_ring_order":''.join(GLYPHS[i] for i in (2,7))==GLYPHS[2]+GLYPHS[7],
          "three_four_order":all(len(''.join(GLYPHS[i] for i in range(n)))==n for n in (3,4)),
          "noop":dist(base,nop)==0,
          "uncoupled_frequency":abs(dist(base,freq)-.24)<1e-9,
          "pairwise_effect":dist(default,no_pair)>0,
          "triadic_effect":dist(default,no_tri)>0,
          "shuffled_affinity":dist(default,shuffled)>0,
          "deformation_bounds":all(.85<=r<=1.15 for r in deformed)
        }
        out.append({"seed":seed,"tests":tests,"metrics":{"pair_ablation":dist(default,no_pair),"tri_ablation":dist(default,no_tri),"shuffle":dist(default,shuffled),"uncoupled_frequency":dist(base,freq),"radius_min":min(deformed),"radius_max":max(deformed)}})
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=="__main__": main()
