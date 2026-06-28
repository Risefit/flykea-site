# -*- coding: utf-8 -*-
"""KEA per-page SEO + content data model. Pure data — rendered by build.py.
Image paths are relative to assets/img/. Copy is v1 (meets on-page SEO spec; expandable)."""

PHONE = "+256 776 333 114"

# ---- Countries we serve (12 confirmed; 13th pending KEA confirmation) ----
COUNTRIES = [
 ("\U0001F1FA\U0001F1EC","Uganda"), ("\U0001F1F0\U0001F1EA","Kenya"),
 ("\U0001F1F8\U0001F1F8","South Sudan"), ("\U0001F1E8\U0001F1E9","DR Congo"),
 ("\U0001F1F3\U0001F1EC","Nigeria"), ("\U0001F1F3\U0001F1EA","Niger"),
 ("\U0001F1F9\U0001F1E9","Chad"), ("\U0001F1E8\U0001F1F2","Cameroon"),
 ("\U0001F1E8\U0001F1EB","Central African Republic"), ("\U0001F1F8\U0001F1F4","Somalia"),
 ("\U0001F1FF\U0001F1E6","South Africa"), ("\U0001F1EE\U0001F1F6","Iraq"),
 ("\U0001F1EE\U0001F1F6","Kurdistan"),
]
# <!-- COUNTRIES: 12 confirmed; confirm the 13th with KEA before publishing -->

# ---- Client / trust strip (confirmed by KEA; supply official logo files for production) ----
CLIENTS = ["TotalEnergies","MSF","United Nations","CNOOC","US DLA","DynCorp","Fluor","Peace Corps"]

# ---- Certifications (confirmed) ----
CERTS = [
 ("AOC","Air Operator Certificates","Uganda <b>AOC&nbsp;097</b>, with additional AOCs held in Chad and South Sudan for cross-border operations."),
 ("AMO","Approved Maintenance Organisation","AMO approvals across Uganda, South Africa, Chad, Central African Republic and Iraq."),
 ("UOC","UAV Operating Certificate","Ugandan CAA Unmanned Aerial Vehicle Operating Certificate (UOC) for drone survey and inspection."),
]

