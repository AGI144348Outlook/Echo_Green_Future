#!/usr/bin/env node
"use strict";
/* F-001 Run447: strict raw JSON key-collision gate around the Run446 source-bound validator.
   A PASS is a custody/consistency receipt only; never release authorization. */
const fs = require("fs");
const crypto = require("crypto");

function assertUniqueJsonKeys(raw, label = "JSON") {
  const s = Buffer.isBuffer(raw) ? raw.toString("utf8") : String(raw);
  JSON.parse(s); // Reject malformed JSON first; this alone does NOT reject duplicate keys.
  let i = 0;
  const ws = () => { while (i < s.length && /[ \t\r\n]/.test(s[i])) i++; };
  function str() {
    if (s[i] !== '"') throw Error(label + ": expected JSON string at offset " + i);
    const start = i++;
    while (i < s.length) {
      const c = s[i++];
      if (c === "\\") { i++; continue; }
      if (c === '"') return JSON.parse(s.slice(start, i));
    }
    throw Error(label + ": unterminated JSON string");
  }
  function value(path) {
    ws();
    if (s[i] === "{") {
      i++; ws();
      const seen = new Set();
      if (s[i] === "}") { i++; return; }
      while (true) {
        ws();
        const key = str(); // Decodes escaped names, e.g. "final" and "f\\u0069nal".
        if (seen.has(key)) throw Error(label + ": duplicate JSON key " + JSON.stringify(key) + " at " + path);
        seen.add(key);
        ws(); if (s[i++] !== ":") throw Error(label + ": expected colon");
        value(path + "/" + key.replace(/~/g, "~0").replace(/\//g, "~1"));
        ws();
        if (s[i] === "}") { i++; return; }
        if (s[i++] !== ",") throw Error(label + ": expected comma");
      }
    }
    if (s[i] === "[") {
      i++; ws();
      if (s[i] === "]") { i++; return; }
      let n = 0;
      while (true) {
        value(path + "/" + n++);
        ws();
        if (s[i] === "]") { i++; return; }
        if (s[i++] !== ",") throw Error(label + ": expected comma");
      }
    }
    if (s[i] === '"') { str(); return; }
    const m = s.slice(i).match(/^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/);
    if (!m) throw Error(label + ": expected JSON value at offset " + i);
    i += m[0].length;
  }
  value("$"); ws();
  if (i !== s.length) throw Error(label + ": unconsumed JSON text at offset " + i);
  return true;
}
const gitSha = bytes => crypto.createHash("sha1")
  .update(Buffer.concat([Buffer.from("blob " + bytes.length), Buffer.from([0]), bytes]))
  .digest("hex");
function readStrict(path) {
  const bytes = fs.readFileSync(path);
  assertUniqueJsonKeys(bytes, path);
  return { json: JSON.parse(bytes.toString("utf8")), sha: gitSha(bytes) };
}
function validateFiles(overlayPath, queuePath, reconciliationPath) {
  const { validateOverlay } = require("./F-001-EDITORIAL-OVERLAY-VALIDATE-446.js");
  const o = readStrict(overlayPath), q = readStrict(queuePath), r = readStrict(reconciliationPath);
  return { errors: validateOverlay(o.json, q.json, r.json, { queueSha: q.sha, reconSha: r.sha }),
           blobs: { overlay: o.sha, queue: q.sha, reconciliation: r.sha } };
}
module.exports = { assertUniqueJsonKeys, readStrict, validateFiles };
if (require.main === module) {
  if (process.argv.length !== 5) {
    console.error("Usage: node F-001-EDITORIAL-OVERLAY-VALIDATE-447.js OVERLAY.json QUEUE.json RECONCILIATION.json");
    process.exit(2);
  }
  try {
    const result = validateFiles(...process.argv.slice(2));
    if (result.errors.length) {
      console.error("FAIL / HOLD: " + result.errors.join("; "));
      process.exitCode = 1;
    } else {
      console.log("PASS / HOLD: source-bound editorial consistency only; F-001 remains UNREVIEWED / NOT LAUNCH-READY");
      console.log("RECEIPT Git blobs (overlay / queue / reconciliation): " +
        result.blobs.overlay + " / " + result.blobs.queue + " / " + result.blobs.reconciliation);
    }
  } catch (e) {
    console.error("FAIL / HOLD: " + e.message);
    process.exitCode = 1;
  }
}
