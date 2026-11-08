"""F-001 section 248 (Claude, 2026-11-08T02Z): read-only v1 -> v3 custody migration
and source-span verifier.

Inputs (read only): CUSTODY-SCHEMA-v3.json, V1-MANIFEST-244.json (next to this file),
and a local clone of AGI144348Outlook/The-TAM-protocol given as argv[1].
Reads blob bytes with `git cat-file` at the pinned ref. Writes nothing; prints
JSON (v3 rows + checks) to stdout. Offsets and hashes only, never quote text.
Usage: python3 -I -B CLAUDE-v3-migrate-248.py /path/to/The-TAM-protocol
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TAM = sys.argv[1]
schema = json.load(open(os.path.join(HERE, "CUSTODY-SCHEMA-v3.json")))
v1 = json.load(open(os.path.join(HERE, "V1-MANIFEST-244.json")))
MISSING = schema["missing_value_marker"]
V3 = [f["name"] for f in schema["unit_fields"] + schema["package_fields"]]
MIG = schema["migration_v1_to_v3"]
V1_FIELDS = sorted(v1[0].keys())


def git(*a):
    return subprocess.run(["git", "-C", TAM] + list(a), check=True,
                          capture_output=True).stdout


def is_cont(b, i):
    return 0 <= i < len(b) and (b[i] & 0xC0) == 0x80


checks = {}
# Schema self-consistency: every v3 field targeted exactly once, every v1 field used.
targets = [m["v3"] for m in MIG]
sources = sorted(m["v1"] for m in MIG if m["v1"] is not None)
checks["v3_field_count"] = len(V3)
checks["migration_targets_equal_v3"] = sorted(targets) == sorted(V3) and len(targets) == len(set(targets))
checks["migration_covers_all_v1"] = sources == V1_FIELDS
checks["v1_field_count"] = len(V1_FIELDS)

rows, cache = [], {}
for r in v1:
    key = (r["source_ref"], r["source_path"])
    if key not in cache:
        tree = git("ls-tree", r["source_ref"], "--", r["source_path"]).decode().split()
        blob_sha = tree[2]
        data = git("cat-file", "blob", blob_sha)
        recomputed = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        cache[key] = (blob_sha, recomputed, data)
    blob_sha, recomputed, data = cache[key]
    s, e = r["byte_start"], r["byte_end_exclusive"]
    out = {}
    for m in MIG:
        if m["v1"] is None:
            out[m["v3"]] = blob_sha if m["v3"] == "source_blob_sha" else MISSING
        else:
            val = r[m["v1"]]
            out[m["v3"]] = MISSING if val is None else val
    rows.append({
        "record": {k: out[k] for k in V3},
        "verify": {
            "blob_sha_recomputed_equal": recomputed == blob_sha,
            "source_sha256_equal": hashlib.sha256(data).hexdigest() == r["source_sha256"],
            "span_in_bounds": 0 <= s < e <= len(data),
            "quote_sha256_equal": hashlib.sha256(data[s:e]).hexdigest() == r["quote_sha256"],
            "utf8_boundary_recheck": (not is_cont(data, s)) and (not is_cont(data, e)),
        },
    })

checks["rows"] = len(rows)
checks["all_verify_true"] = all(all(x["verify"].values()) for x in rows)
checks["no_promotion"] = all(
    x["record"]["rights_decision"] == "REVIEW" and x["record"]["editorial_decision"] == "HOLD"
    and x["record"]["publication_authorization_ref"] == MISSING for x in rows)
print(json.dumps({"checks": checks, "rows": rows}, sort_keys=True, indent=1))
