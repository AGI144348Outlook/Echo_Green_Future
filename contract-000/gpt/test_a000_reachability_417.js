#!/usr/bin/env node
// Run417 source-bound static check; execute: node test_a000_reachability_417.js <path-to-pinned-genesis.py>
// Pre-test: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/90
// Pin source Git blob: 63eb982989b4f3478d649430b555c8f4ba755c27; verify blob separately with git hash-object.
const fs = require('node:fs');
const path = process.argv[2];
if (!path) { console.error('usage: node test_a000_reachability_417.js <genesis.py>'); process.exit(2); }
const src = fs.readFileSync(path, 'utf8');
const lines = src.split('\n');
const n = s => src.split(s).length - 1;
const checks = [
  ['single ReshIdentity class', n('class ReshIdentity:')===1],
  ['no in-file ReshIdentity constructor', n('ReshIdentity(')===0],
  ['single PeCommunicator class', n('class PeCommunicator:')===1],
  ['no in-file PeCommunicator constructor', n('PeCommunicator(')===0],
  ['open_exchanges only definition', n('open_exchanges(')===1],
  ['one self.resh.anchor in open_exchanges', n('self.resh.anchor()')===1 && lines[3519].includes('self.resh.anchor()')],
  ['generality call once in orchestrator', n('lobby.compute_generality_scores()')===2 && lines[4650].includes('lobby.compute_generality_scores()')],
  ['plain Lobby constructed before generality', lines[4640].includes('lobby = Lobby(self.matrix)')],
  ['Resh set conversion exists', n('resh_agent.definition_words = list(set(')===1],
  ['study proposals not invoked in-file', n('run_study_proposals(')===3 && lines[1523].includes('def run_study_proposals(')]
];
for (const [name, ok] of checks) console.log((ok?'PASS ':'FAIL ')+name);
process.exit(checks.every(x=>x[1])?0:1);
// NOTE: static lexical checks only; external callers, dynamic dispatch, and other modules not covered.
