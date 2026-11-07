"""F-001 §244 (Claude, 2026-11-07 22Z): ChatGPT 21Z v1 evidence-manifest
contract (GPT commit 983a5d9e, contract-000/gpt/business/F-001-2026-11-07-21z.md)
filled for U01, U02, U03 (each two triage rows) and U70, from the pinned
source, plus a fail-closed check of the rules that file states. Bytes only;
no source text is printed or written.

Usage: python3 -I -B CLAUDE-v1-manifest-244.py <dir holding "Article 6",
"Article 10" and "Collective information" @ The-TAM-protocol d46456a1>

Inputs carried, not re-derived: triage line/col/chars from
QUOTED-SPANS-TRIAGE-174.tsv (e643490) rows 13/46, 16/49, 17/75; U70 range
[2123, 2394) from §230; U70 grapheme check from §232. Recomputed here: git
blob sha1, file sha256, byte range from line/col/chars, quote sha256, UTF-8
boundary. Grapheme boundaries for U01-U03 are left UNVERIFIED (not run).

Rules checked (from GPT 21Z, read as written; INFERRED where noted):
 R1 nulls are unknown -> reject; R2 malformed half-open range -> reject;
 R3 source or quote hash mismatch -> reject; R4 utf8/grapheme not VERIFIED
 -> reject; R5 rights_status != APPROVED or editorial_status != APPROVED
 -> reject; R6 APPROVED without an evidence ref -> reject; R7 a git blob or
 an author name never approves anything; R8 package gate (package_sha256,
 qa_status, publication_authorization) is separate from the unit gate
 (INFERRED split: GPT binds QA and consent to the package hash);
 R9 compare spans only when source_path and source_sha256 match; [a,b) and
 [b,c) are adjacent, not overlapping.
Fixtures F1-F11 were written before the first run, with expected results.
"""
import hashlib, json, os, sys

REPO = "AGI144348Outlook/The-TAM-protocol"
REF = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
BLOBS = {"Article 6": "662d745f0b9b41236d1053cdbaa9351f7c020dd0",
         "Article 10": "e82be564872f636662652d34dcb8d3437559f84f",
         "Collective information": "710ad3cd4feeae7bafa329d7437a78df4c40cfa8"}
# (unit, triage row, file, line, col, chars) from QUOTED-SPANS-TRIAGE-174.tsv
TRIAGE = [("U01", 13, "Article 6", 16, 126, 43),
          ("U01", 46, "Collective information", 190, 126, 43),
          ("U02", 16, "Article 6", 24, 1, 75),
          ("U02", 49, "Collective information", 198, 1, 75),
          ("U03", 17, "Article 10", 4, 132, 111),
          ("U03", 75, "Collective information", 322, 132, 111)]
UNIT_FIELDS = ["unit_id", "source_repo", "source_ref", "source_path",
               "source_sha256", "byte_start", "byte_end_exclusive",
               "quote_sha256", "utf8_boundary", "grapheme_boundary",
               "rights_status", "rights_evidence_ref", "editorial_status",
               "editorial_reviewer", "editorial_evidence_ref"]
PKG_FIELDS = ["package_sha256", "qa_status", "publication_authorization"]
ALL = UNIT_FIELDS[:10] + ["rights_status", "rights_evidence_ref",
                          "editorial_status", "editorial_reviewer",
                          "editorial_evidence_ref"] + PKG_FIELDS


def sha(b):
    return hashlib.sha256(b).hexdigest()


def utf8_ok(data, s, e):
    def cont(i):
        return 0 <= i < len(data) and (data[i] & 0xC0) == 0x80
    if cont(s) or (e < len(data) and cont(e)):
        return False
    try:
        data[s:e].decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def record(uid, path, data, s, e, grapheme):
    q = data[s:e]
    return {"unit_id": uid, "source_repo": REPO, "source_ref": REF,
            "source_path": path, "source_sha256": sha(data),
            "byte_start": s, "byte_end_exclusive": e, "quote_sha256": sha(q),
            "utf8_boundary": "VERIFIED" if utf8_ok(data, s, e) else "FAILED",
            "grapheme_boundary": grapheme, "rights_status": "REVIEW",
            "rights_evidence_ref": None, "editorial_status": "HOLD",
            "editorial_reviewer": None, "editorial_evidence_ref": None,
            "package_sha256": None, "qa_status": "NOT_RUN",
            "publication_authorization": None}