# ============================ SERVICE PAGES ============================
# dict keys: slug,kw,title,desc,h1,eyebrow,stype,hero,og,lead,secs[(h2,html)],faqs[(q,a)],
#            related[(label,slug)], gallery[rel imgs]
SERVICES = [
{
 "slug":"services/oil-gas-aviation","kw":"oil and gas charter flights Uganda",
 "title":"Oil & Gas Charter Flights Uganda | KEA Aviation",
 "desc":"Oil & gas charter flights in Uganda — crew rotation, cargo and medevac for energy operators from Kajjansi Airfield, Kampala. Call KEA +256 776 333 114.",
 "h1":"Oil & Gas Charter Flights in Uganda","eyebrow":"Industrial B2B","stype":"Oil and gas aviation support",
 "hero":"2019/01/Oil-Gas-and-Mining.jpg","og":"2019/01/Oil-Gas-and-Mining.jpg",
 "lead":"KEA provides <b>oil and gas charter flights in Uganda</b> and across the region from our base at <b>Kajjansi Airfield, Kampala</b> — moving crews, equipment and time-critical cargo to fields, exploration camps and remote sites.",
 "secs":[
  ("Built for energy-sector operations","<p>Fixed-wing and rotary-wing aircraft handle crew rotation, supply runs, seismic support and casualty evacuation standby. We operate routinely into unprepared strips and remote camps, and hold AOCs in Uganda (AOC 097), Chad and South Sudan for seamless cross-border tasking.</p>"),
  ("One accountable operator","<p>From a single charter to a multi-year rotation, KEA plans, crews and maintains the operation in-house through our own Approved Maintenance Organisation, backed by a 24/7 operations desk. Trusted by energy and service operators including TotalEnergies, CNOOC and Fluor.</p>"),
 ],
 "faqs":[
  ("Do you fly to remote oil & gas sites?","Yes. We operate to bush airstrips, exploration camps and remote sites across Uganda, DRC, South Sudan and the wider region, including short and unprepared strips."),
  ("Can you provide medevac standby on contract?","Yes — dedicated air-ambulance standby and casualty evacuation cover for site operations, available 24/7."),
  ("Are you licensed for cross-border charter?","KEA holds Uganda AOC 097 plus AOCs in Chad and South Sudan, with AMO approvals across five countries."),
 ],
 "related":[("Remote Site Operations","services/remote-site-operations"),("Cargo Charter","services/cargo-charter"),("Medical Evacuation","services/medical-evacuation")],
 "gallery":["2019/01/Oil-Gas-and-Mining.jpg","2019/12/Oil-and-Gas-DAR-Post.jpg","2019/01/Passenger-and-Cargo-Transportation.jpg","2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg"],
},
{
 "slug":"services/medical-evacuation","kw":"medical evacuation flights Uganda",
 "title":"Medical Evacuation Flights Uganda | KEA Aviation",
 "desc":"Medical evacuation and air ambulance flights in Uganda and East Africa — fixed-wing and helicopter, 24/7, from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"Medical Evacuation Flights in Uganda","eyebrow":"Emergency","stype":"Air ambulance and medical evacuation",
 "hero":"2019/01/Medevac-KEA.jpg","og":"2019/01/Medevac-KEA.jpg",
 "lead":"KEA flies <b>medical evacuation flights in Uganda</b> and across East Africa, 24/7, from <b>Kajjansi Airfield, Kampala</b> — rapid fixed-wing and helicopter air ambulance for patients, casualties and remote-site emergencies.",
 "secs":[
  ("Air ambulance, ready around the clock","<p>Our aircraft can be configured for stretcher patients with accompanying medical crew, and we coordinate with hospitals, insurers and assistance companies to move patients quickly and safely. Helicopter HEMS reaches sites that fixed-wing cannot.</p>"),
  ("Cover for remote operations","<p>For oil, gas, mining and NGO sites, KEA provides contracted medevac standby so a casualty is never far from definitive care. Tasking runs through a 24/7 operations desk with crews on call.</p>"),
 ],
 "faqs":[
  ("Is KEA medevac available 24/7?","Yes. Emergency medical flights can be activated around the clock — call +256 776 333 114."),
  ("Do you carry medical crew and equipment?","Aircraft are configured for stretcher transport with accompanying medical personnel and equipment as the mission requires."),
  ("Can you evacuate from remote sites?","Yes — helicopter and short-field fixed-wing let us reach remote camps and airstrips across the region."),
 ],
 "related":[("Search & Rescue Helicopter","services/search-rescue-helicopter"),("Oil & Gas Aviation","services/oil-gas-aviation"),("Helicopter Charter Kampala","helicopter-charter-kampala")],
 "gallery":["2019/01/Medevac-KEA.jpg","2019/04/Air-ambulance-paramedics.jpg","2019/12/Loading-Stretcher-1.jpg","2019/12/Medevac-Crews-Caravan.jpg"],
},
{
 "slug":"helicopter-charter-kampala","kw":"helicopter charter Kampala Uganda",
 "title":"Helicopter Charter Kampala Uganda | KEA Aviation",
 "desc":"Helicopter charter in Kampala, Uganda — hire a Bell 412 or 206 for charter, survey and external load from Kajjansi Airfield. Call KEA +256 776 333 114.",
 "h1":"Helicopter Charter in Kampala, Uganda","eyebrow":"Charter","stype":"Helicopter charter",
 "hero":"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg","og":"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg",
 "lead":"Charter a helicopter in Kampala with KEA from <b>Kajjansi Airfield</b>. <b>Helicopter charter in Kampala, Uganda</b> for passenger transfers, survey, external-load and remote-site access — Bell 412, Bell 206 and heavy-lift options.",
 "secs":[
  ("The right rotor for the task","<p>Our Bell 412 carries up to 13 in comfort or lifts underslung loads; the Bell 206 suits light tasks and recce; and heavy-lift Mi-8 capacity supports the largest projects. Crews are experienced in mountain, lake and remote-site operations.</p>"),
  ("Point-to-point across the region","<p>Skip road transfers and reach sites directly — national parks, camps, rigs and project sites across Uganda and neighbouring countries. We handle permits and planning end to end.</p>"),
 ],
 "faqs":[
  ("Which helicopters can I charter?","Bell 412 (up to 13 pax), Bell 206 for light tasks, and heavy-lift Mi-8 capacity for large loads."),
  ("Do you fly external / underslung loads?","Yes — see our external load helicopter service for construction, energy and remote-project lifts."),
  ("Where do helicopter charters depart from?","Our base is Kajjansi Airfield, Kampala, with repositioning across Uganda and the region."),
 ],
 "related":[("External Load Helicopter","services/external-load-helicopter"),("Aerial Survey","services/aerial-survey-geophysical"),("VIP & Corporate Charter","services/vip-corporate-charter")],
 "gallery":["2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg","2019/01/External-Load-Work.jpg","2021/08/B412-Flying-with-Lake-and-Rocky-Scenery.jpg","2019/01/Helicopter-Rear-Door-Open.jpg"],
},
{
 "slug":"services/ngo-humanitarian-charter","kw":"NGO charter flights Uganda",
 "title":"NGO & Humanitarian Charter Uganda | KEA Aviation",
 "desc":"NGO and humanitarian charter flights in Uganda, DRC and South Sudan — relief passengers, cargo and medevac from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"NGO & Humanitarian Charter Flights in Uganda","eyebrow":"Industrial B2B","stype":"Humanitarian and NGO air charter",
 "hero":"2019/04/Air-ambulance-paramedics.jpg","og":"2019/04/Air-ambulance-paramedics.jpg",
 "lead":"KEA is a trusted partner for <b>NGO charter flights in Uganda</b> and <b>humanitarian air services</b> across the region, flown from <b>Kajjansi Airfield, Kampala</b> — moving relief teams, supplies and patients into hard-to-reach locations.",
 "secs":[
  ("Reliable lift for relief operations","<p>We support UN agencies and international NGOs including MSF with passenger and cargo rotations, field-hospital resupply and medevac. Our Cessna Caravan fleet is ideal for short, rough strips, while larger aircraft handle bulk loads.</p>"),
  ("Cross-border and remote reach","<p>With AOCs in Uganda, Chad and South Sudan and long experience in the DRC, KEA reaches deployment sites where scheduled services don't fly — dependable, compliant and safety-led.</p>"),
 ],
 "faqs":[
  ("Do you work with UN agencies and NGOs?","Yes — KEA flies for UN agencies and NGOs including MSF and the WFP, on both ad-hoc and long-term contracts."),
  ("Can you fly relief cargo and passengers together?","Yes, subject to load and safety limits; we tailor each rotation to the mission."),
  ("Which countries do you serve for humanitarian work?","Uganda, DRC, South Sudan, Chad and the wider region — see Countries We Serve."),
 ],
 "related":[("Charter Flights to DRC","services/charter-flights-drc"),("Charter Flights to South Sudan","services/charter-flights-south-sudan"),("Cargo Charter","services/cargo-charter")],
 "gallery":["2019/04/Air-ambulance-paramedics.jpg","2021/08/Caravan-in-Kidepo.jpg","2019/12/Medevac-Crews-Caravan.jpg"],
},
{
 "slug":"services/aerial-survey-geophysical","kw":"aerial survey Uganda East Africa",
 "title":"Aerial Survey Uganda & East Africa | KEA Aviation",
 "desc":"Aerial survey and geophysical flights across Uganda and East Africa with sensor-equipped aircraft from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"Aerial Survey & Geophysical Flights in Uganda","eyebrow":"Specialist Ops","stype":"Aerial survey and geophysical operations",
 "hero":"2019/01/Aerial-Survey-KEA.jpg","og":"2019/01/Aerial-Survey-KEA.jpg",
 "lead":"KEA flies <b>aerial survey in Uganda and East Africa</b> from <b>Kajjansi Airfield, Kampala</b> — airborne geophysical surveys, mapping and wildlife census with stable, sensor-equipped platforms including the DA42 Guardian.",
 "secs":[
  ("Stable platforms, precise lines","<p>Our special-mission DA42 and survey-configured fleet fly long, accurate survey lines for magnetic, radiometric and photographic work, supporting mining, exploration and conservation clients across the region.</p>"),
  ("From the air to the data","<p>We coordinate with your survey team on sensor integration, line planning and base-of-operations logistics, and can combine fixed-wing survey with UAV LiDAR and orthophoto capture for finer detail.</p>"),
 ],
 "faqs":[
  ("What survey work can KEA support?","Geophysical (magnetic/radiometric) survey, aerial photography/mapping and wildlife census, plus UAV LiDAR and orthophoto."),
  ("Can you mobilise to a remote survey base?","Yes — we routinely operate from remote bases across Uganda and East Africa."),
  ("Do you offer drone survey too?","Yes — see our UAV operations service for LiDAR and orthophoto mapping."),
 ],
 "related":[("UAV / Drone Operations","services/uav-drone-operations"),("Pipeline Patrol","services/pipeline-patrol"),("Oil & Gas Aviation","services/oil-gas-aviation")],
 "gallery":["2019/01/Aerial-Survey-KEA.jpg","2019/04/DA42-Camera.jpg","2019/04/DA42-Back.jpg","2015/07/ground-breaking-animal-census.jpg"],
},
{
 "slug":"services/remote-site-operations","kw":"remote site aviation Uganda Africa",
 "title":"Remote Site Aviation Uganda | KEA Aviation",
 "desc":"Remote site and bush airstrip aviation for mining, energy and NGO operations across Uganda and Africa from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"Remote Site Aviation Support in Uganda & Africa","eyebrow":"Industrial B2B","stype":"Remote site aviation support",
 "hero":"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg","og":"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg",
 "lead":"KEA delivers <b>remote site aviation in Uganda and across Africa</b> from <b>Kajjansi Airfield, Kampala</b> — connecting bush airstrips, camps and project sites that scheduled airlines never reach.",
 "secs":[
  ("Aircraft built for austere strips","<p>Our Cessna Caravans and rotary fleet operate from short, unprepared surfaces, while heavy-lift capacity handles outsized loads. We plan fuel, permits and ground handling for the most isolated locations.</p>"),
  ("End-to-end project support","<p>From crew change cycles to resupply and medevac standby, KEA runs the air bridge for mining, energy and humanitarian projects — one operator, fully accountable, 24/7.</p>"),
 ],
 "faqs":[
  ("Can you operate from unprepared airstrips?","Yes — short and unprepared strips are routine for our Caravan and rotary fleet."),
  ("Do you handle fuel and permits at remote sites?","Yes, we plan fuel, overflight/landing permits and ground handling as part of the service."),
  ("Can you combine resupply with medevac standby?","Yes — many site contracts bundle scheduled rotations with on-call medevac."),
 ],
 "related":[("Oil & Gas Aviation","services/oil-gas-aviation"),("NGO & Humanitarian Charter","services/ngo-humanitarian-charter"),("Cargo Charter","services/cargo-charter")],
 "gallery":["2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg","2021/08/Caravan-in-Kidepo.jpg","2021/08/Kajjansi_KEA.jpg"],
},
{
 "slug":"services/aircraft-leasing","kw":"wet lease dry lease ACMI aircraft Uganda",
 "title":"Aircraft Leasing & ACMI Uganda | KEA Aviation",
 "desc":"Wet lease, dry lease and ACMI aircraft from a CAA-licensed Uganda operator — fixed and rotary wing from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"Aircraft Leasing, Wet Lease & ACMI in Uganda","eyebrow":"Leasing","stype":"Aircraft leasing and ACMI",
 "hero":"2019/02/Fleet-B1900.jpg","og":"2019/02/Fleet-B1900.jpg",
 "lead":"KEA offers <b>wet lease, dry lease and ACMI aircraft in Uganda</b> from <b>Kajjansi Airfield, Kampala</b> — putting CAA-licensed capacity and crews to work for operators, governments and projects across Africa.",
 "secs":[
  ("ACMI, wet and dry lease","<p>Take aircraft, crew, maintenance and insurance (ACMI/wet lease) for turnkey capacity, or dry-lease airframes into your own AOC. Fixed-wing and rotary options are available for short-term surges or long-term programmes.</p>"),
  ("A licensed regional partner","<p>With AOCs in Uganda, Chad and South Sudan and AMO approvals across five countries, KEA is a credible lease partner that keeps your operation compliant and flying.</p>"),
 ],
 "faqs":[
  ("What is the difference between wet, dry and ACMI lease?","Wet/ACMI includes Aircraft, Crew, Maintenance and Insurance; dry lease provides the airframe only into your AOC."),
  ("What aircraft can KEA lease out?","Fixed-wing (Caravan, 1900D, PC-12) and rotary-wing, subject to availability."),
  ("Do you support cross-border lease operations?","Yes — our multi-country AOC and AMO footprint supports regional operations."),
 ],
 "related":[("Aircraft Maintenance & MRO","services/aircraft-maintenance-mro"),("Cargo Charter","services/cargo-charter"),("Fleet","fleet.html")],
 "gallery":["2019/02/Fleet-B1900.jpg","2019/02/Fleet-PC12.jpg","2019/02/Fleet-C208B.jpg"],
},
{
 "slug":"services/pipeline-patrol","kw":"pipeline patrol aviation Uganda",
 "title":"Pipeline Patrol Aviation Uganda | KEA Aviation",
 "desc":"Aerial pipeline patrol and powerline inspection for energy operators across Uganda from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"Pipeline Patrol & Aerial Inspection in Uganda","eyebrow":"Specialist Ops","stype":"Pipeline patrol and aerial inspection",
 "hero":"2019/01/Aerial-Survey-KEA.jpg","og":"2019/01/Aerial-Survey-KEA.jpg",
 "lead":"KEA flies <b>pipeline patrol aviation in Uganda</b> from <b>Kajjansi Airfield, Kampala</b> — routine aerial inspection of pipelines, powerlines and right-of-way corridors for energy and infrastructure operators.",
 "secs":[
  ("Eyes along the line","<p>Fixed-wing, helicopter and UAV patrols detect encroachment, leaks, third-party interference and ROW issues early, with imagery and data delivered to your team for action.</p>"),
  ("Scheduled or on demand","<p>Set up a recurring patrol programme or call us for ad-hoc inspections after an event. We combine crewed aircraft with Matrice 400 UAV capture for close-up detail.</p>"),
 ],
 "faqs":[
  ("What can aerial pipeline patrol detect?","Encroachment, leaks, third-party interference, ROW vegetation and access issues."),
  ("Do you use drones for inspection?","Yes — our UAV operations add high-resolution LiDAR and imagery to crewed patrols."),
  ("Can patrols be scheduled regularly?","Yes — recurring programmes or on-demand inspections are both available."),
 ],
 "related":[("UAV / Drone Operations","services/uav-drone-operations"),("Aerial Survey","services/aerial-survey-geophysical"),("Oil & Gas Aviation","services/oil-gas-aviation")],
 "gallery":[],
},
{
 "slug":"services/search-rescue-helicopter","kw":"search and rescue helicopter Uganda",
 "title":"Search & Rescue Helicopter Uganda | KEA Aviation",
 "desc":"Helicopter search and rescue and casualty evacuation support across Uganda and East Africa from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"Search & Rescue Helicopter Services in Uganda","eyebrow":"Emergency","stype":"Search and rescue helicopter",
 "hero":"2019/01/Medevac-KEA.jpg","og":"2019/01/Medevac-KEA.jpg",
 "lead":"KEA provides <b>search and rescue helicopter</b> and casualty-evacuation support in Uganda and East Africa from <b>Kajjansi Airfield, Kampala</b> — rapid rotary-wing response for projects and operations in remote terrain.",
 "secs":[
  ("Rotary response where it counts","<p>Helicopters reach incident sites that ground teams and fixed-wing cannot, lifting casualties directly to medical care. Crews are experienced in mountain, lake and bush operations.</p>"),
  ("Contracted SAR & medevac cover","<p>For energy, mining and event clients, KEA can provide standby SAR and medevac cover with defined response times, coordinated through a 24/7 operations desk.</p>"),
 ],
 "faqs":[
  ("Can KEA provide standby SAR cover?","Yes — contracted standby with defined response times for site and event operations."),
  ("Which aircraft are used for SAR?","Bell 412 and heavy-lift rotary capacity, configured for the mission."),
  ("Is the service available 24/7?","Yes — activate via +256 776 333 114."),
 ],
 "related":[("Medical Evacuation","services/medical-evacuation"),("Helicopter Charter Kampala","helicopter-charter-kampala"),("Disaster Response","services/disaster-response")],
 "gallery":[],
},
{
 "slug":"services/external-load-helicopter","kw":"underslung load helicopter Uganda",
 "title":"Underslung Load Helicopter Uganda | KEA Aviation",
 "desc":"Helicopter external and underslung load lift for construction, energy and remote projects across Uganda and Africa from Kajjansi. Call KEA +256 776 333 114.",
 "h1":"Underslung & External Load Helicopter in Uganda","eyebrow":"Specialist Ops","stype":"External load helicopter operations",
 "hero":"2019/01/External-Load-Work.jpg","og":"2019/01/External-Load-Work.jpg",
 "lead":"KEA flies <b>underslung load helicopter operations in Uganda</b> from <b>Kajjansi Airfield, Kampala</b> — precision external-load lifts for construction, energy, telecoms and remote projects.",
 "secs":[
  ("Precision lifting, anywhere","<p>Our Bell 412 and heavy-lift capacity place equipment, materials, towers and supplies exactly where roads can't reach — on ridgelines, islands, rigs and project sites.</p>"),
  ("Planned and flown safely","<p>Every lift is planned for load, weather and terrain by experienced crews, with rigging and ground-team coordination built into the operation.</p>"),
 ],
 "faqs":[
  ("What loads can you lift externally?","Equipment, building materials, tower sections and supplies within the aircraft's certified limits."),
  ("Where can you deliver underslung loads?","Remote ridgelines, islands, rigs and sites unreachable by road across the region."),
  ("Which helicopter is used?","Primarily the Bell 412, with heavy-lift capacity for larger loads."),
 ],
 "related":[("Helicopter Charter Kampala","helicopter-charter-kampala"),("Remote Site Operations","services/remote-site-operations"),("Oil & Gas Aviation","services/oil-gas-aviation")],
 "gallery":["2019/01/External-Load-Work.jpg","2019/01/Helicopter-Rear-Door-Open.jpg"],
},
{
 "slug":"services/disaster-response","kw":"disaster response aviation Uganda",
 "title":"Disaster Response Aviation Uganda | KEA Aviation",
 "desc":"Rapid airlift, relief cargo and aerial support for disaster response across Uganda and the region, mobilised from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"Disaster Response Aviation in Uganda","eyebrow":"Specialist Ops","stype":"Disaster response aviation",
 "hero":"2021/03/PHOTO-2021-02-23-13-56-15.jpg","og":"2021/03/PHOTO-2021-02-23-13-56-15.jpg",
 "lead":"KEA provides <b>disaster response aviation in Uganda</b> and the region from <b>Kajjansi Airfield, Kampala</b> — rapid airlift of responders and relief cargo, aerial assessment and casualty evacuation when time matters.",
 "secs":[
  ("Mobilise fast","<p>Fixed-wing, rotary and UAV assets deploy quickly to move teams and supplies, survey affected areas from the air and evacuate casualties — supporting government and humanitarian responders.</p>"),
  ("Coordinated relief lift","<p>We work alongside UN agencies and NGOs to sustain the air bridge into affected zones, including remote and cross-border locations across Uganda, DRC and South Sudan.</p>"),
 ],
 "faqs":[
  ("How quickly can KEA mobilise?","Assets can be tasked rapidly through our 24/7 operations desk — call +256 776 333 114."),
  ("Can you provide aerial assessment?","Yes — crewed aircraft and UAVs provide rapid aerial imagery of affected areas."),
  ("Do you support NGO/UN relief operations?","Yes — we regularly fly for UN agencies and NGOs in the region."),
 ],
 "related":[("NGO & Humanitarian Charter","services/ngo-humanitarian-charter"),("Medical Evacuation","services/medical-evacuation"),("UAV / Drone Operations","services/uav-drone-operations")],
 "gallery":[],
},
{
 "slug":"charter-flights-kampala","kw":"charter flight Kampala same day",
 "title":"Charter Flights Kampala — Same Day | KEA Aviation",
 "desc":"Same-day private charter flights from Kampala across Uganda and Africa — fixed wing and helicopter from Kajjansi Airfield. Call KEA +256 776 333 114.",
 "h1":"Charter Flights in Kampala — Same-Day Available","eyebrow":"Charter","stype":"Private charter flights",
 "hero":"2020/03/Helicopter-Services-In-Uganda-KEA.jpg","og":"2020/03/Helicopter-Services-In-Uganda-KEA.jpg",
 "lead":"Need to fly today? KEA arranges <b>same-day charter flights from Kampala</b> at <b>Kajjansi Airfield</b> — private fixed-wing and helicopter charter across Uganda, East Africa and beyond, on your schedule.",
 "secs":[
  ("Fly on your timetable","<p>Charter removes the wait. Tell us the route, dates and passenger or cargo load and we'll match the right aircraft — from a light Cessna 210 to a 19-seat Beechcraft 1900D or a helicopter for direct site access.</p>"),
  ("One call, fully handled","<p>Permits, planning and handling are taken care of by our operations desk. For urgent requests, call us directly and we'll move quickly.</p>"),
 ],
 "faqs":[
  ("Can KEA arrange a same-day charter?","Often yes, subject to aircraft and crew availability — call +256 776 333 114 for the fastest answer."),
  ("Where do charters depart from?","Kajjansi Airfield, Kampala, with pickups arranged regionally."),
  ("What size groups can you carry?","From one passenger to 19 on the Beechcraft 1900D, plus cargo configurations."),
 ],
 "related":[("Helicopter Charter Kampala","helicopter-charter-kampala"),("VIP & Corporate Charter","services/vip-corporate-charter"),("Cargo Charter","services/cargo-charter")],
 "gallery":["2020/03/Helicopter-Services-In-Uganda-KEA.jpg","2019/04/Caravan-1.jpg","2019/02/Fleet-PC12.jpg","2019/01/Cargo-Charter.jpg"],
},
{
 "slug":"services/cargo-charter","kw":"cargo charter flights Uganda Africa",
 "title":"Cargo Charter Flights Uganda & Africa | KEA Aviation",
 "desc":"Air freight and cargo charter across Uganda, DRC and Africa — outsized and time-critical loads from Kajjansi, Kampala. Call KEA +256 776 333 114.",
 "h1":"Cargo Charter Flights in Uganda & Africa","eyebrow":"Cargo","stype":"Cargo and freight charter",
 "hero":"2019/01/Cargo-Charter.jpg","og":"2019/01/Cargo-Charter.jpg",
 "lead":"KEA flies <b>cargo charter flights across Uganda and Africa</b> from <b>Kajjansi Airfield, Kampala</b> — time-critical, outsized and project cargo delivered to main airports and remote strips alike.",
 "secs":[
  ("Freight that has to arrive","<p>From urgent spares to project equipment and relief supplies, our Caravan and larger aircraft carry cargo where and when it's needed, including bush strips and cross-border destinations.</p>"),
  ("Projects and relief","<p>We support energy, mining and humanitarian logistics with dedicated cargo rotations, working alongside agencies including the WFP and MSF.</p>"),
 ],
 "faqs":[
  ("What cargo can you carry?","Time-critical spares, project equipment, perishables and relief supplies within aircraft limits."),
  ("Can you deliver to remote strips?","Yes — our short-field fleet reaches sites that scheduled cargo can't."),
  ("Do you fly cross-border cargo?","Yes — across Uganda, DRC, South Sudan, Chad and the region."),
 ],
 "related":[("Oil & Gas Aviation","services/oil-gas-aviation"),("NGO & Humanitarian Charter","services/ngo-humanitarian-charter"),("Remote Site Operations","services/remote-site-operations")],
 "gallery":["2019/01/Cargo-Charter.jpg","2019/01/Passenger-and-Cargo-Transportation.jpg"],
},
{
 "slug":"services/vip-corporate-charter","kw":"VIP charter Kampala executive flight",
 "title":"VIP & Corporate Charter Kampala | KEA Aviation",
 "desc":"Discreet VIP and executive charter from Kampala for corporate and government travel across Africa, from Kajjansi Airfield. Call KEA +256 776 333 114.",
 "h1":"VIP & Corporate Charter Flights in Kampala","eyebrow":"VIP / Corporate","stype":"VIP and corporate charter",
 "hero":"2019/02/Fleet-PC12.jpg","og":"2019/02/Fleet-PC12.jpg",
 "lead":"KEA flies <b>VIP and corporate charter from Kampala</b> at <b>Kajjansi Airfield</b> — discreet, comfortable executive travel for business and government across Uganda and Africa.",
 "secs":[
  ("Executive comfort, regional reach","<p>The pressurised Pilatus PC-12 and Beechcraft 1900D combine speed and comfort for executive teams, while helicopters add direct site and lodge access. Schedules flex to your day, not an airline's.</p>"),
  ("Confidential and seamless","<p>From ramp-side arrival to onward transfers, we handle the detail discreetly, with the safety and compliance of a CAA-licensed operator.</p>"),
 ],
 "faqs":[
  ("Which aircraft are used for VIP charter?","Pilatus PC-12 and Beechcraft 1900D for fixed-wing, plus helicopters for direct access; jets on request."),
  ("Can you arrange ground transfers?","Yes — door-to-aircraft and onward transfers are arranged as part of the service."),
  ("Do you fly across Africa?","Yes — corporate and government travel region-wide, supported by multi-country AOCs."),
 ],
 "related":[("Private Jet Charter","services/private-jet-charter"),("Charter Flights Kampala","charter-flights-kampala"),("Helicopter Charter Kampala","helicopter-charter-kampala")],
 "gallery":["2019/02/Fleet-PC12.jpg","2019/04/PC12-Interior.jpg"],
},
{
 "slug":"services/private-jet-charter","kw":"private jet charter Uganda Kampala",
 "title":"Private Jet Charter Uganda & Kampala | KEA Aviation",
 "desc":"Private jet and executive charter from Kampala across Africa, arranged by a CAA-licensed operator at Kajjansi Airfield. Call KEA +256 776 333 114.",
 "h1":"Private Jet & Executive Charter in Uganda","eyebrow":"VIP / Corporate","stype":"Private jet charter",
 "hero":"2019/02/Fleet-PC12.jpg","og":"2019/02/Fleet-PC12.jpg",
 "lead":"KEA arranges <b>private jet charter in Uganda</b> and <b>Kampala</b> from <b>Kajjansi Airfield</b> — executive jet and turboprop travel across Africa, planned and flown to the standards of a CAA-licensed operator.",
 "secs":[
  ("The right executive aircraft","<p>For longer or faster sectors we source the appropriate private jet; for regional trips our pressurised PC-12 and 1900D offer jet-like comfort with the flexibility to use shorter strips.</p>"),
  ("A trusted regional operator","<p>With its own AOCs, AMO and 24/7 operations desk, KEA delivers private aviation that is discreet, compliant and reliable across the continent.</p>"),
 ],
 "faqs":[
  ("Does KEA offer private jet charter?","Yes — we arrange private jets for executive and government travel, alongside our executive turboprop fleet."),
  ("What's the difference vs corporate charter?","Private jet charter prioritises speed and range; our PC-12/1900D suit regional and short-strip trips."),
  ("How do I get a quote?","Call +256 776 333 114 or use the quote form with your route and dates."),
 ],
 "related":[("VIP & Corporate Charter","services/vip-corporate-charter"),("Charter Flights Kampala","charter-flights-kampala"),("Fleet","fleet.html")],
 "gallery":["2019/02/Fleet-PC12.jpg","2019/04/PC12-Interior.jpg"],
},
{
 "slug":"services/charter-flights-drc","kw":"charter flights DRC from Kampala",
 "title":"Charter Flights to DRC from Kampala | KEA Aviation",
 "desc":"Private charter from Kampala into the DRC — passengers and cargo to Kinshasa, Goma and remote sites from Kajjansi Airfield. Call KEA +256 776 333 114.",
 "h1":"Charter Flights to DRC from Kampala","eyebrow":"Cross-border","stype":"Cross-border charter to DRC",
 "hero":"2021/03/PHOTO-2021-02-23-13-56-15.jpg","og":"2021/03/PHOTO-2021-02-23-13-56-15.jpg",
 "lead":"KEA flies <b>charter flights to the DRC from Kampala</b> and <b>Kajjansi Airfield</b> — passengers and cargo to Bunia, Goma, Kinshasa and remote eastern-DRC sites, with deep regional experience.",
 "secs":[
  ("Experienced in the DRC","<p>KEA has long supported operations in the DRC, including humanitarian flying for MSF in Bunia. We know the airfields, the permits and the conditions, and plan accordingly.</p>"),
  ("Passengers and cargo","<p>From corporate and NGO passenger rotations to relief and project cargo, we provide reliable, compliant cross-border lift on ad-hoc or contract terms.</p>"),
 ],
 "faqs":[
  ("Which DRC destinations do you serve?","Bunia, Goma, Kinshasa and remote eastern-DRC sites, subject to permits."),
  ("Do you fly NGO operations into the DRC?","Yes — including long-term humanitarian contracts such as MSF in Bunia."),
  ("Can you carry cargo cross-border?","Yes — passengers and cargo, planned for each route."),
 ],
 "related":[("NGO & Humanitarian Charter","services/ngo-humanitarian-charter"),("Charter Flights to South Sudan","services/charter-flights-south-sudan"),("Cargo Charter","services/cargo-charter")],
 "gallery":["2021/08/Caravan-in-Kidepo.jpg","2021/03/PHOTO-2021-02-23-13-56-15.jpg"],
},
{
 "slug":"services/charter-flights-south-sudan","kw":"charter flights South Sudan from Uganda",
 "title":"Charter Flights South Sudan from Uganda | KEA",
 "desc":"Charter flights from Uganda to Juba and across South Sudan — NGO, energy and corporate passengers and cargo from Kajjansi. Call KEA +256 776 333 114.",
 "h1":"Charter Flights to South Sudan from Uganda","eyebrow":"Cross-border","stype":"Cross-border charter to South Sudan",
 "hero":"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg","og":"2021/08/Mi8-Helicopter-Kajjansi-KEA-1.jpg",
 "lead":"KEA flies <b>charter flights to South Sudan from Uganda</b>, departing <b>Kajjansi Airfield, Kampala</b> — Juba and beyond for NGO, energy and corporate clients, with a local AOC for in-country operations.",
 "secs":[
  ("In-country capability","<p>KEA holds a South Sudan AOC, supporting operations to Juba and remote locations across the country for humanitarian, energy and corporate clients.</p>"),
  ("Reliable cross-border lift","<p>Passenger rotations, relief and project cargo and medevac standby — planned, permitted and flown by an experienced regional operator.</p>"),
 ],
 "faqs":[
  ("Do you hold a South Sudan AOC?","Yes — KEA operates under a South Sudan AOC in addition to Uganda AOC 097."),
  ("Which destinations do you serve?","Juba and remote locations across South Sudan, subject to permits."),
  ("Can you provide medevac in South Sudan?","Yes — medevac standby and casualty evacuation can be contracted."),
 ],
 "related":[("NGO & Humanitarian Charter","services/ngo-humanitarian-charter"),("Charter Flights to DRC","services/charter-flights-drc"),("Oil & Gas Aviation","services/oil-gas-aviation")],
 "gallery":[],
},
{
 "slug":"services/aircraft-maintenance-mro","kw":"aircraft MRO maintenance Entebbe",
 "title":"Aircraft MRO & Maintenance Entebbe | KEA Aviation",
 "desc":"CAA-approved aircraft maintenance, MRO and hangarage near Entebbe and Kampala at Kajjansi Airfield for fixed and rotary wing. Call KEA +256 776 333 114.",
 "h1":"Aircraft Maintenance & MRO near Entebbe","eyebrow":"Our AMO","stype":"Aircraft maintenance and MRO",
 "hero":"2018/08/maintenance-hangarage.jpg","og":"2018/08/maintenance-hangarage.jpg",
 "lead":"KEA's Approved Maintenance Organisation delivers <b>aircraft MRO and maintenance near Entebbe</b> at <b>Kajjansi Airfield, Kampala</b> — line and base maintenance, plus hangarage, for fixed and rotary-wing aircraft.",
 "secs":[
  ("In-house engineering","<p>Our AMO keeps our own fleet and third-party aircraft airworthy with scheduled and unscheduled maintenance, component support and modifications, backed by experienced licensed engineers.</p>"),
  ("Regional AMO footprint","<p>AMO approvals span Uganda, South Africa, Chad, Central African Republic and Iraq, so we can support aircraft on operations across the region, not just at base.</p>"),
 ],
 "faqs":[
  ("What aircraft can KEA maintain?","Fixed-wing (Caravan, 1900D, PC-12) and rotary-wing types within our AMO scope."),
  ("Do you offer hangarage?","Yes — hangarage and parking are available at Kajjansi."),
  ("Where are your AMO approvals held?","Uganda, South Africa, Chad, C.A.R. and Iraq."),
 ],
 "related":[("Aircraft Leasing","services/aircraft-leasing"),("Fleet","fleet.html"),("Certifications","certifications")],
 "gallery":["2018/08/maintenance-hangarage.jpg","2019/01/1900-Maintenance.jpg","2019/01/1900-Maintenance2.jpg","2019/01/1900-Maintenance3.jpg"],
},
{
 "slug":"services/uav-drone-operations","kw":"drone survey UAV LiDAR mapping Uganda",
 "title":"UAV Drone Survey & LiDAR Mapping Uganda | KEA",
 "desc":"CAA-certified UAV operations in Uganda — DJI Matrice 400 RTK for LiDAR, orthophoto mapping and asset inspection from Kajjansi. Call KEA +256 776 333 114.",
 "h1":"UAV Drone Survey & LiDAR Mapping in Uganda","eyebrow":"UAV Operations","stype":"UAV drone survey and inspection",
 "hero":"2026/06/Matrice-400-RTK-KEA.jpg","og":"2026/06/Matrice-400-RTK-KEA.jpg",
 "lead":"KEA flies <b>CAA-certified UAV operations in Uganda</b> from <b>Kajjansi Airfield, Kampala</b> — drone survey, LiDAR and orthophoto mapping and asset inspection with the DJI Matrice 400 RTK, under our Ugandan CAA UAV Operating Certificate (UOC).",
 "secs":[
  ("Survey-grade data capture","<p>The Matrice 400 RTK delivers centimetre-accurate <b>orthophoto mapping</b>, <b>LiDAR mapping</b> and <b>animal point sampling</b> for survey, conservation and engineering clients — fast, repeatable and safe.</p>"),
  ("Asset monitoring & inspection","<p>We inspect and monitor critical infrastructure — communications towers, powerlines and pipelines — capturing high-resolution imagery and 3D data to support maintenance and integrity programmes.</p>"),
  ("Certified and integrated","<p>Operating under a Ugandan CAA UOC, our UAV team works alongside our crewed survey and patrol services so you get the right tool for each task, from a single accountable operator.</p>"),
 ],
 "faqs":[
  ("Is KEA licensed to fly drones commercially?","Yes — KEA holds a Ugandan CAA UAV Operating Certificate (UOC)."),
  ("What UAV do you operate?","The DJI Matrice 400 RTK, with LiDAR, RGB and thermal payload options."),
  ("What can you map or inspect?","Orthophoto and LiDAR mapping, animal point sampling, and inspection of towers, powerlines and pipelines."),
 ],
 "related":[("Aerial Survey","services/aerial-survey-geophysical"),("Pipeline Patrol","services/pipeline-patrol"),("Oil & Gas Aviation","services/oil-gas-aviation")],
 "gallery":["2026/06/Matrice-400-RTK-KEA.jpg"],
},
]

