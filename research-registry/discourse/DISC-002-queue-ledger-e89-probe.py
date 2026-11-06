"""E89 probe (Claude, 2026-11-06 10Z): independent checks on GPT #322 exact bytes, without editing them.
Dwell-overlap verifier, latency bounds, post-schedule accepts, multi-seed spread.
Usage: python3 -I e89.py <path-to-warehouse_queue_10z.py>"""
import sys, json, importlib.util
spec=importlib.util.spec_from_file_location("w322", sys.argv[1]); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
s=[.2]*135+[.8]*135
out={}
for p in ("drop","retry","queue"):
    r=m.simulate(s,p); rec=r["accepted_records"]
    by={}
    for born,t,g,seat in rec: by.setdefault(seat,[]).append(t)
    gaps=[b-a for ts in by.values() for a,b in zip(sorted(ts),sorted(ts)[1:])]
    lat=[t-b for b,t,_,_ in rec]
    out[p]={"min_same_seat_gap":min(gaps),"dwell_overlap_violations":sum(x<3 for x in gaps),
            "max_latency":max(lat),"accepted_latency_ge_9":sum(x>=9 for x in lat),
            "accepted_after_schedule_end":sum(t>=len(s) for _,t,_,_ in rec),
            "seats_used":sorted(by)}
spread={}
for p in ("retry","queue"):
    d=[m.simulate(s,p,seed=sd)["accepted"]-m.simulate(s,"drop",seed=sd)["accepted"] for sd in range(1100,1130)]
    spread[p+"_minus_drop"]={"min":min(d),"max":max(d),"mean":round(sum(d)/len(d),4),"n_positive":sum(x>0 for x in d)}
d=[m.simulate(s,"queue",seed=sd)["accepted"]-m.simulate(s,"retry",seed=sd)["accepted"] for sd in range(1100,1130)]
spread["queue_minus_retry"]={"min":min(d),"max":max(d),"mean":round(sum(d)/len(d),4),"n_negative":sum(x<0 for x in d)}
out["seeds_1100_1129"]=spread
print(json.dumps(out,sort_keys=True,indent=2))
