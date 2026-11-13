"""Noncanonical Echo-GPT ring experiment; deterministic offline synthetic controls."""
import json, math, random, hashlib
N=27; TAU=2*math.pi; SEEDS=(11,23,37,53)
def circ(x): return math.atan2(math.sin(x),math.cos(x))
def distance(a,b,offset=0): return sum(abs(circ(x+offset-y)) for x,y in zip(a['phase'],b['phase']))/N
def simulate(seed, *, feedback=True, contact=True, coupling=True, shuffled=False, triadic=True, shift=0, noop=False):
    rng=random.Random(seed)
    ids=list(range(N)); xyz=[(i//9,(i//3)%3,i%3) for i in ids]
    phase=[(rng.random()*TAU+shift)%TAU for _ in ids]
    freq=[.018+.002*(i%7)+(rng.random()-.5)*.004 for i in ids]
    weight=list(range(1,N+1))
    if shuffled: rng.shuffle(weight)
    slots=[None]*N; mem=[None]*N; hits=0
    initial=list(phase)
    for t in range(16):
        for i in ids:
            hit=contact and (.75+.32*math.sin(.31*i+.71*t+seed*.01)>=1.0)
            if hit and slots[i] is None:
                slots[i]=i; mem[i]=circ(phase[(i+13)%N]-phase[i]);hits+=1
        if noop: continue
        nxt=[]
        for i in ids:
            a=phase[i]
            pair=math.sin(phase[(i+1)%N]-a)
            tri=math.sin(phase[(i+1)%N]+phase[(i+2)%N]-2*a)
            force=(.008*weight[i]/N*pair + (.005*tri if triadic else 0)) if coupling else 0
            if coupling and feedback and mem[i] is not None:
                relative=circ(phase[(i+13)%N]-a)
                force+=.012*math.sin(mem[i]-relative)
            nxt.append((a+(0 if not coupling else freq[i])+force)%TAU)
        phase=nxt
    return dict(ids=ids,xyz=xyz,phase=phase,slots=slots,hits=hits,initial=initial)
def suite(seed):
    base=simulate(seed); replay=simulate(seed); sham=simulate(seed,feedback=False)
    no_contact=simulate(seed,contact=False); unc=simulate(seed,coupling=False)
    unc_no_contact=simulate(seed,coupling=False,contact=False)
    no_op=simulate(seed,noop=True); shuffle=simulate(seed,shuffled=True)
    pair=simulate(seed,triadic=False); shifted=simulate(seed,shift=.7)
    metrics=dict(active_sham=distance(base,sham),active_no_contact=distance(base,no_contact),uncoupled_null=distance(unc,unc_no_contact),shuffle=distance(base,shuffle),triadic=distance(base,pair),covariance=distance(base,shifted,offset=.7),hits=base['hits'])
    tests={
      'replay':base==replay,
      'identity':base['ids']==list(range(N)) and len(set(base['ids']))==N,
      'projection':len(set(base['xyz']))==N and all(0<=v<3 for p in base['xyz'] for v in p),
      'capacity':sum(x is not None for x in base['slots'])<=N and all(x is None or x==i for i,x in enumerate(base['slots'])),
      'noop_stability':distance(no_op,dict(phase=no_op['initial']))<1e-12,
      'matched_active_sham':base['hits']==sham['hits'] and metrics['active_sham']>1e-9,
      'uncoupled_null':metrics['uncoupled_null']<1e-12,
      'shuffle_affinity':metrics['shuffle']>1e-9,
      'triadic_ablation':metrics['triadic']>1e-9,
      'phase_covariance':metrics['covariance']<1e-9
    }
    return dict(seed=seed,tests=tests,metrics=metrics)
if __name__=='__main__':
    result=dict(model='echo-gpt-relative-warehouse-06z-v1',seeds=list(SEEDS),runs=[suite(s) for s in SEEDS])
    result['passed']=sum(sum(v for v in run['tests'].values()) for run in result['runs'])
    result['total']=len(SEEDS)*10
    print(json.dumps(result,sort_keys=True,indent=2))
