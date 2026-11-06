"""F-001 §218 (Claude, 2026-11-06 19Z): group the fail-closed over-rejections of §217 option (b) into
classes a human can adjudicate once per class, instead of ~960 single cases (ChatGPT 19Z, 47410cb6:
over-rejections stay release blockers until adjudicated). Over-rejection = option (b) forbids a span
boundary that the UAX #29 oracle (`regex` \\X) allows. Synthetic one/two-character text only.
argv[1] = CLAUDE-span-option-b-217.py, argv[2] = CLAUDE-span-zwj-215.py, argv[3] = CLAUDE-span-gap-classes-214.py.
Loading §217 re-runs its census (output discarded); this script only reads its functions."""
import contextlib, importlib.util, io, json, re, sys, unicodedata as u
def load(name, path, *args):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    old = sys.argv; sys.argv = [path, *args]
    try:
        with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    finally: sys.argv = old
    return m
b = load("b217", sys.argv[1], sys.argv[2], sys.argv[3])
def why(s, i):
    if b.r215.rule215(s, i): return "rule215"
    if ord(s[i-1]) in b.PREPEND: return "PREPEND"
    if ord(s[i]) in b.NO_BEFORE: return "NO_BEFORE"
    return "VIRAMA_B"
VOWEL = re.compile(r" LETTER (SHORT |CANDRA |VOCALIC |PRISHTHAMATRA )?(A|AA|I|II|U|UU|E|EE|AI|O|OO|AU|R|RR|L|LL)$")
classes = {}
def add(ctx, s, extra):
    k = ctx + " | " + why(s, 1) + " | " + extra
    classes.setdefault(k, {"n": 0, "examples": []}); classes[k]["n"] += 1
    if len(classes[k]["examples"]) < 3: classes[k]["examples"].append(" ".join("U+%04X" % ord(c) for c in s))
assigned = [cp for cp in range(0x110000) if u.category(chr(cp)) not in ("Cn", "Cs", "Co")]
for ctx, mk in (("before:a+c", lambda c: "a" + c), ("after:c+a", lambda c: c + "a")):
    for cp in assigned:
        s = mk(chr(cp))
        if b.rule217b(s, 1) and not b.uax(s, 1): add(ctx, s, "cat=" + u.category(chr(cp)))
for v in sorted(b.VIRAMA_B):
    for cp in range(max(0, v - 0x80), v + 0x80):
        c = chr(cp)
        if not u.category(c).startswith("L"): continue
        s = chr(v) + c
        if b.rule217b(s, 1) and not b.uax(s, 1):
            add("virama+letter", s, "V=%04X next=%s" % (v, "independent-vowel(by name)" if VOWEL.search(u.name(c, "")) else "other-letter"))
out = {"unicode_stdlib": u.unidata_version, "regex": b.regex.__version__,
       "total": sum(x["n"] for x in classes.values()), "n_classes": len(classes),
       "classes": dict(sorted(classes.items()))}
print(json.dumps(out, indent=1, sort_keys=True))
