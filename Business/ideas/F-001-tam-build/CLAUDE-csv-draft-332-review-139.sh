#!/bin/sh
# F-001 §139 (Claude 22Z): extra negative controls for ChatGPT run 332's draft builder/checker.
# Read-only on the TAM clone copies; not pre-registered. Usage: sh this.sh <tam-clone@d46456a> <dir-with-332-scripts>
set -u; T=$1; D=$2; W=$(mktemp -d); B=$D/F-001-REBUILD-DATASETS-332.py; C=$D/F-001-CSV-PIN-CHECK-332.py
python3 -I -B "$B" "$T" "$W/o1" >/dev/null && python3 -I -B "$B" "$T" "$W/o2" >/dev/null && cmp "$W/o1/dataset-a.csv" "$W/o2/dataset-a.csv" && cmp "$W/o1/dataset-b.csv" "$W/o2/dataset-b.csv" && echo "R0 rebuild byte-identical: PASS"
cp -r "$T" "$W/x1"; git -C "$W/x1" update-index --skip-worktree Dataset_B_Binary_Matrix.md; sed -i 's/0\.85g/0.86g/' "$W/x1/Dataset_B_Binary_Matrix.md"
echo "X1 status lines (expect 0): $(git -C "$W/x1" status --porcelain | wc -l)"; python3 -I -B "$B" "$W/x1" "$W/ox1" >/dev/null 2>&1; echo "X1 builder exit (expect 1): $?"
python3 -I -B "$C" "$W/x1" d46456a18fe412398d0ae37ec5a8c4eebb44e0c9 "$W/o1" >/dev/null; echo "X1 checker exit (expect 1): $?"
cp -r "$T" "$W/x2"; touch "$W/x2/extra.txt"; python3 -I -B "$B" "$W/x2" "$W/ox2" >/dev/null 2>&1; echo "X2 untracked file, builder exit (expect 1): $?"
cp -r "$T" "$W/x3"; echo extra.txt >> "$W/x3/.git/info/exclude"; touch "$W/x3/extra.txt"; python3 -I -B "$B" "$W/x3" "$W/ox3" >/dev/null 2>&1; echo "X3 ignored file, builder exit (0 = accepted): $?"
rm -rf "$W"
