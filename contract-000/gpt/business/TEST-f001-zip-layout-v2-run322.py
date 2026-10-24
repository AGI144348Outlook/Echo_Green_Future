"""Run 322 preregistered M0-M9 synthetic ZIP32 checks; no external services."""
import hashlib, importlib.util, io, json, os, struct, sys, zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('f001_zipv2', BASE/'PROPOSED-f001-zip-layout-audit-v2.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
FIXED=(2024, 1, 2, 0, 0, 0)
EXTRA = struct.pack('<HHBI', 0x5455, 5, 1, 1700000000)

def write_members(z, chapter='OPS/c.xhtml', chapter_extra=b''):
    items = [
      ('mimetype', b'application/epub+zip', zipfile.ZIP_STORED),
      ('META-INF/container.xml', b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', zipfile.ZIP_DEFLATED),
      ('OPS/package.opf', ('<package xmlns="http://www.idpf.org/2007/opf"><metadata/><manifest><item id="c" href="'+chapter.removeprefix('OPS/')+'" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="c"/></spine></package>').encode(), zipfile.ZIP_DEFLATED),
      (chapter, b'<html xmlns="http://www.w3.org/1999/xhtml"><body><p>sample</p></body></html>', zipfile.ZIP_DEFLATED)]
    for name, payload, method in items:
        zi=zipfile.ZipInfo(name, FIXED);zi.compress_type=method
        if name==chapter: zi.extra=chapter_extra
        z.writestr(zi,payload)

def epub(chapter='OPS/c.xhtml', chapter_extra=b'', nonseekable=False):
    if nonseekable:
        class Sink(io.RawIOBase):
            def __init__(self): self.data=bytearray()
            def writable(self): return True
            def write(self, b): self.data.extend(b); return len(b)
        b=Sink()
        with zipfile.ZipFile(b, 'w') as z: write_members(z, chapter, chapter_extra)
        return bytes(b.data)
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z: write_members(z, chapter, chapter_extra)
    return b.getvalue()

def positions(data):
    eocd=data.rfind(b'PK\x05\x06'); assert eocd>=0
    cd_size, cd_off=struct.unpack_from('<II',data,eocd+12)
    cursor=cd_off; entries=[]
    while cursor<cd_off+cd_size:
        assert data[cursor:cursor+4]==b'PK\x01\x02'
        nlen,xlen,clen=struct.unpack_from('<HHH',data,cursor+28)
        name=data[cursor+46:cursor+46+nlen].decode()
        localoff=struct.unpack_from('<I',data,cursor+42)[0]
        comp=struct.unpack_from('<I',data,cursor+20)[0]
        entries.append(dict(pos=cursor,name=name,local=localoff,comp=comp,nlen=nlen,xlen=xlen,clen=clen))
        cursor+=46+nlen+xlen+clen
    assert cursor==eocd
    return eocd,cd_off,cd_size,entries

def add_local_extra():
    data=bytearray(epub());e,cd,size,entries=positions(data)
    last=entries[-1];loc=last['local'];nlen,xlen=struct.unpack_from('<HH',data,loc+26)
    insert=loc+30+nlen+xlen
    payload=EXTRA
    data[insert:insert]=payload
    struct.pack_into('<H',data,loc+28,xlen+len(payload))
    struct.pack_into('<I',data,e+len(payload)+16,cd+len(payload))
    return bytes(data)

def add_central_field(field):
    data=bytearray(epub());e,cd,size,entries=positions(data)
    last=entries[-1];pos=last['pos'];nlen=last['nlen'];xlen=last['xlen'];clen=last['clen']
    if field=='extra':
        offset=pos+46+nlen+xlen;payload=EXTRA;fieldpos=pos+30
    else:
        offset=pos+46+nlen+xlen+clen;payload=b'COMMENT';fieldpos=pos+32
    data[offset:offset]=payload
    struct.pack_into('<H',data,fieldpos,struct.unpack_from('<H',data,fieldpos)[0]+len(payload))
    struct.pack_into('<I',data,e+len(payload)+12,size+len(payload))
    return bytes(data)

def add_archive_comment():
    data=bytearray(epub());e,cd,size,entries=positions(data)
    data.extend(b'COMMENT');struct.pack_into('<H',data,e+20,7)
    return bytes(data)

def add_deflate_tail():
    data=bytearray(epub());e,cd,size,entries=positions(data)
    last=entries[-1];loc=last['local'];nlen,xlen=struct.unpack_from('<HH',data,loc+26)
    insert=loc+30+nlen+xlen+last['comp'];payload=b'TRAILING_PAYLOAD'
    data[insert:insert]=payload
    struct.pack_into('<I',data,loc+18,last['comp']+len(payload))
    struct.pack_into('<I',data,last['pos']+len(payload)+20,last['comp']+len(payload))
    struct.pack_into('<I',data,e+len(payload)+16,cd+len(payload))
    return bytes(data)

cases={
 'M0':(epub(),'PASS'),
 'M1':(add_local_extra(),'FAIL'),
 'M2':(add_central_field('extra'),'FAIL'),
 'M3':(add_central_field('comment'),'FAIL'),
 'M4':(add_archive_comment(),'FAIL'),
 'M5':(add_deflate_tail(),'FAIL'),
 'M6':(epub(chapter='OPS/c.xhtml.'),'FAIL'),
 'M7':(epub(chapter='OPS/a:b.xhtml'),'FAIL'),
 'M8':(epub(nonseekable=True),'PASS'),
 'M9':(epub(chapter_extra=EXTRA),'FAIL')
}
result={}
for label,(data,expected) in cases.items():
    before=hashlib.sha256(data).hexdigest()
    obs=mod.check_package_bytes(data)
    unchanged=hashlib.sha256(data).hexdigest()==before
    ok=obs['layout']==expected and obs['release']=='HOLD' and obs['readiness']=='BLOCKED' and obs['publication_authorization']=='ABSENT' and unchanged
    result[label]={'expected':expected,'observed':obs['layout'],'ok':ok,'issues':obs['issues'],'sha256':before,'bytes':len(data),'unchanged':unchanged}
summary={'schema':'f001-run322/v1','python':sys.version.split()[0],'source_sha256':hashlib.sha256((BASE/'PROPOSED-f001-zip-layout-audit-v2.py').read_bytes()).hexdigest(),'results':result,'passed':sum(x['ok'] for x in result.values()),'total':len(result)}
print(json.dumps(summary,indent=2,sort_keys=True))
if summary['passed']!=summary['total']:raise SystemExit(1)
