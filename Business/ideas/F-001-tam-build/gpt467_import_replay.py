# F-001 §166 (Claude 13Z): headless Chromium replay of GPT Run467 review page incl. DRAFT import.
# Usage: python3 -I replay467.py /abs/page.html /abs/workdir   (desktop + phone-sized emulation; not a real Android device)
import json,sys,copy,os
from playwright.sync_api import sync_playwright
path,wd=sys.argv[1],sys.argv[2];out={}
def snap(pg): return pg.evaluate("[...document.querySelectorAll('article')].map(a=>[a.querySelector('select').value,a.querySelector('textarea').value])")
with sync_playwright() as p:
  b=p.chromium.launch()
  for name,ca in [("desktop",{}),("phone-emulated",dict(viewport={"width":412,"height":915},device_scale_factor=2.6,is_mobile=True,has_touch=True))]:
    ctx=b.new_context(accept_downloads=True,**ca);pg=ctx.new_page();errs=[];net=[]
    pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.on("request",lambda r: net.append(r.url) if not r.url.startswith(("file:","blob:","data:")) else None)
    pg.goto("file://"+path);pg.wait_for_timeout(400)
    r={"errors":errs,"cards":pg.locator("article").count(),"hold_text":"HOLD" in pg.inner_text("body"),"approved_option":pg.locator('option[value="APPROVED"]').count()}
    if r["cards"]:
      opts=pg.locator("article select").first.evaluate("s=>[...s.options].map(o=>o.value)")
      st=[o for o in opts if o][0]
      pg.locator("article select").first.select_option(st);pg.locator("article textarea").first.fill("<img src=x onerror=alert(1)> note")
      with pg.expect_download() as d: pg.click("#export")
      exp=json.load(open(d.value.path()));fp=os.path.join(wd,name+"-export.json");json.dump(exp,open(fp,"w"),indent=2)
      before=snap(pg);pg.reload();pg.wait_for_timeout(300);blank=snap(pg)
      pg.set_input_files("#restore",fp);pg.wait_for_timeout(300)
      r["roundtrip_restored"]=snap(pg)==before and blank!=before;r["msg_valid"]=pg.inner_text("#message")
      r["img_injected"]=pg.locator("article img").count()
      base=snap(pg);neg={}
      def forge(k,f):
        j=copy.deepcopy(exp);f(j);fp2=os.path.join(wd,f"{name}-{k}.json");open(fp2,"w").write(j if isinstance(j,str) else json.dumps(j))
        pg.set_input_files("#restore",fp2);pg.wait_for_timeout(200)
        neg[k]={"unchanged":snap(pg)==base,"msg":pg.inner_text("#message")[:120]}
      forge("approval_true",lambda j:j.__setitem__("timothy_approval_authenticated",True))
      forge("publication_true",lambda j:j.__setitem__("publication_authorized",True))
      forge("unknown_id",lambda j:j["items"][5].__setitem__("occurrence_id","X#nope"))
      forge("duplicate_id",lambda j:j["items"][6].__setitem__("occurrence_id",j["items"][7]["occurrence_id"]))
      forge("wrong_pin",lambda j:j["source_pins"].__setitem__(list(j["source_pins"])[0],"0"*40))
      forge("status_APPROVED",lambda j:j["items"][3].__setitem__("draft_status","APPROVED"))
      forge("note_1001",lambda j:j["items"][2].__setitem__("draft_note","a"*1001))
      forge("swapped_order",lambda j:j["items"].__setitem__(slice(0,2),[j["items"][1],j["items"][0]]))
      big=os.path.join(wd,name+"-big.json");open(big,"w").write(" "*262145+json.dumps(exp))
      pg.set_input_files("#restore",big);pg.wait_for_timeout(200);neg["file_256KiB_plus"]={"unchanged":snap(pg)==base,"msg":pg.inner_text("#message")[:120]}
      r["negatives"]=neg;r["after_errors"]=list(errs)
    r["network"]=net;out[name]=r;ctx.close()
  b.close()
print(json.dumps(out,indent=1))
