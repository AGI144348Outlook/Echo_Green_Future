"""F-001 §216 (Claude, 2026-11-06 17Z): (1) run ChatGPT 16Z fixtures F215-1/F215-2 (GPT numbering) against
the §215 rule; (2) census, over every code point assigned in the stdlib's Unicode data, of where the §215 rule
disagrees with the UAX #29 extended-grapheme-cluster boundaries of the third-party `regex` module (\\X), for a
boundary directly before c (context 'a'+c) and directly after c (c + right context). Synthetic text only.
argv[1] = path to CLAUDE-span-zwj-215.py, argv[2] = path to CLAUDE-span-gap-classes-214.py."""
import contextlib, hashlib, importlib.util, io, json, sys, unicodedata as u
import regex
def load(name, path, *args):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    old = sys.argv; sys.argv = [path, *args]
    try:
        with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    finally: sys.argv = old
    return m
r215 = load("r215", sys.argv[1], sys.argv[2])
def uax(s, i):  # True = boundary at i is INSIDE an extended grapheme cluster (must reject)
    pos, k = set(), 0
    for g in regex.findall(r"\X", s): k += len(g); pos.add(k)
    return 0 < i < len(s) and i not in pos
FX = [("GPT-F215-1 MAN ZWJ WOMAN, end after ZWJ", "\U0001F468‍\U0001F469", 2, True),
      ("GPT-F215-1b whole sequence (boundaries 0 and 3 only)", "\U0001F468‍\U0001F469", 3, False),
      ("GPT-F215-2a ends before Mc, ccc 0 (KA + AA sign U+093E)", "का", 1, True),
      ("GPT-F215-2b ends before Me, ccc 0 ('1' + U+20DD enclosing circle)", "1⃝", 1, True),
      ("CL-F216-1 after Prepend U+0600 (Arabic number sign) + digit", "؀١", 1, True),
      ("CL-F216-2 Indic conjunct KA VIRAMA | SSA (GB9c, Unicode 15.1)", "क्ष", 2, True)]
rows = []
for name, s, i, must in FX:
    b = s.encode(); a215 = r215.rule215(s, i); x = uax(s, i)
    rows.append({"fixture": name, "bytes": len(b), "sha256_16": hashlib.sha256(b).hexdigest()[:16], "boundary": i,
                 "must_reject": must, "ccc_of_next": u.combining(s[i]) if i < len(s) else None,
                 "cat_of_next": u.category(s[i]) if i < len(s) else None,
                 "s215": "rejects" if a215 else "accepts", "uax29_regex": "rejects" if x else "accepts"})
census = {}
for ctx in ("before:a+c", "after:c+a", "after:c+U+0937", "after:c+U+1F469"):
    miss, over = [], []
    for cp in range(0x110000):
        c = chr(cp)
        if u.category(c) in ("Cn", "Cs", "Co"): continue
        if ctx == "before:a+c": s = "a" + c
        else: s = c + {"after:c+a": "a", "after:c+U+0937": "ष", "after:c+U+1F469": "\U0001F469"}[ctx]
        a, x = r215.rule215(s, 1), uax(s, 1)
        if x and not a: miss.append(cp)
        elif a and not x: over.append(cp)
    def ranges(l):
        out = []
        for cp in l:
            if out and out[-1][1] == cp - 1: out[-1][1] = cp
            else: out.append([cp, cp])
        return ["%04X" % a if a == b else "%04X-%04X" % (a, b) for a, b in out]
    census[ctx] = {"s215_accepts_but_uax29_joins": len(miss), "miss_ranges_first20": ranges(miss)[:20],
                   "miss_cats": sorted({u.category(chr(c)) for c in miss}),
                   "s215_rejects_but_uax29_breaks": len(over), "over_cats": sorted({u.category(chr(c)) for c in over})}
print(json.dumps({"unicode_stdlib": u.unidata_version, "regex": regex.__version__, "fixtures": rows, "census": census},
                 indent=1, sort_keys=True))
