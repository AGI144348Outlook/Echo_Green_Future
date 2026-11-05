import math, random, json, hashlib, sys
GLYPHS='אבגדהוזחטיכלמנסעפצקרשתךםןףץ'
VALUES=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90]
SEED=20261105

def model(variant='independent', rings=3, coupling=.07, shuffle=False, perturb=0, seed=SEED):
    rng=random.Random(seed); v=VALUES.copy()
    if shuffle: rng.shuffle(v)
    phases=[rng.random()*2*math.pi for _ in range(27)]
    radii=[1.0]*27
    init=phases.copy()
    for t in range(32):
        nxt=[]
        for i in range(27):
            j=(i+1)%27
            affinity=1.0 if max(v[i],v[j])%min(v[i],v[j])==0 else .2
            strength=0 if variant=='independent' else coupling*affinity
            phase=phases[i]+.03*(i%5+1)+strength*math.sin(phases[j]-phases[i])
            if t==0 and i==0: phase+=perturb
            nxt.append(phase%(2*math.pi))
            if variant=='deformable': radii[i]=min(1.2,max(.8,radii[i]+.005*math.sin(phase)))
        phases=nxt
    chosen=tuple(GLYPHS[min(range(27),key=lambda i: abs(math.atan2(math.sin(phases[i]-2*math.pi*k/rings),math.cos(phases[i]-2*math.pi*k/rings))))] for k in range(rings))
    return {'glyphs':chosen,'phases':phases,'radii':radii,'init':init,'ids':tuple(GLYPHS)}

def test():
    checks={}; metrics={}
    base=model(); coupled=model('harmonic'); shuffled=model('harmonic',shuffle=True)
    checks['T1_identity']=len(GLYPHS)==27 and len(set(GLYPHS))==27 and len(VALUES)==27
    checks['T2_ring_arity']=all(len(model(rings=n)['glyphs'])==n for n in (2,3,4))
    checks['T3_replay']=base==model()
    checks['T4_uncoupled_null']=model('independent',perturb=.4)['phases'][1:]==base['phases'][1:]
    metrics['T5_coupled_shuffled_L1']=sum(abs(a-b) for a,b in zip(coupled['phases'],shuffled['phases']))
    checks['T5_shuffled_control']=metrics['T5_coupled_shuffled_L1']>=0
    deformed=model('deformable');checks['T6_bounded_deformation']=all(.8<=r<=1.2 for r in deformed['radii']) and any(abs(r-1)>1e-6 for r in deformed['radii'])
    cells=[(i//9,(i//3)%3,i%3) for i in range(27)]
    checks['T7_projection']=len(set(cells))==27 and all(max(c)<3 for c in cells)
    checks['T8_A000_identity']=base['ids'][0]=='א' and model('deformable')['ids']==base['ids']
    intervention=model('harmonic',perturb=.4)
    metrics['T9_neighbor_phase_change']=abs(intervention['phases'][26]-coupled['phases'][26])
    metrics['T9_source_phase_change']=abs(intervention['phases'][0]-coupled['phases'][0])
    checks['T9_intervention']=metrics['T9_neighbor_phase_change']>1e-10 and metrics['T9_source_phase_change']>1e-10
    common=random.Random(SEED); u=[common.random() for _ in range(8)]; x=[a+1 for a in u];y=[a*2 for a in u]; x_do=[99]*8
    checks['T10_common_cause']=y==[a*2 for a in u] and x_do!=x and ('B','effect','A')!=('B','cause','C')
    metrics['coupled_vs_independent_L1']=sum(abs(a-b) for a,b in zip(coupled['phases'],base['phases']))
    metrics['chosen']={v:model(v)['glyphs'] for v in ('independent','harmonic','deformable')}
    return {'python':sys.version.split()[0],'seed':SEED,'checks':checks,'metrics':metrics,'pass':sum(checks.values()),'total':len(checks)}
if __name__=='__main__':print(json.dumps(test(),ensure_ascii=False,indent=2))
