# F-001 §178 (Claude 01Z, 2026-10-31): independent replay of GPT Run480's pinned v472 HTML through the Node CLIs, plus a headless
# Chromium load (desktop + phone-sized emulation; not a real Android device, not a screen reader).
# Usage: python3 -I gpt480_cli_replay.py /abs/dir   (dir holds the six files below, copied byte-exact from
#        contract-000-gpt-run480-20261030-2000:contract-000/gpt/business/). Needs node and Python playwright. No network use.
import json, os, subprocess, sys, hashlib
from playwright.sync_api import sync_playwright
d = sys.argv[1]; os.chdir(d)
G, T = "f001_review_companion_472.js", "test_f001_review_dom_476.js"
R, L, I = "F-001-EDITORIAL-DECISIONS-458.tsv", "F-001-SOURCE-LOCATION-RESULTS-462.tsv", "F-001-DECISION-INTAKE-PENDING-463.tsv"
GPT_HTML, PIN = "F-001-82-EDITORIAL-REVIEW-DRAFT-480.html", "090693176dce082e4a40bf77abb821f3844e0918"
def blob(p):
    b = open(p, "rb").read(); return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
def node(*a): r = subprocess.run(["node", *a], capture_output=True, text=True); return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:]
for f in ("c1.html", "c2.html", "c3.html", "c4.html", "tampered.html"):
    if os.path.exists(f): os.remove(f)
out = {"inputs": {f: blob(f) for f in (G, T, R, L, I, GPT_HTML)}}
rows = {}
rows["P1 CLI generate"] = node(G, R, L, I, "c1.html"); rows["P1 output blob"] = blob("c1.html")
rows["P1 byte-identical to GPT 480 artifact"] = open("c1.html", "rb").read() == open(GPT_HTML, "rb").read()
node(G, R, L, I, "c2.html"); rows["P2 second generate identical"] = open("c1.html", "rb").read() == open("c2.html", "rb").read()
rows["N1 output exists (wx)"] = node(G, R, L, I, "c1.html")
open("t_r.tsv", "wb").write(open(R, "rb").read() + b"\n")
rows["N2 register +1 byte"] = list(node(G, "t_r.tsv", L, I, "c3.html")) + [os.path.exists("c3.html")]
rows["N3 location/intake swapped"] = list(node(G, R, I, L, "c4.html")) + [os.path.exists("c4.html")]
rows["H1 harness CLI, correct pin"] = node(T, "c1.html", PIN)
rows["H2 harness CLI, wrong pin"] = node(T, "c1.html", "0" * 40)
open("tampered.html", "w").write(open("c1.html").read().replace("NOT an approval", "an approval"))
rows["H3 tampered html, original pin"] = node(T, "tampered.html", PIN)
rows["H4 tampered html, its own pin"] = node(T, "tampered.html", blob("tampered.html"))
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, ca in [("desktop", {}), ("phone-emulated", dict(viewport={"width": 412, "height": 915}, device_scale_factor=2.6, is_mobile=True, has_touch=True))]:
        ctx = b.new_context(**ca); pg = ctx.new_page(); errs, net = [], []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("request", lambda r: net.append(r.url) if not r.url.startswith(("file:", "blob:", "data:")) else None)
        pg.goto("file://" + os.path.join(d, "c1.html")); pg.wait_for_timeout(400)
        rows["C " + name] = {"page_errors": len(errs), "outbound_requests": len(net), "articles": pg.locator("article").count(),
                             "hold_in_text": "HOLD" in pg.inner_text("body"), "approved_option": pg.locator('option[value="APPROVED"]').count(),
                             "horizontal_overflow": pg.evaluate("document.documentElement.scrollWidth > window.innerWidth")}
        ctx.close()
    b.close()
out["rows"] = rows
txt = json.dumps(out, indent=1); print(txt); print("sha256", hashlib.sha256(txt.encode()).hexdigest())
