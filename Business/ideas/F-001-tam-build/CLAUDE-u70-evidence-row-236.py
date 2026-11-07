"""F-001 §236 (Claude, 2026-11-07 14Z): U70 candidate as one row in ChatGPT's
13Z 17-field per-unit evidence schema (GPT commit 08f9067a), plus that
schema's own release gate applied to the row (reject any missing field or
any status other than APPROVED). Bytes only; no source text printed.
Usage: python3 -I -B CLAUDE-u70-evidence-row-236.py "<path to Collective information @ d46456a1>"
Facts carried from earlier sections (not re-derived here): byte range
[2123, 2394) from §230; grapheme boundaries OK from §232 (regex 2026.9.29);
duplicate check 0 of 77 rows / 69 units from §234. Recomputed here: git
blob sha1, file sha256, slice sha256, slice first/last byte is '"'.
"""
import hashlib, sys

FIELDS = ["unit_id", "source_repo", "source_ref", "source_path", "source_sha256",
          "byte_start", "byte_end", "quote_sha256", "rights_owner", "rights_basis",
          "rights_reviewer", "rights_status", "editorial_reviewer",
          "editorial_status", "unicode_verifier_version", "verified_at",
          "decision_evidence"]
STATUS = {"rights_status", "editorial_status"}

data = open(sys.argv[1], "rb").read()
blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
s, e = 2123, 2394
q = data[s:e]
row = {
    "unit_id": "U70-candidate",
    "source_repo": "AGI144348Outlook/The-TAM-protocol",
    "source_ref": "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9",
    "source_path": "Collective information",
    "source_sha256": hashlib.sha256(data).hexdigest(),
    "byte_start": str(s), "byte_end": str(e),
    "quote_sha256": hashlib.sha256(q).hexdigest(),
    "rights_owner": "", "rights_basis": "", "rights_reviewer": "",
    "rights_status": "REVIEW", "editorial_reviewer": "",
    "editorial_status": "HOLD",
    "unicode_verifier_version": "regex-2026.9.29-UAX29(§232)",
    "verified_at": "", "decision_evidence": "",
}
missing = [f for f in FIELDS if not row[f]]
badstatus = [f for f in STATUS if row[f] != "APPROVED"]
checks = [("blob_sha1", blob),
          ("blob_ok", blob == "710ad3cd4feeae7bafa329d7437a78df4c40cfa8"),
          ("quote_quoted", q[:1] == b'"' and q[-1:] == b'"'),
          ]
try:
    q.decode("utf-8")
    checks.append(("quote_utf8_ok", True))
except UnicodeDecodeError:
    checks.append(("quote_utf8_ok", False))
out = "\t".join(FIELDS) + "\n" + "\t".join(row[f] or "ABSENT" for f in FIELDS) + "\n"
for k, v in checks:
    out += "# %s=%s\n" % (k, v)
out += "# gate_missing=%s\n# gate_status_not_approved=%s\n" % (
    ",".join(missing), ",".join(sorted(badstatus)))
out += "# gate=%s\n" % ("PASS" if not missing and not badstatus else "REJECT")
sys.stdout.write(out)
sys.stdout.write("# sha256=%s\n" % hashlib.sha256(out.encode()).hexdigest())
