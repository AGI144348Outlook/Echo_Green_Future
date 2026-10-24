"""Run 321 K0-K7 synthetic ZIP layout preflight checks; no external services."""
import hashlib
import importlib.util
import io
import json
import struct
import zipfile

SRC='/mnt/data/PROPOSED-f001-zip-layout-audit-v1.py'
spec=importlib.util.spec_from_file_location('layout321', SRC)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def members(z, mime_type=zipfile.ZIP_STORED, mime=b'application/epub+zip'):
    z.writestr(zipfile.ZipInfo('mimetype'), mime, compress_type=mime_type)
    z.writestr('META-INF/container.xml', b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
    z.writestr('OPS/package.opf', b'<package xmlns="http://www.idpf.org/2007/opf"><metadata/><manifest><item id="c" href="c.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="c"/></spine></package>', compress_type=zipfile.ZIP_DEFLATED)
    z.writestr('OPS/c.xhtml', b'<html xmlns="http://www.w3.org/1999/xhtml"><body><p>x</p></body></html>', compress_type=zipfile.ZIP_DEFLATED)


def epub(**kw):
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z: members(z,**kw)
    return b.getvalue()


def split(data):
    e=data.rfind(b'PK\x05\x06'); size, off=struct.unpack_from('<II',data,e+12)
    return data[:off],data[off:off+size],bytearray(data[e:e+22])

PAY=b'X'*4096

def k1():
    body,cd,eocd=split(epub());struct.pack_into('<I',eocd,16,len(body)+len(PAY))
    return body+PAY+cd+bytes(eocd)

def k2():
    d=epub();body,cd,eocd=split(d);struct.pack_into('<I',eocd,16,len(d)+len(PAY))
    return d+PAY+cd+bytes(eocd)

def k4():
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:
        members(z);z.writestr('OPS2',b'file');z.writestr(zipfile.ZipInfo('OPS2/'),b'')
    return b.getvalue()


def k5():
    class NS(io.RawIOBase):
        def __init__(self):self.b=bytearray()
        def writable(self):return True
        def write(self,x):self.b+=x;return len(x)
    s=NS()
    with zipfile.ZipFile(s,'w') as z:members(z)
    return bytes(s.b)


def k6():
    d=bytearray(k5());idx=d.find(b'PK\x07\x08')
    assert idx>0,'descriptor signature not found'
    d[idx+4]^=1
    return bytes(d)


cases={'K0':(epub(),'PASS'),'K1':(k1(),'FAIL'),'K2':(k2(),'FAIL'),
       'K3':(epub(mime_type=zipfile.ZIP_DEFLATED,mime=b'text/plain'),'FAIL'),
       'K4':(k4(),'FAIL'),'K5':(k5(),'PASS'),'K6':(k6(),'FAIL'),
       'K7':(epub()+b'EXTRA','FAIL')}
results={}
for key,(data,expected) in cases.items():
    before=hashlib.sha256(data).hexdigest()
    actual=m.check_package_bytes(data)
    unchanged=hashlib.sha256(data).hexdigest()==before
    ok=actual['layout']==expected and actual['release']=='HOLD' and actual['readiness']=='BLOCKED' and unchanged
    results[key]={'expected':expected,'observed':actual['layout'],'ok':ok,
                  'issues':actual['issues'],'sha256':before,'unchanged':unchanged,'bytes':len(data)}
print(json.dumps({'schema':'f001-zip-layout-run321','results':results,'passed':sum(x['ok'] for x in results.values()),'total':len(results)},indent=2,sort_keys=True))
if not all(x['ok'] for x in results.values()):raise SystemExit(1)
