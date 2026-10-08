"""ECHO Dataset Crawler.

Searches open dataset catalogs (Zenodo, Hugging Face, data.gov) by keyword,
saves every catalog record with provenance, and downloads small files
(default: 10 MB each) when the record carries an open license.

Standard library only: runs in GitHub Actions and in Pydroid 3.

Safety:
- Downloaded files are stored as data. They are never opened, unzipped,
  imported or executed by this crawler.
- Only official catalog APIs are called. No page scraping.
- Requests are rate-limited per source and identify the crawler.

usage:
  python3 crawl.py                 # normal run
  python3 crawl.py --dry-run       # records only, no file downloads
  python3 crawl.py --probe         # save one raw response per source, then stop
  python3 crawl.py --source zenodo # one source only
"""
import argparse, gzip, hashlib, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # .../Datasets
CONFIG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
CATALOG = os.path.join(ROOT, "catalog")
FILES = os.path.join(ROOT, "files")
STATE = os.path.join(ROOT, "state")
UA = CONFIG["user_agent"]
NOW = lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
_last_call = {}


# ----------------------------------------------------------------- helpers
def log(*a):
    print(*a, flush=True)


def safe(s, n=80):
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", str(s)).strip("._")
    return (s[:n] or "item")


def get_json(source, url, headers=None):
    """GET a JSON document, respecting the per-source delay. Returns (data, raw_bytes)."""
    gap = CONFIG["sources"][source]["seconds_between_requests"]
    wait = _last_call.get(source, 0) + gap - time.time()
    if wait > 0:
        time.sleep(wait)
    h = {"User-Agent": UA, "Accept": "application/json"}
    h.update(headers or {})
    for attempt in range(3):
        _last_call[source] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
                raw = r.read()
                return json.loads(raw.decode("utf-8")), raw
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 2:
                pause = int(e.headers.get("Retry-After", "30") or 30)
                log(f"  {source}: HTTP {e.code}, waiting {pause}s")
                time.sleep(min(pause, 120))
                continue
            raise


