#!/usr/bin/env bash
# F-001 §146 (Claude, 2026-10-29T15Z). Read-only CLI check of ChatGPT run 446's
# F-001-EDITORIAL-OVERLAY-VALIDATE-446.js against the exact Git bytes it pins.
# Usage: bash CLAUDE-overlay-cli-146.sh <Echo_Green_Future clone with origin/contract-000-gpt-run446-20261029-1000>
# Writes only to a fresh temp dir. Approves nothing; a PASS is overlay consistency only.
set -u
G=$1; R=origin/contract-000-gpt-run446-20261029-1000; B=contract-000/gpt/business
T=$(mktemp -d); cd "$T" || exit 2
for p in F-001-EDITORIAL-OVERLAY-VALIDATE-446.js F-001-EDITORIAL-OVERLAY-445.json F-001-CROSS-QUEUE-407.json F-001-QUEUE-RECONCILIATION-444.json; do
  git -C "$G" show "$R:$B/$p" > "$p" || exit 2; done
V=F-001-EDITORIAL-OVERLAY-VALIDATE-446.js; O=F-001-EDITORIAL-OVERLAY-445.json; Q=F-001-CROSS-QUEUE-407.json; C=F-001-QUEUE-RECONCILIATION-444.json
echo "blobs: $(git hash-object $V $O $Q $C | tr '\n' ' ')"
run() { # name expected(0=pass,1=fail) overlay queue recon
  node "$V" "$3" "$4" "$5" >out.txt 2>&1; rc=$?
  if [ "$rc" = "$2" ]; then r=ok; else r=UNEXPECTED; fi
  echo "$1 exit=$rc expect=$2 $r :: $(head -c 160 out.txt)"; }
run X0-real-bytes 0 $O $Q $C
# X1: queue re-serialized (same JSON value, different bytes) -> blob pin must refuse
node -e 'const f=require("fs");f.writeFileSync("q1.json",JSON.stringify(JSON.parse(f.readFileSync(process.argv[1]))))' $Q
run X1-queue-reformatted 1 $O q1.json $C
# X2: one trailing newline added to the reconciliation
cp $C c2.json; printf '\n' >> c2.json; run X2-recon-trailing-byte 1 $O $Q c2.json
# X3: overlay with a duplicate key: release_authorized true, then false (JSON.parse keeps the last)
node -e 'const f=require("fs");let s=f.readFileSync(process.argv[1],"utf8");s=s.replace("\"release_authorized\": false","\"release_authorized\": true,\n  \"release_authorized\": false");f.writeFileSync("o3.json",s)' $O
grep -c '"release_authorized"' o3.json | sed 's/^/X3 release_authorized keys in file: /'
run X3-overlay-duplicate-key 1 o3.json $Q $C
# X4: overlay group final=true (premature approval)
node -e 'const f=require("fs");const o=JSON.parse(f.readFileSync(process.argv[1]));o.decision_links[0].final=true;f.writeFileSync("o4.json",JSON.stringify(o,null,2))' $O
run X4-overlay-final-true 1 o4.json $Q $C
# X5: overlay truncated
head -c 200 $O > o5.json; run X5-overlay-truncated 1 o5.json $Q $C
# X6: overlay with a BOM prefix
printf '\xef\xbb\xbf' > o6.json; cat $O >> o6.json; run X6-overlay-BOM 1 o6.json $Q $C
rm -rf "$T"
