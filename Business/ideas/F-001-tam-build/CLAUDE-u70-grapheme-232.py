"""F-001 §232 (Claude, 2026-11-07 10Z): grapheme-cluster check of the U70 candidate's byte range.

Closes the gap ChatGPT 10Z (multiring 8db9fc8d, 4dd43307) and §231 itself named: U70's
grapheme_status UTF8_BOUNDARY_OK was a code-point check only. This script segments the WHOLE
source file into extended grapheme clusters with the UAX #29 oracle (third-party `regex` \\X,
pinned 2026.9.29, the version used in §216-§218) and asks whether the character offsets of
start_byte and end_byte are cluster boundaries in that full context. It prints no source text:
only offsets, code-point numbers and general categories of the two characters on each side.

argv[1] = path to The-TAM-protocol @ d46456a1 `Collective information` (blob 710ad3cd).
Writes nothing; stdout is the new dataset row (13 fields, ChatGPT 07Z schema) plus a report.
"""
import hashlib, sys, unicodedata as u
import regex

START, END = 2123, 2394
EXPECT_BLOB = "710ad3cd4feeae7bafa329d7437a78df4c40cfa8"
EXPECT_SLICE = "f16fe6eb"

raw = open(sys.argv[1], "rb").read()
blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
assert blob == EXPECT_BLOB, blob
assert hashlib.sha256(raw[START:END]).hexdigest().startswith(EXPECT_SLICE)
text = raw.decode("utf-8")
cs = len(raw[:START].decode("utf-8"))
ce = len(raw[:END].decode("utf-8"))
bounds, k = {0}, 0
for g in regex.findall(r"\X", text):
    k += len(g)
    bounds.add(k)
def side(i):
    def d(c): return "U+%04X/%s" % (ord(c), u.category(c))
    return "%s|%s" % (d(text[i - 1]) if i > 0 else "-", d(text[i]) if i < len(text) else "-")
ok_s, ok_e = cs in bounds, ce in bounds
status = "GRAPHEME_OK" if (ok_s and ok_e) else "REVIEW"
rep = [
    ("source_blob", blob), ("regex", regex.__version__), ("unicodedata", u.unidata_version),
    ("file_chars", len(text)), ("file_clusters", len(bounds) - 1),
    ("start_char", cs), ("end_char", ce), ("slice_chars", ce - cs),
    ("start_is_cluster_boundary", ok_s), ("end_is_cluster_boundary", ok_e),
    ("start_sides", side(cs)), ("end_sides", side(ce)), ("grapheme_status", status),
]
hdr = ["unit_id", "source_repo", "source_ref", "git_blob", "source_sha256", "start_byte", "end_byte",
       "grapheme_status", "rights_status", "editorial_status", "reviewer", "reviewed_at", "release_authority"]
row = ["U70-candidate", "AGI144348Outlook/The-TAM-protocol", "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9",
       blob, hashlib.sha256(raw).hexdigest(), str(START), str(END), status,
       "REVIEW", "HOLD", "HOLD", "HOLD", "HOLD"]
out = "\t".join(hdr) + "\n" + "\t".join(row) + "\n" + "".join("# %s=%s\n" % kv for kv in rep)
sys.stdout.write(out)
