"""F-001 §211 synthetic fixtures (Claude, 2026-11-06 12Z). Stdlib only; no real manuscript text.
Checks span rules of §209/§210 and ChatGPT 11Z draft (da592456) on boundary cases."""
import hashlib, unicodedata as u

def span(src, r):
    (a, b) = r.split("-"); l1, c1 = map(int, a.split(":")); l2, c2 = map(int, b.split(":"))
    lines = src.split("\n")
    if not (1 <= l1 <= l2 <= len(lines)) or (l1 == l2 and c1 > c2) or c1 < 1 or c2 < 1:
        return None
    if c1 > len(lines[l1 - 1]) or c2 > len(lines[l2 - 1]):
        return None
    if l1 == l2:
        return lines[l1 - 1][c1 - 1:c2]
    return "\n".join([lines[l1 - 1][c1 - 1:]] + lines[l1:l2 - 1] + [lines[l2 - 1][:c2]])

def report(name, src, r):
    s = span(src, r)
    nfc = u.is_normalized("NFC", src)
    if s is None:
        print(name, r, "src_nfc=%s" % nfc, "OUT_OF_BOUNDS"); return
    first, last = s[:1], s[-1:]
    nxt_i = None
    splits = bool(first) and u.combining(first) != 0
    # does the code point after the span combine onto it?
    full = src.split("\n"); l2, c2 = map(int, r.split("-")[1].split(":")); line = full[l2 - 1]
    if c2 < len(line) and u.combining(line[c2]) != 0: splits = True
    print(name, r, "src_nfc=%s" % nfc, "span_nfc=%s" % u.is_normalized("NFC", s),
          "cps=%d" % len(s), "bytes=%d" % len(s.encode()), "splits_cluster=%s" % splits,
          "bom=%s" % s.startswith("﻿"), "cr=%s" % ("\r" in s),
          "sha256=%s" % hashlib.sha256(s.encode()).hexdigest()[:16])

q = "aq̃b synthetic"          # q + combining tilde: no precomposed form, stays 2 code points in NFC
report("F211-1", q, "1:1-1:2")      # ends between q and its tilde
report("F211-2", q, "1:3-1:4")      # starts on a lone combining mark
report("F211-3", q, "1:2-1:3")      # whole cluster
report("F211-4", "﻿line one\nline two", "1:1-1:4")   # BOM is column 1
report("F211-5", "line one\r\nline two", "1:1-1:9")      # CRLF: CR becomes a column
report("F211-6", "line one\nline two\n", "2:1-3:1")       # final LF: empty last line
