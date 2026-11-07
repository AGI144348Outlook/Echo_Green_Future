# F-001 §228 (Claude 2026-11-07 06Z): for every row of QUOTED-SPANS-TRIAGE-174.tsv, locate the span in
# The-TAM-protocol@d46456a1 and report the 0-based index of its opening quote among the same-style
# quote characters on its line (straight U+0022 counted on their own; curly U+201C/U+201D counted
# together). Odd index for straight quotes = the span runs from a closing quote to the next opening
# quote, i.e. the gap BETWEEN two quotations. Prints JSON only; no quoted text is printed.
# Usage: python3 -I -B CLAUDE-quote-parity-228.py <TRIAGE tsv> <path to The-TAM-protocol clone>
import csv, json, subprocess, sys
tri, repo = sys.argv[1], sys.argv[2]
cache, out = {}, []
for r in csv.DictReader(open(tri, encoding="utf-8"), delimiter="\t"):
    f = r["file"]
    if f not in cache:
        cache[f] = subprocess.run(["git", "-C", repo, "show", f"d46456a1:{f}"], capture_output=True, check=True).stdout.decode("utf-8")
    t = cache[f]; lines = t.split("\n"); ln, col, n = int(r["line"]), int(r["col"]), int(r["chars"])
    s = sum(len(l) + 1 for l in lines[:ln - 1]) + col - 1; e = s + n
    L = lines[ln - 1]; o = s - sum(len(l) + 1 for l in lines[:ln - 1])
    c0, c1 = t[s], t[e - 1]
    if c0 == '"':
        idx = [i for i, c in enumerate(L) if c == '"']; style = "straight"
    else:
        idx = [i for i, c in enumerate(L) if c in "“”"]; style = "curly"
    k = idx.index(o) if o in idx else None
    out.append({"row": int(r["row"]), "style": style, "open_cp": f"U+{ord(c0):04X}", "close_cp": f"U+{ord(c1):04X}",
                "quotes_on_line": len(idx), "open_index": k,
                "prev_is_alnum": s > 0 and t[s-1].isalnum(), "next_is_alnum": e < len(t) and t[e].isalnum(),
                "inter_quote_gap": style == "straight" and k is not None and k % 2 == 1})
summary = {"rows": len(out), "straight": sum(x["style"] == "straight" for x in out),
           "curly": sum(x["style"] == "curly" for x in out),
           "inter_quote_gap_rows": [x["row"] for x in out if x["inter_quote_gap"]],
           "odd_quote_count_lines_rows": [x["row"] for x in out if x["quotes_on_line"] % 2 == 1],
           "word_attached_both_edges_rows": [x["row"] for x in out if x["prev_is_alnum"] and x["next_is_alnum"]]}
print(json.dumps({"summary": summary, "rows": out}, sort_keys=True))
