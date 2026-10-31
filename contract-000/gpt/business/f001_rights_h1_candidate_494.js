#!/usr/bin/env node
// Candidate parsing repair only. NOT rights clearance or release authorization.
// Synthetic local tests reported under Issue #171; H2 evidence validation remains absent.
const fs = require('node:fs');
const [queuePath, idsPath] = process.argv.slice(2);
const fail = (why) => { console.error('H1 REJECT: ' + why); process.exitCode = 1; };
if (!queuePath || !idsPath) { fail('two explicit input paths required'); }
else {
  try {
    const rows = fs.readFileSync(queuePath, 'utf8').replace(/\r\n/g, '\n').replace(/\n$/, '').split('\n');
    const expected = fs.readFileSync(idsPath, 'utf8').replace(/\r\n/g, '\n').replace(/\n$/, '').split('\n');
    const header = ['unit_id','classification','evidence_ref','reviewer_id','decision_date'].join('\t');
    if (rows.shift() !== header) throw Error('unexpected TSV header');
    if (expected.length !== 69 || new Set(expected).size !== 69 || expected.some(x => !x.trim() || x !== x.trim())) throw Error('invalid expected ID manifest');
    if (rows.length !== 69) throw Error('expected 69 decision rows');
    const allowed = new Set(['PENDING','ORIGINAL','LICENSED','PERMISSION_GRANTED','REMOVE','REWRITE']);
    const seen = new Set();
    for (const row of rows) {
      const fields = row.split('\t');
      if (fields.length !== 5) throw Error('invalid column count');
      const [id, classification] = fields;
      if (!id || id !== id.trim() || seen.has(id) || !allowed.has(classification)) throw Error('invalid ID/classification');
      seen.add(id);
    }
    if (expected.some(id => !seen.has(id))) throw Error('missing expected ID');
    process.stdout.write('H1 STRUCTURE PASS — NOT RIGHTS CLEARANCE OR PUBLICATION APPROVAL\n');
  } catch (e) { fail(e.message); }
}
