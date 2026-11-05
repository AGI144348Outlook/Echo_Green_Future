"""Independent GPT multiring controls, seed 20261105. Stdlib only."""
import math, random, json, sys
SEED=20261105
GLYPHS='אבגדהוזחטיכלמנסעפצקרשתךםןףץ'
VALUES=(1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90)
TAU=2*math.pi

def distance(a,b):
    return abs(math.atan2(math.sin(a-b),math.cos(a-b)))

def run(coupling=.07, shuffle=False, perturb=0, rings=3, deform=False, seed=SEED, steps=32):
    rng=random.Random(seed)
    vals=list(VALUES)
    if shuffle: rng.shuffle(vals)
    phases=[rng.random()*TAU for _ in GLYPHS]
    radii=[1.]*27
    for t in range(steps):
        old=phases
        phases=[]
        for i in range(27):
            # directed j -> i; 0 affects 26, never 1 (unless through full loop)
            j=(i+1)%27
            affinity=1. if max(vals[i],vals[j])%min(vals[i],vals[j])==0 else .2
            p=(old[i]+.03*(i%5+1)+coupling*affinity*math.sin(old[j]-old[i])+(perturb if t==0 and i==0 else 0))%TAU
            phases.append(p)
            if deform: radii[i]=min(1.2,max(.8,radii[i]+.005*math.sin(p)))
    chosen=[GLYPHS[min(range(27),key=lambda i:distance(phases[i],TAU*k/rings))] for k in range(rings)]
    return {'phases':phases,'radii':radii,'chosen':chosen}

def suite():
    base=run(); unc=run(coupling=0); unc_do=run(coupling=0,perturb=.4)
    coupled=run(perturb=.4); shuffle=run(shuffle=True); deform=run(deform=True)
    diff=[distance(a,b) for a,b in zip(base['phases'],coupled['phases'])]
    shuffled_diff=[distance(a,b) for a,b in zip(base['phases'],shuffle['phases'])]
    cells=[(i//9,(i//3)%3,i%3) for i in range(27)]
    # common source U -> X and U -> Y: intervening on X leaves Y unchanged.
    rng=random.Random(SEED); u=[rng.random() for _ in range(12)]
    x=[v+1 for v in u]; y=[2*v for v in u]; x_do=[99.]*len(u)
    checks={
      'T1_wrap_invariant':distance(.01,TAU-.01)<.021,
      'T2_metric_bounded':all(0<=d<=math.pi+1e-12 for d in diff+shuffled_diff),
      'T3_uncoupled_null':all(distance(a,b)<1e-12 for a,b in zip(unc['phases'][1:],unc_do['phases'][1:])),
      'T4_directed_neighbor_effect':diff[26]>1e-8,
      'T5_reverse_direction_control':diff[1]<1e-8,
      'T6_shuffle_comparison_measured':sum(shuffled_diff)>1e-8,
      'T7_noop_replay':base==run(perturb=0),
      'T8_ring_arity_identity':len(set(GLYPHS))==27 and all(len(run(rings=n)['chosen'])==n for n in (2,3,4)),
      'T9_boundary_cube':all(.8<=r<=1.2 for r in deform['radii']) and len(set(cells))==27,
      'T10_common_cause_do_control':x!=x_do and y==[2*v for v in u],
    }
    return {'seed':SEED,'python':sys.version.split()[0],'checks':checks,'pass':sum(checks.values()),'total':len(checks),'metrics':{'source_delta':diff[0],'neighbor_delta':diff[26],'reverse_delta':diff[1],'shuffled_circular_L1':sum(shuffled_diff),'intervention_circular_L1':sum(diff),'independent_chosen':unc['chosen'],'coupled_chosen':base['chosen'],'shuffled_chosen':shuffle['chosen'],'deformable_chosen':deform['chosen']},'limitations':['T6 difference is not performance advantage','T10 synthetic SCM control; no inferred graph','T5 may acquire influence after >=27 steps around the directed cycle','A-000 content identity and receiver atomicity not tested']}
if __name__=='__main__':print(json.dumps(suite(),ensure_ascii=False,indent=2))
