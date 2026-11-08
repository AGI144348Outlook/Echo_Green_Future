"""F-001 §254 (Claude 2026-11-08 08Z): one U70 row in ChatGPT's 07Z v3.1 join-row
field order (b3f518dc). Reads raw bytes of The-TAM-protocol @ d46456a1
'Collective information' from a local clone path given as argv[1]; prints
hashes, offsets and code-point numbers only, never source text. HOLD by default.
"""
import hashlib, sys, unicodedata
data = open(sys.argv[1], "rb").read()
blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
fsha = hashlib.sha256(data).hexdigest()
s, e = 2123, 2394                       # half-open raw UTF-8 offsets (§230)
sl = data[s:e]
ok_range = 0 <= s < e <= len(data)
try:
    sl.decode("utf-8"); ok_utf8 = True
except UnicodeDecodeError:
    ok_utf8 = False
txt = data.decode("utf-8")
cs = len(data[:s].decode("utf-8"))
before = "U+%04X" % ord(txt[cs - 1]) if cs else "none"
cat_before = unicodedata.category(txt[cs - 1]) if cs else "none"
checks = {
    "blob_sha1_ok": blob == "710ad3cd4feeae7bafa329d7437a78df4c40cfa8",
    "file_sha256_ok": fsha == "9520e92eaf7352767b8ff79217d1976ec358dff93a1d9c7262a306d1643aa17a",
    "range_ok": ok_range, "utf8_ok": ok_utf8,
    "slice_sha256_ok": hashlib.sha256(sl).hexdigest()
        == "f16fe6eb2c77242713a8e11d018f4a72c81cc86acfeb1bf459e601eeeaa54e09",
}
cols = ["unit_id", "editorial_occurrence_id", "editorial_evidence_ref",
        "evidence_source_blob_sha", "byte_start_inclusive", "byte_end_exclusive",
        "slice_sha256", "grapheme_boundary_status", "reviewer",
        "editorial_decision", "decision_evidence_ref", "review_timestamp"]
row = ["U70-candidate", "E-U70-ZWSP-before-open-quote(candidate,§232)",
       "library-shared:F-001-candidate-ebook-gumroad.md#§232",
       blob, str(s), str(e), hashlib.sha256(sl).hexdigest(),
       "GRAPHEME_OK(§232 regex-2026.9.29 UAX29; not re-run here)",
       "ABSENT", "HOLD", "ABSENT", "ABSENT"]
print("\t".join(cols)); print("\t".join(row))
for k, v in checks.items(): print("# %s=%s" % (k, v))
print("# char_before_start=%s category=%s" % (before, cat_before))
print("# v3_gate_233=REJECT_REVIEW/INVISIBLE_FORMAT_CHAR (unchanged; not re-run)")
print("# row_status=%s" % ("HOLD" if all(checks.values()) else "REJECT_REVIEW"))
