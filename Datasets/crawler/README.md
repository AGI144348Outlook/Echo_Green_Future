# ECHO Dataset Crawler

Searches three open dataset catalogs by keyword and builds a catalog of what it finds. Small, openly licensed files come with it.

| Source | How | Key needed |
|---|---|---|
| Zenodo | `zenodo.org/api/records`, datasets only | No |
| Hugging Face | `huggingface.co/api/datasets` plus each dataset's file list | No (gated datasets are skipped) |
| data.gov | `api.gsa.gov/technology/datagov/v4/search` | Optional `DATAGOV_API_KEY` secret. Without it the crawler uses `DEMO_KEY`, which allows 30 requests an hour and 50 a day. |

It uses only official catalog APIs, so there is no page scraping. It needs only Python's standard library, so it also runs in Pydroid 3.

## What it writes (all under `Datasets/`)

```
INDEX.md
catalog/<source>/<id>/
  record.json
  record.raw.json.gz
files/<source>/<id>/<file>
state/seen.json
state/skipped.json
state/runs.json
state/probe/
```

Each `record.json` carries source, version, date, license, method and checksum. All start unverified except downloaded files whose checksum matches a catalog-published checksum.

Downloaded files are stored as inert data. The crawler never opens, unzips, imports or executes them.

## Download rules

Downloads require an allowed license, <=10 MB per file, <=300 MB aggregate, and a matching catalog checksum when one is published. Everything else is recorded with its reason and source link.

## Schedule

`schedule.txt` controls cadence. GitHub wakes the workflow hourly; the crawler decides whether a run is due. Manual workflow runs ignore the schedule.

## Setup / validation

The workflow lives on the default branch but checks out and commits to `code-library-registry`.

Run probe first, then dry-run, before allowing normal downloads. The crawler was originally authored without live access to all three APIs, so probe mode is the compatibility check.

Manual:
```
python3 Datasets/crawler/crawl.py --probe
python3 Datasets/crawler/crawl.py --dry-run
python3 Datasets/crawler/crawl.py --source zenodo
```