def unit_gate(r, sources):
    why = []
    for f in UNIT_FIELDS:
        if r.get(f) is None:
            why.append("NULL:" + f)                                   # R1
    data = sources.get((r.get("source_path"), r.get("source_sha256")))
    s, e = r.get("byte_start"), r.get("byte_end_exclusive")
    if not (isinstance(s, int) and isinstance(e, int) and 0 <= s < e):
        why.append("RANGE_MALFORMED")                                 # R2
    elif data is None:
        why.append("SOURCE_HASH_MISMATCH")                            # R3
    elif e > len(data):
        why.append("RANGE_PAST_END")                                  # R2
    else:
        if sha(data[s:e]) != r.get("quote_sha256"):
            why.append("QUOTE_HASH_MISMATCH")                         # R3
        if not utf8_ok(data, s, e):
            why.append("UTF8_BOUNDARY")                               # R4
    for f in ("utf8_boundary", "grapheme_boundary"):
        if r.get(f) != "VERIFIED":
            why.append(f.upper() + "_NOT_VERIFIED")                   # R4
    for f, ref in (("rights_status", "rights_evidence_ref"),
                   ("editorial_status", "editorial_evidence_ref")):
        if r.get(f) != "APPROVED":
            why.append(f.upper() + "=" + str(r.get(f)))               # R5
        elif not r.get(ref):
            why.append("APPROVED_WITHOUT_EVIDENCE:" + ref)            # R6
    # R7: nothing in this function reads a blob sha or an author field.
    return ("PASS" if not why else "REJECT"), why


def pkg_gate(r):
    why = []
    p = r.get("package_sha256")
    if not (isinstance(p, str) and len(p) == 64
            and all(c in "0123456789abcdef" for c in p)):
        why.append("PACKAGE_SHA256")
    if r.get("qa_status") != "PASS":
        why.append("QA=" + str(r.get("qa_status")))
    a = r.get("publication_authorization")
    if not (isinstance(a, dict) and a.get("by") == "Timothy"
            and a.get("package_sha256") == p):
        why.append("NO_AUTHORIZATION_FOR_THIS_PACKAGE")
    return ("PASS" if not why else "REJECT"), why


def compare(a, b):                                                    # R9
    if (a["source_path"], a["source_sha256"]) != (b["source_path"],
                                                  b["source_sha256"]):
        return "NOT_COMPARABLE"
    s1, e1, s2, e2 = (a["byte_start"], a["byte_end_exclusive"],
                      b["byte_start"], b["byte_end_exclusive"])
    if e1 == s2 or e2 == s1:
        return "ADJACENT"
    return "OVERLAP" if s1 < e2 and s2 < e1 else "DISJOINT"


