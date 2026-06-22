#!/usr/bin/env python3
# KEA static site generator. Edit content below, then: python3 build.py
import os, html
ROOT = os.path.dirname(os.path.abspath(__file__))
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

SOL = [
 ("charter-flights","Charter Flights"),
 ("helicopter-and-fixed-wing","Helicopter and Fixed Wing"),
 ("medical-division","Medical Division"),
 ("aerial-and-geophysical-survey","Aerial and Geophysical Survey"),
 ("oil-gas-and-mining","Oil, Gas and Mining"),
 ("maintenance-and-hangarage","Maintenance and Hangarage"),
]

def nav(active=""):
    sub="".join('<a href="/solutions/%s.html">%s</a>'%(s,t) for s,t in SOL)
    def cls(k): return ' class="active"' if k==active else ''
    return f'''<header id="hdr"><div class="wrap nav">
<a href="/index.html" class="nav-logo"><img src="{LOGO_GREEN}" alt="KEA — Kampala Executive Aviation"></a>
<nav><ul class="nav-links">
<li class="has-sub"><a href="/solutions/charter-flights.html"{cls('solutions')}>Solutions</a><div class="submenu">{sub}</div></li>
<li><a href="/fleet.html"{cls('fleet')}>Fleet</a></li>
<li><a href="/about.html"{cls('about')}>About</a></li>
<li><a href="/news.html"{cls('news')}>News</a></li>
<li><a href="/careers.html"{cls('careers')}>Careers</a></li>
<li><a href="/contact.html"{cls('contact')}>Contact</a></li>
</ul></nav>
<button class="burger" aria-label="Open menu"><span></span><span></span><span></span></button>
</div>
<div class="mobile-menu">
<a href="/solutions/charter-flights.html">Solutions</a><a href="/fleet.html">Fleet</a><a href="/about.html">About</a><a href="/news.html">News</a><a href="/careers.html">Careers</a><a href="/contact.html">Contact</a>
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
<div class="foot-col"><h4>Solutions</h4>{"".join('<a href="/solutions/%s.html">%s</a>'%(s,t) for s,t in SOL)}</div>
<div class="foot-col"><h4>Company</h4><a href="/fleet.html">Fleet</a><a href="/about.html">About</a><a href="/news.html">News</a><a href="/careers.html">Careers</a><a href="/contact.html">Contact</a>
<div class="foot-pay"><a class="btn btn-primary" style="padding:.7rem 1.2rem" href="{PAY}" target="_blank" rel="noopener">Make a Payment →</a></div></div>
</div>
<div class="foot-bottom"><span class="mono">© 2026 KEA — Kampala Executive Aviation</span><span class="mono">Specialist Aviation Solutions · Kajjansi, Uganda</span></div>
</div></footer>'''

def page(path, title, desc, body, active=""):
    doc=f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{nav(active)}
{body}
{FOOT}
<script>{JS}</script></body></html>'''
    full=os.path.join(ROOT,path)
    os.makedirs(os.path.dirname(full),exist_ok=True)
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

def banner(eyebrow,title,text,bg,btn=("Explore our capability","/solutions/charter-flights.html")):
    return f'''<div class="banner"><div class="bg" style="background-image:url('{bg}')"></div>
