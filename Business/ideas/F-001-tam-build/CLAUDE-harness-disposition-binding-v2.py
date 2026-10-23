import sys, json, csv, io, hashlib, subprocess, shutil, os
V, A = sys.argv[1], sys.argv[2]
PIN = hashlib.sha256(open(A,'rb').read()).hexdigest()
H = ["object","measured_g","units","registry_sign","stated_deviation_pct","term","expected_g","recomputed_deviation_pct","stated_matches_recomputed"]
os.makedirs("w", exist_ok=True)
def rows_of(p):
    return list(csv.reader(io.StringIO(open(p,'rb').read().decode('utf-8-sig'), newline='')))
def rec(csvp, lines=None, **over):
    r = rows_of(csvp); fl = [(i,row) for i,row in enumerate(r[1:],2) if row[-1]=="False"]
    if lines is not None: fl=[x for x in fl if x[0] in lines]
    d = {"record_version":2, "dataset_a_sha256":hashlib.sha256(open(csvp,'rb').read()).hexdigest(), "decision_reference":None,
         "rows":[{"csv_line":i, **{k:row[H.index(k)] for k in ("object","measured_g","units","stated_deviation_pct","recomputed_deviation_pct")},
                  "disposition":"RETAIN_STATED_WITH_DISCLOSURE","explanation":"SYNTHETIC test record, not an editorial decision"} for i,row in fl]}
    d.update(over); return d
def wj(n,d,raw=None):
    p=f"w/{n}.json"; open(p,'w').write(raw if raw is not None else json.dumps(d)); return p
def run(n, c, r, pin, exp):
    p = subprocess.run([sys.executable,"-I","-B",V,c,r,pin],capture_output=True,text=True)
    try: o=json.loads(p.stdout); st=o["status"]; b=o["binding"]; rel=o["release"]; fl=o["flagged_csv_lines"]
    except Exception: st=b=rel=fl="-"
    ok = (p.returncode, st) == exp
    print(f"{'PASS' if ok else 'FAIL'} {n:4} exit {p.returncode} {st}/{b}/{rel} {fl} {(o.get('errors') if st!='-' else p.stderr.strip()[-80:]) if True else ''}")
    return ok
res=[]
before=hashlib.sha256(open(A,'rb').read()).hexdigest()
res.append(run("V1","%s"%A,"w/none.json",PIN,(3,"PENDING")))
res.append(run("V2",A,wj("v2",rec(A)),PIN,(0,"RECORDED_UNAUTHENTICATED")))
res.append(run("V3",A,wj("v2",rec(A)),"0"*64,(1,"INVALID")))
res.append(run("V4",A,wj("v2",rec(A)),"abc",(1,"INVALID")))
res.append(run("V5",A,wj("v2",rec(A)),PIN.upper(),(0,"RECORDED_UNAUTHENTICATED")))
lf="w/a_lf.csv"; open(lf,'wb').write(open(A,'rb').read().replace(b"\r\n",b"\n"))
res.append(run("V6",lf,wj("v6",rec(lf)),PIN,(1,"INVALID")))  # re-encoded + re-bound vs original pin
res.append(run("V7",A,wj("v7",rec(A,lines=[6])),PIN,(1,"INVALID")))
d=rec(A); d["rows"][0]["csv_line"]-=1
res.append(run("V8",A,wj("v8",d),PIN,(1,"INVALID")))  # off-by-one
d=rec(A); d["rows"].append(dict(d["rows"][0]))
res.append(run("V9",A,wj("v9",d),PIN,(1,"INVALID")))  # duplicate
res.append(run("V10",A,wj("v10",rec(A,record_version=1)),PIN,(1,"INVALID")))
res.append(run("V11",A,wj("v11",None,raw='{"record_version":2,"record_version":2}'),PIN,(1,"INVALID")))
d=rec(A); d["rows"][0]["disposition"]="READY"
res.append(run("V12",A,wj("v12",d),PIN,(1,"INVALID")))
d=rec(A); d["rows"][0]["explanation"]="  "
res.append(run("V13",A,wj("v13",d),PIN,(1,"INVALID")))
clean="w/clean.csv"; r=rows_of(A); r=[r[0]]+[x[:-1]+["True"] for x in r[1:]]
s=io.StringIO(); csv.writer(s).writerows(r); open(clean,'w',newline='').write(s.getvalue()); CP=hashlib.sha256(open(clean,'rb').read()).hexdigest()
res.append(run("V14",clean,"w/none.json",CP,(0,"NO_FLAGGED_ROWS")))
res.append(run("V15",clean,wj("v15",rec(clean)),CP,(0,"NO_FLAGGED_ROWS")))
res.append(run("V16",clean,wj("v16",rec(A)),CP,(1,"INVALID")))  # record bound to other CSV
res.append(run("V17",A,"w",PIN,(1,"INVALID")))  # record path is a directory
d=rec(A); d["rows"][0]["csv_line"]=True
res.append(run("V18",A,wj("v18",d),PIN,(1,"INVALID")))
res.append(run("V19",A,wj("v19",None,raw="["*100000+"]"*100000),PIN,(1,"INVALID")))  # deep nesting
p=subprocess.run([sys.executable,"-I","-B",V,A,"x.json"],capture_output=True); print(("PASS" if p.returncode==64 else "FAIL"),"V20 usage exit",p.returncode); res.append(p.returncode==64)
print("pass", sum(res), "/", len(res), "| real CSV unchanged:", before==hashlib.sha256(open(A,'rb').read()).hexdigest())
