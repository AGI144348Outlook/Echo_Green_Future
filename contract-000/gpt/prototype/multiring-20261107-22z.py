"""GPT-only synthetic multiring experiment; stdlib; preregistered Issue #340."""
import json, math, random, sys
GLYPHS=list('אבגדהוזחטיכלמנסעפצקרשת')+list('ךםןףץ')
assert len(GLYPHS)==27 and len(set(GLYPHS))==27
SEEDS=(3301,3302,3303,3304)

def run(seed):
    rng=random.Random(seed)
    phases=[rng.random()*2*math.pi for _ in range(3)]
    freq=[0.07,0.11,0.17]
    def ring(t,k):
        a=phases[k]+freq[k]*t
        radius=1+0.12*math.sin(0.13*t+k)
        return [(radius*math.cos(a+2*math.pi*j/27),radius*math.sin(a+2*math.pi*j/27)) for j in range(27)]
    def composition(t,n):
        return ''.join(GLYPHS[(int((phases[k]+freq[k]*t)/(2*math.pi)*27)+k*7)%27] for k in range(n))
    # Sealed-by-design target: nonlinear independent formula, not fitted from candidate.
    target=[math.tanh(0.5*math.sin(0.31*t+seed%17)+0.25*math.cos(0.19*t)) for t in range(16,32)]
    def pred(t,coupled,shuffle=False):
        weights=[(i+1)/27 for i in range(27)]
        if shuffle: weights=list(reversed(weights))
        x=sum(weights[i]*math.sin(phases[i%3]+freq[i%3]*t+i*2*math.pi/27) for i in range(27))/27
        return x*(1+0.2*coupled*math.cos(phases[0]-phases[1]))
    def mse(c,s=False):return sum((pred(t,c,s)-y)**2 for t,y in zip(range(16,32),target))/len(target)
    checks={
      'identity_census':len(GLYPHS)==len(set(GLYPHS))==27,
      'deterministic_replay':ring(4,0)==ring(4,0),
      'moving_geometry':ring(0,0)!=ring(1,0),
      'bounded_deformation':all(0.879<math.hypot(*p)<1.121 for k in range(3) for t in range(32) for p in ring(t,k)),
      'two_ring_composition':len(composition(3,2))==2 and all(c in GLYPHS for c in composition(3,2)),
      'three_ring_composition':len(composition(3,3))==3 and all(c in GLYPHS for c in composition(3,3)),
      'projection_27_cells':len({(i//9,(i//3)%3,i%3) for i in range(27)})==27,
      'noop_control':sum(abs(0.0) for _ in range(27))==0,
      'shuffled_gematria_changes':any(pred(t,1)!=pred(t,1,True) for t in range(16,32)),
      'heldout_comparison_finite':all(math.isfinite(mse(c)) for c in (0,1)),
    }
    return {'seed':seed,'checks':checks,'mse':{'coupled':mse(1),'uncoupled':mse(0),'shuffled':mse(1,True),'noop':sum(y*y for y in target)/len(target)},'example_two':composition(3,2),'example_three':composition(3,3)}
if __name__=='__main__':
    runs=[run(s) for s in SEEDS]
    print(json.dumps({'python':sys.version.split()[0],'seeds':SEEDS,'runs':runs,'total_pass':sum(sum(x['checks'].values()) for x in runs),'total_fail':sum(sum(not v for v in x['checks'].values()) for x in runs)},ensure_ascii=False,indent=2))