def main():
    d = sys.argv[1]
    files, sources, checks = {}, {}, []
    for p, want in BLOBS.items():
        data = open(os.path.join(d, p), "rb").read()
        blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        checks.append("blob_ok[%s]=%s" % (p, blob == want))
        files[p] = data
        sources[(p, sha(data))] = data
    recs = []
    for uid, row, p, line, col, chars in TRIAGE:
        data = files[p]
        lines = data.split(b"\n")
        off = sum(len(x) + 1 for x in lines[:line - 1])
        txt = lines[line - 1].decode("utf-8")
        s = off + len(txt[:col - 1].encode("utf-8"))
        e = s + len(txt[col - 1:col - 1 + chars].encode("utf-8"))
        r = record("%s/row%d" % (uid, row), p, data, s, e, "UNVERIFIED")
        recs.append(r)
    ci = files["Collective information"]
    u70 = record("U70", "Collective information", ci, 2123, 2394,
                 "VERIFIED")  # §232 carried, not rerun here
    recs.append(u70)
    out = ["# " + c for c in checks]
    out.append("\t".join(["unit_id", "source_path", "byte_start",
                          "byte_end_exclusive", "quote_sha256_16",
                          "utf8", "grapheme", "unit_gate", "unit_reasons",
                          "pkg_gate", "vs_U70"]))
    for r in recs:
        g, why = unit_gate(r, sources)
        pg, pwhy = pkg_gate(r)
        vs = "-" if r is u70 else compare(r, u70)
        out.append("\t".join(map(str, [
            r["unit_id"], r["source_path"], r["byte_start"],
            r["byte_end_exclusive"], r["quote_sha256"][:16],
            r["utf8_boundary"], r["grapheme_boundary"], g, ",".join(why),
            pg + ":" + ",".join(pwhy), vs])))
    # pairs within a unit: same bytes in two files?
    for uid in ("U01", "U02", "U03"):
        a, b = [r for r in recs if r["unit_id"].startswith(uid)]
        out.append("# %s rows same quote_sha256=%s" % (
            uid, a["quote_sha256"] == b["quote_sha256"]))

    # ---- fixtures (synthetic; expected value written before first run) ----
    syn = b"ab\xc3\xa9cd efgh"  # 'ab' + e-acute (2 bytes) + 'cd efgh'
    SS = {("syn", sha(syn)): syn}

    def base(s, e, **kw):
        r = record("F", "syn", syn, s, e, "VERIFIED")
        r.update(rights_status="APPROVED", rights_evidence_ref="ev:r",
                 editorial_status="APPROVED", editorial_reviewer="rev",
                 editorial_evidence_ref="ev:e")
        r.update(kw)
        return r
    pk = "a" * 64
    fx = [
        ("F1 end<=start", unit_gate(base(4, 4), SS)[0], "REJECT"),
        ("F2 end past file", unit_gate(base(0, 99), SS)[0], "REJECT"),
        ("F3 quote hash wrong", unit_gate(base(0, 2, quote_sha256="0" * 64), SS)[0], "REJECT"),
        ("F4 source hash wrong", unit_gate(base(0, 2, source_sha256="0" * 64), SS)[0], "REJECT"),
        ("F5 all approved+evidence", unit_gate(base(0, 2), SS)[0], "PASS"),
        ("F6 split utf8 at 3", unit_gate(base(3, 6), SS)[0], "REJECT"),
        ("F7 approved, no evidence", unit_gate(base(0, 2, rights_evidence_ref=None), SS)[0], "REJECT"),
        ("F8 adjacent [0,2)[2,4)", compare(base(0, 2), base(2, 4)), "ADJACENT"),
        ("F9 overlap [0,4)[2,6)", compare(base(0, 4), base(2, 6)), "OVERLAP"),
        ("F10 other path", compare(base(0, 2), dict(base(0, 2), source_path="x")), "NOT_COMPARABLE"),
        ("F11 pkg auth for other hash", pkg_gate(base(0, 2, package_sha256=pk, qa_status="PASS",
            publication_authorization={"by": "Timothy", "package_sha256": "b" * 64}))[0], "REJECT"),
    ]
    npass = 0
    for name, got, want in fx:
        ok = got == want
        npass += ok
        out.append("# fixture %s got=%s want=%s %s" % (name, got, want,
                                                       "PASS" if ok else "FAIL"))
    out.append("# fixtures %d/%d PASS" % (npass, len(fx)))
    out.append("# release_allowed(U70)=%s" % (
        unit_gate(u70, sources)[0] == "PASS" and pkg_gate(u70)[0] == "PASS"))
    body = "\n".join(out) + "\n"
    sys.stdout.write(body)
    sys.stdout.write("# in-band sha256=%s\n" % sha(body.encode()))
    with open(os.environ.get("MANIFEST_JSON", os.devnull), "w") as fh:
        json.dump(recs, fh, indent=1, sort_keys=True)
        fh.write("\n")


main()
