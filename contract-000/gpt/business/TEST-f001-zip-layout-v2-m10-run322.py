"""Prospectively added M10: malformed raw DEFLATE must fail closed, not crash."""
import hashlib, importlib.util, io, json, struct, sys, zipfile
from pathlib import Path
P=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('z322',P/'PROPOSED-f001-zip-layout-audit-v2.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
b=io.BytesIO()
with zipfile.ZipFile(b,'w') as z:
 for name, payload,method in [('mimetype',b'application/epub+zip',zipfile.ZIP_STORED),('OPS/c.xhtml',b'<html>content</html>',zipfile.ZIP_DEFLATED)]:
  zi=zipfile.ZipInfo(name,(2024,1,2,0,0,0));zi.compress_type=method;z.writestr(zi,payload)
data=bytearray(b.getvalue()); cd=data.find(b'PK\x01\x02'); second=data.find(b'PK\x01\x02',cd+4)
assert second>=0
loc=struct.unpack_from('<I',data,second+42)[0]
nlen,xlen=struct.unpack_from('<HH',data,loc+26)
start=loc+30+nlen+xlen
assert data[start:start+2]!=b'\xff\xff'
data[start:start+2]=b'\x07\xff'  # raw DEFLATE block type 3: invalid
frozen=bytes(data);before=hashlib.sha256(frozen).hexdigest()
try:
 obs=m.check_package_bytes(frozen)
 observed=obs['layout'];error=None
 ok=(observed=='FAIL' and obs['release']=='HOLD' and obs['readiness']=='BLOCKED')
except Exception as exc:
 observed='EXCEPTION';error=type(exc).__name__+': '+str(exc);ok=False
print(json.dumps({'case':'M10','expected':'FAIL/no exception','observed':observed,'error':error,'ok':ok,'sha256':before,'unchanged':hashlib.sha256(frozen).hexdigest()==before,'python':sys.version.split()[0]},indent=2))
if not ok:raise SystemExit(1)
