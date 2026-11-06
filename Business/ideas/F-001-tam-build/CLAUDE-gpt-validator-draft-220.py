"""F-001 §220 (Claude, 2026-11-06 22Z): exercise ChatGPT's 21Z read-only validator
draft (imported as a library, its CLI is not used) on fixed fixtures.
Usage: python3 -I -B CLAUDE-gpt-validator-draft-220.py <path to F-001-READONLY-VALIDATOR-DRAFT.py>
Prints one JSON object. Not rights clearance; no source file is read or written."""
import hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("v", sys.argv[1]); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
def h(b): return hashlib.sha256(b).hexdigest()
src = "Aleph א then é and \U0001F469‍\U0001F4BB end".encode()
t = src.decode()
cases = {
 "exact_ascii": (src, h(src), 0, 5, "Aleph"),
 "digest_mismatch": (src, "0"*64, 0, 5, "Aleph"),
 "invalid_utf8": (b"\xff\xfe", h(b"\xff\xfe"), 0, 1, "x"),
 "bool_index": (src, h(src), False, 5, "Aleph"),
 "empty_span": (src, h(src), 3, 3, ""),
 "split_combining_mark": (src, h(src), t.index("é"), t.index("é")+1, "e"),
 "split_zwj_sequence": (src, h(src), t.index("\U0001F469"), t.index("\U0001F469")+1, "\U0001F469"),
 "bom_prefixed": (b"\xef\xbb\xbfAleph", h(b"\xef\xbb\xbfAleph"), 0, 5, "Aleph"),
 "byte_offsets_misread_as_codepoints": (src, h(src), 6, 8, "א "),
}
out = {k: v.inspect_span(*a) for k, a in cases.items()}
for r in out.values(): r.pop("source_sha256", None)
print(json.dumps(out, sort_keys=True, ensure_ascii=True))
