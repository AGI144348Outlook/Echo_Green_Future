"""Noncanonical independent ledger mutation oracle; prereg Issue #331 comment 6704782114."""
import json, hashlib
SEEDS=(1106,1107,1108,1109)
def arrivals(seed):
 s=seed; out=[]
 for t in range(32):
  s=(1664525*s+1013904223)&0xffffffff
  if s/4294967296 < .73:out.append(t)
 return out
def trace(seed):
 ids=arrivals(seed); ev=[]; queue=[]; seat=None; release=-1
 for t in range(45):
  if seat is not None and t>=release:ev.append([t,'release',seat]);seat=None
  if t in ids:ev.append([t,'arrival',t]);queue.append(t)
  while queue and t-queue[0]>=6:ev.append([t,'expire',queue.pop(0)])
  if seat is None and queue:seat=queue.pop(0);release=t+3;ev.append([t,'admit',seat])
 return ev

def audit(seed,events):
 expected=set(arrivals(seed)); seen=set();terminal=set();waiting=[];seat=None;started=None;errors=[];last=-1
 for t,k,i in events:
  if t<last or t>=45:errors.append('time_order_or_horizon')
  last=t
  if k=='arrival':
   if i not in expected or t!=i:errors.append('unknown_arrival')
   if i in seen:errors.append('duplicate_arrival')
   seen.add(i);waiting.append(i)
  elif k=='admit':
   if i not in seen or i in terminal:errors.append('unknown_admit')
   if seat is not None:errors.append('overlap')
   if not waiting or waiting[0]!=i:errors.append('fifo')
   if i in waiting:waiting.remove(i)
   seat=i;started=t
  elif k=='expire':
   if i not in waiting:errors.append('invalid_expiry')
   if i in waiting:waiting.remove(i)
   if i in terminal:errors.append('duplicate_terminal')
   terminal.add(i)
  elif k=='release':
   if seat!=i:errors.append('release_identity')
   if started is None or t-started!=3:errors.append('dwell')
   if i in terminal:errors.append('duplicate_terminal')
   terminal.add(i);seat=None;started=None
  else:errors.append('unknown_event')
 if seen!=expected:errors.append('census')
 if terminal!=expected:errors.append('terminal_census')
 if seat is not None:errors.append('open_seat')
 if waiting:errors.append('unresolved_queue')
 return sorted(set(errors))

def mutate(base,kind):
 e=[x[:] for x in base]
 def ix(k):return next(i for i,x in enumerate(e) if x[1]==k)
 if kind=='duplicate_arrival': e.insert(ix('arrival')+1,e[ix('arrival')][:])
 elif kind=='missing_arrival':e.pop(ix('arrival'))
 elif kind=='duplicate_terminal':j=next(i for i,x in enumerate(e) if x[1] in ('release','expire'));e.insert(j+1,e[j][:])
 elif kind=='missing_terminal':e.pop(next(i for i,x in enumerate(e) if x[1] in ('release','expire')))
 elif kind=='premature_release':j=ix('release');e[j][0]-=1
 elif kind=='delayed_release':j=ix('release');e[j][0]+=1
 elif kind=='seat_overlap':j=ix('admit');e.insert(j+1,[e[j][0],'admit',e[j][2]])
 elif kind=='fifo_reversal':j=ix('admit');e[j][2]=99999
 elif kind=='unknown_id':j=ix('arrival');e[j][2]=99999
 elif kind=='open_at_horizon':e.pop(max(i for i,x in enumerate(e) if x[1]=='release'))
 return e
TYPES=('duplicate_arrival','missing_arrival','duplicate_terminal','missing_terminal','premature_release','delayed_release','seat_overlap','fifo_reversal','unknown_id','open_at_horizon')
def main():
 rows=[]
 for seed in SEEDS:
  base=trace(seed);baseline=audit(seed,base)
  for typ in TYPES:
   mutant=mutate(base,typ);errs=audit(seed,mutant)
   rows.append({'seed':seed,'type':typ,'activated':mutant!=base,'detected':bool(errs),'errors':errs})
  rows.append({'seed':seed,'type':'baseline_noop','errors':baseline,'pass':not baseline})
 result={'schema':'echo-gpt-331-independent-oracle-v1','seeds':SEEDS,'types':TYPES,'rows':rows,'activated':sum(r.get('activated',False) for r in rows),'detected':sum(r.get('detected',False) for r in rows),'baseline_clean':sum(r.get('pass',False) for r in rows),'limitations':['oracle independently implemented but synthetic fixture shares event semantics','not real spatial coupling or learning','mutation families not independent statistical samples']}
 print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
