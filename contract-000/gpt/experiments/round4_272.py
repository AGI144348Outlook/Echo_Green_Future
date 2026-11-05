import json,random,sys
OPS={'א':'init','ר':'govern','ת':'seal','ע':'perceive','ג':'traverse','פ':'express','ד':'filter','מ':'flow','ל':'direct'}
class Invalid(Exception):pass
def execute(seq,inp=7):
 s={'value':inp,'buffer':None,'initialized':False,'governed':False,'sealed':False,'trace':[],'output':None}
 try:
  for g in seq:
   if g not in OPS:raise Invalid('unknown glyph')
   if s['sealed']:raise Invalid('after seal')
   op=OPS[g]
   if op=='init':
    if s['initialized']:raise Invalid('double init')
    s['initialized']=True
   elif op=='govern':
    if not s['initialized'] or s['governed']:raise Invalid('govern precondition')
    s['governed']=True
   elif op=='seal':
    if not s['governed']:raise Invalid('seal precondition')
    s['sealed']=True
   elif op=='perceive':s['buffer']=s['value']
   elif op=='traverse':
    if s['buffer'] is None:raise Invalid('traverse precondition')
    s['buffer']+=1
   elif op=='express':
    if s['buffer'] is None:raise Invalid('express precondition')
    s['output']=s['buffer']
   elif op=='filter':s['buffer']=max(0,s['value'])
   elif op=='flow':
    if s['buffer'] is None:raise Invalid('flow precondition')
    s['buffer']*=2
   elif op=='direct':
    if s['buffer'] is None:raise Invalid('direct precondition')
    s['value']=s['buffer']
   s['trace'].append(op)
  return {'ok':True,'state':s}
 except Invalid as e:return {'ok':False,'error':str(e),'state':None}
def run():
 tests={}
 tests['01_registry']={'pass':len(OPS)==9 and len(set(OPS.values()))==9}
 a=execute('ארת');tests['02_ארת']={'pass':a['ok'] and a['state']['sealed'] and a['state']['governed'],'trace':a['state']['trace']}
 b=execute('עגפ');tests['03_עגפ']={'pass':b['ok'] and b['state']['output']==8,'trace':b['state']['trace']}
 c=execute('דמל',-3);tests['04_דמל']={'pass':c['ok'] and c['state']['value']==0,'trace':c['state']['trace']}
 sh=execute('תרא');tests['05_shuffle']={'pass':not sh['ok'],'error':sh.get('error')}
 ab=execute('את');tests['06_ablation']={'pass':not ab['ok'],'error':ab.get('error')}
 tests['07_replay']={'pass':execute('עגפ')==execute('עגפ')}
 x=execute('דמל',-3);y=execute('דמל',9);tests['08_isolation']={'pass':x['state']['value']==0 and y['state']['value']==18}
 unk=execute('אב');tests['09_unknown_fail_closed']={'pass':not unk['ok'] and unk['state'] is None}
 rng=random.Random(272);samples=[''.join(rng.choice('ארתעגפדמל') for _ in range(3)) for _ in range(500)]
 outcomes=[execute(s) for s in samples];accepted=sum(o['ok'] for o in outcomes)
 tests['10_random_control']={'pass':all(o['state'] is None for o in outcomes if not o['ok']),'accepted':accepted,'total':len(samples),'acceptance_rate':accepted/len(samples),'unique_accepted':len(set(s for s,o in zip(samples,outcomes) if o['ok']))}
 return {'issue':272,'python':sys.version.split()[0],'tests':tests,'limitations':'Toy operator semantics explicitly authored; permissive cross-family sequencing; no learning or semantic emergence.'}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
