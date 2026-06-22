#!/usr/bin/env python3
"""
Bake all flykea.com images into the project so the site is fully self-contained.
Run once, from inside the flykea-site folder:   python3 bake-images.py
Needs only Python 3 (standard library). Safe to re-run.
"""
import os, re, urllib.request, ssl
ROOT = os.path.dirname(os.path.abspath(__file__))
PREFIX = "https://flykea.com/wp-content/uploads/"
LOCAL  = "/assets/img/"
EXT = (".jpg",".jpeg",".png",".gif",".svg",".webp",".mp4",".pdf")
ctx = ssl.create_default_context()
ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE  # tolerate odd host certs

# 1) collect every flykea uploads URL used anywhere in the project
urls=set()
for dp,_,fs in os.walk(ROOT):
    if os.sep+"assets"+os.sep+"img" in dp: continue
    for f in fs:
        if f.endswith((".html",".py",".css")):
            txt=open(os.path.join(dp,f),encoding="utf-8",errors="ignore").read()
            for m in re.findall(r'https://flykea\.com/wp-content/uploads/[^\s"\')]+', txt):
                if m.lower().endswith(EXT): urls.add(m)
print("Found %d media files to download."%len(urls))

# 2) download each, mirroring the path under assets/img/
ok=fail=skip=0
for u in sorted(urls):
    rel=u[len(PREFIX):]
    dest=os.path.join(ROOT,"assets","img",rel)
    os.makedirs(os.path.dirname(dest),exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest)>200:
        skip+=1; continue
    try:
        req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
        data=urllib.request.urlopen(req,timeout=40,context=ctx).read()
        if len(data)<=200 and b"allowlist" in data: raise RuntimeError("blocked")
        open(dest,"wb").write(data); ok+=1; print("  ok  ",rel)
    except Exception as e:
        fail+=1; print("  FAIL",rel,"->",e)
print("Downloaded %d, skipped %d, failed %d."%(ok,skip,fail))

# 3) rewrite every reference from the live URL to the local path
if ok+skip>0:
    n=0
    for dp,_,fs in os.walk(ROOT):
        for f in fs:
            if f.endswith((".html",)):
                p=os.path.join(dp,f); t=open(p,encoding="utf-8").read()
                if PREFIX in t:
                    open(p,"w",encoding="utf-8").write(t.replace(PREFIX,LOCAL)); n+=1
    # keep the generator in sync for future rebuilds
    bp=os.path.join(ROOT,"build.py")
    if os.path.exists(bp):
        t=open(bp,encoding="utf-8").read().replace('U   = "%s"'%PREFIX,'U   = "%s"'%LOCAL)
        open(bp,"w",encoding="utf-8").write(t)
    print("Rewrote image paths in %d HTML files. Site is now self-contained."%n)
print("Done. Deploy the folder as usual.")
