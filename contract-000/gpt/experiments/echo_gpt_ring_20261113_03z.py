"""Synthetic GPT-owned 27-seat ring portfolio; no semantic or physical claims."""
import json, math, random, hashlib
N=27
SEEDS=(11,23,37,53)
TAU=2*math.pi

def simulate(seed, *, feedback=True, coupling=3, shuffle=False, detune=False, phase_shift=0., boundary=1., noop=False, steps=54):
    rng=random.Random(seed)
    ids=tuple(range(N))
    pos=tuple((i//9,(i//3)%3,i%3) for i in ids)
    weights=list(range(1,N+1))
    if shuffle: rng.shuffle(weights)
    phase=[(rng.random()*TAU+phase_shift)%TAU for _ in ids]
    freq=[.018+.003*(i%7)+(rng.random()-.5)*(.008 if detune else .002) for i in ids]
    occupancy=[None]*N
    contact_count=0
    for t in range(steps):
        # A contact occurs when a glyph's synthetic radial excursion crosses boundary.
        for i in ids:
            radial=.75+.32*math.sin(.19*t+.31*i+seed*.01)
            if radial>=boundary and occupancy[i] is None:
                occupancy[i]=i
                contact_count+=1
        if noop: continue
        nextphase=[]
        for i in ids:
            a=phase[i]
            pair=math.sin(phase[(i+1)%N]-a)
            tri=math.sin(phase[(i+1)%N]+phase[(i+2)%N]-2*a)
            quad=math.sin(phase[(i+1)%N]+phase[(i+2)%N]+phase[(i+3)%N]-3*a)
            aff=weights[i]/N
            force=.006*aff*pair
            if coupling>=3: force+=.004*tri
            if coupling>=4: force+=.002*quad
            if feedback and occupancy[i] is not None:
                force+=.002*math.sin(phase[(i+13)%N]-a)
            nextphase.append((a+freq[i]+force)%TAU)
        phase=nextphase
    return dict(ids=ids,positions=pos,phase=phase,occupancy=occupancy,contacts=contact_count)

def distance(a,b):
    return sum(abs(math.atan2(math.sin(x-y),math.cos(x-y))) for x,y in zip(a['phase'],b['phase']))/N

def suite(seed):
    base=simulate(seed)
    replay=simulate(seed)
    null=simulate(seed,noop=True)
    null0=simulate(seed,noop=True,feedback=False)
    unc=simulate(seed,feedback=False)
    unc_sham=simulate(seed,feedback=False,boundary=2.)
    sham=simulate(seed,boundary=2.)
    shuffled=simulate(seed,shuffle=True)
    pair=simulate(seed,coupling=2)
    four=simulate(seed,coupling=4)
    shifted=simulate(seed,phase_shift=.7)
    vals={
      'identity':len(set(base['ids']))==N and all(v==i for i,v in enumerate(base['ids'])),
      'projection':len(set(base['positions']))==N and all(0<=x<3 for p in base['positions'] for x in p),
      'replay':base==replay,
      'noop':distance(null,null0)==0,
      'uncoupled':distance(unc,unc_sham)==0,
      'border_causality':base['contacts']>0 and sham['contacts']==0 and distance(base,sham)>1e-9,
      'shuffled_affinity':distance(base,shuffled)>1e-9,
      'triadic_ablation':distance(base,pair)>1e-9,
      'fourbody_ablation':distance(base,four)>1e-9,
      'covariance_capacity':distance(base,shifted)<1e-10 and len([v for v in base['occupancy'] if v is not None])<=N
    }
    return {'seed':seed,'pass':vals,'metrics':{'contacts':base['contacts'],'border_L1':distance(base,sham),'shuffle_L1':distance(base,shuffled),'triadic_L1':distance(base,pair),'fourbody_L1':distance(base,four),'phase_covariance_L1':distance(base,shifted)}}

if __name__=='__main__':
    result={'model':'echo-gpt-ring-03z-v1','seeds':SEEDS,'results':[suite(s) for s in SEEDS]}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
