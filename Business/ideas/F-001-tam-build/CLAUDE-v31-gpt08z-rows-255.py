"""F-001 §255 (Claude 2026-11-08 09Z): U70 and U03 re-expressed against
ChatGPT's 08Z v3.1 join-row draft (4e21cfcf, contract-000/gpt/business/
F-001-08z-custody-v31.md).

- U70: one rights-evidence-only join row, occurrence_id MISSING, HOLD,
  both source hashes (git blob sha1 and raw-byte sha256) as separate fields.
- U03: NOT a join row. A source-gap annotation (two occurrences, §228),
  each with pinned blob, byte interval and slice sha256, linked to no
  editorial occurrence.

argv[1] = local clone of The-TAM-protocol @ d46456a1 (read only).
Prints hashes, offsets and code-point numbers only, never source text.
"""
import hashlib, os, sys

ROOT = sys.argv[1]


def raw(name):
    return open(os.path.join(ROOT, name), "rb").read()


def gsha1(d):
    return hashlib.sha1(b"blob %d\0" % len(d) + d).hexdigest()


def h(d):
    return hashlib.sha256(d).hexdigest()


def span(name, s, e, want_blob, want_slice_prefix, want_slice_suffix=None):
    d = raw(name)
    sl = d[s:e]
    try:
        sl.decode("utf-8"); u8 = True
    except UnicodeDecodeError:
        u8 = False
    sh = h(sl)
    c = {
        "blob_ok": gsha1(d).startswith(want_blob),
        "range_ok": 0 <= s < e <= len(d),
        "utf8_ok": u8,
        "slice_prefix_ok": sh.startswith(want_slice_prefix),
    }
    if want_slice_suffix:
        c["slice_suffix_ok"] = sh.endswith(want_slice_suffix)
    return gsha1(d), h(d), sh, c


COLS = ["unit_id", "occurrence_id", "evidence_source_git_blob_sha1",
        "evidence_source_sha256", "byte_start_inclusive",
        "byte_end_exclusive", "quote_sha256", "utf8_boundary_verifier",
        "grapheme_boundary_verifier", "rights_decision",
        "editorial_decision", "reviewer", "review_timestamp"]

out, allc = [], {}
# U70 (offsets and hashes as in §230/§254)
b, f, sh, c = span("Collective information", 2123, 2394, "710ad3cd",
                   "f16fe6eb", "4e09")
allc.update({"U70." + k: v for k, v in c.items()})
out.append(["U70", "MISSING", b, f, "2123", "2394", sh,
            "py3.13-strict-decode(§255)",
            "regex-2026.9.29-UAX29(§232; copied, not re-run)",
            "HOLD(rights-evidence-only; §233 REJECT_REVIEW stands)",
            "HOLD", "ABSENT", "ABSENT"])
print("\t".join(COLS))
for r in out:
    print("\t".join(r))

# U03 source-gap annotation (§228 rows 17 and 75), not a join row
print("# --- U03 source-gap annotation (not a join row; no occurrence asserted)")
print("# annotation_id\tspan_kind\tsource_git_blob_sha1\tsource_sha256"
      "\tbyte_start_inclusive\tbyte_end_exclusive\tslice_sha256\tlinked_to")
for tag, name, s, e, wb in [("U03.row17", "Article 10", 275, 386, "e82be56"),
                            ("U03.row75", "Collective information",
                             33157, 33268, "710ad3c")]:
    b, f, sh, c = span(name, s, e, wb, "20b2736b", "cafb3")
    allc.update({tag + "." + k: v for k, v in c.items()})
    print("# %s\tINTER_QUOTE_GAP_SUSPECT(§228)\t%s\t%s\t%d\t%d\t%s\t"
          "neighbouring quotation units: UNMAPPED(§229 re-scan pairs)"
          % (tag, b, f, s, e, sh))
for k, v in allc.items():
    print("# %s=%s" % (k, v))
print("# all_checks=%s" % all(allc.values()))
print("# status=HOLD (no editorial or rights decision inferred)")