# ============================ NEWS / BLOG ============================
# NEWS items (newest first). keys: date, slug, title, img, summary, body(html)
NEWS_NEW = [
{
 "date":"2026-03-02","slug":"uganda-caa-uav-operating-certificate","title":"KEA awarded Ugandan CAA UAV Operating Certificate",
 "img":"2026/06/Matrice-400-RTK-KEA.jpg",
 "summary":"KEA has gained its UAV Operating Certificate (UOC) from the Uganda CAA, formally adding certified drone operations to its capability.",
 "body":"<p>In 2026 KEA was awarded its <b>UAV Operating Certificate (UOC)</b> by the Uganda Civil Aviation Authority, formally adding certified unmanned operations to the company's portfolio.</p><p>Flying the <b>DJI Matrice 400 RTK</b>, the new UAV division delivers orthophoto and LiDAR mapping, animal point sampling and asset monitoring for towers, powerlines and pipelines — complementing KEA's crewed survey and patrol services.</p><p>The certificate positions KEA as one of the region's few operators able to offer integrated crewed and uncrewed aerial data capture under a single accountable organisation.</p>",
},
{
 "date":"2026-06-01","slug":"msf-bell-412-abeche-chad","title":"KEA to support MSF in Abéché, Chad with the Bell 412",
 "img":"2021/08/B412-Flying-with-Lake-and-Rocky-Scenery.jpg",
 "summary":"From June 2026 KEA's Bell 412 helicopter supports MSF humanitarian operations based in Abéché, eastern Chad.",
 "body":"<p>From <b>June 2026</b>, KEA is providing its <b>Bell 412 helicopter</b> to support Médecins Sans Frontières (MSF) operations in <b>Abéché, eastern Chad</b>.</p><p>The contract places rotary-wing capability at the heart of MSF's regional response, enabling rapid access to communities and facilities that are difficult to reach by road. KEA operates in Chad under a local AOC with AMO support in-country.</p><p>The award builds on KEA's long relationship with humanitarian operators across Central Africa and the Sahel.</p>",
},
{
 "date":"2025-09-15","slug":"msf-c208ex-long-term-contract-bunia-drc","title":"Long-term MSF contract for the Cessna 208EX in Bunia, DRC",
 "img":"2021/08/Caravan-in-Kidepo.jpg",
 "summary":"KEA secured a long-term contract to provide a Cessna Caravan 208EX to MSF humanitarian operations in Bunia, DR Congo.",
 "body":"<p>KEA has been awarded a <b>long-term contract</b> to provide a brand-new <b>Cessna Caravan 208EX</b> to Médecins Sans Frontières (MSF) in <b>Bunia, DR Congo</b>.</p><p>The aircraft supports MSF's humanitarian operations across the region, moving medical teams, patients and supplies into locations that scheduled services do not reach. The 208EX's short-field performance and reliability make it ideally suited to eastern-DRC conditions.</p><p>The contract deepens KEA's established presence in the DRC and its partnership with leading humanitarian organisations.</p>",
},
{
 "date":"2025-02-10","slug":"drc-operations-move-kalemie-to-bunia","title":"KEA relocates DRC operations from Kalemie to Bunia",
 "img":"2021/03/PHOTO-2021-02-23-13-56-15.jpg",
 "summary":"In February 2025 KEA moved its DRC base of operations from Kalemie to Bunia to better support humanitarian tasking in the east.",
 "body":"<p>In <b>February 2025</b>, KEA relocated its DR Congo base of operations from <b>Kalemie to Bunia</b>.</p><p>The move places KEA's aircraft and crews closer to humanitarian demand in eastern DRC, improving response times and access for the agencies and NGOs the company supports. Bunia becomes the hub for KEA's growing Caravan operations in the country.</p>",
},
{
 "date":"2024-11-20","slug":"three-new-cessna-caravan-208ex","title":"KEA adds three brand-new Cessna Caravan 208EX",
 "img":"2019/02/Fleet-C208B.jpg",
 "summary":"Across 2024–25 KEA took delivery of three factory-new Cessna Caravan 208EX aircraft, expanding its short-field fleet.",
 "body":"<p>Across <b>2024 and 2025</b>, KEA took delivery of <b>three brand-new Cessna Caravan 208EX aircraft, direct from the factory</b>.</p><p>The 208EX is the most capable Caravan variant, with a more powerful engine for hot-and-high and short-field operations — ideal for the bush strips and remote sites KEA serves across Uganda, the DRC and the region.</p><p>The investment significantly expands KEA's passenger and cargo capacity for charter, humanitarian and remote-site contracts.</p>",
},
{
 "date":"2024-06-05","slug":"wfp-c208-humanitarian-contract-renewal","title":"UN WFP renews KEA's C208 humanitarian contract for two years",
 "img":"2019/04/Caravan-1.jpg",
 "summary":"The United Nations World Food Programme renewed KEA's Cessna 208 humanitarian aviation contract for a further two years in 2024.",
 "body":"<p>In <b>2024</b>, the United Nations <b>World Food Programme (WFP)</b> renewed KEA's <b>Cessna 208 humanitarian aviation contract for a further two years</b>.</p><p>The renewal recognises KEA's reliability and safety record in support of WFP operations, providing dependable passenger and cargo lift into the field. It underlines KEA's standing as a trusted aviation partner to the UN and the humanitarian community.</p>",
},
]

