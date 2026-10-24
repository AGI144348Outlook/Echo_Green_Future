#!/bin/sh
# DISC-002 E34 (Claude, 2026-10-24T19Z): seed sweep of the Echo journeyman shadow run 3,
# control vs the ת/ק failures-box replay. Exploratory, NOT pre-registered.
#
# Usage: sh DISC-002-boxes-seed-sweep-e34.sh <scratch worktree of integration/echo-whole @ a16093e>
# The worktree must be a throwaway checkout: the sweep rewrites files under inventory/.
# Nothing is pushed; the script restores inventory/ with `git checkout` after each run.
#
# The only change to the sweep is the seed: a scratch copy replaces the fixed `seed=1025,`
# with an environment variable. Each run starts with an empty boxes_replay/ folder.
set -eu
WT=$1
cd "$WT"
SW=inventory/automation/sweeps
sed 's/seed=1025,/seed=int(os.environ.get("E34_SEED","1025")),/' $SW/sweep_1_automation.py > $SW/sweep_e34.py
echo "seed | control hits, discarded | boxes hits, discarded, tav cards, qof cards"
for seed in 1025 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
  git checkout -q -- inventory
  rm -rf $SW/boxes_replay
  E34_SEED=$seed python3 -I $SW/sweep_e34.py "$WT" >/dev/null 2>&1
  c=$(python3 -I -c 'import json;d=json.load(open("inventory/automation/sweeps/echo_shadow_3.json"));print(d["hits"],sum(1 for k in d["checkpoints"] if k["decision"]=="DISCARDED"))')
  E34_SEED=$seed python3 -I $SW/sweep_e34.py "$WT" --boxes >/dev/null 2>&1
  b=$(python3 -I -c 'import json;d=json.load(open("inventory/automation/sweeps/echo_shadow_3_boxes.json"));print(d["hits"],sum(1 for k in d["checkpoints"] if k["decision"]=="DISCARDED"),d["boxes"]["tav_cards"],d["boxes"]["qof_cards"])')
  echo "$seed | $c | $b"
done
git checkout -q -- inventory
rm -f $SW/sweep_e34.py
