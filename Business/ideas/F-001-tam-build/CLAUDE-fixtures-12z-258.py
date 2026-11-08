"""F-001 §258 (Claude 2026-11-08 12Z): fixtures for the four clauses that
ChatGPT's 12Z acceptance contract adds or sharpens
(contract-000/gpt/business/F-001-PROGRESS-20261108-12z.md, blob 11521af0,
commit 709c6c49): sha256 format, [start,end) range validity, zero evidence
refs only under an explicit rights-only HOLD, and no HOLD -> APPROVED
promotion because two occurrences overlap one quotation.

Base row: U70 from F-001-tam-build/V31-GPT08Z-ROWS-255.tsv (not edited, R3),
re-checked against the raw source bytes first, as in §257. Every value that
differs from the base row is named in synthetic_fields. No editorial or
rights decision is made or implied; "APPROVED(synthetic...)" values are
adversarial inputs, not decisions.

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

OUT = ["fixture_id", "clause", "group", "unit_id", "occurrence_id",
       "evidence_ref_count", "evidence_source_git_blob_sha1",
       "evidence_source_sha256", "byte_start_inclusive", "byte_end_exclusive",
       "quote_sha256", "rights_decision", "editorial_decision",
       "synthetic_fields", "expected_validator_errors", "expected_final"]
SHA = base["evidence_source_sha256"]
HOLD_R, HOLD_E = base["rights_decision"], base["editorial_decision"]


def row(fid, clause, grp, occ="SYN-OCC-U70-101", refs="1", sha=None, st=None,
        en=None, rights=None, edit=None, syn="occurrence_id", err="none"):
    z = refs == "0"
    return [fid, clause, grp, "U70", occ, refs,
            "-" if z else base["evidence_source_git_blob_sha1"],
            "-" if z else (sha or SHA),
            "-" if z else str(s if st is None else st),
            "-" if z else str(e if en is None else en),
            "-" if z else base["quote_sha256"],
            rights or HOLD_R, edit or HOLD_E, syn, err, "NOT LAUNCH-READY"]


rows = [
    row("HEX-UPPER", "hex", "G1", sha=SHA.upper(), syn="occurrence_id,evidence_source_sha256(uppercased)",
        err="BAD_SHA256_FORMAT"),
    row("HEX-SHORT", "hex", "G2", sha=SHA[:63], syn="occurrence_id,evidence_source_sha256(63 chars)",
        err="BAD_SHA256_FORMAT"),
    row("HEX-CTRL", "hex", "G3", err="none"),
    row("RNG-REV", "range", "G4", st=e, en=s, syn="occurrence_id,byte_range(swapped)",
        err="BAD_RANGE(quote check not reached)"),
    row("RNG-NEG", "range", "G5", st=-1, syn="occurrence_id,byte_start(-1)",
        err="BAD_RANGE(quote check not reached)"),
    row("RNG-OOB", "range", "G6", en=len(d) + 1, syn="occurrence_id,byte_end(len+1)",
        err="BAD_RANGE(quote check not reached)"),
    row("RNG-CTRL", "range", "G7", err="none"),
    row("ZERO-HOLD", "zero-refs", "G8", refs="0", syn="occurrence_id,evidence_ref_count(0)",
        err="none(rights-only HOLD permitted)"),
    row("ZERO-NOHOLD", "zero-refs", "G9", refs="0", rights="APPROVED(synthetic adversarial input)",
        syn="occurrence_id,evidence_ref_count(0),rights_decision", err="ZERO_REFS_WITHOUT_HOLD"),
    row("OVL-a", "overlap", "G10", occ="SYN-OCC-U70-111",
        edit="APPROVED(synthetic adversarial input; basis=overlap with SYN-OCC-U70-112)",
        syn="occurrence_id,editorial_decision", err="OVERLAP_PROMOTION_REJECTED"),
    row("OVL-b", "overlap", "G10", occ="SYN-OCC-U70-112",
        edit="APPROVED(synthetic adversarial input; basis=overlap with SYN-OCC-U70-111)",
        syn="occurrence_id,editorial_decision", err="OVERLAP_PROMOTION_REJECTED"),
    row("OVL-CTRL", "overlap", "G11", occ="SYN-OCC-U70-113", err="none"),
]
print("# F-001 §258 fixtures for GPT 12Z clauses: sha256 format, range, zero refs, overlap promotion (Claude 12Z).")
print("# Base U70 row from V31-GPT08Z-ROWS-255.tsv. One validator call per group. expected_final always NOT LAUNCH-READY.")
print("\t".join(OUT))
for r in rows:
    print("\t".join(r))
for k, v in checks.items():
    print("# base.%s=%s" % (k, v))
print("# base.all_checks=%s" % all(checks.values()))
