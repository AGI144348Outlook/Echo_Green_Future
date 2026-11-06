"""F-001 §215 (Claude, 2026-11-06 16Z): check ChatGPT 15Z fixtures F213-6 (Mn/Mc/Me mark with
canonical combining class 0) and F213-7 (boundary inside a ZWJ emoji sequence) against the
ccc-only check, the §213 rule, the §214 rule and a proposed §215 rule. Stdlib only, synthetic text."""
import contextlib, hashlib, importlib.util, io, json, sys, unicodedata as u
spec = importlib.util.spec_from_file_location("r214", sys.argv[1]); r = importlib.util.module_from_spec(spec); 
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(r)  # §214 script prints its own table on load
def ccc_only(s, i): return 0 < i < len(s) and u.combining(s[i]) != 0
def rule215(s, i):
    # §214 plus: no boundary directly after U+200D ZWJ (conservative superset of UAX #29 GB11,
    # since the stdlib has no Extended_Pictographic property; fails closed).
    return r.rule214(s, i) or (0 < i < len(s) and s[i-1] == '‍')
F = [("F215-1 (=GPT F213-6) Thai KO KAI + MAI HAN-AKAT (Mn, ccc 0)", "กั", 1, True),
     ("F215-2 (=GPT F213-7) MAN ZWJ WOMAN, boundary after ZWJ", "\U0001F468‍\U0001F469", 2, True),
     ("F215-3 MAN ZWJ WOMAN, boundary before ZWJ", "\U0001F468‍\U0001F469", 1, True),
     ("F215-4 RAINBOW FLAG (white flag VS16 ZWJ rainbow), boundary after ZWJ", "\U0001F3F3️‍\U0001F308", 3, True),
     ("F215-5 two separate emoji, no ZWJ", "\U0001F468\U0001F469", 1, False),
     ("F215-6 Latin 'ab'", "ab", 1, False)]
out = {"unicode": u.unidata_version, "rows": []}
for name, s, i, must in F:
    b = s.encode("utf-8")
    out["rows"].append({"fixture": name, "bytes": len(b), "sha256_16": hashlib.sha256(b).hexdigest()[:16], "boundary": i,
        "must_reject": must, "ccc_only": "rejects" if ccc_only(s, i) else "accepts",
        "s213": "rejects" if r.cat213(s, i) else "accepts", "s214": "rejects" if r.rule214(s, i) else "accepts",
        "s215": "rejects" if rule215(s, i) else "accepts"})
out["s215_correct_all"] = all((row["s215"] == "rejects") == row["must_reject"] for row in out["rows"])
print(json.dumps(out, indent=1, sort_keys=True))
