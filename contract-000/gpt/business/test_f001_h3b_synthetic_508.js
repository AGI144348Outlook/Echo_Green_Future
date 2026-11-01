#!/usr/bin/env node
// F-001 H3b synthetic-only preregistered regression harness. No rights authorization.
// Protocol: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/186
'use strict';
const fs=require('node:fs'),os=require('node:os'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const {check}=require('./f001_h3b_descriptor_gate_505.js');
const root=fs.mkdtempSync(path.join(os.tmpdir(),'f001-h3b-'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
let passed=0,failed=0;
function scenario(name,record,expected){
  try { const actual=check(root,record);
    assert.equal(actual.status,expected);
    assert.equal(actual.release,'HOLD');
    assert.equal(actual.rights_clearance,'NOT_DETERMINED');
    console.log('PASS',name,actual.reason);passed++;
  } catch(e) {console.error('FAIL',name,e.message);failed++;}
}
try {
 fs.writeFileSync(path.join(root,'ok.txt'),'synthetic evidence');
 const good={ref:'synthetic-only',file:'ok.txt',document_sha256:sha('synthetic evidence')};
 scenario('matching-bytes-still-HOLD',good,'HUMAN_REVIEW_REQUIRED');
 scenario('digest-mismatch',{...good,document_sha256:'0'.repeat(64)},'REJECT');
 scenario('missing-file',{...good,file:'missing.txt'},'REJECT');
 scenario('parent-traversal',{...good,file:'../ok.txt'},'REJECT');
 scenario('absolute-posix',{...good,file:'/tmp/ok.txt'},'REJECT');
 scenario('windows-drive',{...good,file:'C:\\temp\\ok.txt'},'REJECT');
 scenario('malformed-digest',{...good,document_sha256:'abc'},'REJECT');
 fs.mkdirSync(path.join(root,'nested'));
 fs.writeFileSync(path.join(root,'nested','ok.txt'),'nested synthetic');
 scenario('nested-regular',{...good,file:'nested/ok.txt',document_sha256:sha('nested synthetic')},'HUMAN_REVIEW_REQUIRED');
 fs.symlinkSync(path.join(root,'ok.txt'),path.join(root,'link.txt'));
 scenario('final-symlink',{...good,file:'link.txt'},'REJECT');
 scenario('directory',{...good,file:'nested'},'REJECT');
} finally {fs.rmSync(root,{recursive:true,force:true});}
console.log(JSON.stringify({passed,failed,source:'f001_h3b_descriptor_gate_505.js',rights:'NOT_DETERMINED'}));
if(failed)process.exitCode=1;
