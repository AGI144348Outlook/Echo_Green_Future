'use strict';
// F-001 H3b-close-v2: supplemental prospective cases registered in Issue #197.
// PREPARATION ONLY. Not executed or an acceptance report. Synthetic fixtures.
// Run only in a disposable offline process; no customer/rights data.
const assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path'),crypto=require('node:crypto');
const {check}=require('./f001_h3b_close_v2_514.js');
const root=fs.mkdtempSync(path.join(os.tmpdir(),'f001-supp-'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
let pass=0,fail=0;
function run(name,fn){try{fn();pass++;console.log('PASS '+name)}catch(e){fail++;console.error('FAIL '+name+': '+e.stack)}}
const record=file=>({ref:'SYNTHETIC',file,document_sha256:sha('fixture')});
try {
  fs.writeFileSync(path.join(root,'regular.txt'),'fixture');
  fs.symlinkSync(path.join(root,'regular.txt'),path.join(root,'linked.txt'));
  run('final-component symlink refuses and holds',()=>{
    const r=check(root,record('linked.txt'));
    assert.equal(r.status,'REJECT');assert.equal(r.release,'HOLD');
    assert.equal(r.rights_clearance,'NOT_DETERMINED');
  });
  fs.mkdirSync(path.join(root,'real'));
  fs.symlinkSync(path.join(root,'real'),path.join(root,'linked-dir'));
  fs.writeFileSync(path.join(root,'real','inside.txt'),'fixture');
  run('intermediate-directory symlink refuses and holds',()=>{
    const r=check(root,record('linked-dir/inside.txt'));
    assert.equal(r.status,'REJECT');assert.equal(r.release,'HOLD');
  });
  const big=path.join(root,'large.bin');
  const fd=fs.openSync(big,'w');
  try{fs.ftruncateSync(fd,16*1024*1024+1)}finally{fs.closeSync(fd)}
  run('oversized regular file refuses and holds',()=>{
    const r=check(root,record('large.bin'));
    assert.equal(r.status,'REJECT');assert.equal(r.release,'HOLD');
    assert.equal(r.reason,'evidence exceeds 16MiB limit');
  });
} finally {fs.rmSync(root,{recursive:true,force:true})}
console.log(JSON.stringify({planned:3,pass,fail,synthetic:true,source:'Run514 exact module'}));
if(fail)process.exitCode=1;
