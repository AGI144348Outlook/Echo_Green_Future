#!/usr/bin/env node
/* Run418 SOURCE-ONLY static reachability assertions, not Genesis runtime execution.
 * Usage: node test_a000_demo_reachability_418.js <pe-demo.py> <genesis.py>
 * Exact intended source pins: demo 64a171a..., Genesis 63eb982... */
'use strict';
function inspect(demo,genesis){
 const checks=[];
 const add=(name,pass)=>checks.push({name,pass:!!pass});
 const loc=s=>demo.indexOf(s);
 const anchor=loc("anchor = resh.anchor()");
 const pe=loc("pe = PeCommunicator(matrix, lobby, resh, ayin)");
 const compute=loc("lobby.compute_generality_scores()");
 const exchange=loc("all_exchanges = pe.open_exchanges(");
 add("demo_imports_Resh_and_Pe",/from echo_governor_skeleton import \([\s\S]*?ReshIdentity, PeCommunicator/.test(demo));
 add("demo_constructs_hebrew_lobby",loc("hebrew_lobby = make_letter_lobby(matrix, HEBREW_ALPHABET")>=0);
 add("demo_constructs_resh",loc("resh = ReshIdentity(matrix, hebrew_lobby=hebrew_lobby)")>=0);
 add("demo_anchors_resh",anchor>=0);
 add("demo_constructs_pe",pe>=0);
 add("demo_calls_open_exchanges",exchange>=0);
 add("generic_generality_before_anchor",compute>=0&&compute<anchor);
 add("pe_after_anchor",anchor>=0&&anchor<pe&&pe<exchange);
 add("no_demo_post_anchor_generality_call",anchor>=0&&!demo.slice(anchor).includes("compute_generality_scores("));
 add("demo_uses_distinct_lobbies",loc("lobby = Lobby(matrix)")>=0&&loc("hebrew_lobby = make_letter_lobby(")>=0);
 add("demo_has_nonportable_absolute_paths",demo.includes('sys.path.insert(0, "/home/claude")')&&demo.includes('THESAURUS = "/home/claude/'));
 add("genesis_pe_can_reanchor",genesis.includes("if not self.resh.validate():")&&genesis.includes("self.resh.anchor()"));
 add("genesis_resolver_is_weak",genesis.includes('and "A-000-RESH" in self.matrix.known')&&genesis.includes('"identity_symbol") == "resh"'));
 return {passed:checks.filter(x=>x.pass).length,total:checks.length,checks,interpretation:"demo provides external wiring but no demo post-anchor generic generality recomputation; not a runtime test"};
}
if(typeof module!=="undefined")module.exports={inspect};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs");
 if(process.argv.length!==4)process.exit(2);
 const r=inspect(fs.readFileSync(process.argv[2],"utf8"),fs.readFileSync(process.argv[3],"utf8"));
 process.stdout.write(JSON.stringify(r,null,2)+"\n");process.exit(r.passed===r.total?0:1);
}