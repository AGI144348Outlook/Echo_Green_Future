import hashlib, json, subprocess, sys, unicodedata
repo = sys.argv[1]
rows = [(16, "Article 6", "662d745", 24, 1, 75), (49, "Collective information", "710ad3c", 198, 1, 75)]
out = []
for row, f, blob, line, col, chars in rows:
    b = subprocess.run(["git", "-C", repo, "show", f"d46456a1:{f}"], capture_output=True, check=True).stdout
    full = subprocess.run(["git", "-C", repo, "rev-parse", f"d46456a1:{f}"], capture_output=True, text=True).stdout.strip()
    t = b.decode("utf-8")
    lines = t.split("\n")
    start_cp = sum(len(l) + 1 for l in lines[:line - 1]) + (col - 1)
    end_cp = start_cp + chars
    sb = len(t[:start_cp].encode()); eb = len(t[:end_cp].encode())
    span_b = b[sb:eb]
    span_t = t[start_cp:end_cp]
    nonascii = [f"U+{ord(c):04X}/{unicodedata.category(c)}" for c in span_t if ord(c) > 127]
    out.append({"row": row, "file": f, "blob_full": full, "blob_prefix_ok": full.startswith(blob),
                "cp": [start_cp, end_cp], "bytes": [sb, eb], "nbytes": eb - sb,
                "byte_slice_equals_cp_slice": span_b == span_t.encode(),
                "sha256": hashlib.sha256(span_b).hexdigest(),
                "first_cp": f"U+{ord(span_t[0]):04X}", "last_cp": f"U+{ord(span_t[-1]):04X}",
                "prev_cp": f"U+{ord(t[start_cp-1]):04X}" if start_cp else None,
                "next_cp": f"U+{ord(t[end_cp]):04X}" if end_cp < len(t) else None,
                "line_len_cp": len(lines[line - 1]), "nonascii_in_span": nonascii,
                "zero_based_first_cp": f"U+{ord(t[start_cp+1]):04X}"})
print(json.dumps(out, sort_keys=True))
