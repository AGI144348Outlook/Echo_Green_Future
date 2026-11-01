#!/usr/bin/env node
// F-001 H3b candidate, DRAFT / UNTESTED. No publication-rights approval.
// A trusted, non-writable evidence root is REQUIRED. Parent-directory replacement
// races remain possible; this is not a sandbox for hostile mutable directories.
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const C=fs.constants;
const reject=(reason)=>({status:'REJECT',reason,rights_clearance:'NOT_DETERMINED',release:'HOLD'});
function check(root,record){
  if(!record||typeof record!=='object'||Array.isArray(record))return reject('record missing');
  if(typeof record.ref!=='string'||!record.ref.trim())return reject('reference missing');
  if(typeof record.document_sha256!=='string'||!/^[a-f0-9]{64}$/i.test(record.document_sha256))return reject('invalid digest');
  if(typeof record.file!=='string'||!record.file.trim())return reject('unsafe evidence path');
  // Reject both POSIX and Windows path syntax regardless of host.
  if(path.posix.isAbsolute(record.file)||path.win32.isAbsolute(record.file)||record.file.includes('\\')||record.file.includes(':'))return reject('unsafe evidence path');
  const segments=record.file.split('/');
  if(segments.some(s=>!s||s==='.'||s==='..'))return reject('unsafe evidence segment');
  const base=path.resolve(root),target=path.resolve(base,...segments);
  if(!target.startsWith(base+path.sep))return reject('evidence outside root');
  let fd;
  try {
    // Source-root and intermediate components must be real directories.
    if(!fs.lstatSync(base).isDirectory())return reject('invalid evidence root');
    let current=base;
    for(const seg of segments.slice(0,-1)){
      current=path.join(current,seg);
      if(!fs.lstatSync(current).isDirectory())return reject('unsafe evidence directory');
    }
    // O_NOFOLLOW protects final component only, where supported.
    if(typeof C.O_NOFOLLOW!=='number')return reject('O_NOFOLLOW unavailable');
    fd=fs.openSync(target,C.O_RDONLY|C.O_NOFOLLOW|C.O_NONBLOCK);
    const st=fs.fstatSync(fd);
    if(!st.isFile())return reject('not a regular file');
    // Bounded evidence documents: fail closed rather than unlimited allocation.
    if(st.size>16*1024*1024)return reject('evidence exceeds 16MiB limit');
    const chunks=[],buffer=Buffer.allocUnsafe(65536);
    let total=0,n;
    while((n=fs.readSync(fd,buffer,0,buffer.length,null))>0){
      total+=n;if(total>16*1024*1024)return reject('evidence exceeds 16MiB limit');
      chunks.push(Buffer.from(buffer.subarray(0,n)));
    }
    const digest=crypto.createHash('sha256').update(Buffer.concat(chunks)).digest('hex');
    if(digest!==record.document_sha256.toLowerCase())return reject('evidence bytes mismatch');
    return {status:'HUMAN_REVIEW_REQUIRED',reason:'bytes match; human authority, scope, provenance and rights unverified',ref:record.ref,verified_sha256:digest,byte_integrity:'MATCH',rights_clearance:'NOT_DETERMINED',release:'HOLD'};
  }catch(e){return reject('evidence unreadable or missing');}
  finally{if(fd!==undefined)fs.closeSync(fd);}
}
module.exports={check};
if(require.main===module){console.error('Draft library-only verifier: import check(root,record). No release authorization.');process.exitCode=2;}
