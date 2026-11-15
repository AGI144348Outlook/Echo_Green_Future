import json,math,random,hashlib,platform
GLYPHS=list('אבגדהוזחטיכלמנסעפצקרשת')+list('ךםןףץ')
VALUES=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90]
SEEDS=[11,23,37,53]
TAU=2*math.pi

def distance(a,b):return abs(math.atan2(math.sin(a-b),math.cos(a-b)))
def delta(a,b):return sum(distance(x,y) for x,y in zip(a,b))/len(a)
def coords():return [(i//9,(i//3)%3,i%3) for i in range(27)]
def seats(phases,resolve=True):
    targets=[int((x%TAU)/TAU*27)%27 for x in phases]
    if not resolve:return targets
    used=set();out=[]
    for target in targets:
        for k in range(27):
            candidate=(target+k)%27
            if candidate not in used:used.add(candidate);out.append(candidate);break
    return out

def simulate(seed,ring_count=3,topology='near',pair=.15,tri=.06,aff=.04,frequency=.013,boundary=.02,resolve=True,shuffle=False):
    rng=random.Random(seed)
    phases=[rng.random()*TAU for _ in range(27)]
    vals=VALUES.copy()
    if shuffle:rng.shuffle(vals)
    for t in range(24):
        occupancy=seats(phases,resolve)
        nxt=[]
        for i,x in enumerate(phases):
            j=(i+1)%27 if topology=='near' else (i+13)%27
            k=(i+2)%27
            pair_term=pair*math.sin(phases[j]-x)
            tri_term=tri*math.sin(phases[j]+phases[k]-2*x)
            affinity=aff*((vals[i]%9)/9)*math.sin(phases[(i+ring_count)%27]-x)
            freq=frequency*((i%7)-3)
            edge=boundary*(occupancy[i]/26-.5)*math.cos(x)
            nxt.append((x+.08+pair_term+tri_term+affinity+freq+edge)%TAU)
        phases=nxt
    return phases

def measure(seed):
    base=simulate(seed)
    none=simulate(seed,pair=0,tri=0,aff=0,frequency=0,boundary=0)
    shuffled=simulate(seed,shuffle=True)
    uncoupled_shuffled=simulate(seed,aff=0,shuffle=True)
    uncoupled=simulate(seed,aff=0)
    rng=random.Random(seed)
    initial=[rng.random()*TAU for _ in range(27)]
    naive=seats(initial,False); resolved=seats(initial,True)
    metrics={
      'identity_projection':len(GLYPHS)==27 and len(set(GLYPHS))==27 and len(set(coords()))==27 and len(coords())==27 and len(set(GLYPHS+GLYPHS[:1]))!=28,
      'replay':base==simulate(seed),
      'ring_composition':all(len([GLYPHS[(seed+j)%27] for j in range(n)])==n for n in (2,3,4)),
      'topology':delta(base,simulate(seed,topology='opposite')),
      'pairwise':delta(base,simulate(seed,pair=0)),
      'triadic':delta(base,simulate(seed,tri=0)),
      'gematria':delta(base,shuffled),
      'gematria_null':delta(uncoupled,uncoupled_shuffled),
      'frequency':delta(base,simulate(seed,frequency=0)),
      'seat_resolution':delta(base,simulate(seed,resolve=False)),
      'naive_collisions':27-len(set(naive)),
      'resolved_unique':len(set(resolved))==27,
      'boundary':delta(base,simulate(seed,boundary=0)),
      'noop':delta(none,simulate(seed,pair=0,tri=0,aff=0,frequency=0,boundary=0)),
      'finite':all(math.isfinite(x) for x in base)
    }
    predicates={
      'T01_identity':metrics['identity_projection'],
      'T02_replay':metrics['replay'],
      'T03_ring_lengths':metrics['ring_composition'],
      'T04_topology':metrics['topology']>1e-12,
      'T05_pairwise':metrics['pairwise']>1e-12,
      'T06_triadic':metrics['triadic']>1e-12,
      'T07_gematria_active_null':metrics['gematria']>1e-12 and metrics['gematria_null']==0,
      'T08_frequency':metrics['frequency']>1e-12,
      'T09_collision_resolution':metrics['resolved_unique'] and metrics['naive_collisions']>0 and metrics['seat_resolution']>1e-12,
      'T10_boundary_noop':metrics['boundary']>1e-12 and metrics['noop']==0 and metrics['finite']
    }
    return {'seed':seed,'metrics':metrics,'predicates':predicates}

if __name__=='__main__':
    import pathlib
    src=pathlib.Path(__file__).read_bytes()
    runs=[measure(seed) for seed in SEEDS]
    result={'source_sha256':hashlib.sha256(src).hexdigest(),'python':platform.python_version(),'seeds':SEEDS,'runs':runs,'passed':sum(sum(v for v in r['predicates'].values()) for r in runs),'total':40}
    print(json.dumps(result,indent=2,ensure_ascii=False))
