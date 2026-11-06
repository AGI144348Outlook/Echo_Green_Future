"""GPT-only synthetic 27-seat ring: preregistration Echo_Green_Future #322.
Run: python warehouse_queue_10z.py (stdlib, fixed seed). No external I/O.
"""
import json, random, math
N=27
STEP=360/N

def opportunities(schedule,seed=1106):
    rng=random.Random(seed)
    return [t for t,e in enumerate(schedule) if rng.random()<max(0,min(1,e))]

def simulate(schedule, policy='drop',seed=1106):
    assert policy in ('drop','retry','queue')
    granted=opportunities(schedule,seed)
    grants=set(granted)
    seats={}; pending=[]; accepted=[]; lost=0; max_backlog=0; retries=0
    for t in range(len(schedule)+12):
        # Release after dwell of 3 steps.
        seats={s:v for s,v in seats.items() if t-v[1]<3}
        if t in grants:
            g=t%N; s=t%2  # amended collision pressure, 2 seats accessible
            pending.append((t,g,s,0))
        if policy=='drop':
            active=pending;pending=[]
        elif policy=='retry':
            active=pending;pending=[]
        else:
            active=pending[:1];pending=pending[1:]
        for born,g,s,attempt in active:
            if s not in seats and all(v[0]!=g for v in seats.values()):
                seats[s]=(g,t);accepted.append((born,t,g,s))
            elif policy=='drop':lost+=1
            elif policy=='retry' and attempt<2:
                pending.append((born,g,s,attempt+1));retries+=1
            elif policy=='queue' and t-born<9:
                pending.append((born,g,s,attempt+1));retries+=1
            else:lost+=1
        max_backlog=max(max_backlog,len(pending))
        assert len(seats)==len({v[0] for v in seats.values()})
        assert len(seats)<=9
    lost+=len(pending)
    # Exactly one terminal outcome per granted opportunity.
    assert len(accepted)+lost==len(granted)
    return {'granted':len(granted),'accepted':len(accepted),'lost':lost,
            'ticks':len(accepted),'completed_cycles':len(accepted)//27,
            'phase':(len(accepted)%27)*STEP,
            'mean_latency':round(sum(t-b for b,t,_,_ in accepted)/len(accepted),5) if accepted else 0,
            'max_backlog':max_backlog,'retries':retries,
            'grant_times':granted,'accepted_records':accepted}

def evaluate():
    s=[.2]*135+[.8]*135
    shuffled=s[:];random.Random(55).shuffle(shuffled)
    drop=simulate(s,'drop');retry=simulate(s,'retry');queue=simulate(s,'queue')
    null=simulate([0]*270,'queue')
    low=simulate([.1]*270,'drop');high=simulate([.9]*270,'drop')
    checks={}
    checks['01_common_grants']=all(x['grant_times']==drop['grant_times'] for x in [retry,queue])
    checks['02_zero_null']=null['granted']==null['accepted']==null['ticks']==0
    checks['03_rate_monotone']=high['granted']>low['granted']
    checks['04_drop_collision_loss']=drop['lost']>0
    checks['05_retry_not_worse']=retry['accepted']>drop['accepted']
    checks['06_queue_recovery']=queue['accepted']>drop['accepted']
    checks['07_conservation']=all(x['accepted']+x['lost']==x['granted'] for x in [drop,retry,queue,null,low,high])
    checks['08_27_cycle']=all(math.isclose(x['phase'],(x['ticks']%27)*STEP,abs_tol=1e-9) and x['completed_cycles']==x['ticks']//27 for x in [drop,retry,queue])
    checks['09_no_simultaneous_collision']=all(len({(t,s) for _,t,_,s in x['accepted_records']})==len(x['accepted_records']) for x in [drop,retry,queue])
    checks['10_replay_shuffle']=simulate(s,'queue')==queue and simulate(shuffled,'queue')['grant_times']!=queue['grant_times']
    return {'issue':322,'seed':1106,'tests':checks,'passed':sum(checks.values()),'total':len(checks),
            'drop':{k:v for k,v in drop.items() if k not in ('grant_times','accepted_records')},
            'retry':{k:v for k,v in retry.items() if k not in ('grant_times','accepted_records')},
            'queue':{k:v for k,v in queue.items() if k not in ('grant_times','accepted_records')},
            'low_grants':low['granted'],'high_grants':high['granted'],
            'shuffled_grants':simulate(shuffled,'queue')['granted']}
if __name__=='__main__':print(json.dumps(evaluate(),sort_keys=True,indent=2))
