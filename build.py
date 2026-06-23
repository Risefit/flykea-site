#!/usr/bin/env python3
# KEA static site generator. Edit content below, then: python3 build.py
import os, html, re
import content as C
ROOT = os.path.dirname(os.path.abspath(__file__))
# Production base URL — change to "https://flykea.com" once the custom domain is live on Vercel.
BASE_URL   = "https://flykea-site-z8af.vercel.app"
PAGES      = []                                   # collected for sitemap.xml
CSS = open(os.path.join(ROOT,'assets','styles.css')).read()
JS  = open(os.path.join(ROOT,'assets','main.js')).read()

U   = "/assets/img/"          # live media base (swap to /assets/img/ once downloaded)
LOGO_GREEN = U+"2018/07/KEA-Logo.png"
LOGO_WHITE = U+"2022/01/KEA-LOGO-White-Screen-01.png"
FAVICON    = U+"2019/08/cropped-KEA-Favicon-270x270.png"
VIDEO      = U+"2019/02/KEA-BANNER-VIDEO6.mp4"
FORM_EMAIL = "reservations@flykea.com"          # where form submissions are emailed
FORM_ACTION= "https://formsubmit.co/"+FORM_EMAIL # no API key needed (one-time activation on first submit)
PHONE="+256 776 333 114"; PHONE2="+256 772 712 554"; EMAIL="reservations@flykea.com"
PAY="https://www.paybills.ug/index.php/Kampala-Executive-Aviation-Limited"
OG_DEFAULT = U+"2020/03/Helicopter-Services-In-Uganda-KEA.jpg"   # default social-share image
JSONLD = ('{"@context":"https://schema.org","@graph":['
  '{"@type":"Organization","name":"Kampala Executive Aviation","alternateName":"KEA",'
  '"url":"'+BASE_URL+'/","logo":"'+BASE_URL+LOGO_GREEN+'","email":"'+EMAIL+'","telephone":"+256776333114",'
  '"address":{"@type":"PostalAddress","streetAddress":"Gate 1, Kajjansi Airstrip","addressLocality":"Kajjansi","addressCountry":"UG"},'
  '"areaServed":["Uganda","Nigeria","DR Congo","Niger","Chad","Kenya","South Sudan"],'
  '"sameAs":["https://www.facebook.com/KampalaExecutiveAviation/","https://www.linkedin.com/company/18443655/","https://twitter.com/fly_kea","https://www.instagram.com/kampalaexecutiveaviation/"]},'
  '{"@type":"WebSite","name":"Kampala Executive Aviation","url":"'+BASE_URL+'/"}]}')

def lazyify(h):
    # add loading=lazy + decoding=async to any <img> in page body that lacks it (header logo stays eager)
    parts=re.split(r'(<img\b[^>]*>)', h); out=[]
    for seg in parts:
        if seg.startswith('<img') and 'loading=' not in seg:
            seg=seg.replace('<img','<img loading="lazy" decoding="async"',1)
        out.append(seg)
    return ''.join(out)

SOL = [
 ("charter-flights","Charter Flights"),
 ("helicopter-and-fixed-wing","Helicopter and Fixed Wing"),
 ("medical-division","Medical Division"),
 ("aerial-and-geophysical-survey","Aerial and Geophysical Survey"),
 ("oil-gas-and-mining","Oil, Gas and Mining"),
 ("maintenance-and-hangarage","Maintenance and Hangarage"),
]

def nav(active=""):
    def cls(k): return ' class="active"' if k==active else ''
    sub=('<div class="submenu submenu-wide">'
      '<div class="grp">Charter</div>'
      '<a href="/charter-flights-kampala/">Charter Flights Kampala</a>'
      '<a href="/helicopter-charter-kampala/">Helicopter Charter Kampala</a>'
      '<a href="/services/vip-corporate-charter/">VIP &amp; Corporate Charter</a>'
      '<a href="/services/private-jet-charter/">Private Jet Charter</a>'
      '<a href="/services/cargo-charter/">Cargo Charter</a>'
      '<div class="grp">Industrial &amp; B2B</div>'
      '<a href="/services/oil-gas-aviation/">Oil &amp; Gas Aviation</a>'
      '<a href="/services/ngo-humanitarian-charter/">NGO &amp; Humanitarian</a>'
      '<a href="/services/remote-site-operations/">Remote Site Operations</a>'
      '<a href="/services/pipeline-patrol/">Pipeline Patrol</a>'
      '<div class="grp">Emergency &amp; Specialist</div>'
      '<a href="/services/medical-evacuation/">Medical Evacuation</a>'
      '<a href="/services/search-rescue-helicopter/">Search &amp; Rescue</a>'
      '<a href="/services/disaster-response/">Disaster Response</a>'
      '<a href="/services/aerial-survey-geophysical/">Aerial Survey</a>'
      '<a href="/services/external-load-helicopter/">External Load</a>'
      '<div class="grp">MRO</div>'
      '<a href="/services/aircraft-maintenance-mro/">Aircraft Maintenance &amp; MRO</a>'
      '<a class="all" href="/services/">All services →</a>'
      '</div>')
    return f'''<header id="hdr"><div class="wrap nav">
<a href="/index.html" class="nav-logo"><img src="{LOGO_GREEN}" alt="KEA — Kampala Executive Aviation"></a>
<nav aria-label="Primary"><ul class="nav-links">
<li class="has-sub"><a href="/services/"{cls('services')}>Services ▾</a>{sub}</li>
<li><a href="/services/aircraft-leasing/"{cls('leasing')}>Leasing</a></li>
<li><a href="/services/uav-drone-operations/"{cls('uav')}>UAV</a></li>
<li><a href="/fleet.html"{cls('fleet')}>Fleet</a></li>
<li><a href="/about.html"{cls('about')}>About</a></li>
<li><a href="/blog/"{cls('blog')}>Blog</a></li>
<li><a href="/contact.html"{cls('contact')}>Contact</a></li>
</ul></nav>
<a class="btn btn-outline nav-quote" href="/quote/">Get a Quote</a>
<button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mobilemenu"><span></span><span></span><span></span></button>
</div>
<div class="mobile-menu" id="mobilemenu">
<a href="/services/">Services</a><a href="/services/aircraft-leasing/">Aircraft Leasing</a><a href="/services/uav-drone-operations/">UAV Operations</a><a href="/fleet.html">Fleet</a><a href="/about.html">About</a><a href="/blog/">Blog</a><a href="/contact.html">Contact</a><a href="/quote/">Get a Quote</a>
</div></header>'''

FOOT=f'''<footer><div class="wrap">
<div class="foot-top">
<div class="foot-col">
<div class="foot-logo"><img src="{LOGO_WHITE}" alt="KEA"></div>
<p>Gate 1, Kajjansi Airstrip, Uganda<br>Tel: {PHONE} / {PHONE2}<br>E-mail: {EMAIL}</p>
<div class="socials">
<a href="https://www.facebook.com/KampalaExecutiveAviation/" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M22 12a10 10 0 1 0-11.5 9.9v-7H7.9V12h2.6V9.8c0-2.6 1.5-4 3.9-4 1.1 0 2.3.2 2.3.2v2.5h-1.3c-1.3 0-1.7.8-1.7 1.6V12h2.9l-.5 2.9h-2.4v7A10 10 0 0 0 22 12z"/></svg></a>
<a href="https://www.linkedin.com/company/18443655/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14zM8.3 18.3V10H5.7v8.3h2.6zM7 8.8a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm11.3 9.5v-4.5c0-2.4-1.3-3.5-3-3.5a2.6 2.6 0 0 0-2.3 1.3V10h-2.6v8.3h2.6v-4.4c0-1.2.2-2.3 1.7-2.3s1.5 1.3 1.5 2.4v4.3h2.4z"/></svg></a>
<a href="https://twitter.com/fly_kea" target="_blank" rel="noopener" aria-label="Twitter"><svg viewBox="0 0 24 24"><path d="M18.9 2H22l-7.1 8.1L23.3 22h-6.6l-5.2-6.8L5.6 22H2.4l7.6-8.7L1 2h6.8l4.7 6.2L18.9 2zm-1.2 18h1.8L7.4 3.8H5.5L17.7 20z"/></svg></a>
<a href="https://www.instagram.com/kampalaexecutiveaviation/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.3 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.3 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.3-2.2-.4a3.8 3.8 0 0 1-1.4-.9 3.8 3.8 0 0 1-.9-1.4c-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.3-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4 1.3-.1 1.7-.1 4.9-.1zm0 1.8c-3.1 0-3.5 0-4.7.1-1.1.1-1.7.2-2.1.4-.5.2-.9.4-1.3.8-.4.4-.6.8-.8 1.3-.2.4-.3 1-.4 2.1-.1 1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c.1 1.1.2 1.7.4 2.1.2.5.4.9.8 1.3.4.4.8.6 1.3.8.4.2 1 .3 2.1.4 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1.1-.1 1.7-.2 2.1-.4.5-.2.9-.4 1.3-.8.4-.4.6-.8.8-1.3.2-.4.3-1 .4-2.1.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c-.1-1.1-.2-1.7-.4-2.1a3.5 3.5 0 0 0-.8-1.3 3.5 3.5 0 0 0-1.3-.8c-.4-.2-1-.3-2.1-.4-1.2-.1-1.6-.1-4.7-.1zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 8a3.1 3.1 0 1 0 0-6.2 3.1 3.1 0 0 0 0 6.2zm6.3-8.2a1.1 1.1 0 1 1-2.3 0 1.1 1.1 0 0 1 2.3 0z"/></svg></a>
</div></div>
<div class="foot-col"><h4>Services</h4><a href="/services/oil-gas-aviation/">Oil &amp; Gas Aviation</a><a href="/services/medical-evacuation/">Medical Evacuation</a><a href="/helicopter-charter-kampala/">Helicopter Charter</a><a href="/services/ngo-humanitarian-charter/">NGO &amp; Humanitarian</a><a href="/services/cargo-charter/">Cargo Charter</a><a href="/services/uav-drone-operations/">UAV Operations</a><a href="/services/aircraft-leasing/">Aircraft Leasing</a><a href="/services/">All services →</a></div>
<div class="foot-col"><h4>Company</h4><a href="/fleet.html">Fleet</a><a href="/about.html">About</a><a href="/certifications/">Certifications</a><a href="/blog/">Blog</a><a href="/contact.html">Contact</a><a href="/news.html">News archive</a>
<div class="foot-pay"><a class="btn btn-primary" style="padding:.7rem 1.2rem" href="{PAY}" target="_blank" rel="noopener">Make a Payment →</a></div></div>
</div>
<div class="foot-bottom"><span class="mono">© 2026 KEA — Kampala Executive Aviation</span><span class="mono">Specialist Aviation Solutions · Kajjansi, Uganda</span></div>
</div></footer>'''

def page(path, title, desc, body, active="", og_image=None, noindex=False, extra_jsonld=""):
    url_path = path[:-10] if path.endswith("index.html") else path   # clean dir URLs
    canon = BASE_URL + "/" + url_path
    ogimg = BASE_URL + (og_image or OG_DEFAULT)
    desc_e, title_e = html.escape(desc), html.escape(title)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow">'
    if not noindex: PAGES.append(url_path)
    extra_ld = ('<script type="application/ld+json">%s</script>'%extra_jsonld) if extra_jsonld else ''
    doc=f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc_e}">
