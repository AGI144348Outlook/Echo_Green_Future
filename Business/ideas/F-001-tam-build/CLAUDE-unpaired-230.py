"""F-001 §230 (Claude, 2026-11-07 08Z): resolve the 2 UNPAIRED lines of §229.
Reads The-TAM-protocol checkout (argv[1], expected @ d46456a1), file
'Collective information'. Pairs the single straight quote on line 22 with the
single straight quote on line 27 if no straight or curly quote lies between
them, and prints offsets, lengths and sha256 only (no source text).
Run: python3 -I -B CLAUDE-unpaired-230.py <tam-checkout>"""
import hashlib, os, sys
root = sys.argv[1]
raw = open(os.path.join(root, "Collective information"), "rb").read()
blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
text = raw.decode("utf-8")
lines = text.split("\n")
out = [("file", "Collective information"), ("blob", blob[:7])]
cands = [i + 1 for i, s in enumerate(lines) if s.count('"') % 2 == 1]
out.append(("odd_lines", ",".join(map(str, cands))))
a, b = 22, 27
qa = [j for j, c in enumerate(lines[a - 1]) if c == '"']
qb = [j for j, c in enumerate(lines[b - 1]) if c == '"']
between = "\n".join(lines[a:b - 1])
clean = (len(qa) == 1 and len(qb) == 1 and not any(c in between for c in '"“”'))
out.append(("open", "L%d c%d" % (a, qa[0] + 1)))
out.append(("close", "L%d c%d" % (b, qb[0] + 1)))
out.append(("no_quote_between", clean))
start_cp = sum(len(s) + 1 for s in lines[:a - 1]) + qa[0]
end_cp = sum(len(s) + 1 for s in lines[:b - 1]) + qb[0] + 1
span = text[start_cp:end_cp]
sb = len(text[:start_cp].encode()); eb = sb + len(span.encode())
assert raw[sb:eb].decode() == span
out.append(("cp_span", "[%d,%d)" % (start_cp, end_cp)))
out.append(("byte_span", "[%d,%d)" % (sb, eb)))
out.append(("chars_incl_marks", len(span)))
out.append(("lines_spanned", b - a + 1))
out.append(("inner_words", len(span.strip('"').split())))
out.append(("span_sha256", hashlib.sha256(span.encode()).hexdigest()))
t = "".join("%s=%s\n" % kv for kv in out)
sys.stdout.write(t + "stdout_sha256=" + hashlib.sha256(t.encode()).hexdigest() + "\n")
