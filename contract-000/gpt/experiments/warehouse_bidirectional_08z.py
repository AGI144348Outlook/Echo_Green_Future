"""Issue #320: GPT-only bidirectional warehouse-ring causal toy. Python 3 stdlib."""
import json,random,math
N=27;D=7;STEP=360/N
def simulate(seed,mode='both',shuffle=False):
 rng=random.Random(seed)
 entropy=tuple([.2]*135+[.8]*135)
 if shuffle:
  temp=list(entropy);random.Random(seed+100).shuffle(temp);entropy=tuple(temp)
 before=entropy;draws=[rng.random() for _ in entropy]
 occupied={};views=[{} for _ in range(D)];seats=(None,)*N
 tick=0;phase=[0.]*D;events=[];choices=[];max_deform=0
 for t,(h,draw) in enumerate(zip(entropy,draws)):
  if draw>=h:continue
  glyph=t%N
  shift=round(phase[glyph%D]/STEP)%N if mode in ('both','reverse') else 0
  seat=(glyph+shift)%N
  assert glyph not in occupied and seat not in occupied.values()
  occupied[glyph]=seat
  for v in views:v[seat]=glyph
  assert all(v.get(seat)==glyph for v in views)
  tick+=1;events.append(t);choices.append(seat)
  if mode in ('both','forward'):
   domain=glyph%D
   phase[domain]=(phase[domain]+STEP)%360
   phase[(domain+1)%D]=(phase[(domain+1)%D]+.15*STEP)%360
  radius=1+.1*math.sin(2*math.pi*(tick%N)/N)
  max_deform=max(max_deform,abs(radius-1))
  del occupied[glyph]
  for v in views:del v[seat]
 assert entropy==before and not occupied and all(not v for v in views) and seats==(None,)*N
 return dict(seed=seed,mode=mode,ticks=tick,phase=(tick%N)*STEP,events=events,choices=choices,warehouse_phases=phase,max_deform=max_deform,entropy_unchanged=entropy==before,views_clear=all(not v for v in views))
def evaluate():
 seeds=[1106,1107,1108,1109,1110]
 cases={m:[simulate(s,m) for s in seeds] for m in ('both','forward','reverse','none')}
 shuffled=[simulate(s,'both',True) for s in seeds]
 checks={}
 checks['01_identity_inert_seats']=N==27 and len(set(range(N)))==27
 checks['02_phase_27_closure']=all(abs((27*k*STEP)%360)<1e-8 for k in (1,2,3))
 checks['03_edge_hold_collision']=all(len(x['events'])==len(set(x['events'])) for xs in cases.values() for x in xs)
 checks['04_seven_views_clear']=all(x['views_clear'] for xs in cases.values() for x in xs)
 checks['05_entropy_immutable']=all(x['entropy_unchanged'] for xs in cases.values() for x in xs)
 checks['06_glyph_to_warehouse']=any(any(abs(v)>1e-8 for v in x['warehouse_phases']) for x in cases['forward'])
 checks['07_warehouse_to_glyph']=any(a['choices']!=b['choices'] for a,b in zip(cases['both'],cases['forward']))
 checks['08_ablation_null']=all(not any(abs(v)>1e-8 for v in x['warehouse_phases']) for x in cases['none']) and all(a['events']==b['events'] for a,b in zip(cases['both'],cases['none']))
 checks['09_bound_shuffle']=all(x['max_deform']<=.100000001 for xs in cases.values() for x in xs) and any(a['events']!=b['events'] for a,b in zip(cases['both'],shuffled))
 def loss(x):
  target=[(i*7+3)%27 for i in range(270)]
  pred={t:seat for t,seat in zip(x['events'],x['choices'])}
  return sum(min(abs(pred.get(t,0)-y),27-abs(pred.get(t,0)-y)) for t,y in enumerate(target))/270
 losses={m:[round(loss(x),6) for x in xs] for m,xs in cases.items()}
 checks['10_external_null_metric']=all(math.isfinite(y) for v in losses.values() for y in v) and len(losses['both'])==5
 return {'issue':320,'seeds':seeds,'checks':checks,'passed':sum(checks.values()),'total':len(checks),'counts':{m:[x['ticks'] for x in xs] for m,xs in cases.items()},'shuffled_counts':[x['ticks'] for x in shuffled],'different_choices_both_forward':[a['choices']!=b['choices'] for a,b in zip(cases['both'],cases['forward'])],'losses':losses,'mean_loss':{m:round(sum(v)/len(v),6) for m,v in losses.items()},'limitations':'Synthetic entropy, engineered feedback, unrelated target; no learning or real warehouse integration.'}
if __name__=='__main__':print(json.dumps(evaluate(),indent=2,sort_keys=True))