<div class="banner-inner reveal"><span class="eyebrow on-dark">{eyebrow}</span><h2>{title}</h2><p>{text}</p>
<a class="btn btn-primary" href="{btn[1]}">{btn[0]} <span class="arr">→</span></a></div></div>'''

IC=U+"2019/04/"; IC1=U+"2019/01/"; IC2=U+"2019/02/"
print("Generating KEA site...")

# ---------------- HOME ----------------
home_body=f'''
<section class="hero" id="top"><div class="fallback"></div>
<video autoplay muted loop playsinline poster="{U}2020/03/Helicopter-Services-In-Uganda-KEA.jpg"><source src="{VIDEO}" type="video/mp4"></video>
<div class="hero-inner"><span class="eyebrow on-dark">Global Specialist Aviation Solutions</span>
<h1>One Airline.<br>Endless Possibilities.</h1>
<p class="lead">A full spectrum of aviation-centric services for government and private clients in the most challenging and austere environments on earth.</p>
<div class="hero-actions"><a class="btn btn-primary" href="https://jietzbhvb7u.typeform.com/KEA-services" target="_blank" rel="noopener">Discover what we can do <span class="arr">→</span></a>
<a class="btn btn-ghost" href="/solutions/charter-flights.html">View our solutions</a></div></div>
<div class="scroll-hint"><span>Scroll</span><span class="line"></span></div></section>

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
<div class="sol-top"><div class="sec-head reveal"><span class="eyebrow">What we do</span><h2>Solutions built for austere environments</h2></div>
<a class="btn btn-outline reveal" href="/contact.html">Talk to our experts <span class="arr">→</span></a></div>
<div class="sol-grid">
<a class="sol-card reveal" href="/solutions/charter-flights.html"><img src="{IC1}Cargo-Charter.jpg" alt="Charter flights"><div class="sol-body"><div class="sol-num">01</div><h3>Charters</h3><p>Safe, fast and worry-free passenger and cargo travel across Africa’s open spaces.</p><span class="sol-more">Learn more →</span></div></a>
<a class="sol-card reveal" href="/solutions/helicopter-and-fixed-wing.html"><img src="{U}2020/03/Helicopter-Services-In-Uganda-KEA.jpg" alt="Rotary and fixed wing"><div class="sol-body"><div class="sol-num">02</div><h3>Rotary &amp; Fixed Wing</h3><p>Fully integrated helicopter and fixed-wing services with an accident-free record.</p><span class="sol-more">Learn more →</span></div></a>
<a class="sol-card reveal" href="/solutions/oil-gas-and-mining.html"><img src="{U}2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg" alt="Oil gas and mining"><div class="sol-body"><div class="sol-num">03</div><h3>Oil, Gas &amp; Mining</h3><p>The safety and quality standards demanded by industry operators, on call.</p><span class="sol-more">Learn more →</span></div></a>
<a class="sol-card reveal" href="/solutions/medical-division.html"><img src="{IC1}Medevac-KEA.jpg" alt="Medical division"><div class="sol-body"><div class="sol-num">04</div><h3>Medical Division</h3><p>24-hour NVG medical evacuation and air ambulance with a 100% safety record.</p><span class="sol-more">Learn more →</span></div></a>
<a class="sol-card reveal" href="/solutions/maintenance-and-hangarage.html"><img src="{U}2018/08/maintenance-hangarage.jpg" alt="Maintenance and hangarage"><div class="sol-body"><div class="sol-num">05</div><h3>Maintenance &amp; Hangarage</h3><p>Third-party maintenance through our Uganda and Iraqi licensed AMO.</p><span class="sol-more">Learn more →</span></div></a>
<a class="sol-card reveal" href="/solutions/aerial-and-geophysical-survey.html"><img src="{IC1}Aerial-Survey-KEA.jpg" alt="Aerial and geophysical survey"><div class="sol-body"><div class="sol-num">06</div><h3>Aerial &amp; Geophysical Survey</h3><p>Fast, accurate and actionable data — from LIDAR to wildlife census.</p><span class="sol-more">Learn more →</span></div></a>
</div></div></section>

{banner("On every mission","When the runway ends, we keep going.","From a stabilised patient at 8,000 feet to a rig crew on a flooded site, our aircraft and crews are built for the places others can’t reach.",IC1+"Medevac-KEA.jpg",("Explore our capability","/solutions/charter-flights.html"))}

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
<a class="btn btn-outline reveal" href="/news.html">View all news <span class="arr">→</span></a></div>
<div class="news-grid" id="latest-news"></div></div></section>