<link rel="canonical" href="{canon}">{robots}
<meta property="og:type" content="website"><meta property="og:site_name" content="Kampala Executive Aviation">
<meta property="og:title" content="{title_e}"><meta property="og:description" content="{desc_e}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{ogimg}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title_e}"><meta name="twitter:description" content="{desc_e}"><meta name="twitter:image" content="{ogimg}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{JSONLD}</script>{extra_ld}
<!-- GA4: replace G-XXXXXXX with KEA's Measurement ID -->
<!-- <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-XXXXXXX');</script> -->
<!-- Search Console: paste KEA's verification token -->
<!-- <meta name="google-site-verification" content="REPLACE_WITH_TOKEN"> -->
<style>{CSS}</style></head><body>
<a class="skip" href="#main">Skip to content</a>
{nav(active)}
<main id="main" tabindex="-1">
{lazyify(body)}
</main>
{FOOT}
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer" hidden>
<button class="lb-close" aria-label="Close viewer">\u2715</button>
<button class="lb-prev" aria-label="Previous image">\u2039</button>
<img class="lb-img" alt="">
<button class="lb-next" aria-label="Next image">\u203a</button>
<div class="lb-cap" aria-live="polite"></div>
</div>
<a class="sticky-quote" href="/quote/">⚡ Get a Quote</a>
<a class="wa-float" href="https://wa.me/256776333114" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 .4C7.4.4.5 7.3.5 15.9c0 2.8.7 5.4 2 7.8L.4 31.6l8.1-2.1c2.3 1.2 4.8 1.9 7.5 1.9 8.6 0 15.5-6.9 15.5-15.5S24.6.4 16 .4zm0 28.3c-2.4 0-4.6-.6-6.5-1.8l-.5-.3-4.8 1.3 1.3-4.7-.3-.5c-1.3-2-2-4.4-2-6.9C3 8.9 8.8 3.1 16 3.1S29 8.9 29 16 23.2 28.7 16 28.7zm8.2-9.6c-.4-.2-2.6-1.3-3-1.4-.4-.2-.7-.2-1 .2s-1.1 1.4-1.4 1.7c-.3.3-.5.3-.9.1-2.4-1.2-4-2.1-5.6-4.8-.4-.7.4-.7 1.2-2.2.1-.3.1-.5 0-.7s-1-2.4-1.4-3.3c-.4-.9-.7-.7-1-.8h-.8c-.3 0-.7.1-1.1.5C7.5 9.3 6.7 10.4 6.7 12s1.2 3.5 1.4 3.8c.2.3 2.4 3.7 5.9 5.2 2.2.9 3 1 4.1.9.7-.1 2.6-1 2.9-2 .4-1 .4-1.8.3-2-.1-.2-.4-.3-.8-.5z"/></svg></a>
<script>{JS}</script></body></html>'''
    full=os.path.join(ROOT,path)
    os.makedirs(os.path.dirname(full) or ".",exist_ok=True)
    open(full,'w').write(doc)
    print("wrote",path)

def page_hero(eyebrow,title,sub,bg):
    return f'''<section class="page-hero"><div class="bg" style="background-image:url('{bg}')"></div>
<div class="inner reveal"><span class="eyebrow on-dark">{eyebrow}</span><h1>{title}</h1><p class="sub">{sub}</p></div></section>'''

def feats(items):
    c="".join(f'<div class="feat reveal"><img class="ic" src="{ic}" alt=""><h3>{t}</h3><p>{p}</p></div>' for ic,t,p in items)
    return f'<div class="feat-grid">{c}</div>'

def cta_band():
    return f'''<div class="cta-band"><div class="wrap reveal"><span class="eyebrow" style="justify-content:center">Have questions?</span>
<h2>Our aviation experts are ready</h2><p>Tell us about your requirement and we’ll help find the solution best suited to your need.</p>
<a class="btn btn-primary" href="/contact.html">Contact us <span class="arr">→</span></a></div></div>'''

def banner(eyebrow,title,text,bg,btn=("Explore our services","/services/")):
    return f'''<div class="banner"><div class="bg" style="background-image:url('{bg}')"></div>
<div class="banner-inner reveal"><span class="eyebrow on-dark">{eyebrow}</span><h2>{title}</h2><p>{text}</p>
<a class="btn btn-primary" href="{btn[1]}">{btn[0]} <span class="arr">→</span></a></div></div>'''

IC=U+"2019/04/"; IC1=U+"2019/01/"; IC2=U+"2019/02/"

# ================= SEO SCHEMA HELPERS =================
import json as _json
def _ld(obj): return _json.dumps(obj, separators=(",",":"), ensure_ascii=False)
def crumb_ld(trail):  # trail = [(name,url_path), ...] ; url_path "" for home
    items=[{"@type":"ListItem","position":i+1,"name":n,
            "item":BASE_URL+"/"+u} for i,(n,u) in enumerate(trail)]
    return _ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
def service_ld(name,desc,stype,url):
    return _ld({"@context":"https://schema.org","@type":"Service","name":name,"description":desc,
      "serviceType":stype,"url":BASE_URL+"/"+url,"areaServed":[c[1] for c in C.COUNTRIES],
      "provider":{"@type":"Organization","name":"Kampala Executive Aviation","telephone":"+256776333114",
        "address":{"@type":"PostalAddress","streetAddress":"Gate 1, Kajjansi Airstrip","addressLocality":"Kajjansi","addressCountry":"UG"}}})
def faq_ld(faqs):
    return _ld({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})
def article_ld(title,desc,url,img,date):
    return _ld({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,
      "image":BASE_URL+U+img,"datePublished":date,"url":BASE_URL+"/"+url,
      "author":{"@type":"Organization","name":"Kampala Executive Aviation"},
      "publisher":{"@type":"Organization","name":"Kampala Executive Aviation","logo":{"@type":"ImageObject","url":BASE_URL+LOGO_GREEN}}})
LOCALBIZ_LD=_ld({"@context":"https://schema.org","@type":"LocalBusiness","name":"Kampala Executive Aviation",
  "image":BASE_URL+OG_DEFAULT,"url":BASE_URL+"/","telephone":"+256776333114","priceRange":"$$$",
  "address":{"@type":"PostalAddress","streetAddress":"Gate 1, Kajjansi Airstrip","addressLocality":"Kajjansi","addressRegion":"Wakiso","addressCountry":"UG"},
  "geo":{"@type":"GeoCoordinates","latitude":-0.1953,"longitude":32.5536},
  "openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"},
  "areaServed":[c[1] for c in C.COUNTRIES]})

def crumbs_html(trail):
    parts=[]
    for i,(n,u) in enumerate(trail):
        if i<len(trail)-1: parts.append(f'<a href="/{u}">{n}</a>')
        else: parts.append(f'<span>{n}</span>')
    return '<div class="crumb"><div class="wrap">'+' / '.join(parts)+'</div></div>'

def crumbs_inline(trail):
    parts=[]
    for i,(n,u) in enumerate(trail):
        if i<len(trail)-1: parts.append(f'<a href="/{u}">{n}</a>')
        else: parts.append(f'<span>{n}</span>')
    return '<div class="crumb-in">'+' / '.join(parts)+'</div>'

# ================= SHARED CONVERSION / TRUST COMPONENTS =================
def quote_form(source="Website"):
    return f'''<section class="quote" id="quote-form"><div class="wrap"><div class="quote-grid">
<div class="reveal"><span class="eyebrow">Request a quote</span><h2 style="font-size:clamp(1.8rem,3.6vw,2.6rem);margin:1rem 0">Get a charter quote</h2>
<p style="color:var(--slate);max-width:44ch">Tell us the route, dates and load — we’ll come back with options. For urgent requests call <a href="tel:+256776333114" style="color:var(--green-ink)">{PHONE}</a>.</p>
<p style="color:var(--slate);font-family:var(--mono);font-size:.82rem;margin-top:1.6rem">Gate 1, Kajjansi Airstrip, Uganda<br>{PHONE} · {PHONE2}<br>{EMAIL}</p></div>
<form class="form" data-formsubmit action="{FORM_ACTION}" method="POST">
<input type="hidden" name="_subject" value="Quote request — flykea.com ({source})">
<input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="/quote-received.html"><input type="hidden" name="source" value="{source}">
<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Company</label><input name="company"></div></div>
<div class="row"><div><label>From</label><input name="route_from" placeholder="Origin"></div><div><label>To</label><input name="route_to" placeholder="Destination"></div></div>
<div class="row"><div><label>Date</label><input name="date" placeholder="dd/mm/yyyy"></div><div><label>Passengers</label><input name="pax" placeholder="PAX count"></div></div>
<div class="row"><div><label>Aircraft preference</label><select name="aircraft"><option>No preference</option><option>Helicopter</option><option>Fixed wing</option><option>Private jet</option><option>Cargo</option></select></div><div><label>Phone</label><input name="phone" type="tel" placeholder="+256…" required></div></div>
<div><label>Message</label><textarea name="message" rows="3"></textarea></div>
<div class="form-status" role="status" aria-live="polite" hidden></div>
<div><button class="btn btn-primary" type="submit">Send request <span class="arr">→</span></button></div>
</form></div></div></section>'''

CHARTER_SLUGS={"charter-flights-kampala","helicopter-charter-kampala","services/cargo-charter",
 "services/vip-corporate-charter","services/private-jet-charter",
 "services/charter-flights-drc","services/charter-flights-south-sudan"}

def quote_map(variant="full", source="Website"):
    if variant=="compact":
        return f'''<section class="qmap-sec compact"><div class="wrap"><div class="qmap compact-tool" data-variant="compact" data-source="{source}">
<div class="qc-row">
<div class="qfld"><label>From</label><input class="q-from" list="qports" placeholder="Origin" value="Kajjansi (Kampala)" autocomplete="off"></div>
<div class="qfld"><label>To</label><input class="q-to" list="qports" placeholder="Destination" autocomplete="off"></div>
<div class="qfld"><label>Pax</label><input class="q-pax" type="number" min="1" max="19" value="4"></div>
<button class="q-go">Estimate</button></div>
<div class="qmap-result qc-result"><span class="qc-line"><b class="q-time">—</b> · <span class="q-ac">—</span> · <span class="q-dist">—</span></span>
<a class="qbtn qbtn-q q-see" href="/quote/">See route &amp; options →</a>
<a class="qbtn qbtn-wa q-wa" target="_blank" rel="noopener">WhatsApp</a></div>
<datalist id="qports"></datalist></div></div></section>
<script src="/assets/quote-map.js" defer></script>'''
    return f'''<section class="qmap-sec"><div class="wrap"><div class="qmap" data-variant="full" data-source="{source}">
<div class="qmap-panel"><span class="eyebrow">Plan your charter</span><h2>Get an instant estimate</h2>
<div class="qfld"><label>From</label><input class="q-from" list="qports" placeholder="Origin airstrip / town" value="Kajjansi (Kampala)" autocomplete="off"></div>
<div class="qfld"><label>To</label><input class="q-to" list="qports" placeholder="Destination" autocomplete="off"><button class="q-swap" title="Swap" aria-label="Swap origin and destination">⇅</button></div>
<div class="qtwo"><div class="qfld"><label>Date</label><input class="q-date" type="date"></div>
<div class="qfld"><label>Passengers</label><input class="q-pax" type="number" min="1" max="19" value="4"></div></div>
<div class="qfld"><label>Mission</label><select class="q-mission"><option value="pax">Passengers</option><option value="cargo">Cargo</option><option value="medevac">Medical evacuation</option><option value="site">Remote site access (helicopter)</option></select></div>
<button class="q-go">Calculate &amp; show route</button>
<datalist id="qports"></datalist></div>
<div class="qmap-mapwrap"><svg class="qmap-map" viewBox="0 0 1000 625" preserveAspectRatio="xMidYMid slice" aria-label="Charter route map"></svg>
<div class="qmap-result"><div class="qr-top">
<div class="qmetric"><div class="qv q-dist">—</div><div class="qk">Distance</div></div>
<div class="qmetric"><div class="qv q-time">—</div><div class="qk">Est. flight time</div></div>
<div class="qreco"><div class="qk2">Recommended aircraft</div><div class="qac q-ac">—</div><div class="qalt q-alt"></div></div>
<div class="qprice-wrap" style="text-align:right"><div class="qprice">Indicative <span class="q-price">—</span></div><div class="qdisc">estimate · KEA confirms exact quote</div></div>
</div><div class="qr-cta"><a class="qbtn qbtn-wa q-wa" target="_blank" rel="noopener">Send on WhatsApp</a><a class="qbtn qbtn-q q-rq" href="#quote-form">Request exact quote →</a></div></div></div>
</div></div></section>
<script src="/assets/quote-map.js" defer></script>'''

def clients_strip():
    lg="".join(f'<span class="lg">{html.escape(n)}</span>' for n in C.CLIENTS)
    return f'''<div class="trust"><div class="wrap"><!-- TRUST: client wordmarks confirmed by KEA; supply official logo files for production -->
