'use strict';
// F-001 H3b-close-v2 synthetic regression candidate, preregistered in issue #197.
// DO NOT treat this file as an executed test report. No publication authority.
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path'),crypto=require('node:crypto');
const {check}=require('./f001_h3b_close_v2_514.js');
const root=fs.mkdtempSync(path.join(os.tmpdir(),'f001-515-'));
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const cases=[];
function test(name,fn){cases.push([name,fn]);}
try {
  fs.writeFileSync(path.join(root,'sample.txt'),'synthetic fixture only');
  const record={ref:'SYNTHETIC',file:'sample.txt',document_sha256:digest('synthetic fixture only')};
  test('matching bytes require human review and HOLD',()=>{
    const r=check(root,record);assert.equal(r.status,'HUMAN_REVIEW_REQUIRED');assert.equal(r.release,'HOLD');assert.equal(r.rights_clearance,'NOT_DETERMINED');
  });
  test('wrong digest rejects and holds',()=>{
    const r=check(root,{...record,document_sha256:'0'.repeat(64)});assert.equal(r.status,'REJECT');assert.equal(r.release,'HOLD');
  });
  test('missing file rejects and holds',()=>{
    const r=check(root,{...record,file:'missing.txt'});assert.equal(r.status,'REJECT');assert.equal(r.release,'HOLD');
  });
  test('traversal rejects and holds',()=>{
    const r=check(root,{...record,file:'../sample.txt'});assert.equal(r.status,'REJECT');assert.equal(r.release,'HOLD');
  });
  test('close fault after match rejects without throwing',()=>{
    const io={...fs,closeSync(){throw new Error('synthetic close fault')}};
    const r=check(root,record,io);assert.equal(r.status,'REJECT');assert.equal(r.release,'HOLD');assert.equal(r.reason,'evidence descriptor close failed');assert.match(r.prior_reason,/bytes match/);
  });
  test('close fault after mismatch retains earlier reason',()=>{
    const io={...fs,closeSync(){throw new Error('synthetic close fault')}};
    const r=check(root,{...record,document_sha256:'0'.repeat(64)},io);
    assert.equal(r.status,'REJECT');assert.equal(r.release,'HOLD');assert.equal(r.prior_reason,'evidence bytes mismatch');
  });
  // Note: injected closeSync intentionally does not close the real descriptor.
  // Isolate in a short-lived process; do not reuse this process for production.
  let failures=0;
  for(const [name,fn] of cases){try{fn();process.stdout.write('PASS '+name+'\n')}catch(e){failures++;process.stderr.write('FAIL '+name+': '+e.message+'\n')}}
  process.stdout.write(JSON.stringify({planned:cases.length,failures,source:'Run514 v2',synthetic:true})+'\n');
  if(failures)process.exitCode=1;
}finally{fs.rmSync(root,{recursive:true,force:true});}