{banner("Have questions?","Our aviation experts are ready.","Tell us about your requirement and we’ll help find the solution best suited to your need.",U+"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg",("Contact us","/contact.html"))}
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
latest="".join(news_card(n) for n in NEWS[:3])
home_body=home_body.replace('<div class="news-grid" id="latest-news"></div>', '<div class="news-grid">%s</div>'%latest)
page("index.html","KEA — Global Specialist Aviation Solutions","A full spectrum of aviation-centric services for government and private clients in challenging and austere environments.",home_body,active="")

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
def gallery(eyebrow,title,imgs):
    cells="".join(f'<div class="g reveal"><img src="{U}{src}" alt="{alt}" loading="lazy"></div>' for src,alt in imgs)
    return f'''<section class="gallery-sec"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2></div><div class="gallery">{cells}</div></div></section>'''

SOLUTION_GALLERIES={
 "charter-flights":("In the field","Chartering across the region",[("2019/01/Cargo-Charter.jpg","Cargo charter loading"),("2019/04/Caravan-1.jpg","Cessna Caravan cabin"),("2019/02/Fleet-PC12.jpg","Pilatus PC-12"),("2020/03/Helicopter-Services-In-Uganda-KEA.jpg","Helicopter charter")]),
 "helicopter-and-fixed-wing":("In the field","Rotary and fixed wing in action",[("2019/01/External-Load-Work.jpg","External load work"),("2019/01/Helicopter-Rear-Door-Open.jpg","Helicopter cargo loading"),("2019/01/Medevac-KEA.jpg","Medevac operations"),("2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg","Mi-8 at Kajjansi")]),
 "medical-division":("In the field","Air ambulance and HEMS",[("2019/04/Air-ambulance-paramedics.jpg","Air ambulance paramedics"),("2019/12/Loading-Stretcher.jpg","Loading a stretcher"),("2019/12/Medevac-Caravan.jpg","Medevac Caravan"),("2019/12/Laughing-CityAmb.jpg","Ground ambulance crew")]),
 "aerial-and-geophysical-survey":("In the field","Survey operations",[("2015/07/ground-breaking-animal-census.jpg","Wildlife census survey"),("2019/01/Aerial-Survey-KEA.jpg","Aerial survey"),("2019/04/DA42-Camera.jpg","DA42 survey sensor"),("2019/04/DA42-Back.jpg","DA42 MPP Guardian")]),
 "oil-gas-and-mining":("In the field","Supporting industry operators",[("2015/02/News-Flying-For-Total.jpg","Flying for Total"),("2019/01/Oil-Gas-and-Mining.jpg","Oil and gas support"),("2014/06/baiji-iraq-oil-refinery.jpg","Baiji refinery extraction"),("2019/01/Passenger-and-Cargo-Transportation.jpg","Crew transportation")]),
 "maintenance-and-hangarage":("Our AMO","Maintenance and hangarage",[("2019/01/1900-Maintenance.jpg","Beechcraft 1900 maintenance"),("2019/01/1900-Maintenance2.jpg","Engine maintenance"),("2019/01/1900-Maintenance3.jpg","Airframe inspection"),("2018/08/maintenance-hangarage.jpg","Hangarage facility")]),
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
    if slug in SOLUTION_GALLERIES:
        eb,tt,imgs=SOLUTION_GALLERIES[slug]
        body+=gallery(eb,tt,imgs)
    body+=extra
    body+=cta_band()
    page("solutions/%s.html"%slug, "%s — KEA"%hero_title, hero_sub, body, active="solutions")

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
 ("Rotary Wing","Bell 412","1 / 2","13","360 NM","125 kt","2019/02/Fleet-B412.jpg"),
 ("Rotary Wing","Bell 206 Jet Ranger","1","4","300 NM","100 kt","2019/02/Fleet-B206.jpg"),
 ("Fixed Wing","Pilatus PC-12","1 / 2","8","1600 NM","250 kt","2019/02/Fleet-PC12.jpg"),
 ("Fixed Wing","Beechcraft 1900D","2","19","1200 NM","285 kt","2019/02/Fleet-B1900.jpg"),
 ("Fixed Wing","Cessna Caravan C208B","1 / 2","13","900 NM","145 kt","2019/02/Fleet-C208B.jpg"),
 ("Fixed Wing","Cessna 210","1","5","700 NM","145 kt","2019/02/Fleet-C210.jpg"),
 ("Special Mission","Diamond DA42 MPP Guardian","1 + 1 sensor","2","1050 NM","125 kt","2019/02/Fleet-Diamond.jpg"),
]
def ac_card(cat,name,crew,pax,rng,spd,img):
    return f'''<div class="ac reveal"><div class="ph"><img src="{U}{img}" alt="{name}" loading="lazy"></div><div class="ac-body"><div class="type">{cat}</div><h3>{name}</h3>
<div class="specs"><div class="s"><div class="v">{crew}</div><div class="k">Crew</div></div>
<div class="s"><div class="v">{pax}</div><div class="k">Passengers</div></div>
<div class="s"><div class="v">{rng}</div><div class="k">Range</div></div>
<div class="s"><div class="v">{spd}</div><div class="k">Cruise</div></div></div></div></div>'''
fleet_cards="".join(ac_card(*a) for a in FLEET)
fleet_body=f'''{page_hero("Uganda’s largest privately owned fleet","Our Fleet","A versatile fixed and rotary wing capability lets us tailor a solution to each client’s unique need.",U+"2020/03/Helicopter-Services-In-Uganda-KEA.jpg")}
<section><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Aircraft</span><h2>Fixed wing, rotary wing and special mission</h2></div>
<div class="fleet-grid">{fleet_cards}</div></div></section>
{gallery("Inside the fleet","Cabins, cockpits and configurations",[("2019/04/B1900_Interior.jpg","Beechcraft 1900D cabin"),("2019/04/B412_Interior.jpg","Bell 412 cabin"),("2019/04/PC12-Interior.jpg","Pilatus PC-12 cabin"),("2019/04/C208B-Interior.jpg","Caravan cabin"),("2019/04/B1900_Cockpit.jpg","Beechcraft 1900D cockpit"),("2019/04/DA42-Cockpit.jpg","DA42 survey cockpit")])}
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
<a class="btn btn-outline" href="/solutions/charter-flights.html">Our solutions <span class="arr">→</span></a></div></div>
<div class="panel fleet-teaser"><div class="inner reveal"><span class="eyebrow">Safety &amp; Quality</span><h2 style="margin:1rem 0">Safety is everything</h2>
<p>We currently hold an accident-free track record, achieved through an increased focus on safety and quality across all spheres of our service. We are the only aviation company in Uganda to have qualified to fly for Total plc, following an intense audit by Total Oil and Gas and Bureau Veritas.</p>
<a class="btn btn-primary" href="{U}2020/04/KEA-Safety-Policy2020-Screen.pdf" target="_blank" rel="noopener">Read our Safety Policy <span class="arr">→</span></a></div></div></div>
<div class="stats" style="padding-top:110px"><div class="wrap"><div class="stats-grid reveal">
<div class="stat"><div class="num" data-target="4000" data-suffix="T">0<span>T</span></div><div class="lbl">Cargo Carried</div></div>
<div class="stat"><div class="num" data-target="40000">0</div><div class="lbl">Passengers Flown</div></div>
<div class="stat"><div class="num" data-target="7800">0</div><div class="lbl">Flights Conducted</div></div>
<div class="stat"><div class="num" data-target="13">0</div><div class="lbl">Countries Worked In</div></div>
</div></div></div>
{gallery("Our people and operations","The team behind every mission",[("2019/02/Our-People.jpg","The KEA team"),("2021/08/Kajjansi_KEA.jpg","Kajjansi base"),("2021/08/Pilots-in-B412-Cockpit.jpg","Flight crew"),("2019/04/Safety-and-Quality.jpg","Safety and quality"),("2020/03/Carousel-1.jpg","Operations"),("2020/03/Carousel-3.jpg","In the field")])}
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
page("thank-you.html","Thank you — KEA","Your message has been received by Kampala Executive Aviation.",thanks_body,active="")

print("DONE. Pages generated.")
