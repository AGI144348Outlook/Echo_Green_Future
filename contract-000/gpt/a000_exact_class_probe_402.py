import ast, pathlib, types
source=pathlib.Path(__file__).with_name('a000_resh_exact_source_excerpt_402.py').read_text()
module=ast.parse(source)
node=next(x for x in module.body if isinstance(x,ast.ClassDef) and x.name=='ReshIdentity')
code=compile(ast.Module(body=[node],type_ignores=[]),'pinned-Genesis-excerpt','exec')
ns={};exec(code,ns);ReshIdentity=ns['ReshIdentity']
class M:
 def __init__(self): self.known={'A-000':{'name':'Governor','status':'ACTIVE'}}
class L:
 def __init__(self, words): self.agents={'resh':types.SimpleNamespace(definition_words=words)}
checks=[]
def check(name,ok):
 checks.append((name,bool(ok)));print(('PASS' if ok else 'FAIL'),name)
m=M();l=L(['before']);r=ReshIdentity(m,l)
check('pre-anchor invalid',r.validate() is False)
r.anchor();first=r._anchor_entry
check('first anchor valid',r.validate() is True)
check('first alias same reference',first is m.known['A-000-RESH'])
r.anchor();second=r._anchor_entry
check('re-anchor replaces alias',second is not first)
check('successful reanchor reference coherent',second is m.known['A-000-RESH'])
l.agents['resh'].definition_words=None
try:r.anchor();failure=False
except TypeError:failure=True
check('reanchor raises TypeError',failure)
check('failed reanchor keeps valid flag',r.validate() is True)
check('failed reanchor leaves stale anchor entry',r._anchor_entry is not m.known['A-000-RESH'])
check('failed reanchor replaces current alias',m.known['A-000-RESH'] is not second)
check('no class-local failure log',not any('failure' in x or 'receipt' in x or 'witness' in x for x in vars(r)))
check('failed reanchor does not clear anchored',r._anchored is True)
# contrast first failure
m2=M();r2=ReshIdentity(m2,L(None))
try:r2.anchor();ff=False
except TypeError:ff=True
check('first anchor fails',ff)
check('first failure invalid',r2.validate() is False)
check('first failure leaves alias', 'A-000-RESH' in m2.known)
# recovery
l.agents['resh'].definition_words=[]
r.anchor()
check('retry valid',r.validate() is True)
check('retry coherent alias ref',r._anchor_entry is m.known['A-000-RESH'])
print(f'{sum(x[1] for x in checks)}/{len(checks)} PASS')
assert all(x[1] for x in checks)
