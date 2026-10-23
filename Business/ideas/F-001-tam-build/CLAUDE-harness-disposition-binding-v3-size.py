# Usage (scratch folder): python3 -I -B CLAUDE-harness-disposition-binding-v3-size.py <parser.py> <dataset-a.csv>
# Claude extra cases for GPT v3 (size bound); synthetic records only
import sys, json, subprocess, hashlib, os, csv, io
V, A = sys.argv[1], sys.argv[2]
PIN = hashlib.sha256(open(A,'rb').read()).hexdigest()
# rec()/rows_of()/H are taken unchanged from CLAUDE-harness-disposition-binding-v2.py in the same folder
_h=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'CLAUDE-harness-disposition-binding-v2.py')).read()
os.makedirs('w',exist_ok=True); exec(_h[_h.index('H = ['):_h.index('def wj')])
def run(n, rp, exp, timeout=20):
    try:
        p = subprocess.run([sys.executable,"-I","-B",V,A,rp,PIN],capture_output=True,text=True,timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"{'PASS' if exp=='TIMEOUT' else 'FAIL'} {n} TIMEOUT after {timeout}s"); return exp=='TIMEOUT'
    try: o=json.loads(p.stdout); st=o["status"]; err=o.get("errors")
    except Exception: st='-'; err=p.stderr.strip()[-100:]
    ok=(p.returncode,st)==exp; print(f"{'PASS' if ok else 'FAIL'} {n} exit {p.returncode} {st} {err}"); return ok
base=json.dumps(rec(A)).encode()
res=[]
for n,size,exp in [("S1",1048576,(0,"RECORDED_UNAUTHENTICATED")),("S2",1048577,(1,"INVALID"))]:
    p=f"w/{n}.json"; open(p,'wb').write(base+b" "*(size-len(base))); assert os.path.getsize(p)==size
    res.append(run(n,p,exp))
p="w/S3.json"; k=(1048576-2)//2; open(p,'w').write("["*k+"]"*k); res.append(run("S3 deep within 1 MiB",p,(1,"INVALID")))
os.path.exists("w/fifo") and os.remove("w/fifo"); os.mkfifo("w/fifo")
# FIFO: stat size 0; nobody writes, so read blocks -> characterizes the stat/read gap (no data stream used)
res.append(run("S4 fifo (no writer)","w/fifo","TIMEOUT",timeout=5))
print("pass",sum(res),"/",len(res))
