"""F-001 quoted-span worksheet (Claude 20Z, §173). Read-only on a TAM checkout. Uses the SAME quoted-span
pattern as rights_scan.py (§172) and prints one row per span: file, blob, line, column, length, and two
counts-only cues. It NEVER prints the quoted text or its neighbours. The last column is left blank for a human:
own phrasing / third-party / unsure. A cue is a pointer, not a finding.
Usage: python3 -I rights_rows.py <tam dir> [files...]  > worksheet.tsv"""
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rights_scan import FILES, PAT  # same pattern and file list as §172

SPAN = re.compile(PAT["quoted_spans_40plus"])
# Attribution cue: a reporting word within 60 characters before or after the span (counts only).
CUE = re.compile(r"(?i)\b(?:said|says|wrote|writes|according to|quoted|states|stated|cited|per|by)\b")
URL = re.compile(PAT["links"])


def rows(d, files):
    yield ["row", "file", "blob", "line", "col", "chars", "cue_words_within_60", "url_same_line", "classification"]
    n = 0
    for f in files:
        p = os.path.join(d, f)
        if not os.path.isfile(p):
            continue
        t = open(p, "rb").read().decode("utf-8", "replace")
        blob = subprocess.run(["git", "-C", d, "hash-object", p], capture_output=True, text=True).stdout.strip()[:7]
        for m in SPAN.finditer(t):
            n += 1
            line = t.count("\n", 0, m.start()) + 1
            col = m.start() - (t.rfind("\n", 0, m.start()) + 1) + 1
            near = t[max(0, m.start() - 60):m.start()] + " " + t[m.end():m.end() + 60]
            ls, le = t.rfind("\n", 0, m.start()) + 1, t.find("\n", m.end())
            same_line = t[ls:le if le != -1 else len(t)]
            yield [str(n), f, blob, str(line), str(col), str(m.end() - m.start()),
                   str(len(CUE.findall(near))), "yes" if URL.search(same_line) else "no", ""]


if __name__ == "__main__":
    for r in rows(sys.argv[1], sys.argv[2:] or FILES):
        print("\t".join(r))
