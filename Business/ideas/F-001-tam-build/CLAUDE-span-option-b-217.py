"""F-001 §217 (Claude, 2026-11-06 18Z): implement §216 option (b) (stdlib lists on top of §215) and measure
what it still misses against the UAX #29 oracle (third-party `regex` \\X), over (1) the §216 one-character
census contexts and (2) every two-character virama context V+L (all ccc=9 code points x all letters of the
same script block +-0x80) with boundary after V. Option (a) is oracle OR §215, so it has zero misses by
construction; it is checked here only for over-rejection. Synthetic text only.
argv[1] = path to CLAUDE-span-zwj-215.py, argv[2] = path to CLAUDE-span-gap-classes-214.py."""
import contextlib, importlib.util, io, json, sys, unicodedata as u
import regex
def load(name, path, *args):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    old = sys.argv; sys.argv = [path, *args]
    try:
        with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    finally: sys.argv = old
    return m
r215 = load("r215", sys.argv[1], sys.argv[2])
PREPEND = {0x0600,0x0601,0x0602,0x0603,0x0604,0x0605,0x06DD,0x070F,0x0890,0x0891,0x08E2,0x0D4E,0x110BD,0x110CD,
           0x111C2,0x111C3,0x1193F,0x11941,0x11A84,0x11A85,0x11A86,0x11A87,0x11A88,0x11A89,0x11D46,0x11F02}
NO_BEFORE = {0x200C,0x0E33,0x0EB3,0xFF9E,0xFF9F} | set(range(0xE0020, 0xE0080))
VIRAMA_B = {0x094D,0x09CD,0x0ACD,0x0B4D,0x0C4D,0x0D4D}
def rule217b(s, i):
    if not (0 < i < len(s)): return False
    if r215.rule215(s, i): return True
    if ord(s[i-1]) in PREPEND or ord(s[i]) in NO_BEFORE: return True
    return ord(s[i-1]) in VIRAMA_B and u.category(s[i]).startswith("L")
def uax(s, i):
    pos, k = set(), 0
    for g in regex.findall(r"\X", s): k += len(g); pos.add(k)
    return 0 < i < len(s) and i not in pos
def rule217a(s, i): return uax(s, i) or r215.rule215(s, i)
def ranges(l):
    out = []
    for cp in l:
        if out and out[-1][1] == cp - 1: out[-1][1] = cp
        else: out.append([cp, cp])
    return ["%04X" % a if a == b else "%04X-%04X" % (a, b) for a, b in out]
res = {"unicode_stdlib": u.unidata_version, "regex": regex.__version__, "census_b": {}, "census_a_over": {}}
assigned = [cp for cp in range(0x110000) if u.category(chr(cp)) not in ("Cn", "Cs", "Co")]
for ctx in ("before:a+c", "after:c+a", "after:c+U+0937", "after:c+U+1F469"):
    miss, over, over_a = [], [], 0
    for cp in assigned:
        c = chr(cp)
        s = "a" + c if ctx == "before:a+c" else c + {"after:c+a": "a", "after:c+U+0937": "ष", "after:c+U+1F469": "\U0001F469"}[ctx]
        b, x = rule217b(s, 1), uax(s, 1)
        if x and not b: miss.append(cp)
        elif b and not x: over.append(cp)
        if rule217a(s, 1) and not x: over_a += 1
    res["census_b"][ctx] = {"miss": len(miss), "miss_ranges_first20": ranges(miss)[:20],
                            "miss_cats": sorted({u.category(chr(c)) for c in miss}), "over": len(over)}
    res["census_a_over"][ctx] = over_a
viramas = [cp for cp in assigned if u.combining(chr(cp)) == 9]
vmiss, vover, vtotal = {}, {}, 0
for v in viramas:
    for cp in range(max(0, v - 0x80), v + 0x80):
        c = chr(cp)
        if not u.category(c).startswith("L"): continue
        s = chr(v) + c; vtotal += 1; b, x = rule217b(s, 1), uax(s, 1)
        if x and not b: vmiss["%04X" % v] = vmiss.get("%04X" % v, 0) + 1
        elif b and not x: vover["%04X" % v] = vover.get("%04X" % v, 0) + 1
res["virama_pairs"] = {"viramas_ccc9": len(viramas), "pairs": vtotal, "b_misses_by_virama": vmiss,
                       "b_over_by_virama": vover}
print(json.dumps(res, indent=1, sort_keys=True))
