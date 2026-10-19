"""F-001 §68 (PROPOSED, scratch-tested, not wired into build_pdf.py): rewrite the
wkhtmltopdf file:// TOC links to in-document GoTo links (or drop them when the
heading is not found), fix the docinfo dates, save with a deterministic ID.
Usage: python3 -I PROPOSED-pdf_fix.py <tam-draft.pdf> <standalone pandoc html> <out.pdf>
Needs pikepdf (free) and pdftotext. Offline only; edits nothing in place."""
import re, subprocess, sys, html as H
import pikepdf
src, htm, dst = sys.argv[1:4]
heads = {m.group(1): re.sub(r"<[^>]+>", "", H.unescape(m.group(2))).strip()
         for m in re.finditer(r'<h[1-3][^>]*id="([^"]+)"[^>]*>(.*?)</h[1-3]>', open(htm, encoding="utf-8").read(), re.S)}
pdf = pikepdf.open(src)
n = len(pdf.pages)
texts = [subprocess.run(["pdftotext", "-f", str(i+1), "-l", str(i+1), "-layout", src, "-"], capture_output=True, text=True).stdout for i in range(n)]
fixed = left = 0
for pi, page in enumerate(pdf.pages):
    for a in page.obj.get("/Annots", []):
        act = a.get("/A")
        if act is None or act.get("/S") != "/URI": continue
        uri = str(act.get("/URI"))
        if not uri.startswith("file://"): continue
        frag = uri.split("#", 1)[1] if "#" in uri else None
        title = heads.get(frag)
        # target: first page after the TOC page whose text contains the heading
        tgt = next((j for j in range(pi+1, n) if title and title in texts[j]), None)
        if tgt is None:
            del a["/A"]; left += 1; continue   # drop the leaking link, keep the text
        a["/A"] = pikepdf.Dictionary(S=pikepdf.Name.GoTo, D=pikepdf.Array([pdf.pages[tgt].obj, pikepdf.Name.Fit]))
        fixed += 1
with pdf.open_metadata(set_pikepdf_as_editor=False) as m: pass
for k in ("/CreationDate", "/ModDate"):
    if k in pdf.docinfo: pdf.docinfo[k] = "D:20000101000000Z"
pdf.save(dst, deterministic_id=True, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
print({"pages": n, "goto": fixed, "dropped": left})
