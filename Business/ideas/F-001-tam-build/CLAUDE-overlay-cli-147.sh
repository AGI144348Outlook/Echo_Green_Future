#!/usr/bin/env bash
# F-001 §147 (Claude, 2026-10-29T16Z). Read-only CLI replay of ChatGPT run 447's strict
# F-001-EDITORIAL-OVERLAY-VALIDATE-447.js (it requires run 446's validator beside it) on the exact
# Git bytes. Same cases as CLAUDE-overlay-cli-146.sh plus escaped and nested duplicate keys.
# Usage: bash CLAUDE-overlay-cli-147.sh <Echo_Green_Future clone with origin/contract-000-gpt-run447-20261029-1100>
# Writes only to a fresh temp dir. Approves nothing; a PASS is overlay consistency only.
set -u
G=$1; R=origin/contract-000-gpt-run447-20261029-1100; B=contract-000/gpt/business
T=$(mktemp -d); cd "$T" || exit 2
for p in F-001-EDITORIAL-OVERLAY-VALIDATE-447.js F-001-EDITORIAL-OVERLAY-VALIDATE-446.js F-001-EDITORIAL-OVERLAY-445.json F-001-CROSS-QUEUE-407.json F-001-QUEUE-RECONCILIATION-444.json; do
  git -C "$G" show "$R:$B/$p" > "$p" || exit 2; done
V=F-001-EDITORIAL-OVERLAY-VALIDATE-447.js; O=F-001-EDITORIAL-OVERLAY-445.json; Q=F-001-CROSS-QUEUE-407.json; C=F-001-QUEUE-RECONCILIATION-444.json
echo "blobs: $(git hash-object $V F-001-EDITORIAL-OVERLAY-VALIDATE-446.js $O $Q $C | tr '\n' ' ')"
run() { node "$V" "$3" "$4" "$5" >out.txt 2>&1; rc=$?
  if [ "$rc" = "$2" ]; then r=ok; else r=UNEXPECTED; fi
  echo "$1 exit=$rc expect=$2 $r :: $(tr '\n' ' ' < out.txt | head -c 220)"; }
run X0-real-bytes 0 $O $Q $C
node -e 'const f=require("fs");f.writeFileSync("q1.json",JSON.stringify(JSON.parse(f.readFileSync(process.argv[1]))))' $Q
run X1-queue-reformatted 1 $O q1.json $C
cp $C c2.json; printf '\n' >> c2.json; run X2-recon-trailing-byte 1 $O $Q c2.json
node -e 'const f=require("fs");let s=f.readFileSync(process.argv[1],"utf8");s=s.replace("\"release_authorized\": false","\"release_authorized\": true,\n  \"release_authorized\": false");f.writeFileSync("o3.json",s)' $O
run X3-overlay-duplicate-key 1 o3.json $Q $C
node -e 'const f=require("fs");const o=JSON.parse(f.readFileSync(process.argv[1]));o.decision_links[0].final=true;f.writeFileSync("o4.json",JSON.stringify(o,null,2))' $O
run X4-overlay-final-true 1 o4.json $Q $C
head -c 200 $O > o5.json; run X5-overlay-truncated 1 o5.json $Q $C
printf '\xef\xbb\xbf' > o6.json; cat $O >> o6.json; run X6-overlay-BOM 1 o6.json $Q $C
# X7: duplicate with an escaped spelling of the same key
node -e 'const f=require("fs");let s=f.readFileSync(process.argv[1],"utf8");s=s.replace("\"release_authorized\": false","\"release_\\u0061uthorized\": true,\n  \"release_authorized\": false");f.writeFileSync("o7.json",s)' $O
grep -c 'release_\\u0061uthorized' o7.json | sed 's/^/X7 escaped keys in file: /'
run X7-overlay-escaped-duplicate 1 o7.json $Q $C
# X8: nested duplicate inside the first decision_links object (first key repeated)
node -e 'const f=require("fs");const s=f.readFileSync(process.argv[1],"utf8");const o=JSON.parse(s);const k=Object.keys(o.decision_links[0])[0];const v=JSON.stringify(o.decision_links[0][k]);const t=s.replace(JSON.stringify(k)+": "+v, JSON.stringify(k)+": "+v+", "+JSON.stringify(k)+": "+v);if(t===s)throw Error("X8 not built");f.writeFileSync("o8.json",t)' $O && run X8-overlay-nested-duplicate 1 o8.json $Q $C
rm -rf "$T"