# Cornerstone blog posts. keys: date,slug,title,kw,desc,img,summary,body(html),is_guide
BLOG_POSTS = [
{
 "date":"2026-02-15","slug":"13-countries-kea-serves","title":"The 13 Countries KEA Serves Across Africa",
 "kw":"KEA 13 countries aviation Africa","img":"2020/03/Helicopter-Services-In-Uganda-KEA.jpg",
 "desc":"Where does KEA fly? A look at the African countries Kampala Executive Aviation operates charter, cargo and medevac flights to. Call +256 776 333 114.",
 "summary":"From a Kajjansi base, KEA's charter, cargo and medevac operations reach right across Africa. Here's where we fly — and why our multi-country footprint matters.",
 "body":"<p>From our base at Kajjansi Airfield, Kampala, KEA operates across a wide footprint of African countries — a reach that lets us support energy, humanitarian and corporate clients wherever they work.</p><h2>Where we operate</h2><p>KEA's confirmed countries of operation include Uganda, Kenya, South Sudan, DR Congo, Nigeria, Niger, Chad, Cameroon, the Central African Republic, Somalia, South Africa and Iraq. Air Operator Certificates in Uganda (AOC 097), Chad and South Sudan, plus AMO approvals in five countries, underpin genuine cross-border capability.</p><h2>Why a multi-country footprint matters</h2><p>Operators rarely need just one country. Energy projects span borders; humanitarian responses move with need; and corporate travel follows opportunity. A single operator licensed and maintained across the region means fewer handovers, consistent safety standards and one accountable partner. Explore our <a href='/services/oil-gas-aviation/'>oil &amp; gas aviation</a> and <a href='/services/ngo-humanitarian-charter/'>NGO &amp; humanitarian charter</a> services to see this in action.</p>",
 "is_guide":False,
},
{
 "date":"2026-01-20","slug":"domestic-flights-uganda-guide-2026","title":"Domestic Flights in Uganda: Complete Guide 2026",
 "kw":"domestic flights Uganda","img":"2021/08/Caravan-in-Kidepo.jpg",
 "desc":"A 2026 guide to domestic flights in Uganda — scheduled vs charter, airstrips, national-park access and how to fly to remote sites. Call KEA +256 776 333 114.",
 "summary":"Scheduled or charter? Which airstrips? How to reach the parks and remote sites? A practical 2026 guide to flying domestically within Uganda.",
 "body":"<p>Uganda's size, road conditions and scattered airstrips make flying the practical choice for many journeys. This guide covers how domestic flights in Uganda work in 2026 and when a charter makes sense.</p><h2>Scheduled vs charter</h2><p>Scheduled domestic services run between a handful of airstrips on fixed timetables. Charter, by contrast, flies on your schedule, to far more destinations — including bush strips that scheduled services never touch. For groups, remote sites or time-critical travel, charter is usually faster overall once transfers are counted.</p><h2>Airstrips and national parks</h2><p>Uganda has dozens of usable airstrips, many serving national parks and remote districts. KEA's short-field Cessna Caravans and helicopters reach these directly from Kajjansi Airfield, Kampala.</p><h2>Reaching remote sites</h2><p>For energy, mining, NGO and corporate operations, direct flights to site save days. See our <a href='/charter-flights-kampala/'>charter flights from Kampala</a> and <a href='/services/remote-site-operations/'>remote site operations</a>.</p><h2>How to book</h2><p>Tell KEA your route, dates and passenger or cargo load and we'll match the right aircraft. Call +256 776 333 114 or request a quote.</p>",
 "is_guide":True,
},
{
 "date":"2026-01-10","slug":"aviation-operator-oil-gas-uganda","title":"Choosing an Aviation Operator for Oil & Gas in Uganda",
 "kw":"oil gas aviation operator Uganda","img":"2019/01/Oil-Gas-and-Mining.jpg",
 "desc":"What to look for when choosing an aviation operator for oil & gas operations in Uganda — safety, AOC, medevac and remote-site capability. Call +256 776 333 114.",
 "summary":"Safety record, AOC status, medevac cover, remote-site capability and accountability — the criteria that matter when contracting aviation for oil & gas in Uganda.",
 "body":"<p>Aviation is mission-critical for oil &amp; gas operations — and the wrong partner is a real risk. Here's what to weigh when selecting an operator in Uganda.</p><h2>Safety and certification first</h2><p>Confirm a valid Air Operator Certificate, a credible safety record and in-house maintenance. KEA operates under Uganda AOC 097, with AOCs in Chad and South Sudan and AMO approvals in five countries.</p><h2>Remote-site and cross-border capability</h2><p>Energy work happens away from main airports and across borders. Short-field aircraft, helicopter access and multi-country licensing are essential — see <a href='/services/remote-site-operations/'>remote site operations</a>.</p><h2>Medevac and 24/7 response</h2><p>A casualty plan is non-negotiable. Look for contracted <a href='/services/medical-evacuation/'>medevac standby</a> with 24/7 activation.</p><h2>One accountable partner</h2><p>Fewer handovers means lower risk. KEA plans, crews and maintains operations in-house. Learn more about our <a href='/services/oil-gas-aviation/'>oil &amp; gas aviation</a> service, or call +256 776 333 114.</p>",
 "is_guide":True,
},
{
 "date":"2025-12-15","slug":"emergency-aviation-east-africa","title":"Emergency Aviation Services in East Africa","kw":"emergency aviation East Africa",
 "img":"2019/01/Medevac-KEA.jpg",
 "desc":"How emergency aviation works in East Africa — medevac, search & rescue and disaster response, and how to plan cover. Call KEA +256 776 333 114.",
 "summary":"Medevac, search & rescue and disaster response across East Africa — how emergency aviation works and how to put cover in place before you need it.",
 "body":"<p>When minutes matter, aviation saves lives across East Africa's vast and often remote terrain. This overview explains the main emergency services and how to plan cover.</p><h2>Medical evacuation</h2><p>Fixed-wing and helicopter air ambulances move patients from remote sites to definitive care. KEA provides <a href='/services/medical-evacuation/'>medevac</a> 24/7 across the region.</p><h2>Search and rescue</h2><p>Rotary-wing <a href='/services/search-rescue-helicopter/'>search and rescue</a> reaches incident sites ground teams cannot, with contracted standby for projects and events.</p><h2>Disaster response</h2><p>Rapid airlift, aerial assessment and relief cargo support government and humanitarian responders — see <a href='/services/disaster-response/'>disaster response aviation</a>.</p><h2>Plan before you need it</h2><p>The best emergency outcomes come from cover arranged in advance. Talk to KEA about standby contracts on +256 776 333 114.</p>",
 "is_guide":True,
},
]
