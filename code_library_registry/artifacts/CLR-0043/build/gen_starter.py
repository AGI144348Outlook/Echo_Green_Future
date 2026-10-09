import json
from nltk.corpus import wordnet as wn
out={}
def add(s,pos,score,depth):
    for l in s.lemmas()[:3]:
        w=l.name().replace('_',' ')
        if any(c.isdigit() for c in w) or len(w)>18: continue
        if w[0].isupper(): continue
        key=w.lower()
        if key in out and out[key]['score']<=score: continue
        hy=s.hypernyms()
        out[key]={'w':key,'pos':pos,'def':s.definition(),'depth':depth,
            'hyper':hy[0].lemmas()[0].name().replace('_',' ') if hy else '',
            'span':0,'score':score,'syn':s.name()}
# nouns & verbs: depth + descendant span
for pos,tag,maxd in (('n','noun',5),('v','verb',1)):
    for s in wn.all_synsets(pos):
        d=s.min_depth()
        if d>maxd: continue
        span=sum(1 for _ in s.closure(lambda x:x.hyponyms()))
        if span<(40 if pos=='n' else 25): continue
        score=d*1000-min(span,999)
        add(s,tag,score,d)
        for l in s.lemmas()[:3]:
            k=l.name().replace('_',' ').lower()
            if k in out and out[k]['syn']==s.name(): out[k]['span']=span
# adjectives/adverbs by usage frequency
for pos,tag in (('a','adjective'),('r','adverb')):
    c=[]
    for s in wn.all_synsets(pos):
        f=sum(l.count() for l in s.lemmas())
        if f>=60: c.append((f,s))
    for f,s in sorted(c,key=lambda x:-x[0])[:(90 if pos=='a' else 30)]:
        add(s,tag,1500-min(f,1000),None)
        k=s.lemmas()[0].name().lower()
        if k in out: out[k]['span']=f
rows=sorted(out.values(),key=lambda r:r['score'])
for i,r in enumerate(rows): r['rank']=i+1; del r['score']
print(len(rows)); print([ (r['w'],r['pos'],r['depth']) for r in rows[:40]])
from collections import Counter; print(Counter(r['pos'] for r in rows))
json.dump(rows,open('/home/claude/build/starter.json','w'),separators=(',',':'))
