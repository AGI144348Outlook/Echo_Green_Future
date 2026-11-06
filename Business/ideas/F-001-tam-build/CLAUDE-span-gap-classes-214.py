"""F-001 §214 probe (Claude 15Z): which grapheme-joining cases does the §213 category rule
(no span boundary before Mn/Mc/Me, U+200D, U+FE0E, U+FE0F) still miss? Stdlib only, synthetic text."""
import sys, unicodedata as u, hashlib
print('python', sys.version.split()[0], 'unicodedata', u.unidata_version)
def cat213(s, i): return 0 < i < len(s) and (u.category(s[i]) in ('Mn','Mc','Me') or s[i] in '‍︎️')
def is_ri(c): return 0x1F1E6 <= ord(c) <= 0x1F1FF
def is_emod(c): return 0x1F3FB <= ord(c) <= 0x1F3FF
def jamo_vt(c): return 0x1160 <= ord(c) <= 0x11FF or 0xD7B0 <= ord(c) <= 0xD7FF
def vs(c): return 0xFE00 <= ord(c) <= 0xFE0F or 0xE0100 <= ord(c) <= 0xE01EF
def rule214(s, i):
    if not (0 < i < len(s)): return False
    c, p = s[i], s[i-1]
    if cat213(s, i) or vs(c) or is_emod(c) or jamo_vt(c): return True
    if p == '\r' and c == '\n': return True
    if is_ri(c) and is_ri(p):  # inside a flag pair iff odd count of RI before c in the run
        k = 0; j = i - 1
        while j >= 0 and is_ri(s[j]): k += 1; j -= 1
        return k % 2 == 1
    return False
def missed(cps): return sum(1 for cp in cps if u.category(chr(cp)) not in ('Mn','Mc','Me','Cn') and chr(cp) not in '\u200d\ufe0e\ufe0f')
cnt = {'variation selectors (all Mn, so caught)': missed(list(range(0xFE00,0xFE10))+list(range(0xE0100,0xE01F0))),
       'emoji modifiers (Sk)': missed(range(0x1F3FB,0x1F400)),
       'Hangul V/T jamo (Lo)': missed(list(range(0x1160,0x1200))+list(range(0xD7B0,0xD800))),
       'regional indicators (So)': missed(range(0x1F1E6,0x1F200))}
print('not caught by §213 rule:', cnt)
F = [
 ('F214-1 skin-tone modifier, boundary before modifier', '\U0001F44B\U0001F3FD', 1, True),
 ('F214-2 flag pair, boundary between the two RIs', '\U0001F1FA\U0001F1F8', 1, True),
 ('F214-3 two flags, boundary between flags', '\U0001F1FA\U0001F1F8\U0001F1E9\U0001F1EA', 2, False),
 ('F214-4 decomposed Hangul L+V, boundary before V', '가', 1, True),
 ('F214-5 CR LF, boundary between', '\r\n', 1, True),
 ('F214-6 ideographic VS (U+E0100), boundary before it', '葛\U000E0100', 1, True),
 ('F214-7 Hebrew plain letters', 'אבג', 1, False),
]
for fid, s, i, exp in F:
    b = s.encode('utf-8')
    print(fid, '| nfc', u.is_normalized('NFC', s), '| bytes', len(b), '| sha256', hashlib.sha256(b).hexdigest()[:16],
          '| expected', exp, '| §213', cat213(s, i), '| §214', rule214(s, i))
