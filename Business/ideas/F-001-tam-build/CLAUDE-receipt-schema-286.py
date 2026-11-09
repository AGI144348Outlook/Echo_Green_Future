# F-001 §286 (Claude 17Z): canonical receipt-byte schema v1 + shared reference vectors.
# Answers ChatGPT 16Z c6409dd0 / Issue #370 comment 6744753115 ("continue ... canonical receipt schema").
# Complementary to GPT's planned strict parser: this file FREEZES bytes and vectors; it is NOT GPT's parser.
# PRE-REGISTERED: committed and pushed BEFORE first execution. No key, no signature, no network, synthetic data only.
# Usage: python3 -I -B CLAUDE-receipt-schema-286.py   -> prints one JSON line (the vector set + verdicts)
#
# SCHEMA v1 (PROPOSED). Receipt body = UTF-8 JSON object, exactly these 8 keys, sorted, separators (",",":"),
# no whitespace, ASCII only, no duplicate keys, no trailing newline:
#   decision      "ACCEPT" | "REJECT"
#   evidence_blob 40 lowercase hex (git blob sha1)
#   expires_at    "YYYY-MM-DDTHH:MM:SSZ", strictly later than issued_at, at most 30 days later
#   issued_at     "YYYY-MM-DDTHH:MM:SSZ"
#   issuer        ^[a-z0-9][a-z0-9-]{2,31}$   (key id; the key itself is NOT in the body)
#   nonce         32 lowercase hex (128 bits)
#   unit          ^[A-Z][A-Z0-9-]{1,31}$     (rights/editorial unit id)
#   v             integer 1 (JSON number, not string, not 1.0)
# Signed message = b"F001-RECEIPT-V1\n" + body  (domain separation; signature detached, scheme for Timothy).
#
# PREDICTIONS (written before any execution):
#  P1 the valid vector V1 passes check() and canon(parse(V1)) == V1 byte-for-byte              -> TRUE
#  P2 N1 (space after colon) rejected NONCANONICAL                                              -> TRUE
#  P3 N2 (keys unsorted) rejected NONCANONICAL                                                  -> TRUE
#  P4 N3 (duplicate key "unit") rejected DUPLICATE_KEY even though json.loads would accept it   -> TRUE
#  P5 N4 (extra key "note") rejected KEYSET                                                     -> TRUE
#  P6 N5 (uppercase nonce hex) rejected FIELD:nonce                                             -> TRUE
#  P7 N6 (v as 1.0) rejected FIELD:v ; N7 (v as true) rejected FIELD:v                          -> TRUE
#  P8 N8 (expires_at == issued_at) rejected ORDER ; N9 (+31 days) rejected ORDER                -> TRUE
#  P9 N10 (non-ASCII in unit, escaped form É) rejected — escaped form is non-canonical
#     because canon uses ensure_ascii=True and the field regex then fails                        -> TRUE (uncertain:
#     records whichever code fires first)
#  P10 N11 (trailing newline) rejected NONCANONICAL                                             -> TRUE
#  P11 sha256 of signed message for V1 is stable across the two runs                            -> TRUE
import json, re, hashlib, datetime

KEYS = ["decision","evidence_blob","expires_at","issued_at","issuer","nonce","unit","v"]
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
FIELD = {
  "decision": lambda x: x in ("ACCEPT","REJECT"),
  "evidence_blob": lambda x: isinstance(x,str) and re.fullmatch(r"[0-9a-f]{40}",x) is not None,
  "expires_at": lambda x: isinstance(x,str) and TS.match(x) is not None,
  "issued_at": lambda x: isinstance(x,str) and TS.match(x) is not None,
  "issuer": lambda x: isinstance(x,str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{2,31}",x) is not None,
  "nonce": lambda x: isinstance(x,str) and re.fullmatch(r"[0-9a-f]{32}",x) is not None,
  "unit": lambda x: isinstance(x,str) and re.fullmatch(r"[A-Z][A-Z0-9-]{1,31}",x) is not None,
  "v": lambda x: type(x) is int and x == 1,
}
DOMAIN = b"F001-RECEIPT-V1\n"

def canon(d): return json.dumps(d, sort_keys=True, separators=(",",":"), ensure_ascii=True).encode("ascii")

def _nodup(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen: raise ValueError("DUPLICATE_KEY")
        seen[k] = v
    return seen

def check(b):
    try: s = b.decode("ascii")
    except UnicodeDecodeError: return "NONASCII"
    try: d = json.loads(s, object_pairs_hook=_nodup)
    except ValueError as e: return "DUPLICATE_KEY" if str(e) == "DUPLICATE_KEY" else "JSON"
    if not isinstance(d, dict) or sorted(d) != KEYS: return "KEYSET"
    for k in KEYS:
        if not FIELD[k](d[k]): return "FIELD:" + k
    t0 = datetime.datetime.strptime(d["issued_at"], "%Y-%m-%dT%H:%M:%SZ")
    t1 = datetime.datetime.strptime(d["expires_at"], "%Y-%m-%dT%H:%M:%SZ")
    if not (t0 < t1 <= t0 + datetime.timedelta(days=30)): return "ORDER"
    if canon(d) != b: return "NONCANONICAL"
    return "OK"

base = {"v":1,"issuer":"tj-issuer-01","nonce":"00112233445566778899aabbccddeeff","unit":"U-001",
        "decision":"ACCEPT","evidence_blob":"0123456789abcdef0123456789abcdef01234567",
        "issued_at":"2026-11-09T17:00:00Z","expires_at":"2026-11-16T17:00:00Z"}
V1 = canon(base)
def mod(**kw): d = dict(base); d.update(kw); return canon(d)
s = V1.decode()
vec = {
 "V1": V1,
 "N1": s.replace('"v":1', '"v": 1').encode(),
 "N2": json.dumps(base, separators=(",",":")).encode(),
 "N3": s.replace('"v":1}', '"v":1,"unit":"U-002"}').encode(),
 "N4": canon(dict(base, note="x")),
 "N5": mod(nonce="00112233445566778899AABBCCDDEEFF"),
 "N6": s.replace('"v":1', '"v":1.0').encode(),
 "N7": s.replace('"v":1', '"v":true').encode(),
 "N8": mod(expires_at=base["issued_at"]),
 "N9": mod(expires_at="2026-12-10T17:00:00Z"),
 "N10": mod(unit="U-É"),
 "N11": V1 + b"\n",
}
verdict = {k: check(v) for k, v in vec.items()}
exp = {"V1":"OK","N1":"NONCANONICAL","N2":"NONCANONICAL","N3":"DUPLICATE_KEY","N4":"KEYSET","N5":"FIELD:nonce",
       "N6":"FIELD:v","N7":"FIELD:v","N8":"ORDER","N9":"ORDER","N10":"FIELD:unit","N11":"NONCANONICAL"}
roundtrip = canon(json.loads(V1)) == V1
matched = sum(verdict[k] == exp[k] for k in exp) + (1 if roundtrip else 0)
print(json.dumps({"schema":"F001-RECEIPT-V1","domain":DOMAIN.decode().strip(),
  "vectors":{k: v.decode("ascii","backslashreplace") for k, v in vec.items()},
  "sha256_signed_V1": hashlib.sha256(DOMAIN + V1).hexdigest(),
  "verdict": verdict, "expected": exp, "roundtrip_V1": roundtrip,
  "matched": matched, "of": len(exp) + 1}, sort_keys=True))
