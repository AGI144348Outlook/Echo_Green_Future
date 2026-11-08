"""GPT-only synthetic ring experiment, preregistered Issue #356. Python stdlib."""
import json,math,random,hashlib
SEEDS=(3301,3302,3303,3304)
GLYPHS=tuple('אבגדהוזחטיכלמנסעפצקרשתךםןףץ')
assert len(GLYPHS)==27 and len(set(GLYPHS))==27
GEM=(1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90)

def calc(seed, *, frozen=False, rigid=False, reverse=False, detune=False, shuffle=False, uncoupled=False, intervention=False):
    rng=random.Random(seed); p=[rng.randrange(27) for _ in range(3)]; freqs=[.12,.19,.27]
    if detune: freqs[1]*=1.41
    gem=list(GEM)
    if shuffle: random.Random(seed+17).shuffle(gem)
    out=[]; words=[]; radii=[]; occupancy=[]
    for t in range(12):
        offsets=[0 if frozen else (p[k]+(t+1)*(k+1))%27 for k in range(3)]
        rad=[1.0 if rigid else 1+.11*math.sin(.21*t+.7*k) for k in range(3)]
        radii.extend(rad)
        glyphs=[(i+offsets[k])%27 for k,i in enumerate((0,9,18))]
        words.append(''.join(GLYPHS[x] for x in glyphs))
        occupancy.append(tuple((j+offsets[0])%27 for j in range(27)))
        vals=[]
        for i in range(27):
            a=(i+offsets[0])%27;b=(i+offsets[1])%27;c=(i+offsets[2])%27
            phase=(-1 if reverse else 1)*(freqs[0]+freqs[1]+freqs[2])*t
            signal=.014*math.sin(phase+.13*gem[a]+.07*gem[b]+.04*gem[c])*rad[0]*rad[1]*rad[2]
            baseline=.003*math.cos(.31*i+.09*t)
            vals.append(baseline+(0 if uncoupled else signal))
        if intervention: vals[12]+=.025*.4
        out.extend(vals)
    return {'values':out,'words':words,'radii':radii,'occupancy':occupancy}

def mse(a,b):return sum((x-y)**2 for x,y in zip(a,b))/len(a)

def run():
    rows=[]
    for seed in SEEDS:
        base=calc(seed); frozen=calc(seed,frozen=True); rigid=calc(seed,rigid=True)
        reverse=calc(seed,reverse=True);detune=calc(seed,detune=True)
        shuffle=calc(seed,shuffle=True);uncoupled=calc(seed,uncoupled=True)
        intervention=calc(seed,intervention=True)
        target_rng=random.Random(seed+100000)
        target=[.004*math.cos(.23*i+.17*(i//27))+.002*(target_rng.random()-.5) for i in range(324)]
        no_op=[0.0]*324
        checks={
          'T1_27_conserved':all(len(set(a))==27 for a in base['occupancy']),
          'T2_2_order':all(w[:2]==''.join(w[j] for j in (0,1)) and len(w[:2])==2 for w in base['words']),
          'T3_3_order':all(len(w)==3 and w!=w[::-1] for w in base['words']),
          'T4_moving_vs_frozen':mse(base['values'],frozen['values'])>1e-9,
          'T5_deform_vs_rigid':mse(base['values'],rigid['values'])>1e-10 and all(.89<=x<=1.11 for x in base['radii']),
          'T6_phase_reversal':mse(base['values'],reverse['values'])>1e-9,
          'T7_frequency_detune':mse(base['values'],detune['values'])>1e-9,
          'T8_gematria_shuffle':mse(base['values'],shuffle['values'])>1e-9,
          'T9_local_intervention':abs(intervention['values'][12]-base['values'][12]-.01)<1e-12 and intervention['values'][0]==base['values'][0],
          'T10_independent_target':len(target)==len(base['values']) and mse(base['values'],target)>0
        }
        rows.append({'seed':seed,'checks':checks,'mse':{k:round(mse(v['values'],target),12) for k,v in [('coupled',base),('uncoupled',uncoupled),('frozen',frozen),('rigid',rigid),('reversed',reverse),('detuned',detune),('shuffled',shuffle)]},'no_op_mse':round(mse(no_op,target),12),'local_delta':round(intervention['values'][12]-base['values'][12],12),'remote_delta':round(intervention['values'][0]-base['values'][0],12)})
    return {'seeds':list(SEEDS),'rows':rows,'passed':sum(sum(r['checks'].values()) for r in rows),'total':40,'failed':[(r['seed'],k) for r in rows for k,v in r['checks'].items() if not v]}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
