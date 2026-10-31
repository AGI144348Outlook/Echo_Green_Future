#!/usr/bin/env node
// F-001 H3 PROPOSED evidence-byte gate. Does NOT grant rights or authorize release.
// Offline, read-only. Does not follow symlinks or allow evidence paths outside root.
// No execution tests performed at creation; preregister before testing.
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
function reject(reason){return {status:'REJECT',reason,rights_clearance:'NOT_DETERMINED',release:'HOLD'};}
function hold(reason,extra={}){return {status:'HUMAN_REVIEW_REQUIRED',reason,rights_clearance:'NOT_DETERMINED',release:'HOLD',...extra};}
function check(root,record){
  if(!record||typeof record!=='object')return reject('record missing');
  if(typeof record.ref!=='string'||!record.ref.trim())return reject('reference missing');
  if(typeof record.document_sha256!=='string'||!/^[a-f0-9]{64}$/i.test(record.document_sha256))return reject('invalid digest');
  if(typeof record.file!=='string'||!record.file.trim()||path.isAbsolute(record.file))return reject('unsafe evidence path');
  const segments=record.file.split(/[\\/]/);
  if(segments.some(s=>s===''||s==='.'||s==='..'))return reject('unsafe evidence segment');
  const base=path.resolve(root),target=path.resolve(base,record.file);
  if(!target.startsWith(base+path.sep))return reject('evidence outside root');
  try{
    let cur=base;
    for(const seg of segments){cur=path.join(cur,seg);if(fs.lstatSync(cur).isSymbolicLink())return reject('symlink evidence path');}
    if(!fs.statSync(target).isFile())return reject('not a regular file');
    const digest=crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex');
    if(digest!==record.document_sha256.toLowerCase())return reject('evidence bytes mismatch');
    return hold('bytes match; reviewer authority, scope, provenance and rights require independent human verification',{ref:record.ref,verified_sha256:digest,byte_integrity:'MATCH'});
  }catch(e){return reject('evidence unreadable or missing');}
}
if(require.main===module){
  if(process.argv.length!==4){console.error('usage: node f001_h3_byte_gate_502.js EVIDENCE_ROOT RECORD_JSON');process.exitCode=2;}
  else{try{const result=check(process.argv[2],JSON.parse(fs.readFileSync(process.argv[3],'utf8')));console.log(JSON.stringify(result));if(result.status==='REJECT')process.exitCode=1;}catch(e){console.error('H3 REJECT: malformed record');process.exitCode=1;}}
}
module.exports={check};
