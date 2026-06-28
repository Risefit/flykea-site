#!/usr/bin/env python3
"""
Generate WebP + responsive derivatives for every JPEG referenced by the built site.
Run after adding new photos:   python3 optimise-images.py
Needs Pillow:                  pip install Pillow
Keeps originals untouched. Safe to re-run (skips up-to-date derivatives).

For each  assets/img/<path>/name.jpg  it writes, alongside the original:
  name.webp        full-size WebP, capped at 1600px wide  (primary, via <picture>)
  name-640.webp    640px WebP                              (small-viewport srcset)
  name-1600.jpg    capped JPEG fallback (only if original > 1700px wide)
build.py's pic() helper picks these up automatically if present.
"""
import os, re, glob
try:
    from PIL import Image, ImageOps
except ImportError:
    raise SystemExit("Pillow is required:  pip install Pillow")

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(ROOT, "assets", "img")
MAXW, SMALLW = 1600, 640

# collect every jpg referenced in the generated HTML (originals + derivative basenames)
refs = set()
for html in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    t = open(html, encoding="utf-8", errors="ignore").read()
    for m in re.findall(r'/assets/img/([^\s"\')]+?)(?:-640)?(?:-1600)?\.(?:jpe?g|webp)', t):
        if os.path.exists(os.path.join(IMG, m + ".jpg")):   refs.add(m + ".jpg")
        elif os.path.exists(os.path.join(IMG, m + ".jpeg")): refs.add(m + ".jpeg")

made = skipped = 0
for rel in sorted(refs):
    src = os.path.join(IMG, rel)
    base = os.path.splitext(src)[0]
    webp, small, fb = base + ".webp", base + "-640.webp", base + "-1600.jpg"
    if os.path.exists(webp) and os.path.exists(small):
        skipped += 1; continue
    try:
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    except Exception as e:
        print("  skip", rel, e); continue
    w, h = im.size
    full = im.resize((MAXW, round(h * MAXW / w)), Image.LANCZOS) if w > MAXW else im
    full.save(webp, "WEBP", quality=82, method=6)
    sw = min(SMALLW, w)
    im.resize((sw, round(h * sw / w)), Image.LANCZOS).save(small, "WEBP", quality=80, method=6)
    if w > 1700:
        full.save(fb, "JPEG", quality=82, optimize=True, progressive=True)
    made += 1; print("  +", rel)

print(f"Done. Generated derivatives for {made} image(s), {skipped} already up to date.")