<div class="lbl">Trusted by operators &amp; agencies across the region</div><div class="logos">{lg}</div></div></div>'''

def countries_section():
    chips="".join(f'<span class="cc"><span class="fl">{f}</span>{html.escape(n)}</span>' for f,n in C.COUNTRIES)
    chips+='<span class="cc todo"><!-- COUNTRIES: confirm 13th -->+ 1 to confirm</span>'
    return f'''<section class="countries"><div class="wrap"><span class="eyebrow">Reach</span>
<h2 style="font-size:clamp(1.9rem,4vw,2.8rem);margin-top:1rem">Countries we serve</h2>
<div class="country-chips">{chips}</div></div></section>'''

def certs_section(dark=True):
    bd="".join(f'<div class="cert-badge"><span class="shield">✚</span><div><div class="mono">{t}</div><h4>{ti}</h4><p>{tx}</p></div></div>' for t,ti,tx in C.CERTS)
    return f'''<section class="cert"><div class="wrap"><span class="eyebrow on-dark">Licensed &amp; approved</span>
<h2 style="color:#fff;font-size:clamp(1.9rem,4vw,2.8rem);margin-top:1rem">Certifications &amp; approvals</h2>
<div class="badges">{bd}</div></div></section>'''

# ================= SERVICE PAGE RENDERER =================
def render_service(s):
    url=s["slug"]+"/"
    trail=[("Home","")]
    if s["slug"].startswith("services/"): trail.append(("Services","services/"))
    trail.append((s["h1"], url))
    secs="".join(f'<h2>{h}</h2>{b}' for h,b in s["secs"])
    faqhtml="".join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(s["faqs"]))
    rel="".join(f'<a class="rel-card" href="/{u}{"" if u.endswith(".html") else "/"}">{l} <span class="arr">→</span></a>' for l,u in s["related"])
    gallery=""
    if s.get("gallery"):
        slides=[(g, s["h1"]) for g in s["gallery"]]
        gallery=carousel_section(slides, s["h1"]+" gallery", s["eyebrow"], "In the field")
    tool = quote_map("full", s["h1"]) if s["slug"] in CHARTER_SLUGS else ""
    body=f'''<section class="svc-hero"><div class="bg" style="background-image:url('{U}{s["hero"]}')"></div>
<div class="inner reveal">{crumbs_inline(trail)}<span class="eyebrow on-dark">{s["eyebrow"]}</span><h1>{s["h1"]}</h1></div></section>
<section style="padding-top:64px"><div class="wrap"><div class="prose reveal"><p>{s["lead"]}</p>{secs}
<div style="margin:2rem 0"><a class="btn btn-primary" href="#quote-form">Get a quote <span class="arr">→</span></a>
<a class="btn btn-outline" href="tel:+256776333114" style="margin-left:.6rem">Call {PHONE}</a></div></div></div></section>
{gallery}
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Questions</span><h2>Frequently asked questions</h2></div>
<div class="faq reveal" style="margin-top:1.5rem">{faqhtml}</div>
<div class="rel-row reveal" style="margin-top:3rem"><h3 style="font-size:1.1rem;margin-bottom:1rem">Related services</h3><div class="rel-grid">{rel}</div></div></div></section>
{tool}
{quote_form(s["h1"])}
<div class="call-band"><div class="wrap"><h2>Talk to operations</h2><p>{PHONE} · {PHONE2} · <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>'''
    schema=service_ld(s["h1"],s["desc"],s["stype"],url)+"\n"+faq_ld(s["faqs"])+"\n"+crumb_ld(trail)
    active = "leasing" if "leasing" in s["slug"] else ("uav" if "uav" in s["slug"] else "services")
    page(url+"index.html", s["title"], s["desc"], body, active=active, og_image=U+s["og"], extra_jsonld=schema)

# ================= BLOG RENDERER =================
def render_blog_index(items):
    cards=""
    for n in items:
        cards+=f'''<a class="news-card reveal" href="/blog/{n["slug"]}/"><div class="nc-img"><img src="{U}{n["img"]}" alt="{html.escape(n["title"])}" loading="lazy"></div>
<div class="nc-body"><span class="nc-date">{n["date"]}</span><h3>{html.escape(n["title"])}</h3><p>{html.escape(n["summary"])}</p></div></a>'''
    body=f'''{page_hero("Insights &amp; updates","KEA Aviation Blog &amp; News","News, contract awards and guides from Kampala Executive Aviation.",U+"2020/03/Helicopter-Services-In-Uganda-KEA.jpg")}
<section><div class="wrap"><div class="news-grid">{cards}</div></div></section>{quote_form("Blog")}'''
    page("blog/index.html","Aviation Blog &amp; News | KEA Aviation",
         "News, contract awards and guides from Kampala Executive Aviation — charter, humanitarian, oil & gas and UAV operations. Call +256 776 333 114.",
         body, active="blog", extra_jsonld=crumb_ld([("Home",""),("Blog","blog/")]))

def render_post(n, is_blog=True):
    url=f'blog/{n["slug"]}/'
    trail=[("Home",""),("Blog","blog/"),(n["title"],url)]
    kw=n.get("kw","")
    title=n["title"]+" | KEA Aviation"
    if len(title)>62: title=n["title"]+" | KEA"
    desc=n.get("desc") or (n["summary"][:150]+" Call +256 776 333 114.")
    bodyhtml=n.get("body","")
    body=f'''<section class="svc-hero" style="min-height:46vh"><div class="bg" style="background-image:url('{U}{n["img"]}')"></div>
<div class="inner reveal">{crumbs_inline(trail)}<span class="eyebrow on-dark">{n["date"]}</span><h1 style="max-width:26ch">{html.escape(n["title"])}</h1></div></section>
<section style="padding-top:60px"><div class="wrap"><div class="prose reveal" style="max-width:74ch;margin:0 auto">{bodyhtml}
<div style="margin-top:2.5rem"><a class="btn btn-primary" href="/quote/">Get a quote <span class="arr">→</span></a>
<a class="btn btn-outline" href="/blog/" style="margin-left:.6rem">← All posts</a></div></div></div></section>
<div class="call-band"><div class="wrap"><h2>Talk to KEA</h2><p>{PHONE} · {PHONE2} · <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>'''
    schema=article_ld(n["title"],desc,url,n["img"],n["date"])+"\n"+crumb_ld(trail)
    if n.get("faqs"): schema+="\n"+faq_ld(n["faqs"])
    page(url+"index.html", title, desc, body, active="blog", og_image=U+n["img"], extra_jsonld=schema)


print("Generating KEA site...")

# ---------------- HOME ----------------
home_body=f'''
<section class="hero" id="top"><div class="fallback"></div>
<video autoplay muted loop playsinline poster="{U}2020/03/Helicopter-Services-In-Uganda-KEA.jpg"><source src="{VIDEO}" type="video/mp4"></video>
<div class="hero-inner"><span class="eyebrow on-dark">CAA-Licensed Operator · Uganda AOC 097</span>
<h1>Aviation Services in Kampala — Kajjansi Airstrip</h1>
<p class="lead">Oil &amp; gas, NGO, medevac, cargo, VIP and UAV operations across 13 African countries — fixed wing, rotary wing and special-mission aircraft from one CAA-licensed operator at Kajjansi Airstrip, Kampala.</p>
<div class="hero-actions"><a class="btn btn-primary" href="/quote/">Get a Quote <span class="arr">→</span></a>
<a class="btn btn-ghost" href="tel:+256776333114">Call {PHONE}</a></div></div>
<div class="scroll-hint"><span>Scroll</span><span class="line"></span></div></section>

<div style="background:var(--tint);padding:34px 0 8px"><div class="wrap"><div class="sec-head reveal" style="margin-bottom:1.2rem"><span class="eyebrow">Instant estimate</span><h2 style="font-size:clamp(1.4rem,2.6vw,1.9rem);margin-top:.6rem">Where do you need to fly?</h2></div></div>{quote_map("compact","Homepage")}</div>

<section><div class="wrap lead-row">
<div class="reveal"><span class="eyebrow">The sky was the limit</span><p class="big" style="margin-top:1.2rem">For over a decade, KEA has supported industry leaders and built a reputation for high-quality, professional service.</p></div>
<div class="reveal"><p>We provide a full spectrum of aviation-centric solutions for your most challenging requirements — engineered around safety, reliability, and the realities of operating where infrastructure runs out.</p><a class="btn btn-outline" href="/about.html">Learn more <span class="arr">→</span></a></div>
</div></section>

<div class="stats"><div class="wrap"><div class="stats-grid reveal">
<div class="stat"><div class="num" data-target="4000" data-suffix="T">0<span>T</span></div><div class="lbl">Cargo Carried</div></div>
<div class="stat"><div class="num" data-target="40000">0</div><div class="lbl">Passengers Flown</div></div>
<div class="stat"><div class="num" data-target="7800">0</div><div class="lbl">Flights Conducted</div></div>
<div class="stat"><div class="num" data-target="13">0</div><div class="lbl">Countries Worked In</div></div>
</div></div></div>

<section><div class="wrap">
<div class="sol-top"><div class="sec-head reveal"><span class="eyebrow">What we do</span><h2>Specialist aviation, matched to the mission</h2></div>
<a class="btn btn-outline reveal" href="/services/">All services <span class="arr">→</span></a></div>
<div class="sol-grid">
<a class="sol-card reveal" href="/services/oil-gas-aviation/"><img src="{IC1}Oil-Gas-and-Mining.jpg" alt="KEA aircraft supporting oil and gas operations in Uganda"><div class="sol-body"><div class="sol-num">01</div><h3>Oil &amp; Gas Aviation</h3><p>Crew rotation, cargo and medevac for energy and mining operators.</p><span class="sol-more">Explore →</span></div></a>
<a class="sol-card reveal" href="/services/medical-evacuation/"><img src="{IC1}Medevac-KEA.jpg" alt="KEA air ambulance medical evacuation aircraft Uganda"><div class="sol-body"><div class="sol-num">02</div><h3>Medical Evacuation</h3><p>Fixed-wing and helicopter air ambulance, 24/7 across East Africa.</p><span class="sol-more">Explore →</span></div></a>
<a class="sol-card reveal" href="/helicopter-charter-kampala/"><img src="{U}2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg" alt="KEA helicopter charter at Kajjansi Airstrip Kampala"><div class="sol-body"><div class="sol-num">03</div><h3>Helicopter Charter</h3><p>Bell 412 &amp; 206 for charter, survey and external-load work.</p><span class="sol-more">Explore →</span></div></a>
<a class="sol-card reveal" href="/services/ngo-humanitarian-charter/"><img src="{IC}Air-ambulance-paramedics.jpg" alt="KEA NGO and humanitarian charter flight Uganda"><div class="sol-body"><div class="sol-num">04</div><h3>NGO &amp; Humanitarian</h3><p>Relief passengers and cargo into remote and cross-border sites.</p><span class="sol-more">Explore →</span></div></a>
<a class="sol-card reveal" href="/services/uav-drone-operations/"><img src="{U}2026/06/Matrice-400-RTK-KEA.jpg" alt="DJI Matrice 400 RTK drone on a KEA UAV survey operation"><div class="sol-body"><div class="sol-num">05</div><h3>UAV / Drone Operations</h3><p>Matrice 400 RTK — LiDAR, orthophoto mapping &amp; asset monitoring.</p><span class="sol-more">Explore →</span></div></a>
<a class="sol-card reveal" href="/services/cargo-charter/"><img src="{IC1}Cargo-Charter.jpg" alt="KEA cargo charter aircraft loading freight Uganda"><div class="sol-body"><div class="sol-num">06</div><h3>Cargo Charter</h3><p>Time-critical and outsized air freight across Uganda and Africa.</p><span class="sol-more">Explore →</span></div></a>
<a class="sol-card reveal" href="/services/vip-corporate-charter/"><img src="{IC2}Fleet-PC12.jpg" alt="KEA Pilatus PC-12 VIP charter aircraft Kampala"><div class="sol-body"><div class="sol-num">07</div><h3>VIP &amp; Private Jet</h3><p>Discreet executive charter for corporate and government travel.</p><span class="sol-more">Explore →</span></div></a>
<a class="sol-card reveal" href="/services/aerial-survey-geophysical/"><img src="{IC1}Aerial-Survey-KEA.jpg" alt="KEA DA42 aerial survey aircraft East Africa"><div class="sol-body"><div class="sol-num">08</div><h3>Aerial Survey</h3><p>Airborne geophysical and survey flights region-wide.</p><span class="sol-more">Explore →</span></div></a>
<a class="sol-card reveal" href="/services/aircraft-leasing/"><img src="{IC2}Fleet-B1900.jpg" alt="KEA Beechcraft 1900D available for aircraft lease and ACMI"><div class="sol-body"><div class="sol-num">09</div><h3>Aircraft Leasing</h3><p>Wet lease, dry lease and ACMI from a CAA-licensed operator.</p><span class="sol-more">Explore →</span></div></a>
</div></div></section>

