"""F-001 §213 probe (Claude 14Z): where does a ccc-only check (unicodedata.combining(c) != 0) miss a
character that must not start a span because it attaches to the previous one? Stdlib only."""
import sys, unicodedata as u, hashlib, collections
print('python', sys.version.split()[0], 'unicodedata', u.unidata_version)
miss = collections.Counter(); ex = {}
for cp in range(0x110000):
    c = chr(cp); cat = u.category(c)
    if cat in ('Mn', 'Mc', 'Me') and u.combining(c) == 0:
        miss[cat] += 1; ex.setdefault(cat, []).append(f'U+{cp:04X}')
print('marks with ccc 0:', dict(miss), {k: v[:4] for k, v in ex.items()})
heb = [cp for cp in range(0x0590, 0x0600) if u.category(chr(cp)) in ('Mn','Mc','Me')]
heb0 = [f'U+{cp:04X}' for cp in heb if u.combining(chr(cp)) == 0]
print('Hebrew block marks', len(heb), 'with ccc 0:', heb0)
def ccc_only(s, i): return i > 0 and u.combining(s[i]) != 0
def cat_rule(s, i): return i > 0 and (u.category(s[i]) in ('Mn','Mc','Me') or s[i] in '‍︎️')
F = [  # (id, text NFC, span start index (0-based codepoint), expected: start splits a sequence?)
 ('F213-1 Hebrew bet+dagesh, start on dagesh', u.normalize('NFC','בּר'), 1, True),
 ('F213-2 Hebrew shin+shin-dot+qamats, start on qamats', u.normalize('NFC','שָׁ'), 2, True),
 ('F213-3 Devanagari ka+aa (Mc), start on aa', u.normalize('NFC','का'), 1, True),
 ('F213-4 ZWJ inside emoji sequence, start on ZWJ', '\U0001F469‍\U0001F4BB', 1, True),
 ('F213-5 Hebrew plain letters, start on letter', 'אבג', 1, False),
]
for fid, s, i, exp in F:
    b = s.encode('utf-8')
    print(fid, '| nfc', u.is_normalized('NFC', s), '| sha256', hashlib.sha256(b).hexdigest()[:16], '| bytes', len(b),
          '| expected', exp, '| ccc-only', ccc_only(s, i), '| category rule', cat_rule(s, i))
