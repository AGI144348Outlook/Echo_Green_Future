"""DISC-002 E38 probe (Claude, 2026-10-29T12Z; not pre-registered).
Tie-breaking in the actual SubAgentMatrix.predict_next of Genesis src/echo_governor_skeleton.py
(blob 63eb982). Only the SubAgentMatrix class is taken from the file (via ast) and run with a stub
parent; nothing else in Genesis is imported or executed. Usage: python3 -I this.py <echo_governor_skeleton.py>"""
import sys, ast
from collections import defaultdict
full=open(sys.argv[1]).read()
node=next(n for n in ast.parse(full).body if isinstance(n,ast.ClassDef) and n.name=='SubAgentMatrix')
src=ast.get_source_segment(full,node)
ns={'defaultdict':defaultdict}
exec(compile(src,'SubAgentMatrix@63eb982','exec'),ns)
Sub=ns['SubAgentMatrix']
class Parent:
    def __init__(s,order):
        s.transitions=defaultdict(lambda: defaultdict(int)); s.cooccurrence=defaultdict(lambda: defaultdict(int)); s.content_units={}
        for w in order: s.transitions['a'][w]+=1
    def index_content(s,text,category=None): pass
    def related_words(s,t): return set()
res={}
for order in (['x','y'],['y','x']):
    p=Parent(order)
    c=Sub('R',{'q'},p)         # 'a' not in domain: no seed
    res['parent '+''.join(order)+', no child obs']=c.predict_next('a')
    c2=Sub('R',{'a'},p)        # 'a' in domain: seeded copy of both
    res['parent '+''.join(order)+', seeded']=c2.predict_next('a')
# child-only tie: parent knows nothing for 'b'; child sees b->m then b->n
p=Parent([]); c=Sub('R',{'b'},p)
c.index_content('b m'); c.index_content('b n')
res['child-only b: m then n']=c.predict_next('b')
p=Parent([]); c=Sub('R',{'b'},p)
c.index_content('b n'); c.index_content('b m')
res['child-only b: n then m']=c.predict_next('b')
# non-dyadic weight: can rounding break an arithmetic tie? g1+c1*w vs g2+c2*w
import itertools
cnt=0;tot=0
for w in (1.1,1.3,0.7,2.0):
    for g1,c1,g2,c2 in itertools.product(range(0,12),repeat=4):
        if (c1-c2)!=0 and abs((g2-g1)/(c1-c2)-w)<1e-12:  # exact tie in reals
            tot+=1
            if g1+c1*w != g2+c2*w: cnt+=1
res['real ties with float mismatch (w in 1.1,1.3,0.7,2.0; counts 0..11)']=f'{cnt}/{tot}'
for k,v in res.items(): print(k,'->',v)