{clients_strip()}

{certs_section()}

{countries_section()}

{banner("On every mission","When the runway ends, we keep going.","From a stabilised patient at 8,000 feet to a rig crew on a flooded site, our aircraft and crews are built for the places others can’t reach.",IC1+"Medevac-KEA.jpg",("Explore our services","/services/"))}

<div class="split">
<div class="panel approach"><div class="inner reveal"><span class="eyebrow">How we work</span><h2 style="margin:1rem 0">Our Approach</h2>
<p>The KEA approach employs the best of technology and innovation to deliver an ongoing commitment to service excellence. Our specialised services are built on a strong, robust team of highly skilled people with deep operational and management competence.</p>
<a class="btn btn-outline" href="/about.html">Learn more <span class="arr">→</span></a></div></div>
<div class="panel fleet-teaser"><div class="inner reveal"><span class="eyebrow">The largest privately owned fleet in Uganda</span><h2 style="margin:1rem 0">Our Fleet</h2>
<p>A versatile fixed and rotary wing capability lets us tailor a solution to each client’s unique need.</p>
<div class="chips"><span class="chip">Bell 412</span><span class="chip">Bell 206 Jet Ranger</span><span class="chip">Pilatus PC12</span><span class="chip">Beechcraft 1900D</span><span class="chip">Caravan C208B</span><span class="chip">Cessna 210</span><span class="chip">DA42 MPP Guardian</span></div>
<a class="btn btn-primary" href="/fleet.html">View all fleet <span class="arr">→</span></a></div></div></div>

<section class="services"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Full capability</span><h2>One operator, fourteen disciplines</h2></div>
<div class="services-grid reveal">
<div class="svc"><span class="idx">01</span><span class="name">Oil, Gas and Mining</span></div><div class="svc"><span class="idx">08</span><span class="name">Scheduled and Adhoc Charter</span></div>
<div class="svc"><span class="idx">02</span><span class="name">Rotary Wing Services</span></div><div class="svc"><span class="idx">09</span><span class="name">Pipeline Patrol</span></div>
<div class="svc"><span class="idx">03</span><span class="name">Fixed Wing Services</span></div><div class="svc"><span class="idx">10</span><span class="name">Disaster and Firefighting</span></div>
<div class="svc"><span class="idx">04</span><span class="name">Medical Evacuation</span></div><div class="svc"><span class="idx">11</span><span class="name">Aerial and Geophysical Survey</span></div>
<div class="svc"><span class="idx">05</span><span class="name">Search and Rescue</span></div><div class="svc"><span class="idx">12</span><span class="name">Logistics and Project Management</span></div>
<div class="svc"><span class="idx">06</span><span class="name">External and Underslung Load Work</span></div><div class="svc"><span class="idx">13</span><span class="name">Remote Camp Construction and Catering</span></div>
<div class="svc"><span class="idx">07</span><span class="name">VIP Transport · Passenger and Cargo</span></div><div class="svc"><span class="idx">14</span><span class="name">Helicopter Emergency Medical Service</span></div>
</div></div></section>

<section class="services" style="background:var(--tint)"><div class="wrap"><div class="sol-top"><div class="sec-head reveal"><span class="eyebrow">From the field</span><h2>Latest News</h2></div>
<a class="btn btn-outline reveal" href="/blog/">View all posts <span class="arr">→</span></a></div>
<div class="news-grid" id="latest-news"></div></div></section>

