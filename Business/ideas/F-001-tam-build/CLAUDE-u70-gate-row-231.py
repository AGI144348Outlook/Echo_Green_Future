"""F-001 §231 (Claude, 2026-11-07 09Z): U70 candidate as one gate row in
ChatGPT's 07Z 13-field schema (73dd7832). Re-reads the pinned source bytes,
re-verifies the §230 span independently of the §230 script (byte slice and
sha256 only), and prints one TSV header + one row. Every field that needs a
human (rights, editorial, reviewer, reviewed_at, release_authority) is
REVIEW/HOLD, never PASS. No source text is printed.
Run: python3 -I -B CLAUDE-u70-gate-row-231.py <tam-checkout @ d46456a1>"""
import hashlib, os, subprocess, sys
root = sys.argv[1]
name = "Collective information"
raw = open(os.path.join(root, name), "rb").read()
blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
ref = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()
sb, eb = 2123, 2394                      # from §230 MULTILINE-QUOTE-230.tsv
span = raw[sb:eb]
ok = (hashlib.sha256(span).hexdigest() ==
      "f16fe6eb2c77242713a8e11d018f4a72c81cc86acfeb1bf459e601eeeaa54e09"
      and span[:1] == b'"' and span[-1:] == b'"')
span.decode("utf-8")                     # raises if the slice cuts a code point
cols = ["unit_id", "source_repo", "source_ref", "git_blob", "source_sha256",
        "start_byte", "end_byte", "grapheme_status", "rights_status",
        "editorial_status", "reviewer", "reviewed_at", "release_authority"]
row = ["U70-candidate", "AGI144348Outlook/The-TAM-protocol", ref, blob,
       hashlib.sha256(raw).hexdigest(), str(sb), str(eb),
       "UTF8_BOUNDARY_OK" if ok else "REVIEW", "REVIEW", "HOLD",
       "HOLD", "HOLD", "HOLD"]
t = "\t".join(cols) + "\n" + "\t".join(row) + "\n"
sys.stdout.write(t)
sys.stderr.write("span_verified=%s stdout_sha256=%s\n"
                 % (ok, hashlib.sha256(t.encode()).hexdigest()))
