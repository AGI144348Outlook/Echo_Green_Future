"use strict";
const { assertUniqueJsonKeys, readStrict } = require("./F-001-EDITORIAL-OVERLAY-VALIDATE-447.js");
const fs = require("fs"), path = require("path"), os = require("os"), crypto = require("crypto");
const cases = [
 ["valid object",'{"release_authorized":false,"decision_links":[{"final":false}]}',true],
 ["X3 duplicate release key",'{"release_authorized":true,"release_authorized":false}',false],
 ["duplicate nested final",'{"decision_links":[{"final":true,"final":false}]}',false],
 ["escaped alias key",'{"final":true,"f\\u0069nal":false}',false],
 ["duplicate queue key",'{"total_occurrences":81,"total_occurrences":82}',false],
 ["duplicate reconciliation key",'{"existing_occurrences":83,"existing_occurrences":82}',false],
 ["different scopes same key",'{"a":{"final":false},"b":{"final":false}}',true],
 ["literal key-like text",'{"notes":"\\\"final\\\": true, \\\"final\\\": false","final":false}',true],
 ["escaped quote key",'{"a\\\"b":1,"a\\\"b":2}',false],
 ["array with duplicate object",'[{"a":1},{"b":1,"b":2}]',false],
 ["valid primitives",'[true,false,null,-1.23e+4,"x",{},[]]',true],
 ["malformed truncated",'{"final":',false],
 ["trailing comma",'{"a":1,}',false],
 ["BOM",'\uFEFF{"a":1}',false],
 ["empty JSON object",'{}',true],
 ["valid unicode escape",'{"\\u0061":1,"b":2}',true],
 ["unicode key collision",'{"a":1,"\\u0061":2}',false],
];
let pass=0;
for(const [name,input,expected] of cases){let got;try{assertUniqueJsonKeys(input,name);got=true}catch(e){got=false};if(got!==expected){console.error('FAIL',name,got,expected);process.exitCode=1}else{console.log('PASS',name);pass++}}
const d=fs.mkdtempSync(path.join(os.tmpdir(),"f001-447-"));
try{const p=path.join(d,"fixture.json"), bytes=Buffer.from('{"a":1}\n');fs.writeFileSync(p,bytes);const r=readStrict(p);const expected=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+bytes.length+"\0"),bytes])).digest("hex");if(r.sha===expected){pass++;console.log('PASS Git blob receipt')}else{process.exitCode=1;console.error('FAIL Git blob receipt')}}finally{fs.rmSync(d,{recursive:true,force:true})}
console.log(`SUMMARY ${pass}/${cases.length+1} PASS; real pinned three-file CLI NOT RUN`);
