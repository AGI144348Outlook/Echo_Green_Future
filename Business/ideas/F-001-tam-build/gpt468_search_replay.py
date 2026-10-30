# F-001 §167 (Claude 14Z): console + search smoke check of ChatGPT Run468 page. Usage: python3 -I search468.py /abs/page.html
import json,sys
from playwright.sync_api import sync_playwright
out={}
with sync_playwright() as p:
  b=p.chromium.launch()
  for name,ca in [("desktop",{}),("phone-emulated",dict(viewport={"width":412,"height":915},device_scale_factor=2.6,is_mobile=True,has_touch=True))]:
    ctx=b.new_context(**ca);pg=ctx.new_page();con=[]
    pg.on("console",lambda m: con.append([m.type,m.text]) if m.type in ("error","warning") else None)
    pg.goto("file://"+sys.argv[1]);pg.wait_for_timeout(400)
    vis=lambda: pg.evaluate("[...document.querySelectorAll('article')].filter(a=>a.offsetParent!==null).length")
    inp=pg.locator("input[type=search], input#search, input[type=text]").first
    first_id=pg.evaluate("(()=>{const a=document.querySelector('article');return a.dataset.id||a.id||a.querySelector('h2,h3,strong').textContent})()")
    r={"console_error_or_warning":con,"visible_before":vis(),"search_box":inp.count()}
    if inp.count():
      inp.fill("zzzz-no-such-text-zzzz");pg.wait_for_timeout(150);r["visible_nonsense"]=vis()
      inp.fill(str(first_id)[:12]);pg.wait_for_timeout(150);r["visible_first_id_query"]=vis();r["query"]=str(first_id)[:12]
      inp.fill("");pg.wait_for_timeout(150);r["visible_cleared"]=vis()
    r["h_overflow_px"]=pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
    out[name]=r;ctx.close()
  b.close()
print(json.dumps(out,indent=1))