def load_json(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def keywords():
    words, section = [], None
    for line in open(os.path.join(HERE, "keywords.txt"), encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        words.append((line, section))
    return words


def norm_license(value):
    """Lower-case license id/URL -> short id, or '' if unknown."""
    if not value:
        return ""
    v = str(value).lower().strip()
    table = [("publicdomain/zero", "cc0-1.0"), ("cc0", "cc0-1.0"), ("public domain", "public-domain"),
             ("publicdomain/mark", "public-domain"), ("us-pd", "public-domain"),
             ("by-sa", "cc-by-sa"), ("by-nc", "cc-by-nc"), ("by-nd", "cc-by-nd"),
             ("creativecommons.org/licenses/by/", "cc-by"), ("cc-by", "cc-by"),
             ("odbl", "odbl"), ("odc-by", "odc-by"), ("pddl", "pddl"),
             ("mit", "mit"), ("apache", "apache-2.0"), ("gpl", "gpl"), ("bsd", "bsd")]
    for needle, short in table:
        if needle.isalpha() and len(needle) <= 6:
            if re.search(r"(?<![a-z])" + needle + r"(?![a-z])", v):
                return short
        elif needle in v:
            return short
    return v[:60]


def license_ok(short):
    return short in CONFIG["download_licenses"]


# ----------------------------------------------------------------- sources
# Each source yields records in one shape:
# {source, source_id, title, description, url, license_raw, version, modified,
#  files: [{name, size, url, checksum}], skip_reason, raw}

def zenodo(q, limit):
    url = "https://zenodo.org/api/records?" + urllib.parse.urlencode(
        {"q": q, "type": "dataset", "size": min(limit, 25), "sort": "bestmatch"})
    data, raw = get_json("zenodo", url)
    hits = data.get("hits", {}).get("hits", data if isinstance(data, list) else [])
    for h in hits[:limit]:
        md = h.get("metadata", {})
        lic = md.get("license") or {}
        files = []
        for f in h.get("files") or []:
            name = f.get("key") or f.get("filename")
            link = (f.get("links") or {}).get("self") or (f.get("links") or {}).get("content")
            files.append({"name": name, "size": f.get("size") or f.get("filesize"),
                          "url": link, "checksum": f.get("checksum")})
        yield {"source": "zenodo", "source_id": str(h.get("id") or h.get("recid")),
               "title": md.get("title", ""), "description": md.get("description", ""),
               "url": (h.get("links") or {}).get("html") or f"https://zenodo.org/records/{h.get('id')}",
               "doi": h.get("doi") or md.get("doi"),
               "license_raw": lic.get("id") if isinstance(lic, dict) else lic,
               "version": md.get("version") or h.get("revision"),
               "modified": h.get("modified") or h.get("updated") or md.get("publication_date"),
               "files": files, "skip_reason": None, "raw": h}


def huggingface(q, limit):
    url = "https://huggingface.co/api/datasets?" + urllib.parse.urlencode(
        {"search": q, "limit": limit, "full": "true"})
    data, raw = get_json("huggingface", url)
    for d in data[:limit]:
        did = d.get("id", "")
        card = d.get("cardData") or {}
        lic = card.get("license")
        if not lic:
            tag = [t for t in d.get("tags", []) if t.startswith("license:")]
            lic = tag[0].split(":", 1)[1] if tag else None
        if isinstance(lic, list):
            lic = lic[0] if lic else None
        rec = {"source": "huggingface", "source_id": did, "title": did,
               "description": d.get("description") or "", "url": f"https://huggingface.co/datasets/{did}",
               "license_raw": lic, "version": d.get("sha"), "modified": d.get("lastModified"),
               "files": [], "skip_reason": None, "raw": d}
        if d.get("gated") or d.get("private") or d.get("disabled"):
            rec["skip_reason"] = "gated, private or disabled: files need an account"
        else:
            tree_url = f"https://huggingface.co/api/datasets/{urllib.parse.quote(did, safe='/')}/tree/main?recursive=true"
            try:
                tree, _ = get_json("huggingface", tree_url)
                for t in tree:
                    if t.get("type") != "file":
                        continue
                    lfs = t.get("lfs") or {}
                    rec["files"].append({
                        "name": t["path"], "size": t.get("size"),
                        "url": f"https://huggingface.co/datasets/{did}/resolve/{d.get('sha') or 'main'}/{urllib.parse.quote(t['path'])}",
                        "checksum": ("sha256:" + lfs["oid"]) if lfs.get("oid") else None})
            except urllib.error.HTTPError as e:
                rec["skip_reason"] = f"file list unavailable (HTTP {e.code})"
        yield rec


def datagov(q, limit):
    key = os.environ.get("DATAGOV_API_KEY") or "DEMO_KEY"
    url = "https://api.gsa.gov/technology/datagov/v4/search?" + urllib.parse.urlencode(
        {"q": q, "per_page": limit, "sort": "relevance"})
    data, raw = get_json("datagov", url, headers={"X-Api-Key": key})
    for r in data.get("results", [])[:limit]:
        dcat = r.get("dcat") or {}
        files = []
        for dist in dcat.get("distribution") or []:
            if not isinstance(dist, dict):
                continue
            link = dist.get("downloadURL") or dist.get("accessURL")
            if link:
                files.append({"name": dist.get("title") or link.rsplit("/", 1)[-1], "size": None,
                              "url": link, "checksum": None,
                              "format": dist.get("format") or dist.get("mediaType"),
                              "is_download": bool(dist.get("downloadURL"))})
        yield {"source": "datagov", "source_id": r.get("identifier") or r.get("slug"),
               "title": r.get("title", ""), "description": r.get("description", ""),
               "url": f"https://catalog.data.gov/dataset/{r.get('slug')}" if r.get("slug") else None,
               "license_raw": dcat.get("license"), "version": dcat.get("modified"),
               "modified": dcat.get("modified"), "publisher": r.get("publisher"),
               "files": files, "skip_reason": None, "raw": r}


SOURCES = {"zenodo": zenodo, "huggingface": huggingface, "datagov": datagov}


# ----------------------------------------------------------------- downloads
def head_size(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            n = r.headers.get("Content-Length")
            return int(n) if n and n.isdigit() else None
    except Exception:
        return None


def download(source, f, dest, cap):
    """Stream to disk with a hard size cap. Returns (sha256, md5, bytes) or raises."""
    gap = CONFIG["sources"][source]["seconds_between_requests"]
    time.sleep(gap)
    req = urllib.request.Request(f["url"], headers={"User-Agent": UA})
    h256, hmd5, n = hashlib.sha256(), hashlib.md5(), 0
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as out:
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            n += len(chunk)
            if n > cap:
                out.close()
                os.remove(tmp)
                raise ValueError(f"exceeded size cap while downloading ({cap} bytes)")
            h256.update(chunk); hmd5.update(chunk); out.write(chunk)
    os.replace(tmp, dest)
    return h256.hexdigest(), hmd5.hexdigest(), n


def check_checksum(declared, sha256, md5):
    if not declared:
        return "no checksum published by source"
    algo, _, val = declared.partition(":")
    mine = {"sha256": sha256, "md5": md5}.get(algo.lower())
    if mine is None:
        return f"checksum algorithm '{algo}' not checked"
    return "match" if mine == val.lower() else "MISMATCH"


def files_bytes():
    total = 0
    for dp, _, fs in os.walk(FILES):
        total += sum(os.path.getsize(os.path.join(dp, f)) for f in fs)
    return total


# ----------------------------------------------------------------- schedule
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def read_schedule():
    """Parse schedule.txt -> (rule dict, timezone). Raises ValueError on anything unclear."""
    tz_name, rule = "UTC", None
    for line in open(os.path.join(HERE, "schedule.txt"), encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.lower().startswith("timezone:"):
            tz_name = line.split(":", 1)[1].strip()
            continue
        line = line.lower()
        if rule is not None:
            raise ValueError("schedule.txt has more than one schedule line")
        if line == "off":
            rule = {"kind": "off"}
        elif re.fullmatch(r"every (\d+) hours?", line):
            n = int(line.split()[1])
            if not 1 <= n <= 168:
                raise ValueError("'every N hours' needs N from 1 to 168")
            rule = {"kind": "every", "hours": n}
        elif line == "daily":
            rule = {"kind": "every", "hours": 24}
        elif re.fullmatch(r"daily at (\d{1,2})", line):
            h = int(line.split()[-1])
            if h > 23:
                raise ValueError("hour must be 0-23")
            rule = {"kind": "daily", "hour": h}
        elif re.fullmatch(r"weekly on (\w+)(?: at (\d{1,2}))?", line):
            m = re.fullmatch(r"weekly on (\w+)(?: at (\d{1,2}))?", line)
            if m.group(1) not in DAYS:
                raise ValueError(f"unknown day '{m.group(1)}'")
            h = int(m.group(2) or 0)
            if h > 23:
                raise ValueError("hour must be 0-23")
            rule = {"kind": "weekly", "day": DAYS.index(m.group(1)), "hour": h}
        else:
            raise ValueError(f"could not read schedule line: '{line}'")
    if rule is None:
        raise ValueError("schedule.txt has no schedule line")
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo(tz_name)
    except Exception:
        raise ValueError(f"unknown timezone '{tz_name}' (use a name like America/Chicago)")
    return rule, tz


def is_due(rule, tz, last_started, now=None):
    """Return (due, reason)."""
    now = now or datetime.now(timezone.utc)
    if rule["kind"] == "off":
        return False, "schedule is off"
    if last_started is None:
        return True, "no previous run"
    last = datetime.fromisoformat(last_started)
    grace = 10 * 60  # GitHub's hourly trigger can be a few minutes early or late
    if rule["kind"] == "every":
        gap = (now - last).total_seconds()
        due = gap >= rule["hours"] * 3600 - grace
        return due, f"last run {gap / 3600:.1f} h ago; interval {rule['hours']} h"
    local_now, local_last = now.astimezone(tz), last.astimezone(tz)
    if rule["kind"] == "daily":
        due = local_now.hour >= rule["hour"] and local_last.date() < local_now.date()
        return due, f"daily at {rule['hour']}:00 {tz}; last run {local_last:%Y-%m-%d %H:%M}"
    if rule["kind"] == "weekly":
        this_week_slot = (local_now - timedelta(days=(local_now.weekday() - rule["day"]) % 7)
                          ).replace(hour=rule["hour"], minute=0, second=0, microsecond=0)
        if this_week_slot > local_now:
            this_week_slot -= timedelta(days=7)
        due = local_last < this_week_slot <= local_now
        return due, f"weekly on {DAYS[rule['day']]} at {rule['hour']}:00 {tz}; last run {local_last:%Y-%m-%d %H:%M}"
    return False, "unknown rule"


# ----------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--source", choices=list(SOURCES))
    ap.add_argument("--scheduled", action="store_true",
                    help="run only if schedule.txt says a run is due (used by the hourly GitHub trigger)")
    args = ap.parse_args()

    if args.scheduled:
        try:
            rule, tz = read_schedule()
        except ValueError as e:
            log(f"schedule.txt problem: {e}")
            sys.exit(1)       # shows as a failed run in GitHub Actions, so the mistake is noticed
        past = [r for r in load_json(os.path.join(STATE, "runs.json"), []) if r.get("started")]
        due, why = is_due(rule, tz, past[-1]["started"] if past else None)
        log(("Run is due: " if due else "Not due: ") + why)
        if not due:
            return

    seen = load_json(os.path.join(STATE, "seen.json"), {})
    skipped = load_json(os.path.join(STATE, "skipped.json"), {})
    run = {"started": NOW(), "dry_run": args.dry_run, "new_records": 0, "updated_records": 0,
           "files_downloaded": 0, "bytes_downloaded": 0, "files_skipped": 0, "errors": []}
    per_file = CONFIG["max_file_mb"] * 1024 * 1024
    budget = CONFIG["max_total_files_mb"] * 1024 * 1024
    used = files_bytes()
    sources = [args.source] if args.source else [s for s, c in CONFIG["sources"].items() if c["enabled"]]

    if args.probe:
        for s in sources:
            try:
                rec = next(SOURCES[s]("dictionary", 1), None)
                save_json(os.path.join(STATE, "probe", f"{s}.json"), rec["raw"] if rec else {"empty": True})
                log(f"probe {s}: ok" if rec else f"probe {s}: no results")
            except Exception as e:
                log(f"probe {s}: FAILED {e}")
        return

    for word, topic in keywords():
        for s in sources:
            limit = CONFIG["sources"][s]["results_per_keyword"]
            log(f"[{s}] {word}")
            try:
                records = list(SOURCES[s](word, limit))
            except Exception as e:
                run["errors"].append({"source": s, "keyword": word, "error": str(e)[:300]})
                log(f"  error: {e}")
                continue
            for rec in records:
                key = f"{s}:{rec['source_id']}"
                folder = os.path.join(CATALOG, s, safe(rec["source_id"]))
                lic = norm_license(rec.get("license_raw"))
                prev = seen.get(key)
                changed = not prev or prev.get("version") != rec.get("version")
                found_by = sorted(set((prev or {}).get("found_by", []) + [word]))
                seen[key] = {"version": rec.get("version"), "last_seen": NOW(), "found_by": found_by}
                if not changed:
                    continue
                run["new_records" if not prev else "updated_records"] += 1

                raw_bytes = json.dumps(rec["raw"], ensure_ascii=False, sort_keys=True).encode("utf-8")
                os.makedirs(folder, exist_ok=True)
                with gzip.open(os.path.join(folder, "record.raw.json.gz"), "wb") as g:
                    g.write(raw_bytes)
                entry = {
                    "id": key, "title": rec["title"], "url": rec["url"], "doi": rec.get("doi"),
                    "description": (rec.get("description") or "")[:2000],
                    "found_by_keywords": found_by, "topic_section": topic,
                    "provenance": {   # same six fields as the Datasets environment; all start unverified
                        "source": {"value": rec["url"], "status": "unverified"},
                        "version": {"value": rec.get("version"), "status": "unverified"},
                        "date": {"value": rec.get("modified"), "status": "unverified"},
                        "license": {"value": rec.get("license_raw"), "normalized": lic or None, "status": "unverified"},
                        "method": {"value": f"catalog API search ({s}) for '{word}'", "status": "unverified"},
                        "checksum": {"value": "sha256:" + hashlib.sha256(raw_bytes).hexdigest(),
                                     "of": "record.raw.json.gz (uncompressed)", "status": "unverified"}},
                    "fetched_at": NOW(), "files": [], "skip_reason": rec.get("skip_reason"),
                    "executable": False}

                for f in rec["files"]:
                    fe = {"name": f["name"], "url": f["url"], "declared_size": f.get("size"),
                          "declared_checksum": f.get("checksum"), "format": f.get("format"), "stored": None}
                    reason = None
                    size = f.get("size")
                    if rec.get("skip_reason"):
                        reason = rec["skip_reason"]
                    elif args.dry_run:
                        reason = "dry run"
                    elif not license_ok(lic):
                        reason = f"license '{lic or 'none stated'}' is not on the download list"
                    elif f.get("is_download") is False:
                        reason = "access page, not a direct download"
                    else:
                        if size is None:
                            size = head_size(f["url"])
                            fe["head_size"] = size
                        if size is None:
                            reason = "size unknown; not downloaded"
                        elif size > per_file:
                            reason = f"larger than {CONFIG['max_file_mb']} MB"
                        elif used + size > budget:
                            reason = f"repository file budget ({CONFIG['max_total_files_mb']} MB) reached"
                    if reason:
                        fe["skipped"] = reason
                        run["files_skipped"] += 1
                        skipped[f"{key}/{f['name']}"] = {"reason": reason, "at": NOW()}
                    else:
                        dest = os.path.join(FILES, s, safe(rec["source_id"]), safe(f["name"], 120))
                        try:
                            sha256, md5, n = download(s, f, dest, per_file)
                            used += n
                            verdict = check_checksum(f.get("checksum"), sha256, md5)
                            fe.update({"bytes": n, "sha256": sha256, "checksum_check": verdict})
                            if verdict == "MISMATCH":
                                os.remove(dest)
                                used -= n
                                fe["skipped"] = "checksum did not match the source's published checksum; file discarded"
                                run["files_skipped"] += 1
                                skipped[f"{key}/{f['name']}"] = {"reason": fe["skipped"], "at": NOW()}
                            else:
                                fe["stored"] = os.path.relpath(dest, ROOT)
                                fe["provenance_checksum_status"] = "verified against source" if verdict == "match" else "unverified"
                                run["files_downloaded"] += 1
                                run["bytes_downloaded"] += n
                        except Exception as e:
                            fe["skipped"] = f"download failed: {str(e)[:200]}"
                            run["files_skipped"] += 1
                    entry["files"].append(fe)
                save_json(os.path.join(folder, "record.json"), entry)

    run["finished"] = NOW()
    run["files_total_mb"] = round(used / 1048576, 2)
    save_json(os.path.join(STATE, "seen.json"), seen)
    save_json(os.path.join(STATE, "skipped.json"), skipped)
    runs = load_json(os.path.join(STATE, "runs.json"), [])
    runs.append(run)
    save_json(os.path.join(STATE, "runs.json"), runs[-200:])
    build_index()
    log(json.dumps(run, indent=1))


def build_index():
    """INDEX.md: one line per record, newest first."""
    rows = []
    for s in sorted(os.listdir(CATALOG)) if os.path.isdir(CATALOG) else []:
        for d in os.listdir(os.path.join(CATALOG, s)):
            r = load_json(os.path.join(CATALOG, s, d, "record.json"), None)
            if r:
                stored = sum(1 for f in r["files"] if f.get("stored"))
                lic = r["provenance"]["license"]["normalized"] or "unknown"
                rows.append((r["fetched_at"], s, r["title"].replace("|", "/")[:90], lic, stored, len(r["files"]),
                             f"catalog/{s}/{d}/record.json", ", ".join(r["found_by_keywords"])))
    rows.sort(reverse=True)
    lines = ["# Dataset catalog", "", f"{len(rows)} records. Generated by crawler/crawl.py; do not edit by hand.", "",
             "| Source | Title | License | Files stored | Keywords | Record |", "|---|---|---|---|---|---|"]
    for t, s, title, lic, st, tot, path, kw in rows:
        lines.append(f"| {s} | {title} | {lic} | {st}/{tot} | {kw} | [record]({path}) |")
    open(os.path.join(ROOT, "INDEX.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
