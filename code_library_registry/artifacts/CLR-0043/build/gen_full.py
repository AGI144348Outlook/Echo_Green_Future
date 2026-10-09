import json,gzip,sys
from nltk.corpus import wordnet as wn
sys.setrecursionlimit(100000)
memo={}
def span(s):
    if s in memo: return memo[s]
    memo[s]=0
    n=sum(span(h)+1 for h in s.hyponyms()); memo[s]=n; return n
P={'n':'noun','v':'verb','a':'adjective','s':'adjective','r':'adverb'}
out={}
for s in wn.all_synsets():
    p=s.pos()
    if p in 'nv':
        d=s.min_depth(); sp=span(s); score=d*100000-min(sp,99999)
    else:
        f=sum(l.count() for l in s.lemmas()); d=None; sp=f; score=1500-min(f,1000)+ (0 if f else 600000)
    hy=s.hypernyms()
    for i,l in enumerate(s.lemmas()):
        w=l.name().replace('_',' ').lower()
        sc=score+i  # later lemmas slightly less central
        if w in out and out[w][0]<=sc: continue
        out[w]=(sc,{'w':w,'pos':P[p],'def':s.definition()[:200],'depth':d,
          'hyper':hy[0].lemmas()[0].name().replace('_',' ') if hy else '','span':sp,'syn':s.name()})
rows=[r for _,r in sorted(out.values(),key=lambda x:x[0])]
for i,r in enumerate(rows): r['rank']=i+1
raw=json.dumps(rows,separators=(',',':')).encode()
open('wordnet-full.json.gz','wb').write(gzip.compress(raw,9))
print(len(rows),len(raw)//1024,'KB raw')
