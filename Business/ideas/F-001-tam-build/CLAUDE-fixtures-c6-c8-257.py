"""F-001 §257 (Claude 2026-11-08 11Z): negative fixtures for clauses 6
(duplicate join rejection) and 8 (changed source invalidates the package)
of ChatGPT's validator acceptance contract (09Z 853960c0; interface 10Z
bbcd8470; 11Z ad8860c7).

Base row: U70 from F-001-tam-build/V31-GPT08Z-ROWS-255.tsv (§255; that
file is not edited, R3). The base row is re-checked against the raw source
bytes first; every fixture value that differs from the base is marked
SYNTHETIC. No editorial or rights decision is made or implied.

argv[1] = local clone of The-TAM-protocol (read only)
argv[2] = path to V31-GPT08Z-ROWS-255.tsv
Prints hashes, offsets and labels only, never source text.
"""
import hashlib, os, subprocess, sys

ROOT, TSV = sys.argv[1], sys.argv[2]
PIN = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
SRC = "Collective information"


def gsha1(d):
    return hashlib.sha1(b"blob %d\0" % len(d) + d).hexdigest()


head = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
d = open(os.path.join(ROOT, SRC), "rb").read()

lines = open(TSV, encoding="utf-8").read().split("\n")
cols = lines[0].split("\t")
base = dict(zip(cols, [l for l in lines if l.startswith("U70\t")][0].split("\t")))
s, e = int(base["byte_start_inclusive"]), int(base["byte_end_exclusive"])
sl = d[s:e]
try:
    sl.decode("utf-8"); u8 = True
except UnicodeDecodeError:
    u8 = False
checks = {
    "clone_head_is_pin": head == PIN,
    "blob_full_match": gsha1(d) == base["evidence_source_git_blob_sha1"],
    "source_sha256_full_match": hashlib.sha256(d).hexdigest() == base["evidence_source_sha256"],
    "range_ok": 0 <= s < e <= len(d),
    "utf8_ok": u8,
    "quote_sha256_full_match": hashlib.sha256(sl).hexdigest() == base["quote_sha256"],
}

OUT = ["fixture_id", "clause", "expected_source_commit", "input_source_commit",
       "unit_id", "occurrence_id", "evidence_source_git_blob_sha1",
       "evidence_source_sha256", "byte_start_inclusive", "byte_end_exclusive",
       "quote_sha256", "rights_decision", "editorial_decision",
       "synthetic_fields", "expected_validator_errors", "expected_final"]


def row(fid, clause, inp=PIN, occ="SYN-OCC-U70-001", src_sha=None, syn="", err=""):
    return [fid, clause, PIN, inp, "U70", occ,
            base["evidence_source_git_blob_sha1"],
            src_sha or base["evidence_source_sha256"],
            str(s), str(e), base["quote_sha256"],
            base["rights_decision"], base["editorial_decision"],
            syn or "occurrence_id", err or "none", "NOT LAUNCH-READY"]


flip = base["evidence_source_sha256"][:-1] + (
    "0" if base["evidence_source_sha256"][-1] != "0" else "1")
rows = [
    row("C6-DUP-a", "6", syn="occurrence_id", err="DUPLICATE_JOIN(C6-DUP-a,C6-DUP-b)"),
    row("C6-DUP-b", "6", syn="occurrence_id", err="DUPLICATE_JOIN(C6-DUP-a,C6-DUP-b)"),
    row("C6-CTRL", "6", occ="SYN-OCC-U70-002", syn="occurrence_id", err="none"),
    row("C8-COMMIT", "8", inp="0" * 40, syn="occurrence_id,input_source_commit",
        err="SOURCE_COMMIT_MISMATCH"),
    row("C8-BYTES", "8", src_sha=flip, syn="occurrence_id,evidence_source_sha256(last hex changed)",
        err="SOURCE_SHA256_MISMATCH"),
    row("C8-CTRL", "8", syn="occurrence_id", err="none"),
]
print("# F-001 §257 fixtures for clauses 6 and 8 (Claude 11Z). Base U70 row from V31-GPT08Z-ROWS-255.tsv.")
print("# All rows: rights HOLD, editorial HOLD; expected_final is always NOT LAUNCH-READY (clause 9).")
print("# C6-DUP-a/b: same unit_id + occurrence_id twice -> both rejected. C6-CTRL: distinct id -> no C6 error.")
print("# C8-COMMIT: input commit differs from pin. C8-BYTES: declared source sha256 differs from bytes. C8-CTRL: matches.")
print("\t".join(OUT))
for r in rows:
    print("\t".join(r))
for k, v in checks.items():
    print("# base.%s=%s" % (k, v))
print("# base.all_checks=%s" % all(checks.values()))
