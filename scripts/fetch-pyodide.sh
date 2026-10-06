#!/bin/sh
# Downloads the pinned Pyodide core into ./pyodide/v0.26.4/ so the site serves it from its own origin.
set -e
V=0.26.4
D="pyodide/v$V"
mkdir -p "$D"
for f in pyodide.js pyodide.asm.js pyodide.asm.wasm python_stdlib.zip pyodide-lock.json; do
  curl -fL "https://cdn.jsdelivr.net/npm/pyodide@$V/$f" -o "$D/$f"
done
sha256sum "$D"/* > "$D/SHA256SUMS"
echo "Pyodide $V saved to $D (checksums in $D/SHA256SUMS)"
