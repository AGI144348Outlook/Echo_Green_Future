import json,gzip
from nltk.corpus import wordnet as wn
def poss(w):
    s=set()
    for x in wn.synsets(w.replace(' ','_')): s.add({'s':'a'}.get(x.pos(),x.pos()))
    return ''.join(sorted(s))
upc={}
def up(name):
    if name in upc: return upc[name]
    s=wn.synset(name); out=[]
    cur=s
    while True:
        h=cur.hypernyms() or cur.instance_hypernyms()
        if not h: break
        cur=h[0]; out.append(cur.lemmas()[0].name().replace('_',' '))
        if len(out)>=14: break
    upc[name]=out; return out
def enrich(rows):
    for r in rows:
        s=wn.synset(r['syn'])
        r['ex']=[e[:160] for e in s.examples()[:2]]
        r['poss']=poss(r['w'])
        r['up']=up(r['syn']) if s.pos() in 'nv' else []
    return rows
st=enrich(json.load(open('starter.json')))
json.dump(st,open('starter.json','w'),separators=(',',':'))
full=json.loads(gzip.decompress(open('wordnet-full.json.gz','rb').read()))
full=enrich(full)
raw=json.dumps(full,separators=(',',':')).encode()
open('data/wordnet-full.json.gz','wb').write(gzip.compress(raw,9))
print(len(st), sum(1 for r in st if r['ex']), len(raw)//1024, 'KB raw full')
print(sum(1 for r in full if r['ex']),'full rows with examples')
