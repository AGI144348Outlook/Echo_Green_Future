"use strict";
/* Run403: source-level checks on pinned Genesis Python, NOT Python runtime.
 * node a000_source_boundary_403.js <genesis-source.py>
 */
function inspect(src){
 const ci=src.indexOf("class ReshIdentity:"),ce=src.indexOf("\nclass ",ci+6);
 if(ci<0||ce<0)throw Error("Resh class missing");
 const cls=src.slice(ci,ce);
 const anchor=cls.split("    def anchor(self) -> dict:")[1]?.split("    def validate(self) -> bool:")[0];
 const valid=cls.split("    def validate(self) -> bool:")[1]?.split("    def report(self) -> str:")[0];
 const call=src.split("    def open_exchanges(self,")[1]?.split("\nclass CrossLobbyBridge:")[0];
 if(!anchor||!valid||!call)throw Error("method missing");
 const tests=[
 ["A-000 field before Lobby",anchor.indexOf('a000["identity_symbol"]')>=0&&anchor.indexOf('a000["identity_symbol"]')<anchor.indexOf("if self.hebrew_lobby:")],
 ["alias before Lobby",anchor.indexOf('self.matrix.known["A-000-RESH"] = {')>=0&&anchor.indexOf('self.matrix.known["A-000-RESH"] = {')<anchor.indexOf("if self.hebrew_lobby:")],
 ["anchored set after Lobby",anchor.indexOf("self._anchored     = True")>anchor.indexOf("if self.hebrew_lobby:")],
 ["anchor reference after Lobby",anchor.indexOf('self._anchor_entry = self.matrix.known["A-000-RESH"]')>anchor.indexOf("if self.hebrew_lobby:")],
 ["validator flag",valid.includes("self._anchored")],
 ["validator alias key",valid.includes('"A-000-RESH" in self.matrix.known')],
 ["validator symbol",valid.includes('"identity_symbol") == "resh"')],
 ["validator no alias-content witness",!valid.includes("self._anchor_entry")&&!valid.includes("aliases")&&!valid.includes("digest")],
 ["caller reanchor on failed validation",call.includes("if not self.resh.validate():\n            self.resh.anchor()")],
 ["caller no local catch",!/(^|\n)\s*(try:|except\b)/.test(call)],
 ["caller proceeds to Ayin",call.indexOf("self.resh.anchor()")<call.indexOf("self.ayin.agentive_entities(")]
 ];
 const failures=tests.filter(t=>!t[1]).map(t=>t[0]);if(failures.length)throw Error("source assertions: "+failures.join("; "));
 return {checks:tests.length,observation:"Conditional reanchor without local exception catch; validation does not inspect alias contents.",scope:"Source-level only; no full Genesis runtime, external witness or race executed."};
}
if(typeof module!=="undefined"&&module.exports){module.exports={inspect};if(require.main===module){const fs=require("fs");if(process.argv.length!==3)throw Error("usage: node checker genesis.py");process.stdout.write(JSON.stringify(inspect(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");}}
