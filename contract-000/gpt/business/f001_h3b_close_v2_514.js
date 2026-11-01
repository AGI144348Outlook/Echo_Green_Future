'use strict';
// F-001 H3b-close-v2 DRAFT. Untested. Trusted immutable evidence root required.
// Parent-directory replacement is NOT prevented. No rights/publication clearance.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const C=fs.constants;
const reject=reason=>({status:'REJECT',reason,rights_clearance:'NOT_DETERMINED',release:'HOLD'});
function check(root,record,io=fs){
  if(!record||typeof record!=='object'||Array.isArray(record))return reject('record missing');
  if(typeof record.ref!=='string'||!record.ref.trim())return reject('reference missing');
  if(typeof record.document_sha256!=='string'||!/^[a-f0-9]{64}$/i.test(record.document_sha256))return reject('invalid digest');
  if(typeof record.file!=='string'||!record.file.trim())return reject('unsafe evidence path');
  if(path.posix.isAbsolute(record.file)||path.win32.isAbsolute(record.file)||record.file.includes('\\')||record.file.includes(':'))return reject('unsafe evidence path');
  const segments=record.file.split('/');
  if(segments.some(s=>!s||s==='.'||s==='..'))return reject('unsafe evidence segment');
  const base=path.resolve(root),target=path.resolve(base,...segments);
  if(!target.startsWith(base+path.sep))return reject('evidence outside root');
  let fd, result;
  try {
    if(!io.lstatSync(base).isDirectory())result=reject('invalid evidence root');
    if(!result){
      let current=base;
      for(const seg of segments.slice(0,-1)){
        current=path.join(current,seg);
        if(!io.lstatSync(current).isDirectory()){result=reject('unsafe evidence directory');break;}
      }
    }
    if(!result&&typeof C.O_NOFOLLOW!=='number')result=reject('O_NOFOLLOW unavailable');
    if(!result){
      fd=io.openSync(target,C.O_RDONLY|C.O_NOFOLLOW|C.O_NONBLOCK);
      const st=io.fstatSync(fd);
      if(!st.isFile())result=reject('not a regular file');
      else if(st.size>16*1024*1024)result=reject('evidence exceeds 16MiB limit');
      else{
        const hash=crypto.createHash('sha256'),buf=Buffer.allocUnsafe(65536);
        let total=0,n;
        while((n=io.readSync(fd,buf,0,buf.length,null))>0){
          total+=n;
          if(total>16*1024*1024){result=reject('evidence exceeds 16MiB limit');break;}
          hash.update(buf.subarray(0,n));
        }
        if(!result){
          const digest=hash.digest('hex');
          result=digest!==record.document_sha256.toLowerCase()?reject('evidence bytes mismatch'):
            {status:'HUMAN_REVIEW_REQUIRED',reason:'bytes match; rights, provenance and authority unverified',ref:record.ref,verified_sha256:digest,byte_integrity:'MATCH',rights_clearance:'NOT_DETERMINED',release:'HOLD'};
        }
      }
    }
  }catch(e){result=reject('evidence unreadable or missing');}
  // Close happens after all decisions; never return from finally. A close error
  // forces HOLD/REJECT but retains the earlier reason for diagnostic review.
  if(fd!==undefined){
    try{io.closeSync(fd);}
    catch(e){result={...reject('evidence descriptor close failed'),prior_reason:result?.reason||'unknown'};}
  }
  return result||reject('verification incomplete');
}
module.exports={check};
