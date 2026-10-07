#!/bin/sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
V="$ROOT/IVS/vendor"
mkdir -p "$V/corpus" "$V/structural-analysis" "$V/visual-signs" "$V/analysis" "$V/hypotheses"
clone_or_update () {
  dest="$1"; url="$2"
  if [ -d "$dest/.git" ]; then
    git -C "$dest" fetch --all --prune
    git -C "$dest" pull --ff-only || true
  else
    git clone "$url" "$dest"
  fi
}
clone_or_update "$V/corpus/mayig-indus-valley-script-corpus" "https://github.com/mayig/indus-valley-script-corpus.git"
clone_or_update "$V/corpus/field-cady-indus_valley_script_corpus" "https://github.com/field-cady/indus_valley_script_corpus.git"
clone_or_update "$V/structural-analysis/epachayan-indus-script" "https://github.com/epachayan/indus-script.git"
clone_or_update "$V/visual-signs/HimanshuAttri-IndusValleyScriptDataset" "https://github.com/HimanshuAttri/IndusValleyScriptDataset.git"
clone_or_update "$V/analysis/varundataquest-Indus-Valley-Text-Analysis" "https://github.com/varundataquest/Indus-Valley-Text-Analysis.git"
clone_or_update "$V/hypotheses/Kee2u-Deciphering_the_Indus_Valley_Script" "https://github.com/Kee2u/Deciphering_the_Indus_Valley_Script.git"
printf '%s\n' "IVS upstream sources ready under IVS/vendor/"
