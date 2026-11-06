"""E86 (Claude, 2026-11-06 07Z): source-text injection into exact #318 blob 5831f6a3 (commit 15ce0b7b).
Same method as #318 run(): replace one unique anchor in the text before 'def run():', exec, call unchanged tests().
A crash in tests() counts as caught. Stdlib only, offline."""
import json,sys,hashlib
src=open(sys.argv[1],encoding="utf8").read()
prefix,sep,suffix=src.partition("def run():")
M={
 "E1_drop_glyph_dup_guard":("if g in self.occupied or s in self.occupied.values():return False","if s in self.occupied.values():return False"),
 "E2_drop_seat_dup_guard":("if g in self.occupied or s in self.occupied.values():return False","if g in self.occupied:return False"),
 "E3_drop_range_guard":("if g not in range(N) or s not in range(N):return False","pass"),
 "E4_drop_leave_guard":("if g not in self.occupied:return False","pass"),
 "E5_coupling_sign":("math.sin(math.radians(prior-phases[j]))","math.sin(math.radians(phases[j]-prior))"),
 "E6_coupling_self":("j=(k+1)%7","j=(k+3)%7"),
 "E7_step_size":("phases[k]=(prior+360/N)%360","phases[k]=(prior+360/7)%360"),
 "E8_coupling_off":("phases[j]=(phases[j]+coupling*math.sin","phases[j]=(phases[j]+0*math.sin"),
 "E9_tick_double":("self.occupied[g]=s;self.ticks+=1","self.occupied[g]=s;self.ticks+=2"),
 "E10_seed_shift":("def events(schedule,seed=1106):","def events(schedule,seed=1107):"),
 "E11_domain_key":("k=t%7;prior=phases[k]","k=(t//7)%7;prior=phases[k]"),
 "E12_leave_keeps_views":("for v in self.views:v.pop(s,None)","pass"),
 "C1_equiv_float":("return (self.ticks%N)*360/N","return (self.ticks%N)*360.0/N"),
 "C2_equiv_clamp_in_domain":("rng.random()<max(0,min(1,e))","rng.random()<e"),
}
out={}
for name,(old,new) in M.items():
 c=prefix.count(old)
 if c!=1: out[name]={"error":"nonunique_or_missing","count":c};continue
 ns={"__name__":"e86","__file__":sys.argv[1]}
 try:
  exec(compile(prefix.replace(old,new,1)+sep+suffix,sys.argv[1],"exec"),ns)
  r,_=ns["tests"]();f=[k for k,v in r.items() if not v]
  out[name]={"caught":bool(f),"failed":f}
 except Exception as e: out[name]={"caught":True,"crash":type(e).__name__}
print(json.dumps({"source_sha256":hashlib.sha256(src.encode()).hexdigest(),"results":out,
 "caught":sorted(k for k,v in out.items() if v.get("caught")),"survived":sorted(k for k,v in out.items() if v.get("caught") is False)},sort_keys=True,indent=1))
