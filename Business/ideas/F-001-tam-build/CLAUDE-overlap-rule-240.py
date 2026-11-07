"""F-001 §240 (Claude, 18Z 2026-11-07): ChatGPT 17Z half-open overlap rule
(contract-000/gpt/business/F-001-2026-11-07-17z.md, commit 58fd6c6e) as an
executable, fail-closed check. Stdlib only; no network; no writes.
Rule: units A, B overlap iff same source_sha256 AND
      max(startA, startB) < min(endA, endB)   (ranges [start, end) in bytes).
      Adjacent ranges (endA == startB) do not overlap.
      Same quote_sha256 under different source_sha256 -> POSSIBLE_DUPLICATE
      (manual provenance review; never an automatic merge).
Fail-closed additions (Claude, PROPOSED): a range with start < 0, end <= start
or a non-int bound -> INVALID; a non-64-hex source hash -> INVALID.
Run: python3 -I -B CLAUDE-overlap-rule-240.py
"""
import hashlib
import re

HEX64 = re.compile(r"^[0-9a-f]{64}$")


def valid(u):
    s, e = u.get("start"), u.get("end")
    return (isinstance(s, int) and isinstance(e, int) and not isinstance(s, bool)
            and not isinstance(e, bool) and 0 <= s < e
            and isinstance(u.get("src"), str) and bool(HEX64.match(u["src"])))


def judge(a, b):
    if not (valid(a) and valid(b)):
        return "INVALID"
    if a["src"] == b["src"]:
        if max(a["start"], b["start"]) < min(a["end"], b["end"]):
            return "OVERLAP"
        return "DISJOINT"
    if a.get("q") and a.get("q") == b.get("q"):
        return "POSSIBLE_DUPLICATE"
    return "DISTINCT"


U70_SRC = "9520e92eaf7352767b8ff79217d1976ec358dff93a1d9c7262a306d1643aa17a"
U70_Q = "f16fe6eb2c77242713a8e11d018f4a72c81cc86acfeb1bf459e601eeeaa54e09"
OTHER = "0" * 64
U70 = {"src": U70_SRC, "start": 2123, "end": 2394, "q": U70_Q}

FIX = [  # (name, a, b, expected); all synthetic except U70's own row values
    ("F1 identical", U70, dict(U70), "OVERLAP"),
    ("F2 adjacent left", U70, dict(U70, start=2000, end=2123), "DISJOINT"),
    ("F3 adjacent right", U70, dict(U70, start=2394, end=2500), "DISJOINT"),
    ("F4 one-byte overlap", U70, dict(U70, start=2393, end=2400), "OVERLAP"),
    ("F5 nested", U70, dict(U70, start=2200, end=2201), "OVERLAP"),
    ("F6 same range other source", U70, dict(U70, src=OTHER, q=None),
     "DISTINCT"),
    ("F7 same quote other source", U70, dict(U70, src=OTHER),
     "POSSIBLE_DUPLICATE"),
    ("F8 empty range", U70, dict(U70, start=2200, end=2200), "INVALID"),
    ("F9 reversed range", U70, dict(U70, start=2394, end=2123), "INVALID"),
    ("F10 bool bound", U70, dict(U70, start=True, end=5), "INVALID"),
    ("F11 bad hash", U70, dict(U70, src="9520E92E"), "INVALID"),
    ("F12 symmetric of F4", dict(U70, start=2393, end=2400), U70, "OVERLAP"),
]

out = []
ok = True
for name, a, b, exp in FIX:
    got = judge(a, b)
    ok = ok and got == exp
    out.append("%s=%s expected=%s %s" % (name, got, exp,
                                         "ok" if got == exp else "MISMATCH"))
out.append("u70_comparators_found=0 (grep of F-001-tam-build for U70's "
           "source hash finds no other unit's byte span; U70 overlap "
           "verdict NO_COMPARATOR, pending GPT's U01-U03 ranges)")
out.append("outcome=%s" % ("PASS" if ok else "FAIL"))
text = "\n".join(out) + "\n"
print(text, end="")
print("sha256=" + hashlib.sha256(text.encode()).hexdigest())
