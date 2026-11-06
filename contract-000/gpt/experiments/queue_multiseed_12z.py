"""Independent offline GPT queue 12Z reproducibility harness, preregistered Issue #324.
This is a compact source representation of the locally executed transcription;
not an independently fetched execution of #323's exact Git blob.
Run python3 contract-000/gpt/experiments/queue_multiseed_12z.py
"""
import json,random,statistics
def grants(schedule,seed):
 r=random.Random(seed)
 return [i for i,p in enumerate(schedule) if r.random()<max(0,min(1,p))]
def sim(schedule,policy,seed,cap=9):
 ids=grants(schedule,seed); arrivals=set(ids);live={};waiting=[];terminal={};accepted=[]
 for t in range(len(schedule)+12):
  live={s:(g,at) for s,(g,at) in live.items() if t-at<3}
  for row in waiting[:]:
   gid,born,g,s,tries=row
   if t-born>=cap:terminal[gid]=('EXPIRED',t);waiting.remove(row)
  if t in arrivals:waiting.append((t,t,t%27,t%2,0))
  if policy=='queue':active=waiting[:1];waiting=waiting[1:]
  else:active=waiting;waiting=[]
  for gid,born,g,s,tries in active:
   if t-born>=cap:terminal[gid]=('EXPIRED',t)
   elif s not in live and g not in [v[0] for v in live.values()]:
    live[s]=(g,t);terminal[gid]=('ACCEPTED',t);accepted.append((gid,born,t,g,s))
   elif policy=='drop':terminal[gid]=('DROPPED',t)
   elif policy=='retry':
    if tries<2:waiting.append((gid,born,g,s,tries+1))
    else:terminal[gid]=('DROPPED',t)
   else:waiting.append((gid,born,g,s,tries+1))
 for gid,born,g,s,tries in waiting:terminal[gid]=('END_PENDING',len(schedule)+12)
 return dict(ids=ids,terminal=terminal,accepted=accepted)
def oracle(r):
 ids=r['ids'];term=r['terminal'];a=r['accepted']
 return dict(ledger=len(ids)==len(set(ids))==len(term) and set(ids)==set(term) and len({x[0] for x in a})==len(a) and all(term[x[0]][0]=='ACCEPTED' for x in a),
 age=all(t-b<9 for _,b,t,_,_ in a),
 overlap=all(s!=s2 or abs(t-t2)>=3 for i,(_,_,t,_,s) in enumerate(a) for _,_,t2,_,s2 in a[i+1:]),
 count=len(a),max_wait=max((t-b for _,b,t,_,_ in a),default=0),
 mean_wait=statistics.mean((t-b for _,b,t,_,_ in a)) if a else 0,
 expired=sum(v[0]=='EXPIRED' for v in term.values()),dropped=sum(v[0]=='DROPPED' for v in term.values()),pending=sum(v[0]=='END_PENDING' for v in term.values()))
def evaluate():
 schedule=[.2]*135+[.8]*135;seeds=range(1100,1130);rows=[]
 for seed in seeds:
  r={p:sim(schedule,p,seed) for p in ('drop','retry','queue')}
  rows.append(dict(seed=seed,**{p:oracle(r[p]) for p in r},same=r['drop']['ids']==r['retry']['ids']==r['queue']['ids'],replay=r['queue']==sim(schedule,'queue',seed)))
 sh=schedule[:];random.Random(55).shuffle(sh)
 checks={
 'ledger':all(row[p]['ledger'] for row in rows for p in ('drop','retry','queue')),
 'age':all(row[p]['age'] for row in rows for p in ('drop','retry','queue')),
 'overlap':all(row[p]['overlap'] for row in rows for p in ('drop','retry','queue')),
 'common_grants':all(row['same'] for row in rows),
 'zero':not grants([0]*270,1106),
 'replay':all(row['replay'] for row in rows),
 'rate':all(len(grants([.9]*270,s))>len(grants([.1]*270,s)) for s in seeds),
 'shuffle':all(grants(sh,s)!=grants(schedule,s) for s in seeds),
 'retry_vs_drop':all(row['retry']['count']>=row['drop']['count'] for row in rows),
 'queue_age_pending':all(row['queue']['max_wait']<9 and row['queue']['pending']==0 for row in rows)}
 return dict(issue=324,checks=checks,passed=sum(checks.values()),total=len(checks),
  metrics={p:dict(mean_accepted=statistics.mean(row[p]['count'] for row in rows),min_accepted=min(row[p]['count'] for row in rows),max_accepted=max(row[p]['count'] for row in rows),expired=sum(row[p]['expired'] for row in rows),dropped=sum(row[p]['dropped'] for row in rows),max_wait=max(row[p]['max_wait'] for row in rows)) for p in ('drop','retry','queue')})
if __name__=='__main__':print(json.dumps(evaluate(),indent=2,sort_keys=True))
