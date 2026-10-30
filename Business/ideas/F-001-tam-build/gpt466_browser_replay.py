# F-001 §165 (Claude 12Z): headless Chromium replay of the GPT Run466 offline review HTML.
# Usage: python3 gpt466_browser_replay.py /abs/path/to/review.html  (desktop + phone-sized emulation; not a real Android device)
import json,sys
from playwright.sync_api import sync_playwright
path=sys.argv[1]; out={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,ctx_args in [("desktop",{}),("phone-emulated",dict(viewport={"width":412,"height":915},device_scale_factor=2.6,is_mobile=True,has_touch=True,user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Mobile Safari/537.36"))]:
        ctx=b.new_context(accept_downloads=True,**ctx_args); pg=ctx.new_page()
        errs=[];reqs=[]
        pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
        pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
        pg.on("request",lambda r: reqs.append(r.url) if not r.url.startswith(("file:","blob:","data:")) else None)
        pg.goto("file://"+path); pg.wait_for_timeout(500)
        r={"errors":errs,"network":reqs,"cards":pg.locator("article").count()}
        r["approved_option"]=pg.locator('option[value="APPROVED"]').count()
        r["scroll_overflow"]=pg.evaluate("document.documentElement.scrollWidth>window.innerWidth")
        if r["cards"]:
            q=pg.locator("article h2").first.inner_text()
            pg.fill("#query",q); r["visible_after_search"]=pg.locator("article:not([hidden])").count()
            pg.fill("#query","")
            pg.locator("article select").first.select_option("DRAFT_REVISE")
            pg.locator("article textarea").first.fill("<b>test</b>")
            with pg.expect_download() as d: pg.click("#export")
            j=json.load(open(d.value.path()))
            r["export"]={k:j[k] for k in ["format","authority","timothy_approval_authenticated","publication_authorized","editorial_overlay_applied"]}
            r["export_items"]=len(j["items"]); r["first_item"]=j["items"][0]
            r["statuses"]=sorted(set(i["draft_status"] for i in j["items"]))
        out[name]=r; ctx.close()
    b.close()
print(json.dumps(out,indent=1))
