// Claude 06Z §275: run pre-registered §273 H1-H10 against GPT v17 blob 61efed28 (read-only copy).
// Usage: node CLAUDE-v17-hostile-275.js <path-to-v17.js>
// Loads the exact source into a fresh vm context; no network, no file writes.
"use strict";
const fs = require("fs"), vm = require("vm"), crypto = require("crypto");
const src = fs.readFileSync(process.argv[2], "utf8");
const blob = crypto.createHash("sha1").update(`blob ${Buffer.byteLength(src)}\0`).update(src).digest("hex");
const ctx = vm.createContext({});
vm.runInContext(src + "\n;globalThis.__gate=gate;globalThis.__tests=tests;", ctx);
const gate = ctx.__gate;
const yes = () => true;           // an accepting verifier any caller can write
const ok = { evidence: [{ id: "E-1", source: "S1", quote: "Q1" }] };
const h = (o) => crypto.createHash("sha256").update(o).digest("hex");
const run = (f) => { try { return f(); } catch (e) { return { THREW: String(e) }; } };
const J = (x) => JSON.parse(JSON.stringify(x));
const rows = [];
function row(id, desc, out, predictionMatched, propertyHolds, note) {
  rows.push({ id, desc, out: J(out), release_hold: out && out.release === "HOLD", prediction_matched: predictionMatched, property_holds: propertyHolds, note });
}
// H1 spoofed custodian: field must be ignored (same result as without it)
{ const a = run(() => gate({ ...ok, trusted_source: "independent_custodian" })), b = run(() => gate(ok));
  const a2 = run(() => gate({ ...ok, trusted_source: "independent_custodian" }, yes)), b2 = run(() => gate(ok, yes));
  const same = JSON.stringify(a) === JSON.stringify(b) && JSON.stringify(a2) === JSON.stringify(b2);
  row("H1", "trusted_source in input, with and without verifier", { noVerifier: a, withYes: a2, release: "HOLD" }, same && a.state === "HOLD", same,
    "field ignored; but REVIEW_READY follows from a caller-written ()=>true, so the spoof moved from a field to the verifier argument"); }
// H2 evidence [""]
{ const o = run(() => gate({ evidence: [""] }, yes)); row("H2", 'evidence=[""] with accepting verifier', o, o.state === "HOLD" && o.errors.length > 0, o.state === "HOLD", "code INVALID_EVIDENCE_ITEM (generic, not empty-item specific)"); }
// H3 string evidence
{ const o = run(() => gate({ evidence: "E-1" }, yes)); row("H3", "evidence='E-1' with accepting verifier", o, o.state === "HOLD" && o.errors.length > 0, o.state === "HOLD"); }
// H4 dict item
{ const o = run(() => gate({ evidence: [{ id: "E-1" }] }, yes)); row("H4", "evidence=[{id}] with accepting verifier", o, o.state === "HOLD" && !o.THREW, o.state === "HOLD"); }
// H5 empty source/quote with sha256('') hashes
{ const o = run(() => gate({ evidence: [{ id: "E-1", source: "", quote: "", source_sha256: h(""), quote_sha256: h("") }] }, yes));
  row("H5", "empty source/quote + sha256('')", o, o.state === "HOLD", o.state === "HOLD", "code INVALID_EVIDENCE_ITEM; also whitespace-only rejected via trim"); }
// H6 caller-asserted machine label
{ const o = run(() => gate({ ...ok, label: "EB-QUOTE", checks_run: [] }, yes)), base = run(() => gate(ok, yes));
  row("H6", "label EB-QUOTE asserted, no checks", o, JSON.stringify(o) === JSON.stringify(base), JSON.stringify(o) === JSON.stringify(base),
    "label ignored (v17 has no label concept); v17 derives no machine label from checks either"); }
// H7 no evidence at all
{ const o = run(() => gate({}, yes)); row("H7", "no evidence field", o, o.state === "HOLD" && o.errors.length > 0, o.state === "HOLD" && o.errors.length > 0); }
// H8 rights as caller string
{ const o = run(() => gate({ ...ok, rights: "cleared" }, yes));
  row("H8", "rights='cleared' with accepting verifier", o, o.state === "HOLD" && o.errors.some((e) => /RIGHT/.test(e)), o.release === "HOLD",
    "v17 has no rights check at all: REVIEW_READY with errors [] and no rights-unverified code"); }
// H9 verifier swap after construction: v17 has no construction; verifier is a per-call argument
{ const o = run(() => gate(ok, yes)); row("H9", "verifier swap after construction", o, null, null,
    "NOT APPLICABLE as written: v17 is a plain function gate(input, verifier); there is no construction to bind to, so every caller chooses the verifier on every call (stronger form of the H9 concern)"); }
// H10 verifier throws
{ let mutated = false; const inp = { evidence: [{ id: "E-1", source: "S1", quote: "Q1" }] };
  const o = run(() => gate(inp, (r) => { r.evidence[0].id = "X"; mutated = true; throw new Error("boom"); }));
  const inputUnchanged = inp.evidence[0].id === "E-1";
  row("H10", "verifier mutates its copy then throws", { ...o, inputUnchanged, verifierRan: mutated }, o.state === "HOLD" && o.errors.includes("VERIFIER_ERROR") && inputUnchanged, o.state === "HOLD" && inputUnchanged); }
// Extra (not pre-registered, EXPLORATORY): truthy non-true verdict, async verifier, throwing getter
const extra = {
  X1_truthy_1: run(() => gate(ok, () => 1)),
  X2_async_true: run(() => gate(ok, async () => true)),
  X3_throwing_getter: run(() => gate({ get evidence() { throw new Error("g"); } }, yes)),
};
const own = run(() => ctx.__tests(3301));
const out = { blob, rows, extra: J(extra), gpt_own_tests: J(own),
  summary: { all_release_hold: rows.every((r) => r.release_hold !== false) && Object.values(extra).every((x) => x.release === "HOLD"),
    prediction_matched: rows.filter((r) => r.prediction_matched === true).map((r) => r.id),
    prediction_failed: rows.filter((r) => r.prediction_matched === false).map((r) => r.id),
    not_applicable: rows.filter((r) => r.prediction_matched === null).map((r) => r.id) } };
process.stdout.write(JSON.stringify(out, null, 1) + "\n");