{banner("Have questions?","Our aviation experts are ready.","Tell us about your requirement and we’ll help find the solution best suited to your need.",U+"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg",("Get a Quote","/quote/"))}
'''

# ---------------- NEWS DATA ----------------
# slug, title, date_display, date_iso, [categories], hero_image, excerpt, [body html blocks]
NEWS=[
 ("remote-medical-clinic","Remote Site Trauma &amp; Resuscitation Center in West Africa","29 October 2021","2021-10-29",["Medical Division","News"],U+"2021/10/Remote-Medical-Clinic-KEA-1.jpg",
  "KEA completed the construction of a new remote-site medical project in West Africa, functioning as a trauma &amp; resuscitation center.",
  ["<p>Through our dedicated medical division, KEA has completed the construction of a new remote site medical project in West Africa. The facility is functioning as a trauma &amp; resuscitation center for a contracted client who required a clinic unit staffed by a minimum of two Advanced Life Support (ALS) critical care practitioners, to provide emergency medical care, primary health care and air medical evacuation care.</p>",
   "<h3>This purpose-built clinic was deployed in less than 6 weeks to a green-field site in an extremely remote location, with KEA given carte blanche over the clinic design and construction.</h3>",
   "<p>Two clinic units were constructed — one for primary health consultations and a larger open-space unit for trauma &amp; resuscitation. An emergency medical response vehicle was equipped and two Advanced Life Support critical care practitioners were placed on call for our client 24/7.</p>",
   "<p>The facility is fully plumbed with ablutions, septic tank and all construction executed to international standards. From seamless floors to easily cleanable walls and elbow-open faucets, all details were considered and tested. To ensure uninterrupted power, the clinic has triple redundancy with an inverter system for seven days of backup power and a generator backing the inverter system.</p>",
   "<p>Operators in remote locations of Africa face daily operational challenges and require effective, efficient solutions tailored to very specific requirements. The challenges — an extremely remote location, extreme weather, security and logistics — presented another opportunity to get creative, solve a problem and deliver a fully functioning facility to a satisfied client.</p>"]),
 ("humanitarian-air-services-drc","KEA Awarded Contract for Humanitarian Air Services in DRC","3 March 2021","2021-03-03",["News","Rotary and Fixed Wing"],U+"2021/03/Kalemie-Banner.jpg",
  "Two Cessna C208B aircraft now fly humanitarian passengers and cargo six days a week across the Tanganyika Province of the DRC.",
  ["<p>KEA has been awarded a contract for two Cessna C208B aircraft for Humanitarian Air Services in the Tanganyika Province of the Democratic Republic of Congo. Since April 2020 we have been providing transportation of passengers and cargo in support of humanitarian efforts. The area of flight operation is currently the Tanganyika province in the South East of the DRC, with Kalemie as our Main Operations Base.</p>",
   "<h3>KEA is currently providing transportation of humanitarian passengers and cargo with six flights per week in the Tanganyika Province of DRC.</h3>",
   "<p>Flight operations are scheduled six days per week, and operated to the airports of Kalemie (FZRF), Nyunzu (FZRN), Kongolo (FZRQ), Kabalo (FZRM), Manono (FZRA) and Moba (FZRB). Infrastructure and facilities are developing since Kalemie gained the status of chief town of the Tanganyika province.</p>"]),
 ("covid-19-update","Ensuring Passenger Safety — Covid-19 Update KEA","26 March 2020","2020-03-26",["News"],U+"2020/03/Coronavirus-COVID-19-AP_GB.jpg",
  "Strict risk-mitigation measures across cleaning, passenger hygiene and health screening, aligned to WHO and government guidelines.",
  ["<p>As the world faces the Covid-19 global pandemic, the health and safety of global travellers has been compromised. Until the virus is brought under control, we are taking every precaution to ensure the safety of passengers and visitors at our facility and on all flights. To comply with hygiene guidelines set by the World Health Organisation and government, KEA has implemented strict risk-mitigation measures for all charter flights.</p>",
   "<h3>Aircraft Cleaning</h3>",
   "<p>Thorough cleaning and disinfection of aircraft cabins and contents after each flight — including trays, seats, handles, seat covers, carpets and objects handled by passengers and crew. Cleaning products and disinfectants are approved by aircraft manufacturers and are effective against a wide range of pathogens.</p>",
   "<h3>Passenger Hygiene &amp; Health</h3>",
   "<p>Hand washing and disinfection is required on premises for all staff, visitors and clientele. Pre-flight briefings highlight best practices to avoid contamination, and hand sanitiser is provided in each aircraft cabin. All passengers and personnel are screened; symptomatic persons are not permitted on the property or aboard flights.</p>"]),
 ("multi-role-helicopter-contract","KEA Awarded a Multi-Year, Multi-Role Helicopter Contract","18 March 2020","2020-03-18",["News","Rotary and Fixed Wing"],U+"2020/03/Chad-News-Banner-Blue-02-scaled.jpg",
  "KEA established a base in N’djamena, Chad with three helicopters covering Chad, Nigeria, Niger and Cameroon.",
  ["<p>Through competitive tender, KEA has been awarded a multi-year, multi-role helicopter contract. KEA has deployed and established a base in N’djamena, Chad, where three helicopters of two types are positioned to provide VIP passenger transportation, cargo/logistics movements and NVG-capable medevac operations. The area of responsibility covers four countries — Chad, Nigeria, Niger and Cameroon — spanning over 40,000 square miles.</p>",
   "<h3>KEA is providing Advanced Life Support (ALS) and Advanced Trauma Life Support (ATLS), through its in-house medical division, on a fifteen-minute notice to launch, 24 hours a day.</h3>",
   "<p>KEA has built many years of experience providing these services in the most austere and hostile environments and looks forward to executing our proven capabilities to best serve our new client.</p>"]),
 ("pau-national-content-conference","KEA Attends PAU 2nd National Content Conference","18 March 2020","2020-03-18",["News"],U+"2020/03/NCC-PAU-2.jpg",
  "KEA attended the 2nd National Content Conference organised by the Petroleum Authority of Uganda at Serena Kampala.",
  ["<p>KEA attended the 2nd National Content Conference organised by the Petroleum Authority of Uganda at Serena Kampala, under the theme ‘Linkages between the Oil and Gas and other sectors of the Ugandan Economy’.</p>",
   "<p>The emerging oil and gas sector in Uganda demands the highest standard of safety and quality from its stakeholders and suppliers. KEA is deepening relationships with the industry to help raise the profile of local companies and establish strong, fruitful partnerships through full compliance.</p>",
   "<h3>KEA provides a range of specialised services that have normally been outsourced to global multi-national companies.</h3>",
   "<p>The influx of personnel in the region is bound to increase demand for transportation within areas of operation and for tourism. With a strong company profile and a proven ability to provide the highest level of safety and quality, KEA and our subsidiaries will provide secure and efficient means to transport greater volumes of cargo, personnel and international travellers around Uganda.</p>"]),
 ("africa-oil-week-2019","KEA Attends Africa Oil Week 2019","16 December 2019","2019-12-16",["News"],U+"2019/12/AOW-Banner-1.jpg",
  "Our commercial manager spent a week in Cape Town meeting fellow players in the oil industry at Africa Oil Week.",
  ["<p>Henk Boneschans, our commercial manager, spent a week in Cape Town, South Africa in early November attending the Africa Oil Week Conference. With over 1,800 delegates and 26 ministers in attendance, KEA was there to meet fellow players in the oil industry and discuss how KEA’s services can be of benefit.</p>",
   "<h3>Our world-class helicopter and fixed-wing capabilities, combined with specialised services such as auto-photo mapping, gravity surveys and magnetic surveys, position us as an invaluable vendor for the oil and gas industry.</h3>",
   "<p>Henk attended many seminars on offer and particularly enjoyed one entitled Local Content and Procurement. He brought back valuable information which will guide our future service operations.</p>"]),
 ("oil-and-gas-south-sudan","Oil and Gas Support In South Sudan","16 December 2019","2019-12-16",["News","Oil Gas and Mining"],U+"2019/12/Oil-and-Gas-DAR-Post.jpg",
  "DAR Petroleum Operating Company contracted KEA’s Bell 412 helicopters for urgent camp and rig support during flooding.",
  ["<p>DAR Petroleum Operating Company (DPOC) recently contracted KEA’s oil-and-gas compliant Bell 412 helicopters to provide urgent camp and rig support required due to flooding in their operational area.</p>",
   "<h3>KEA mobilised their helicopters in record time to ensure DPOC’s daily oil production was not disrupted.</h3>",
   "<p>This in turn ensures South Sudan’s critical oil revenues continue to flow.</p>"]),
 ("medevac-training-simulation","Medical Evacuation Interactive Training Simulation","15 December 2019","2019-12-15",["News"],U+"2019/12/Medevac-Crews-Caravan-Banner.jpg",
  "In preparation for Priority Air Ambulance, KEA trained medics alongside City Ambulance partners at Kajjansi Airfield.",
  ["<p>In preparation for the launch of Priority Air Ambulance, we have been training our medics alongside our partners at City Ambulance. Together with their ground ambulance proficiency and our air ambulance expertise, we are able to offer world-class services. Patients can be seamlessly transported from the site of an accident to their chosen clinic or hospital using a combination of ground ambulances, aeroplanes and helicopters.</p>",
   "<h3>A patient was simulated to have been airlifted for a higher level of medical care in Kampala.</h3>",
   "<p>The training at Kajjansi Airfield focused on transferring patients from the scene of an accident to the plane or helicopter and then on to the ground ambulance. Part of the training focused on safety around aircraft, safe approach, the operations command system and team interaction. Improved procedures were identified and revised to ensure smooth future operations.</p>"]),
 ("pibor-floods-relief","Disaster Relief for Floods in Pibor, Eastern South Sudan","30 October 2019","2019-10-30",["News","Rotary and Fixed Wing"],U+"2019/10/Pibor-Banner.jpg",
  "KEA supported an international non-profit in flood-hit Pibor, flying critical medical aid where roads were impassable.",
  ["<p>KEA is currently supporting an international non-profit organisation in Pibor, South Sudan. Due to extreme flooding, vast majorities of the area including its airfield are flooded, so KEA’s versatile and expedite helicopter services are required. Critical medical aid is being flown in to treat and prevent outbreaks of potential illness.</p>",
   "<h3>Due to extreme flooding, vast majorities of the area including its airfield are flooded, so KEA’s versatile and expedite helicopter services are required.</h3>",
   "<p>The risks posed to the population are many — from malnutrition to the rapid spread of disease as access to medical care is restricted and floods have contaminated water sources. With a helicopter as the only way to transport medical and other vital supplies, the situation is truly critical.</p>"]),
 ("private-pilot-scholarship","National Scholarship for Private Pilot Licence","15 October 2019","2019-10-15",["News"],U+"2019/10/Post-PAAcadmy2.jpg",
  "Our academy, Pangea Aviation Academy, announced a scholarship for one individual to obtain their Private Pilot Licence.",
  ["<p>On 26 July 2019, our Aviation Academy, Pangea Aviation Academy, proudly announced a scholarship opportunity for one individual to obtain their Private Pilot Licence (PPL) from our Kajjansi-based training facility.</p>",
   "<h3>Pangea Aviation Academy has trained over 230 pilots over the last 22 years.</h3>",
   "<p>The move supports the growth of the Ugandan aviation industry. With the revival of Uganda Airlines and a rising need for pilots globally, the future looks promising. The scholarship application was open to the public and closed on 31 August, with the winner announced by December 2019. Pangea Aviation Academy is growing to train IATA-certified professionals across the aviation disciplines, with a vision to become Africa’s premier aviation academy.</p>"]),
 ("priority-air-ambulance","Priority Air Ambulance Unveils First Responder Capabilities","15 October 2019","2019-10-15",["News"],U+"2019/10/Priority-Air-Ambulance.jpg",
  "Our affiliate Priority Air Ambulance unveiled new air-ambulance capabilities at the Emergency Care Conference in Jinja.",
  ["<p>Our affiliate company, Priority Air Ambulance, unveiled proposed new capabilities for an air ambulance service new to Uganda at the Emergency Care Conference held in Jinja during 2–4 August 2019. The Bell 412 that will be part of the three-aircraft air ambulance fleet operating out of Kajjansi was staged at the event with its pilot, ground support, technical and medical crew, alongside two ground ambulances from City Ambulance.</p>",
   "<h3>Priority Air Ambulance, Uganda’s pioneer first responder, brings the hospital to the patient when time is critical.</h3>",
   "<p>Priority Air Ambulance is registering as an NGO and has teamed up with Kampala Executive Aviation, which provides the air assets and Air Operator Certificate. Flights carry dedicated medical crew and state-of-the-art equipment including a defibrillator, ECG monitor, spinal immobilisation and advanced airway management equipment. The Jinja event was a great success in raising awareness of fast, reliable inter-facility transfers and primary medical response flights.</p>"]),
 ("200-tourists-uganda","KEA flies over 200 international Tourists around Uganda","15 February 2019","2019-02-15",["News","Rotary and Fixed Wing"],U+"2019/02/200-Tourists.jpg",
  "A unique two-day operation flying over 200 international tourists across multiple tourism locations in Uganda.",
  ["<p>KEA is proud to announce a unique two-day operation involving flying over 200 international tourists across multiple tourism locations in Uganda on multiple fixed-wing aircraft. The group landed at Entebbe International Airport on 13 February 2019 and departed for their destinations aboard our fleet on 14 February 2019, from Entebbe airport and Kajjansi Airfield where our Fixed Base Operations are located.</p>",
   "<h3>This is the first of its kind mass movement of air passengers to be completed domestically in Uganda.</h3>",
   "<p>We are honoured to be of service and very proud of our crews who worked tirelessly for weeks to make this a success. The operation took several weeks of preparation, with safety and efficiency the priority. Our crews worked within tight timeframes to ferry passengers across many local destinations. With the limitations and austere conditions of Ugandan runways, an operation of this scale truly took operational excellence and industry expertise.</p>"]),
 ("flyuganda-scheduled-flights","KEA launches FlyUganda Scheduled Flights","3 November 2018","2018-11-03",["News"],U+"2018/11/Fly-uganda2.jpg",
  "On 2 November 2018, KEA launched scheduled domestic flights under its subsidiary FlyUganda.",
  ["<h3>On 2 November 2018, KEA launched scheduled domestic flights under its subsidiary FlyUganda.</h3>",
   "<p>The move was made to meet the demand for scheduled flights to major tourism destinations in Uganda. The first route launched was Kajjansi–Kihihi, with future plans to expand to Kidepo Valley National Park, Murchison Falls National Park and Queen Elizabeth. FlyUganda also continues to offer fixed-wing and helicopter charter flights to all locations in Uganda and East Africa.</p>"]),
 ("beechcraft-1900d","New Arrivals To the KEA Fleet — Beechcraft 1900D","19 February 2016","2016-02-19",["News"],U+"2016/02/News-Beechcraft3.jpg",
  "The strategic acquisition of two Beechcraft 1900Ds brings multi-engine safety and airliner-style comfort.",
  ["<h3>Providing multi-engine safety and airliner-style comfort.</h3>",
   "<p>The KEA team continues to expand the services we provide to our customers. With the strategic acquisition of two Beechcraft 1900Ds onto our AOC, we are now able to provide multi-engine safety and airliner-style comfort for our passengers.</p>"]),
 ("ground-breaking-animal-census","Ground-breaking Animal Census","July 2015","2015-07-01",["Aerial and Geophysical Survey","News"],U+"2015/07/ground-breaking-animal-census.jpg",
  "Combining Visionmap A3 Edge aerial mapping with facial-recognition software to produce the world’s most accurate animal census.",
  ["<p>KEA is proud to be a leader in aerial surveys and orthophoto-mapping. For many years KEA has produced orthophoto maps for traditional requirements such as national land surveys, agricultural projects, infrastructure development and border security.</p>",
   "<h3>Combining our Visionmap A3 Edge aerial mapping equipment with facial-recognition software, we are able to achieve the world’s most accurate animal census.</h3>",
   "<p>During June and July, KEA performed surveys over Murchison Falls National Park in Uganda. By mapping the entire park in ultra-high resolution, we can run the pictures through our bespoke software, which counts all visible animals in the park automatically.</p>"]),
 ("flying-for-total-cnooc-tullow","Now Flying for Total E&amp;P, CNOOC and Tullow Oil","17 February 2015","2015-02-17",["News","Oil Gas and Mining"],U+"2015/02/News-Flying-For-Total.jpg",
  "KEA announces the award of a contract with the three main oil companies in Uganda.",
  ["<h3>KEA is proud to announce the award of a contract with the three main oil companies in Uganda.</h3>",
   "<p>Our Bell 412 helicopter fleet will now be flying for Total E&amp;P, CNOOC and Tullow Oil.</p>"]),
 ("total-bureau-veritas-audit","KEA Undertakes an Intense Audit by Total Oil and Gas and Bureau Veritas","22 January 2015","2015-01-22",["News","Oil Gas and Mining"],U+"2019/01/TopBanner.jpg",
  "KEA passed an intense audit, becoming the only aviation company in Uganda qualified to fly for Total plc.",
  ["<h3>KEA is happy to report that we passed the audit and have become the only aviation company in Uganda qualified to fly for Total plc.</h3>",
   "<p>KEA undertook an intense audit by Total Oil and Gas and Bureau Veritas from Paris, France. During the three-day audit, all aspects of our company were under scrutiny to assess whether we meet the demanding standards of the international oil and gas aviation industry — covering flight operations, aircraft maintenance, and safety and quality procedures.</p>"]),
 ("baiji-oil-refinery-extraction","KEA Provides Extraction Flights From the Baiji Oil Refinery","17 June 2014","2014-06-17",["News"],U+"2014/06/baiji-iraq-oil-refinery.jpg",
  "KEA was contracted to provide extraction flights from the Baiji Oil refinery, flying under Night Vision Goggles.",
  ["<p>KEA were based in Erbil, Kurdistan providing both medical evacuation and passenger transport services. With the rise of ISIS that summer, tensions were high and the need for our services grew.</p>",
   "<h3>On 17 June, KEA was contracted by a European government to provide extraction flights from the Baiji Oil refinery. Seventy-six employees of a multi-national company were trapped in the refinery and had no safe passage to exit the country.</h3>",
   "<p>Our skilled and brave crews provided the service at night under the cover of darkness, flying under Night Vision Goggles (NVGs). By daybreak the crews had tirelessly worked to bring everyone to safety.</p>"]),
]

def news_card(n):
    slug,title,dd,di,cats,img,exc=n[0],n[1],n[2],n[3],n[4],n[5],n[6]
    tags="".join('<span class="tag">%s</span>'%c for c in cats)
    return f'''<a class="post reveal" href="/news/{slug}.html"><div class="ph"><img src="{img}" alt="" loading="lazy"></div>
<div class="post-body"><div class="tags">{tags}</div><div class="date">{dd}</div><h3>{title}</h3><p>{exc}</p><span class="rm">Read more →</span></div></a>'''

# inject 3 latest into home
def _home_card(n):
    return f'''<a class="news-card reveal" href="/blog/{n["slug"]}/"><div class="nc-img"><img src="{U}{n["img"]}" alt="{html.escape(n["title"])}" loading="lazy"></div>
