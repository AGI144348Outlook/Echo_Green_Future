# LHEA environments

Each environment stands alone and links to its siblings. The Directory lists them all.

| Path | Environment |
|---|---|
| `/directory/` | Directory |
| `/datasets/` | Datasets: raw data stored unaltered, with provenance |

## Python runtime

Pages load Pyodide 0.26.4 from this site's own origin at `/pyodide/v0.26.4/`, so nothing is fetched from a third party at runtime.

Before the first deploy, run once from the repo root:

    sh scripts/fetch-pyodide.sh

This saves about 14 MB of Pyodide files and writes their SHA-256 sums. Commit them, or have your build step run the script.

## Deploying to Cloudflare Pages

1. Push this folder to GitHub.
2. In Cloudflare Pages, connect the repo. Build command: `sh scripts/fetch-pyodide.sh` (or none, if the files are committed). Output directory: `/`.
3. `_headers` gives the Pyodide files long-lived caching and the correct wasm type.

## Adding an environment

1. Copy `datasets/index.html` as a starting shell, change `CONFIG.DB_NAME` and `CONFIG.ENV`, and strip what does not belong. A new environment starts inert.
2. Add it to `ENVIRONMENTS` in `directory/index.html`.
3. Link it back to `/directory/`.

## Storage

Each environment keeps its own IndexedDB database (`lhea-env-<name>`), with one record per item. Data stays in the visitor's browser.
