"""GPT-only independent queue ledger, preregistered Echo_Green_Future issue #323.
python queue_11z.py ; stdlib only, fixed seeds; no external I/O except stdout.
"""
import json, math, random
N=27; STEP=360/N

def grants(schedule,seed=1106):
    rng=random.Random(seed)
    return [i for i,e in enumerate(schedule) if rng.random()<max(0,min(1,e))]

def simulate(schedule,policy='queue',seed=1106,age_cap=9,broken_expiry=False):
    assert policy in ('queue','drop','retry')
    arrivals=grants(schedule,seed)
    arrival_set=set(arrivals)
    live={}; waiting=[]; terminal={}; accepted=[]; phase=0.; wraps=0; max_backlog=0
    for t in range(len(schedule)+12):
        live={s:(gid,at) for s,(gid,at) in live.items() if t-at<3}
        # Expire EVERY waiting item, before admitting any of them.
        if not broken_expiry:
            for row in waiting[:]:
                gid,born,g,s,tries=row
                if t-born>=age_cap:
                    terminal[gid]=('EXPIRED',t);waiting.remove(row)
        if t in arrival_set:
            waiting.append((t,t,t%N,t%2,0))
        if policy=='queue':
            active=waiting[:1];waiting=waiting[1:]
        else:
            active=waiting;waiting=[]
        for gid,born,g,s,tries in active:
            if not broken_expiry and t-born>=age_cap:
                terminal[gid]=('EXPIRED',t)
            elif s not in live and g not in [v[0] for v in live.values()]:
                live[s]=(g,t);terminal[gid]=('ACCEPTED',t)
                accepted.append((gid,born,t,g,s))
                phase=(phase+STEP)%360
                if len(accepted)%27==0:wraps+=1
            elif policy=='drop':
                terminal[gid]=('DROPPED',t)
            elif policy=='retry':
                if tries<2:waiting.append((gid,born,g,s,tries+1))
                else:terminal[gid]=('DROPPED',t)
            else:
                waiting.append((gid,born,g,s,tries+1))
        max_backlog=max(max_backlog,len(waiting))
    for gid,born,g,s,tries in waiting:
        terminal[gid]=('END_PENDING',len(schedule)+12)
    return dict(grant_ids=arrivals,terminal=terminal,accepted=accepted,phase=phase,
                wraps=wraps,max_backlog=max_backlog,accepted_after_end=sum(t>=len(schedule) for _,_,t,_,_ in accepted))

def external_oracle(result,cap=9):
    ids=result['grant_ids'];term=result['terminal'];acc=result['accepted']
    exact=(len(ids)==len(set(ids))==len(term) and set(ids)==set(term) and
           sum(1 for gid,_,_,_,_ in acc if term[gid][0]=='ACCEPTED')==len(acc) and
           len({x[0] for x in acc})==len(acc))
    ages=[t-born for _,born,t,_,_ in acc]
    no_overlap=all(not (s1==s2 and abs(t1-t2)<3) for i,(_,_,t1,_,s1) in enumerate(acc)
                   for _,_,t2,_,s2 in acc[i+1:])
    return dict(exact=exact,age_ok=all(a<cap for a in ages),max_age=max(ages,default=0),
                no_overlap=no_overlap,phase_ok=math.isclose(result['phase'],(len(acc)%27)*STEP,abs_tol=1e-9),
                wraps_ok=result['wraps']==len(acc)//27)

def compose_two_ring(ids):
    left=tuple(ids);right=tuple(reversed(ids))
    return tuple((left[i],right[(i+3)%27]) for i in range(27))

def evaluate():
    schedule=[.2]*135+[.8]*135
    shuffled=schedule[:];random.Random(55).shuffle(shuffled)
    d=simulate(schedule,'drop');r=simulate(schedule,'retry');q=simulate(schedule,'queue')
    zero=simulate([0]*270);low=simulate([.1]*270);high=simulate([.9]*270)
    oq=external_oracle(q);od=external_oracle(d);orr=external_oracle(r)
    bad=simulate(schedule,'queue',broken_expiry=True);ob=external_oracle(bad)
    pairs=compose_two_ring(tuple(range(27)))
    tests={
      '01_ledger_bijection':all(x['exact'] for x in [oq,od,orr]),
      '02_age_cap':all(x['age_ok'] for x in [oq,od,orr]),
      '03_zero_grants':len(zero['grant_ids'])==len(zero['accepted'])==0,
      '04_common_grants':d['grant_ids']==r['grant_ids']==q['grant_ids'],
      '05_phase_independent_state':all(x['phase_ok'] and x['wraps_ok'] for x in [oq,od,orr]),
      '06_dwell_overlap_oracle':all(x['no_overlap'] for x in [oq,od,orr]),
      '07_replay':q==simulate(schedule,'queue'),
      '08_shuffled_timing':grants(shuffled)!=grants(schedule),
      '09_policy_tradeoff':len(r['accepted'])>=len(d['accepted']) and len(q['accepted'])>=len(d['accepted']),
      '10_two_ring_identity':len(pairs)==27 and {a for a,b in pairs}==set(range(27)) and {b for a,b in pairs}==set(range(27))
    }
    return dict(issue=323,seed=1106,tests=tests,passed=sum(tests.values()),total=len(tests),
      grants=len(q['grant_ids']),counts={p:{'accepted':len(x['accepted']),
      'outcomes':{status:sum(v[0]==status for v in x['terminal'].values()) for status in ('ACCEPTED','EXPIRED','DROPPED','END_PENDING')},
      'phase':round(x['phase'],9),'wraps':x['wraps'],'post_end':x['accepted_after_end'],
      'max_age':external_oracle(x)['max_age'],'max_backlog':x['max_backlog']}
      for p,x in [('drop',d),('retry',r),('queue',q)]},
      low_grants=len(low['grant_ids']),high_grants=len(high['grant_ids']),
      shuffled_grants=len(grants(shuffled)),
      negative_expiry_mutant={'max_age':ob['max_age'],'overage_detected':not ob['age_ok'],
                              'accepted':len(bad['accepted'])},
      limits=['phase state is incremented in same acceptance loop; oracle checks arithmetic but not independent physical dynamics',
              'two-ring composition identity only; no semantic evaluation or genuine coupling',
              'two-seat contention synthetic; entropy is exogenous proxy'])
if __name__=='__main__':print(json.dumps(evaluate(),sort_keys=True,indent=2))