<div class="nc-body"><span class="nc-date">{n["date"]}</span><h3>{html.escape(n["title"])}</h3><p>{html.escape(n["summary"])}</p></div></a>'''
latest="".join(_home_card(n) for n in C.NEWS_NEW[:3])
home_body=home_body.replace('<div class="news-grid" id="latest-news"></div>', '<div class="news-grid">%s</div>'%latest)
page("index.html","Aviation Services Kampala & Kajjansi | KEA Aviation",
     "CAA-licensed aviation in Uganda — oil & gas, NGO, medevac, cargo, VIP and UAV charter across 13 African countries from Kajjansi Airstrip, Kampala. Call +256 776 333 114.",
     home_body, active="", extra_jsonld=LOCALBIZ_LD)

# news index
cards="".join(news_card(n) for n in NEWS)
news_body=f'''{page_hero("From the field","News","Operational milestones, contract awards and stories from the world’s most austere environments.",U+"2019/01/TopBanner.jpg")}
<section><div class="wrap"><div class="news-grid">{cards}</div></div></section>'''
page("news.html","News — KEA","Latest news from Kampala Executive Aviation.",news_body,active="news")

# article pages
for i,n in enumerate(NEWS):
    slug,title,dd,di,cats,img,exc,body=n
    blocks="".join(body)
    prev=NEWS[i-1] if i>0 else None
    nxt=NEWS[i+1] if i<len(NEWS)-1 else None
    n[0]
    rel=""
    if prev or nxt:
        rel='<div style="display:flex;justify-content:space-between;gap:1rem;border-top:1px solid var(--line-dark);margin-top:2.5rem;padding-top:1.5rem;font-family:var(--mono);font-size:.78rem">'
        rel+=('<a class="back" href="/news/%s.html">← %s</a>'%(prev[0],prev[1]) if prev else '<span></span>')
        rel+=('<a class="back" href="/news/%s.html">%s →</a>'%(nxt[0],nxt[1]) if nxt else '<span></span>')
        rel+='</div>'
    tags=" · ".join(cats)
    art=f'''{page_hero(tags,title,dd,img)}
<article class="article"><div class="meta">{dd} &nbsp;·&nbsp; {tags}</div>
<div class="body reveal">{blocks}</div>
<div style="margin-top:2.5rem"><a class="btn btn-outline" href="/news.html">← All news</a></div>
{rel}</article>{cta_band()}'''
    page("news/%s.html"%slug, "%s — KEA"%title.replace('&amp;','&'), exc.replace('&amp;','&'), art, active="news")

# ---------------- SOLUTION PAGES ----------------
def pic(rel, alt, sizes="(max-width:820px) 92vw, 33vw", lazy=True):
    """<picture> with WebP + responsive srcset and a JPEG fallback; plain <img> if no derivatives."""
    base=os.path.splitext(rel)[0]
    webp=base+".webp"; webp640=base+"-640.webp"; fb=base+"-1600.jpg"
    R=os.path.join(ROOT,"assets","img"); a=html.escape(alt)
    lz='loading="lazy" decoding="async"' if lazy else 'decoding="async"'
    if os.path.exists(os.path.join(R,webp)):
        fbsrc=U+(fb if os.path.exists(os.path.join(R,fb)) else rel)
        return (f'<picture><source type="image/webp" srcset="{U}{webp640} 640w, {U}{webp} 1600w" sizes="{sizes}">'
                f'<img src="{fbsrc}" alt="{a}" {lz}></picture>')
    return f'<img src="{U}{rel}" alt="{a}" {lz}>'

def alt_for(name, rel):
    f=rel.lower()
    if "interior" in f: return f"{name} cabin interior"
    if "cockpit" in f:  return f"{name} cockpit"
    if "camera" in f:   return f"{name} survey sensor"
    if "medevac" in f:  return f"{name} medevac configuration"
    if "back" in f:     return f"{name} rear loading"
    return f"{name} exterior"

_cn=[0]
def _carousel_div(slides, label, ar="16/10", autoplay=False):
    _cn[0]+=1; cid=f"car{_cn[0]}"; n=len(slides)
    li=[]
    for i,(rel,alt) in enumerate(slides):
        wp=os.path.splitext(rel)[0]+".webp"
        full=U+(wp if os.path.exists(os.path.join(ROOT,"assets","img",wp)) else rel)
        li.append(f'<li class="slide" role="group" aria-roledescription="slide" aria-label="{i+1} of {n}">'
                  f'<button class="slide-btn" data-full="{full}" data-alt="{html.escape(alt)}" aria-label="View full size: {html.escape(alt)}">{pic(rel,alt)}</button></li>')
    nav=''
    if n>1:
        dots="".join('<button class="cdot" data-i="%d" aria-label="Slide %d"%s></button>'%(i,i+1,' aria-current="true"' if i==0 else '') for i in range(n))
        nav=(f'<button class="cbtn cprev" aria-label="Previous slide" aria-controls="{cid}">\u2039</button>'
             f'<button class="cbtn cnext" aria-label="Next slide" aria-controls="{cid}">\u203a</button>'
             f'<div class="cdots" role="group" aria-label="Choose slide">{dots}</div>')
    ap=' data-autoplay="1"' if (autoplay and n>1) else ''
    return (f'<div class="carousel" id="{cid}" role="region" aria-roledescription="carousel" aria-label="{html.escape(label)}"{ap} style="--ar:{ar}">'
            f'<ul class="carousel-track" tabindex="0" aria-label="{html.escape(label)} slides">{"".join(li)}</ul>{nav}</div>')

def carousel_section(slides, label, eyebrow, title, ar="16/10"):
    return (f'<section class="gallery-sec"><div class="wrap">'
            f'<div class="sec-head reveal"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2></div>'
            f'{_carousel_div(slides,label,ar)}</div></section>')

SOL_CAROUSELS={
 "charter-flights":("In the field","Chartering across the region",[("2019/01/Cargo-Charter.jpg","Cargo charter loading"),("2021/08/Caravan-in-Kidepo.jpg","Caravan in Kidepo"),("2019/04/Caravan-1.jpg","Cessna Caravan cabin"),("2019/02/Fleet-PC12.jpg","Pilatus PC-12 on the ramp"),("2020/03/Helicopter-Services-In-Uganda-KEA.jpg","Helicopter charter")]),
 "helicopter-and-fixed-wing":("In the field","Rotary and fixed wing in action",[("2019/01/External-Load-Work.jpg","External load work"),("2019/01/Helicopter-Rear-Door-Open.jpg","Helicopter cargo loading"),("2021/08/B412-Flying-with-Lake-and-Rocky-Scenery.jpg","Bell 412 over Uganda"),("2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg","Mi-8 at Kajjansi"),("2019/01/Medevac-KEA.jpg","Medevac operations"),("2021/03/PHOTO-2021-02-23-13-56-15.jpg","Chad deployment")]),
 "medical-division":("In the field","Air ambulance and HEMS",[("2019/04/Air-ambulance-paramedics.jpg","Air ambulance paramedics"),("2019/12/Gerald-in-Plane.jpg","Patient transfer aboard"),("2019/12/Loading-Stretcher-1.jpg","Loading a stretcher"),("2019/12/Medevac-Crews-Caravan.jpg","Medevac crews and Caravan"),("2019/01/Medevac-KEA.jpg","Medevac aircraft"),("2019/12/Laughing-CityAmb.jpg","Ground ambulance crew")]),
 "aerial-and-geophysical-survey":("In the field","Survey operations",[("2019/01/Aerial-Survey-KEA.jpg","Aerial survey"),("2015/07/ground-breaking-animal-census.jpg","Wildlife census survey"),("2021/08/Kajjansi_KEA.jpg","Kajjansi base"),("2019/04/DA42-Camera.jpg","DA42 survey sensor"),("2019/04/DA42-Back.jpg","DA42 MPP Guardian")]),
 "oil-gas-and-mining":("In the field","Supporting industry operators",[("2019/12/Oil-and-Gas-DAR-Post.jpg","Oil and gas operations"),("2015/02/News-Flying-For-Total.jpg","Flying for Total"),("2014/06/baiji-iraq-oil-refinery.jpg","Baiji refinery extraction"),("2019/01/Oil-Gas-and-Mining.jpg","Oil and gas support"),("2019/01/Passenger-and-Cargo-Transportation.jpg","Crew transportation"),("2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg","Heavy-lift Mi-8")]),
 "maintenance-and-hangarage":("Our AMO","Maintenance and hangarage",[("2019/01/1900-Maintenance.jpg","Beechcraft 1900 maintenance"),("2019/01/1900-Maintenance2.jpg","Engine maintenance"),("2019/01/1900-Maintenance3.jpg","Airframe inspection"),("2019/01/Helicopter-Rear-Door-Open.jpg","Helicopter servicing"),("2018/08/maintenance-hangarage.jpg","Hangarage facility")]),
}
ABOUT_CAROUSEL=[("2019/02/Our-People.jpg","The KEA team"),("2021/08/Kajjansi_KEA.jpg","Kajjansi base"),("2021/08/Pilots-in-B412-Cockpit.jpg","Flight crew in a Bell 412"),("2019/04/Safety-and-Quality.jpg","Safety and quality"),("2020/03/Carousel-1.jpg","Operations"),("2020/03/Carousel-2.jpg","In the field"),("2020/03/Carousel-3.jpg","On the ramp")]
FLEET_GALLERIES={
 "Bell 412":["2019/02/Fleet-B412.jpg","2019/04/B412_Interior.jpg","2019/04/B412_Medevac_Config.jpg"],
 "Bell 206 Jet Ranger":["2019/02/Fleet-B206.jpg"],
 "Pilatus PC-12":["2019/02/Fleet-PC12.jpg","2019/04/PC12-Interior.jpg"],
 "Beechcraft 1900D":["2019/02/Fleet-B1900.jpg","2019/04/B1900_Interior.jpg","2019/04/B1900_Interior2.jpg","2019/04/B1900_Cockpit.jpg"],
 "Cessna Caravan C208B":["2019/02/Fleet-C208B.jpg","2019/04/C208B-Interior.jpg"],
 "Cessna 210":["2019/02/Fleet-C210.jpg","2019/04/C210-MLW2.jpg","2019/04/210_Interior.jpg"],
 "Diamond DA42 MPP Guardian":["2019/02/Fleet-Diamond.jpg","2019/04/DA42-Camera.jpg","2019/04/DA42-Cockpit.jpg","2019/04/DA42-Interior.jpg","2019/04/DA42-Back.jpg"],
}

def solution_page(slug,nav_title,hero_eyebrow,hero_title,hero_sub,hero_bg,lead_big,lead_p,cards,extra="",og=""):
    body=f'''{page_hero(hero_eyebrow,hero_title,hero_sub,hero_bg)}
