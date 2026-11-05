import math,random,json,sys
GLYPHS='אבגדהוזחטיכלמנסעפצקרשתךםןףץ'
TAU=2*math.pi
def simulate(n=3,seed=41,steps=75,dt=.13,k=.32,hetero=0.,offset=0,raystep=0.,order=None):
    rng=random.Random(seed)
    phases=[[TAU*j/27+rng.uniform(-.32,.32)+.21*r for j in range(27)] for r in range(n)]
    initial=[p[:] for p in phases]
    freqs=[[.16+.005*j+hetero*(r-(n-1)/2)*(.13+.002*j) for j in range(27)] for r in range(n)]
    for _ in range(steps):
        new=[]
        for r in range(n):
            row=[]
            for j,p in enumerate(phases[r]):
                target=phases[(r+1)%n][(j+offset)%27]
                row.append(p+dt*(freqs[r][j]+k*math.sin(target-p)))
            new.append(row)
        phases=new
    readout=[]
    for r in range(n):
        ray=raystep*r
        readout.append(min(range(27),key=lambda j:abs(math.atan2(math.sin(phases[r][j]-ray),math.cos(phases[r][j]-ray)))))
    if order is None: order=list(range(n))
    selected=[readout[r] for r in order]
    word=''.join(GLYPHS[j] for j in selected)
    z=sum(complex(math.cos(phases[r][j]),math.sin(phases[r][j])) for r in range(n) for j in range(27))/(27*n)
    return {'word':word,'ids':selected,'unique':len(set(selected)),'coherence':abs(z),'phases':phases,'initial':initial,'freqs':freqs}
def test():
    base=dict(n=3,seed=41)
    a=simulate(**base)
    records={}
    records['01_identity']={'pass':len(GLYPHS)==27 and len(set(GLYPHS))==27}
    records['02_output_lengths']={'pass':all(len(simulate(n=n)['ids'])==n for n in (2,3,4))}
    records['03_replay']={'pass':simulate(**base)==simulate(**base)}
    records['04_full_turn_ray']={'pass':a['ids']==simulate(**base,raystep=TAU)['ids']}
    zero=simulate(**base,k=0)
    drift=max(abs(zero['phases'][r][j]-(zero['initial'][r][j]+75*.13*zero['freqs'][r][j])) for r in range(3) for j in range(27))
    records['05_zero_coupling_analytic']={'pass':drift<1e-11,'max_error':drift}
    rev=simulate(**base,order=[2,1,0])
    records['06_ring_order_equivariance']={'pass':rev['ids']==list(reversed(a['ids']))}
    baseline=[simulate(seed=s) for s in range(20,50)]
    hetero=[simulate(seed=s,hetero=1.8) for s in range(20,50)]
    metrics=lambda arr:{'mean_unique':sum(x['unique'] for x in arr)/len(arr),'unique_words':len(set(x['word'] for x in arr)),'mean_coherence':sum(x['coherence'] for x in arr)/len(arr)}
    records['07_frequency_heterogeneity']={'control':metrics(baseline),'treatment':metrics(hetero)}
    offset=[simulate(seed=s,offset=5) for s in range(20,50)]
    records['08_index_offset']={'control':metrics(baseline),'treatment':metrics(offset)}
    rays=[simulate(seed=s,raystep=TAU/3) for s in range(20,50)]
    records['09_ray_offset']={'control':metrics(baseline),'treatment':metrics(rays)}
    stress=[simulate(n=n,seed=s,k=k,hetero=h,offset=o,raystep=ray) for n in (2,3,4) for s in (0,1,2,3,4) for k in (0,.32,.9) for h,o,ray in ((0,0,0),(1.8,5,TAU/3))]
    records['10_stress']={'pass':all(0<=x['coherence']<=1+1e-12 and math.isfinite(x['coherence']) and len(x['ids']) in (2,3,4) for x in stress),'cases':len(stress)}
    return {'round':3,'issue':271,'python':sys.version.split()[0],'seed_main':41,'steps':75,'dt':.13,'tests':records,'caveat':'synthetic oscillator and arbitrary nearest-ray readout; no language or cognition validation'}
if __name__=='__main__':print(json.dumps(test(),indent=2,ensure_ascii=False))
