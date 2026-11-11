# Synthetic F-001 verifier fixtures; preregistered Issue #421 before execution.
# Exact verifier source: Git blob f63749b1d8a53b8282923d6c41ee156ff4fad1ab
import csv,hashlib,json,pathlib,subprocess,sys,tempfile
V=pathlib.Path(__file__).with_name('f001_release_verify_draft.py')
FILES=('book.pdf','book.epub','editorial.csv','rights.csv','qa.json','approvals.json')
def rehash(p):
    (p/'manifest.json').write_text(json.dumps({'sha256':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in FILES if (p/n).exists()}}))
def setup(p):
    (p/'book.pdf').write_bytes(b'%PDF synthetic');(p/'book.epub').write_bytes(b'PK synthetic')
    for name,n in [('editorial',82),('rights',70)]:
        with (p/(name+'.csv')).open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['item_id','decision','evidence_ref'])
            w.writerows((f'{name}-{i:03d}','PENDING',f'synthetic-{i}') for i in range(n))
    (p/'qa.json').write_text('{}');(p/'approvals.json').write_text('{}');rehash(p)
def mutate(p,i):
    if i==2:(p/'book.pdf').unlink()
    if i==3:(p/'book.pdf').unlink();(p/'book.pdf').symlink_to(p/'book.epub')
    if i==4:(p/'manifest.json').write_text('{"sha256":{},"sha256":{}}')
    if i==5:(p/'book.epub').write_bytes(b'TAMPER')
    if i==6:
        d=json.loads((p/'manifest.json').read_text());d['sha256']['book.pdf']='x'*64;(p/'manifest.json').write_text(json.dumps(d))
    if i in (7,8):
        q=p/'editorial.csv';s=q.read_text().splitlines()
        if i==7:s[-1]=s[-2]
        else:s[1]=s[1].replace('synthetic-0','')
        q.write_text('\n'.join(s)+'\n');rehash(p)
    if i==9:
        q=p/'rights.csv';q.write_text('\n'.join(q.read_text().splitlines()[:-1])+'\n');rehash(p)
    if i==10:(p/'qa.json').write_text('{bad');rehash(p)
EXPECTED=['','independent issuer authorization','missing/unsafe artifact','missing/unsafe artifact','duplicate JSON key','sha256 mismatch','bad sha256 syntax','duplicate item_id','incomplete editorial.csv','incomplete rights.csv','Expecting property name']
results=[]
for i in range(1,11):
    with tempfile.TemporaryDirectory() as d:
        p=pathlib.Path(d);setup(p);mutate(p,i)
        x=subprocess.run([sys.executable,'-I','-B',str(V),str(p)],capture_output=True,text=True,timeout=10)
        y=json.loads(x.stdout)
        results.append({'type':i,'passed':x.returncode==2 and y.get('status')=='HOLD' and EXPECTED[i] in y.get('reason',''),'exit':x.returncode,'reason':y.get('reason')})
print(json.dumps({'test_types':10,'passed':sum(x['passed'] for x in results),'results':results},indent=2))