<section><div class="wrap lead-row">
<div class="reveal"><span class="eyebrow">{nav_title}</span><p class="big" style="margin-top:1.2rem">{lead_big}</p></div>
<div class="reveal"><p style="color:var(--slate);font-size:1.05rem;margin:1.4rem 0 2rem">{lead_p}</p><a class="btn btn-outline" href="/contact.html">Request a quote <span class="arr">→</span></a></div>
</div>'''
    if cards:
        body+=f'<div class="wrap">{feats(cards)}</div>'
    body+='</section>'
    if slug in SOL_CAROUSELS:
        eb,tt,imgs=SOL_CAROUSELS[slug]
        body+=carousel_section(imgs, tt, eb, tt)
    body+=extra
    body+=cta_band()
    page("solutions/%s.html"%slug, "%s — KEA"%hero_title, hero_sub, body, active="solutions")

solution_page = lambda *a, **k: None   # old /solutions/* replaced by keyword-first /services/* pages (301s in vercel.json)
solution_page("charter-flights","Charter Flights","Safe, fast and worry-free travel","Charter Flights",
 "Reliable helicopter and fixed-wing charters across Africa.",IC1+"Cargo-Charter.jpg",
 "We offer the best solutions for safe, fast and worry-free travel across Africa’s wide open spaces.",
 "Avoid the hazards and discomforts of road travel in these regions on a KEA private charter. Given our network, we have the unique ability to fly you directly to your destination and land on-property.",
 [(IC+"Aircraft-02.svg","Passenger and Cargo","Charter flights with a reliable operator are the best solution for safe, fast and worry-free travel across Africa’s wide open spaces."),
  (IC+"VIP-15.svg","VIP Transport","Experienced in the conveyance of VIP delegations and their families for business or leisure, with a focus on safety, security and discretion."),
  (IC+"Location-pin-18.svg","Business Charter","Flights for corporate clients with unique requirements, chartering an aircraft to any destination."),
  (IC+"Scenery-16.svg","Scenic Flights","Flights for special occasions and events, including personal events and air tours / scenic flights.")],
 banner("Uganda’s largest privately owned fleet","Private travel made easy and accessible.","With a versatile fixed and rotary wing capability, we give you all the options to make private travel simple — wherever you need to be.",U+"2020/03/Helicopter-Services-In-Uganda-KEA.jpg",("View the fleet","/fleet.html")))

solution_page("helicopter-and-fixed-wing","Rotary and Fixed Wing","Fully integrated aviation solutions","Rotary and Fixed Wing Services",
 "A strong, robust team of highly skilled people with an accident-free record.",U+"2020/03/Helicopter-Services-In-Uganda-KEA.jpg",
 "KEA’s fixed and rotary wing service is built upon a strong, robust team of highly skilled resources.",
 "Our operational history starts in 2008 and we currently hold an accident-free track record, achieved through an increased focus on safety and quality across all spheres of our service, with great aeroplane and helicopter operational and management competence.",
 [(IC+"Aircraft-02.svg","Passenger and Cargo","Smooth, secure transportation of passengers and cargo — from crew rotations to VIP transport, through scheduled and adhoc charters."),
  (IC+"helicopter-Medical-01-01.svg","Medical Evacuation","Dedicated aircraft for medical evacuation and HEMS patient transport, operating 24 hours a day with Night Vision Goggle equipment."),
  (IC+"Oil-Rig-03.svg","Oil, Gas and Mining","The highest level of safety and quality demanded by industry — surveillance, crew rotations, LIDAR mapping and medical evacuation."),
  (IC+"Rescue-04.svg","Search and Rescue","Capable of carrying out and supporting domestic and international search &amp; rescue over water, land, jungle and mountainous terrain.")],
 banner("24-hour capability","Search and rescue, day or night.","Our SAR teams are equipped with ELTs, SART beacons, flight following and VHF/UHF/tactical communications — using Night-Vision-Goggle-compatible helicopters and hoist equipment.",U+"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg",("Talk to our experts","/contact.html")))

solution_page("medical-division","Medical Division","Saving lives for over a decade","KEA Medical Division",
 "Quality care even in the most challenging environments.",IC1+"Medevac-KEA.jpg",
 "We have over 10 years’ medical evacuation experience with a 100% safety record.",
 "Through its medical division, KEA supports remote-site clinics, 24-hour NVG medical evacuations and air ambulance requirements. Our highly trained, pre-hospital medical flight crew delivers compassionate, quality care even in the most challenging of environments, to both private and government clients.",
 [(IC+"Rescue-04.svg","Helicopter Specialized","Our helicopters access rugged, isolated locations, carrying multiple patients to the nearest suitable facility while being stabilised and treated in flight."),
  (IC+"Worker-20.svg","High Risk Operations","Our expertise in emergency and patient transportation makes us the perfect partner for organisations in remote settings or high-risk operations."),
  (IC+"Life-Support-19.svg","Advanced Life Support","Advanced life support skills paired with extensive equipment let us respond to natural disasters, workplace mishaps, combat situations and accidents.")],
 banner("24/7 response","Our night-vision capability makes 24/7 emergency response possible.","Highly skilled crews and NVG-equipped aircraft mean we can respond to emergencies around the clock.",U+"2019/12/Medevac-Crews-Caravan-Banner.jpg",("Contact the medical division","/contact.html")))

solution_page("aerial-and-geophysical-survey","Aerial &amp; Geophysical Survey","Fast, accurate and actionable data","Aerial and Geophysical Survey",
 "Make better decisions with accurate and actionable data.",IC1+"Aerial-Survey-KEA.jpg",
 "KEA performs a variety of aerial and geophysical surveys with expert crews, multiple aircraft and modern processing software.",
 "From pipeline survey, seismic survey, LIDAR surveys, electricity and powerline survey, architectural, road and drainage, land and wildlife survey and more — using state-of-the-art technology and highly trained crews, we generate fast, accurate and actionable results, individually tailored to your needs.",
 [],
 banner("World-first capability","The world’s most accurate animal census.","Combining our Visionmap A3 Edge aerial mapping with facial-recognition software, KEA mapped Murchison Falls National Park in ultra-high resolution to count every visible animal automatically.",U+"2015/07/ground-breaking-animal-census.jpg",("Read the story","/news/ground-breaking-animal-census.html")))

solution_page("oil-gas-and-mining","Oil, Gas and Mining","Fully customizable solutions","Oil, Gas and Mining Support",
 "The highest level of safety and quality demanded by industry operators.",U+"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg",
 "We employ the best of technology and innovation to deliver service excellence in oil, gas and mining support.",
 "Since 2015 we have served industry leaders in Uganda’s oil and gas operations. From surveillance, crew rotations, LIDAR mapping and medical evacuation, we are well equipped to cater to this challenging and dynamic line of work, scaling our solutions to meet industry standards.",
 [(IC2+"Offshore-12.svg","Onshore &amp; Offshore Transport","Both rotary and fixed-wing transportation solutions for passengers and cargo."),
  (IC2+"Dispatch-14.svg","Flight Dispatch &amp; Asset Tracking","Our flight-following system lets dispatch and ground crews track aircraft, providing reliable real-time coverage of all your assets."),
  (IC2+"Medevac-13.svg","Medical Evacuation","Highly trained, pre-hospital medical flight crew delivering quality care even in the most challenging environments."),
  (IC2+"Offshore-12.svg","Aerial Construction","Flexibility to execute complex construction projects thanks to a diverse, well-maintained fleet and highly trained crews.")],
 banner("OGP 590 / 390 compliant","Built to the standards your operation demands.","To provide the highest level of oil, gas and mining support, we strictly adhere to required technical documentation such as OGP 590 / 390 and customer technical orders.",U+"2019/12/Oil-and-Gas-DAR-Post.jpg",("Request a quote","/contact.html")))

maint_extra=f'''<section style="background:var(--tint)"><div class="wrap">
<div class="sec-head reveal"><span class="eyebrow">Licensed AMO</span><h2>Aircraft we maintain</h2></div>
<div class="prose reveal" style="margin-top:1.5rem"><ul style="columns:2;max-width:none">
<li>Beechcraft 1900 series</li><li>Beechcraft 350 series</li><li>Pilatus PC12 series</li><li>Cessna 208 series</li>
<li>Cessna 172, 206, 210 series</li><li>Bell / Agusta-Bell 412 series</li><li>Bell 206 series</li><li>Rotary wing platforms</li></ul></div></div></section>'''
solution_page("maintenance-and-hangarage","Maintenance &amp; Hangarage","Third-party maintenance services","Aircraft Maintenance and Hangarage",
 "Scheduled and non-scheduled maintenance through our Uganda and Iraqi licensed AMO.",U+"2018/08/maintenance-hangarage.jpg",
 "KEA can provide third-party maintenance services through our Uganda and Iraqi licensed AMO.",
 "We maintain all our aircraft through our AMO, which has the capacity to carry out scheduled and non-scheduled maintenance, minor sheet-metal repairs and avionic repairs. With a highly specialised crew of aero engineers from around the globe, we maintain aircraft to the highest industry safety standards.",
 [(IC1+"Scheduled-01.svg","Scheduled Maintenance","All preventative maintenance at regular intervals — 100-hour, annual and progressive inspections, plus preflight checks to keep aircraft airworthy."),
  (IC1+"Unscheduled-01.svg","Unscheduled Maintenance","We address unexpected issues immediately to ensure the safety of pilots and passengers."),
  (IC1+"Sheet-Repairs-01.svg","Sheet Repairs","Complex structural repairs — from installation to repair and replacement of sheet-metal components and structural assemblies."),
  (IC1+"Avionics-01.svg","Avionics","From radios and radars to navigation equipment, our technicians troubleshoot and replace electrical and mechanical components.")],
 maint_extra)

# ---------------- FLEET ----------------
FLEET=[
 ("Rotary Wing","Bell 412","1 / 2","13","360 NM","125 kt"),
 ("Rotary Wing","Bell 206 Jet Ranger","1","4","300 NM","100 kt"),
 ("Fixed Wing","Pilatus PC-12","1 / 2","8","1600 NM","250 kt"),
 ("Fixed Wing","Beechcraft 1900D","2","19","1200 NM","285 kt"),
 ("Fixed Wing","Cessna Caravan C208B","1 / 2","13","900 NM","145 kt"),
 ("Fixed Wing","Cessna 210","1","5","700 NM","145 kt"),
 ("Special Mission","Diamond DA42 MPP Guardian","1 + 1 sensor","2","1050 NM","125 kt"),
]
def ac_card(cat,name,crew,pax,rng,spd):
    gal=FLEET_GALLERIES.get(name,[])
    slides=[(rel, alt_for(name,rel)) for rel in gal]
    media=_carousel_div(slides, name+" photo gallery", ar="16/10") if slides else ''
    return f'''<div class="ac reveal">{media}<div class="ac-body"><div class="type">{cat}</div><h3>{name}</h3>
