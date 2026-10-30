"""F-001 rights-scan counter (Claude 19Z, §172). Read-only on a TAM checkout; prints counts only, never the matched text.
Implements the §9 step 3 inventory as counts per file: image references, links, block quotes, quoted spans,
code fences, licence/copyright words, font names, and personal-data patterns (emails, phone-like numbers).
A count is a pointer for a human reader, not a rights finding. Usage: python3 -I rights_scan.py <tam dir> [files...]"""
import sys, os, re, json, hashlib, subprocess
FILES = ["README.md", "Article 1 Hacksilber", "Article 2 Water Weight Computes", "The Color Dyed and Dental Records",
         "Article 5", "Article 6", "Article 10", "Collective information",
         "URLs to storedNotebookLM Diagramed Infographics"]
PAT = {
    "image_refs": r"!\[[^\]]*\]\([^)]*\)|<img\b|\.(?:png|jpe?g|gif|svg|webp)\b",
    "links": r"https?://\S+",
    "notebooklm_links": r"notebooklm\.google\.com\S*",
    "block_quote_lines": r"(?m)^\s*>",
    "quoted_spans_40plus": r"[\"“][^\"”\n]{40,}[\"”]",
    "code_fences": r"(?m)^\s*```",
    "licence_words": r"(?i)\b(?:copyright|licen[cs]e|all rights reserved|creative commons|cc[- ]by)\b|©",
    "font_words": r"(?i)\bfont(?:-family)?\b|\.(?:ttf|otf|woff2?)\b",
    "email_like": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "phone_like": r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)",
}
def main(d, files):
    out = {"tam_head": subprocess.run(["git", "-C", d, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip(), "files": {}}
    for f in files:
        p = os.path.join(d, f)
        if not os.path.isfile(p): out["files"][f] = "MISSING"; continue
        b = open(p, "rb").read(); t = b.decode("utf-8", "replace")
        blob = subprocess.run(["git", "-C", d, "hash-object", p], capture_output=True, text=True).stdout.strip()[:7]
        out["files"][f] = {"blob": blob, "bytes": len(b), **{k: len(re.findall(v, t)) for k, v in PAT.items()}}
    tot = {k: sum(v[k] for v in out["files"].values() if isinstance(v, dict)) for k in PAT}
    out["totals"] = tot
    print(json.dumps(out, indent=1, sort_keys=True))
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:] or FILES)
