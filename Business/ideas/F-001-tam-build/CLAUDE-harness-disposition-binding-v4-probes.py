# Usage (scratch folder): python3 -I -B CLAUDE-harness-disposition-binding-v4-probes.py <parser.py> <dataset-a.csv> <path to CLAUDE-harness-disposition-binding-v2.py>
# Claude extra probes P1-P6 for GPT v4 (broken-symlink record, symlinked parent, CSV as FIFO/directory/symlink, 64 MiB CSV); synthetic records only, writes only under ./w
import csv, io, sys, json, subprocess, hashlib, os, time, resource
V, A = sys.argv[1], sys.argv[2]
exec(open(sys.argv[3]).read()[open(sys.argv[3]).read().index('H = ['):open(sys.argv[3]).read().index('def wj')])
PIN = hashlib.sha256(open(A,'rb').read()).hexdigest()
os.makedirs('w', exist_ok=True)
good = 'w/good.json'; open(good,'w').write(json.dumps(rec(A)))
def run(n, csvp, rp, pin=PIN, t=4):
    t0=time.time()
    try: p=subprocess.run([sys.executable,'-I','-B',V,csvp,rp,pin],capture_output=True,text=True,timeout=t)
    except subprocess.TimeoutExpired: print(n,'TIMEOUT', t,'s'); return
    try: o=json.loads(p.stdout); print(n,'exit',p.returncode,o['status'],o['errors'],f'{time.time()-t0:.2f}s')
    except Exception: print(n,'exit',p.returncode,'no JSON',p.stderr.strip()[-120:])
# P1 broken symlink as record
os.path.lexists('w/broken') or os.symlink('w/nonexistent.json','w/broken'); run('P1 record=broken symlink',A,'w/broken')
# P2 record under a symlinked parent directory
os.makedirs('w/real',exist_ok=True); open('w/real/r.json','w').write(open(good).read())
os.path.lexists('w/linkdir') or os.symlink(os.path.abspath('w/real'),'w/linkdir'); run('P2 record via symlinked parent dir',A,'w/linkdir/r.json')
# P3 CSV as FIFO with no writer
os.path.exists('w/csvfifo') or os.mkfifo('w/csvfifo'); run('P3 csv=FIFO (no writer)','w/csvfifo',good)
# P4 CSV as directory
run('P4 csv=directory','w/real',good)
# P5 CSV via symlink to the real file
os.path.lexists('w/csvlink') or os.symlink(os.path.abspath(A),'w/csvlink'); run('P5 csv=symlink to real A','w/csvlink',good)
# P6 oversized regular CSV (64 MiB of zeros, pin of that file): read fully before rejection
big='w/big.csv'; open(big,'wb').write(b'\0'*(64<<20)); bp=hashlib.sha256(open(big,'rb').read()).hexdigest()
run('P6 csv=64 MiB regular (own pin)',big,good,pin=bp,t=20)
os.remove(big)