<div class="specs"><div class="s"><div class="v">{crew}</div><div class="k">Crew</div></div>
<div class="s"><div class="v">{pax}</div><div class="k">Passengers</div></div>
<div class="s"><div class="v">{rng}</div><div class="k">Range</div></div>
<div class="s"><div class="v">{spd}</div><div class="k">Cruise</div></div></div></div></div>'''
fleet_cards="".join(ac_card(*a) for a in FLEET)
fleet_body=f'''{page_hero("Uganda’s largest privately owned fleet","Our Fleet","A versatile fixed and rotary wing capability lets us tailor a solution to each client’s unique need.",U+"2020/03/Helicopter-Services-In-Uganda-KEA.jpg")}
<section><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Aircraft</span><h2>Fixed wing, rotary wing and special mission</h2></div>
<p class="reveal" style="color:var(--slate);max-width:60ch;margin-top:1rem">Tap any aircraft photo to view the full gallery — exteriors, cabins and cockpits.</p>
<div class="fleet-grid">{fleet_cards}</div></div></section>
{banner("One operator","The right aircraft for every mission profile.","From single-engine bush operations to multi-engine airliner comfort and sensor-equipped survey platforms — we match the airframe to the task.",U+"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg",("Discuss your requirement","/contact.html"))}'''
page("fleet.html","Fleet — KEA","KEA operates the largest privately owned fleet in Uganda — fixed wing, rotary wing and special mission aircraft.",fleet_body,active="fleet")

# ---------------- ABOUT ----------------
about_body=f'''{page_hero("Who we are","Specialist Aviation Solutions","For over a decade KEA has supported industry leaders across Africa and the Middle East.",U+"2020/03/Helicopter-Services-In-Uganda-KEA.jpg")}
<section><div class="wrap lead-row">
<div class="reveal"><span class="eyebrow">About KEA</span><p class="big" style="margin-top:1.2rem">One airline. Endless possibilities.</p></div>
<div class="reveal prose"><p>Kampala Executive Aviation provides a full spectrum of aviation-centric services for government and private clients in the most challenging and austere environments on earth. Our operational history starts in 2008, and across that time we have built a reputation for high-quality, professional service.</p>
<p>We operate the largest privately owned fleet in Uganda, with a versatile fixed and rotary wing capability that lets us tailor a solution to each client’s unique need.</p></div>
</div></section>
<div class="split">
<div class="panel approach"><div class="inner reveal"><span class="eyebrow">How we work</span><h2 style="margin:1rem 0">Our Approach</h2>
<p>The KEA approach employs the best of technology and innovation to deliver an ongoing commitment to service excellence. Our specialised services are built on a strong, robust team of highly skilled people with deep operational and management competence.</p>
<a class="btn btn-outline" href="/services/">Our services <span class="arr">→</span></a></div></div>
<div class="panel fleet-teaser"><div class="inner reveal"><span class="eyebrow">Safety &amp; Quality</span><h2 style="margin:1rem 0">Safety is everything</h2>
<p>We currently hold an accident-free track record, achieved through an increased focus on safety and quality across all spheres of our service. We are the only aviation company in Uganda to have qualified to fly for Total plc, following an intense audit by Total Oil and Gas and Bureau Veritas.</p>
<a class="btn btn-primary" href="{U}2020/04/KEA-Safety-Policy2020-Screen.pdf" target="_blank" rel="noopener">Read our Safety Policy <span class="arr">→</span></a></div></div></div>
<div class="stats" style="padding-top:110px"><div class="wrap"><div class="stats-grid reveal">
<div class="stat"><div class="num" data-target="4000" data-suffix="T">0<span>T</span></div><div class="lbl">Cargo Carried</div></div>
<div class="stat"><div class="num" data-target="40000">0</div><div class="lbl">Passengers Flown</div></div>
<div class="stat"><div class="num" data-target="7800">0</div><div class="lbl">Flights Conducted</div></div>
<div class="stat"><div class="num" data-target="13">0</div><div class="lbl">Countries Worked In</div></div>
</div></div></div>
{carousel_section(ABOUT_CAROUSEL,"KEA people and operations","Our people and operations","The team behind every mission")}
{cta_band()}'''
page("about.html","About — KEA","Kampala Executive Aviation: specialist aviation solutions with an accident-free track record since 2008.",about_body,active="about")

# ---------------- CAREERS ----------------
careers_body=f'''{page_hero("Join the team","Careers at KEA","We welcome different kinds of talent — from pilots and engineers to medical and operations crew.",U+"2019/12/Medevac-Crews-Caravan-Banner.jpg")}
<section><div class="wrap lead-row">
<div class="reveal"><span class="eyebrow">We welcome different kinds of talent</span><p class="big" style="margin-top:1.2rem">Great people are at the heart of everything we do.</p></div>
<div class="reveal prose"><p>We are always interested to hear from talented, safety-minded professionals who want to work in some of the most demanding aviation environments in the world. While we may not have open positions advertised at all times, we keep every application on file and will be in touch when a suitable role opens up.</p>
<p>To be considered, send us your CV and a short note about the kind of role you’re looking for.</p></div>
</div>
<div class="wrap"><div class="sec-head reveal" style="margin-top:1rem"><span class="eyebrow">Submit your CV</span><h2>Send us your details</h2></div>
<form class="form reveal" data-formsubmit action="{FORM_ACTION}" method="POST" enctype="multipart/form-data">
<input type="hidden" name="_subject" value="New CV submission — flykea.com careers">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="/thank-you.html">
<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="row"><div><label>Full name</label><input type="text" name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<div class="row"><div><label>Phone</label><input type="tel" name="phone"></div><div><label>Role of interest</label><input type="text" name="role" placeholder="e.g. Pilot, AME, Medic"></div></div>
<div><label>Message</label><textarea name="message" placeholder="Tell us about yourself"></textarea></div>
<div><label>Attach CV (PDF / Word)</label><input type="file" name="attachment" accept=".pdf,.doc,.docx"></div>
<div class="form-status" role="status" aria-live="polite" hidden></div>
<div><button class="btn btn-primary" type="submit">Submit application <span class="arr">→</span></button></div>
</form></div></section>'''
page("careers.html","Careers — KEA","Join Kampala Executive Aviation. Submit your CV to be considered for future roles.",careers_body,active="careers")

# ---------------- CONTACT ----------------
contact_body=f'''{page_hero("Get in touch","Contact KEA","Tell us about your requirement and we’ll help find the solution best suited to your need.",U+"2019/01/TopBanner.jpg")}
<section><div class="wrap contact-grid">
<div class="reveal">
<div class="contact-card">
<div class="line"><strong>Address</strong></div><div class="line">Gate 1, Kajjansi Airstrip, Uganda</div>
<div class="line"><strong>Telephone</strong></div><div class="line">{PHONE}<br>{PHONE2}</div>
<div class="line"><strong>Email</strong></div><div class="line"><a href="mailto:{EMAIL}" style="color:var(--green-ink)">{EMAIL}</a></div>
<div class="line"><strong>Payments</strong></div><div class="line"><a href="{PAY}" target="_blank" rel="noopener" style="color:var(--green-ink)">Make a payment online →</a></div>
</div>
<div class="map"><iframe loading="lazy" src="https://www.google.com/maps?q=Kajjansi+Airfield,+Uganda&output=embed" title="KEA — Kajjansi Airfield"></iframe></div>
</div>
<div class="reveal">
<span class="eyebrow">Send a message</span><h2 style="font-size:clamp(1.6rem,3vw,2.2rem);margin:1rem 0 0">How can we help?</h2>
<form class="form" data-formsubmit action="{FORM_ACTION}" method="POST">
<input type="hidden" name="_subject" value="New enquiry — flykea.com contact form">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="/thank-you.html">
<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="row"><div><label>Full name</label><input type="text" name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<div class="row"><div><label>Phone</label><input type="tel" name="phone"></div><div><label>Service of interest</label><select name="service"><option>General enquiry</option><option>Charter flight</option><option>Medical evacuation</option><option>Oil, gas and mining</option><option>Aerial / geophysical survey</option><option>Maintenance &amp; hangarage</option></select></div></div>
<div><label>Message</label><textarea name="message" required></textarea></div>
<div class="form-status" role="status" aria-live="polite" hidden></div>
<div><button class="btn btn-primary" type="submit">Send enquiry <span class="arr">→</span></button></div>
</form>
</div>
</div></section>'''
page("contact.html","Contact — KEA","Contact Kampala Executive Aviation — Gate 1, Kajjansi Airstrip, Uganda.",contact_body,active="contact")

# ---------------- THANK YOU (form redirect target) ----------------
thanks_body=f'''<section style="padding:9rem 0 7rem"><div class="wrap"><div class="thanks reveal">
<div class="tick">✓</div>
<span class="eyebrow" style="justify-content:center">Message received</span>
<h1 style="font-size:clamp(2rem,4vw,2.8rem);margin:.8rem 0 1rem">Thank you</h1>
<p class="big" style="margin-bottom:2rem">Your message has reached the KEA team. We’ll review it and be in touch as soon as we can.</p>
<a class="btn btn-primary" href="/index.html">Back to home <span class="arr">→</span></a>
</div></div></section>'''
page("thank-you.html","Thank you — KEA","Your message has been received by Kampala Executive Aviation.",thanks_body,active="",noindex=True)

# ================= GENERATE NEW SEO PAGES =================
def _blurb(s): return re.sub('<[^>]+>','',s['lead'])[:96].rsplit(' ',1)[0]+'…'

for s in C.SERVICES:
    render_service(s)

# ---- Services hub ----
hub_cards="".join(
 f'<a class="sol-card reveal" href="/{s["slug"]}/"><img src="{U}{s["hero"]}" alt="{html.escape(s["h1"])}">'
 f'<div class="sol-body"><div class="sol-num">{i+1:02d}</div><h3>{s["h1"].replace(" in Uganda","").replace(" near Entebbe","")}</h3>'
 f'<p>{html.escape(_blurb(s))}</p><span class="sol-more">Explore →</span></div></a>'
 for i,s in enumerate(C.SERVICES))
hub_body=f'''{page_hero("What we do","Aviation Services in Uganda &amp; Africa","Charter, oil &amp; gas, humanitarian, medevac, cargo, survey, UAV, leasing and MRO — one CAA-licensed operator at Kajjansi Airstrip, Kampala.",U+"2020/03/Helicopter-Services-In-Uganda-KEA.jpg")}
<section><div class="wrap"><div class="prose reveal" style="margin-bottom:2.5rem"><p>KEA delivers a full spectrum of <b>aviation services in Uganda</b> and across 13 African countries from <b>Kajjansi Airstrip, Kampala</b>. Explore each capability below, or <a href="/quote/">request a quote</a>.</p></div>
<div class="sol-grid">{hub_cards}</div></div></section>
{clients_strip()}{certs_section()}{quote_form("Services hub")}'''
hub_items=_ld({"@context":"https://schema.org","@type":"ItemList","itemListElement":[
  {"@type":"ListItem","position":i+1,"name":s["h1"],"url":BASE_URL+"/"+s["slug"]+"/"} for i,s in enumerate(C.SERVICES)]})
page("services/index.html","Aviation Services in Uganda | KEA Aviation",
     "Full-spectrum aviation services in Uganda — charter, oil & gas, NGO, medevac, cargo, survey, UAV, leasing and MRO from Kajjansi, Kampala. Call +256 776 333 114.",
     hub_body, active="services",
     extra_jsonld=hub_items+"\n"+crumb_ld([("Home",""),("Services","services/")]))

# ---- Certifications ----
cert_body=f'''{page_hero("Licensed &amp; approved","Certifications & Approvals","KEA operates under Air Operator Certificates and Approved Maintenance Organisation approvals across the region.",U+"2018/08/maintenance-hangarage.jpg")}
<section><div class="wrap"><div class="prose reveal"><p>Kampala Executive Aviation is a fully CAA-licensed operator. We hold <b>Uganda AOC&nbsp;097</b>, with additional Air Operator Certificates in <b>Chad</b> and <b>South Sudan</b>; Approved Maintenance Organisation (AMO) approvals in <b>Uganda, South Africa, Chad, the Central African Republic and Iraq</b>; and a Ugandan CAA <b>UAV Operating Certificate (UOC)</b> for certified drone operations.</p>
<p style="color:var(--slate);font-family:var(--mono);font-size:.82rem"><!-- CERTS: certificate numbers/scopes beyond AOC 097 to be confirmed by KEA before publishing --></p></div></div></section>
{certs_section()}{quote_form("Certifications")}'''
page("certifications/index.html","Certifications & Approvals (AOC, AMO, UOC) | KEA Aviation",
     "KEA holds Uganda AOC 097 plus AOCs in Chad & South Sudan, AMO approvals in five countries, and a Ugandan CAA UAV Operating Certificate. Call +256 776 333 114.",
     cert_body, active="", extra_jsonld=crumb_ld([("Home",""),("Certifications","certifications/")]))

# ---- Quote page ----
quote_body=f'''{page_hero("Request a quote","Get a Charter Quote","Estimate your route and aircraft instantly, then send it to us on WhatsApp or request an exact quote below.",U+"2019/04/Caravan-1.jpg")}
{quote_map("full","Quote page")}
{quote_form("Quote page")}'''
page("quote/index.html","Get a Charter Quote | KEA Aviation",
     "Request a charter, cargo, medevac or UAV quote from KEA — CAA-licensed aviation from Kajjansi Airstrip, Kampala. Call +256 776 333 114.",
     quote_body, active="", extra_jsonld=crumb_ld([("Home",""),("Get a Quote","quote/")]))

# ---- Quote received (form target, noindex) ----
qr_body=f'''<section style="padding:9rem 0 7rem"><div class="wrap"><div class="thanks reveal">
<div class="tick">✓</div><span class="eyebrow" style="justify-content:center">Request received</span>
<h1 style="font-size:clamp(2rem,4vw,2.8rem);margin:.8rem 0 1rem">Thank you</h1>
<p class="big" style="margin-bottom:2rem">Your quote request has reached the KEA operations team. We’ll review it and be in touch as soon as we can.</p>
<a class="btn btn-primary" href="/index.html">Back to home <span class="arr">→</span></a></div></div></section>'''
page("quote-received.html","Quote request received — KEA","Your quote request has been received by Kampala Executive Aviation.",qr_body,active="",noindex=True)

# ---- Blog (news stories + cornerstone guides) ----
ALL_POSTS=sorted(C.NEWS_NEW + C.BLOG_POSTS, key=lambda x:x["date"], reverse=True)
render_blog_index(ALL_POSTS)
for _n in ALL_POSTS:
    render_post(_n)

# ---------------- sitemap.xml + robots.txt ----------------
_urls="".join(f'<url><loc>{BASE_URL}/{p}</loc><changefreq>monthly</changefreq></url>' for p in sorted(set(PAGES)))
open(os.path.join(ROOT,'sitemap.xml'),'w').write(
  '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+_urls+'</urlset>\n')
open(os.path.join(ROOT,'robots.txt'),'w').write(
  "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE_URL)
print("wrote sitemap.xml (%d urls) + robots.txt" % len(set(PAGES)))

print("DONE. Pages generated.")
