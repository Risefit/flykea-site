/* ===== KEA Trade Portal =====================================================
   Agent accounts, multi-leg charter calculator (rack / net / margin),
   booking workflow, branded client quotes, reservations queue, funnel reports.
   ========================================================================== */
(function () {
"use strict";

var SUPABASE_URL = "https://utlynkvxqdplfrsxxrez.supabase.co";
var SUPABASE_KEY = "sb_publishable_f28aljVLZ6dEx2NUOdZqEg_bvosgf0d";
var RESERVATIONS = "reservations@flykea.com";
var TC_VERSION   = "2026.1";
var TAXI_HRS     = 0.5;
var RANGE_PCT    = 0.10;
var BASE         = "Kajjansi (Kampala)";

var sb = null, ME = null, AGENT = null, IS_STAFF = false, MY_ROLE = "";
var PORTS = [], TOWNS = [], FLEET = [], LOSS = [], RATES = [];
var LEGS = [{ from: BASE, to: "" }];
var LAST = null, QMAP = {};

function $(s, r) { return (r || document).querySelector(s); }
function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]; }); }
function money(n) { return n == null ? "\u2014" : "$" + Math.round(n).toLocaleString("en-US"); }
function fmtHrs(h) { var m = Math.round(h * 60); return Math.floor(m / 60) + "h " + ("0" + (m % 60)).slice(-2) + "m"; }
function today() { return new Date().toISOString().slice(0, 10); }
function busy(on) { document.body.classList.toggle("pt-busy", !!on); }
function toast(msg, bad) {
  var t = document.createElement("div");
  t.className = "pt-toast" + (bad ? " bad" : ""); t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(function () { t.classList.add("go"); }, 10);
  setTimeout(function () { t.remove(); }, 5000);
}
/* ---- transactional mail: browser sends only a record id; the edge function
       resolves the recipient and content server-side ---- */
async function mail(type, id) {
  try {
    var r = await sb.functions.invoke("send-mail", { body: { type: type, id: id } });
    if (r.error) { console.warn("mail", type, r.error); return false; }
    if (r.data && r.data.ok === false) { console.warn("mail", type, r.data.error); return false; }
    return true;
  } catch (e) { console.warn("mail failed", e); return false; }
}

/* ---- map pin picker (Leaflet, loaded on demand) ---- */
var MAPOBJ = null, MAPMARK = null;
function loadLeaflet() {
  return new Promise(function (resolve, reject) {
    if (window.L) return resolve();
    var css = document.createElement("link");
    css.rel = "stylesheet"; css.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
    document.head.appendChild(css);
    var s = document.createElement("script");
    s.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    s.onload = function () { resolve(); };
    s.onerror = function () { reject(new Error("map failed")); };
    document.head.appendChild(s);
  });
}
function setPin(lat, lng) {
  if (!MAPOBJ) return;
  if (MAPMARK) MAPMARK.setLatLng([lat, lng]);
  else MAPMARK = window.L.marker([lat, lng], { draggable: true }).addTo(MAPOBJ)
        .on("dragend", function (e) { var c = e.target.getLatLng(); setPin(c.lat, c.lng); });
  var v = lat.toFixed(4) + ", " + lng.toFixed(4);
  var lbl = $("#pt-pin-val"); if (lbl) lbl.textContent = v;
  var use = $("#pt-pin-use"); if (use) use.dataset.coord = v;
}
async function openPinMap() {
  var box = $("#pt-mapmodal"); if (!box) return;
  box.hidden = false;
  try { await loadLeaflet(); }
  catch (e) { toast("Could not load the map \u2014 check your connection.", true); box.hidden = true; return; }
  if (!MAPOBJ) {
    MAPOBJ = window.L.map("pt-map").setView([1.3733, 32.2903], 7);
    window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18, attribution: "&copy; OpenStreetMap contributors" }).addTo(MAPOBJ);
    MAPOBJ.on("click", function (e) { setPin(e.latlng.lat, e.latlng.lng); });
    PORTS.forEach(function (pt) {
      if (pt.lat == null || pt.lng == null) return;
      window.L.circleMarker([pt.lat, pt.lng], { radius: 4, color: "#56750F",
        fillColor: "#90B820", fillOpacity: 0.9, weight: 1 }).addTo(MAPOBJ).bindTooltip(pt.name);
    });
  }
  setTimeout(function () { MAPOBJ.invalidateSize(); }, 60);
}
function closePinMap() { var b = $("#pt-mapmodal"); if (b) b.hidden = true; }

function haversineNm(a, b) {
  var R = 6371, r = Math.PI / 180;
  var dLa = (b[0] - a[0]) * r, dLo = (b[1] - a[1]) * r, la1 = a[0] * r, la2 = b[0] * r;
  var x = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(la1) * Math.cos(la2) * Math.sin(dLo / 2) * Math.sin(dLo / 2);
  return (R * 2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x))) / 1.852;
}

function findPlace(name) {
  name = (name || "").trim().toLowerCase();
  if (!name) return null;
  var f = PORTS.filter(function (p) { return p.name.toLowerCase() === name; });
  if (!f.length) f = PORTS.filter(function (p) { return p.name.toLowerCase().indexOf(name) >= 0; });
  if (f.length) return f[0];
  var t = TOWNS.filter(function (p) { return p.name.toLowerCase() === name; });
  if (!t.length) t = TOWNS.filter(function (p) { return p.name.toLowerCase().indexOf(name) >= 0; });
  if (t.length) return { code: null, name: t[0].name + " (town)", lat: t[0].lat, lng: t[0].lng, country_code: "UG" };
  return null;
}
function pickAircraft(distNm, pax, heli) {
  var pool = FLEET.filter(function (a) { return a.active !== false; });
  if (heli) {
    var h = pool.filter(function (a) { return a.category === "rotary" && a.seats >= pax; });
    h.sort(function (x, y) { return x.hourly_rack - y.hourly_rack; });
    return h[0] || pool.filter(function (a) { return a.category === "rotary"; })[0];
  }
  var c = pool.filter(function (a) { return a.category !== "rotary" && a.seats >= pax && a.range_nm >= distNm * 0.6; });
  if (!c.length) c = pool.filter(function (a) { return a.category !== "rotary" && a.seats >= pax; });
  if (!c.length) c = pool.slice();
  c.sort(function (x, y) { return (x.seats - pax) - (y.seats - pax) || x.hourly_rack - y.hourly_rack; });
  return c[0];
}
function bookRate(acCode, fromName, toName) {
  if ((fromName || "").toLowerCase().indexOf("kajjansi") < 0) return null;
  var t = (toName || "").toLowerCase();
  for (var i = 0; i < RATES.length; i++) {
    var r = RATES[i];
    if (r.aircraft_code !== acCode || !r.verified) continue;
    var rt = (r.to_name || "").toLowerCase();
    if (t === rt || t.indexOf(rt) === 0) return r;
  }
  return null;
}

function show(view) {
  $$(".pt-view").forEach(function (v) { v.hidden = v.dataset.view !== view; });
  $$(".pt-tab").forEach(function (t) { t.classList.toggle("on", t.dataset.go === view); });
  if (view === "quotes")   loadMyQuotes();
  if (view === "bookings") loadMyBookings();
  if (view === "reports")  loadReports();
  if (view === "admin")    loadApplications();
  if (view === "rates")    loadRates();
  if (view === "desk")     loadDesk();
  if (view === "queue")    loadQueue();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ================= AUTH ================= */
async function boot() {
  if (!window.supabase) return;
  sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
  var s = await sb.auth.getSession();
  await onSession(s.data.session);
  sb.auth.onAuthStateChange(function (_e, sess) { onSession(sess); });
}

async function onSession(session) {
  ME = session ? session.user : null;
  if (!ME) { AGENT = null; IS_STAFF = false; gate("auth"); return; }
  var r = await sb.from("agents").select("*").eq("id", ME.id).maybeSingle();
  AGENT = r.data || null;
  var st = await sb.from("staff").select("user_id,role").eq("user_id", ME.id).maybeSingle();
  IS_STAFF = !!(st.data); MY_ROLE = st.data ? st.data.role : "";
  if (!AGENT && !IS_STAFF) {
    var md = ME.user_metadata || {};
    if (md.agency_name) {
      var ins = await sb.from("agents").insert({
        id: ME.id, agency_name: md.agency_name, contact_name: md.contact_name || "",
        email: ME.email, phone: md.phone || null, country: md.country || null,
        city: md.city || null, website: md.website || null,
        tc_accepted_at: new Date().toISOString(), tc_version: md.tc_version || TC_VERSION
      }).select().single();
      if (!ins.error) { AGENT = ins.data; gate("pending"); return; }
    }
    gate("apply"); return;
  }
  if (IS_STAFF || (AGENT && AGENT.status === "approved")) { await enterPortal(); return; }
  gate(AGENT.status === "rejected" ? "rejected" : "pending");
}

function gate(which) {
  $$(".pt-gate").forEach(function (g) { g.hidden = g.dataset.gate !== which; });
  $("#pt-app").hidden = true; $("#pt-gates").hidden = false;
  if (which === "pending" && AGENT) $("#pt-pending-name").textContent = AGENT.agency_name || "";
}

async function enterPortal() {
  $("#pt-gates").hidden = true; $("#pt-app").hidden = false;
  $("#pt-who").textContent = IS_STAFF ? ("KEA " + (MY_ROLE || "staff")) : (AGENT.agency_name || ME.email);
  $$(".pt-staff-only").forEach(function (n) { n.hidden = !IS_STAFF; });
  await loadReference();
  renderLegs();
  if (!IS_STAFF) { fillProfileForm(); loadNotifications(); }
  show(IS_STAFF ? "queue" : "quote");
}

async function loadReference() {
  var a = await sb.from("aircraft").select("*").eq("active", true).order("sort_order");
  FLEET = a.data || [];
  var p = await sb.from("airfields").select("*").eq("active", true).order("sort_order").order("name");
  PORTS = p.data || [];
  var t = await sb.from("towns").select("*").eq("active", true).order("name");
  TOWNS = t.data || [];
  var l = await sb.from("loss_reasons").select("*").eq("active", true).order("sort_order");
  LOSS = l.data || [];
  var rr = await sb.from("route_rates").select("*").order("to_name");
  RATES = rr.data || [];

  var dl = $("#pt-ports"); dl.innerHTML = "";
  PORTS.forEach(function (x) { var o = document.createElement("option"); o.value = x.name; dl.appendChild(o); });
  var tl = $("#pt-townlist");
  if (tl) { tl.innerHTML = ""; TOWNS.forEach(function (x) { var o = document.createElement("option"); o.value = x.name; tl.appendChild(o); }); }
  var ov = $("#pt-ac"); ov.innerHTML = '<option value="">Best match (automatic)</option>';
  FLEET.forEach(function (x) { var o = document.createElement("option"); o.value = x.code; o.textContent = x.name; ov.appendChild(o); });
  renderFleetSpecs();
}

/* ================= MULTI-LEG ROUTE ================= */
function renderLegs() {
  var box = $("#pt-legs"); if (!box) return;
  box.innerHTML = LEGS.map(function (lg, i) {
    var first = i === 0;
    return '<div class="pt-leg" data-i="' + i + '"><span class="pt-leg-n">' + (i + 1) + '</span>' +
      '<div class="pt-fld"><label>' + (first ? "From" : "Then from") + '</label>' +
      '<input class="pt-leg-from" list="pt-ports" value="' + esc(lg.from) + '"' + (first ? '' : ' readonly') + ' autocomplete="off"></div>' +
      '<div class="pt-fld"><label>To</label>' +
      '<input class="pt-leg-to" list="pt-ports" value="' + esc(lg.to) + '" placeholder="Destination" autocomplete="off"></div>' +
      (LEGS.length > 1 ? '<button class="pt-leg-x" data-rmleg="' + i + '" title="Remove leg" type="button">&times;</button>' : '<span class="pt-leg-x"></span>') +
      '</div>';
  }).join("");
}
function readLegs() {
  $$(".pt-leg").forEach(function (row) {
    var i = +row.dataset.i;
    LEGS[i].from = $(".pt-leg-from", row).value;
    LEGS[i].to   = $(".pt-leg-to", row).value;
  });
  for (var i = 1; i < LEGS.length; i++) LEGS[i].from = LEGS[i - 1].to;
}
function addLeg() {
  readLegs();
  if (LEGS.length >= 6) { toast("Six legs maximum \u2014 contact reservations for longer itineraries.", true); return; }
  LEGS.push({ from: LEGS[LEGS.length - 1].to || "", to: "" });
  renderLegs();
}
function removeLeg(i) {
  readLegs(); LEGS.splice(i, 1);
  if (!LEGS.length) LEGS = [{ from: BASE, to: "" }];
  for (var k = 1; k < LEGS.length; k++) LEGS[k].from = LEGS[k - 1].to;
  renderLegs(); if (LAST) calculate();
}

/* ================= CALCULATOR ================= */
function calculate() {
  readLegs();
  var coordRaw = ($("#pt-coord").value || "").trim();
  var m = coordRaw.match(/(-?\d+\.?\d*)[ ,]+(-?\d+\.?\d*)/);

  var pts = [], names = [], legRows = [];
  var home = findPlace(LEGS[0].from);
  if (!home) { toast("Choose a valid origin.", true); return; }
  pts.push(home); names.push(home.name);

  for (var i = 0; i < LEGS.length; i++) {
    var dest = null;
    if (i === LEGS.length - 1 && m) {
      dest = { code: null, name: "Custom site " + (+m[1]).toFixed(3) + ", " + (+m[2]).toFixed(3), lat: +m[1], lng: +m[2], country_code: "UG" };
    } else if (LEGS[i].to) {
      dest = findPlace(LEGS[i].to);
    }
    if (!dest) break;
    pts.push(dest); names.push(dest.name);
  }
  if (pts.length < 2) { toast("Choose a destination from the list, or enter coordinates.", true); return; }

  var pax = Math.max(1, +$("#pt-pax").value || 1);
  var mission = $("#pt-mission").value;
  var heli = mission === "site" || !!m;
  var nights = Math.max(0, +$("#pt-nights").value || 0);
  var dayStop = $("#pt-daystop").checked;

  var total = 0, allCoords = true;
  for (var j = 0; j < pts.length - 1; j++) {
    var a = pts[j], b = pts[j + 1];
    if (a.lat == null || b.lat == null) { allCoords = false; legRows.push({ from: a.name, to: b.name, nm: null }); continue; }
    var d = haversineNm([a.lat, a.lng], [b.lat, b.lng]);
    total += d; legRows.push({ from: a.name, to: b.name, nm: +d.toFixed(1) });
  }
  var lastPt = pts[pts.length - 1], backNm = 0;
  if (allCoords && lastPt.lat != null && home.lat != null && lastPt.name !== home.name) {
    backNm = haversineNm([lastPt.lat, lastPt.lng], [home.lat, home.lng]);
  }

  var forced = $("#pt-ac").value;
  var ac = forced ? FLEET.filter(function (x) { return x.code === forced; })[0] : pickAircraft(total, pax, heli);
  if (!ac) { toast("No suitable aircraft found.", true); return; }

  var flightNm = total + backNm;
  var flightHrs = allCoords ? flightNm / (+ac.cruise_kt || 150) : 0;
  var block = flightHrs + TAXI_HRS * Math.max(1, legRows.length);

  var rack, method = "estimate";
  var single = (legRows.length === 1) && !m;
  var bk = single ? bookRate(ac.code, home.name, pts[1].name) : null;
  if (bk) { rack = +bk.rack; method = "book"; }
  else { rack = Math.max(+ac.min_charge || 0, block * +ac.hourly_rack); }

  if (dayStop) rack += (+ac.day_stop || 0);
  var nightRate = ac.night_stop == null ? null : +ac.night_stop;
  var nightUnknown = nights > 0 && nightRate == null;
  if (nights > 0 && nightRate != null) rack += nights * nightRate;
  var net = rack * (+ac.net_factor || 0.9);

  LAST = {
    legs: legRows, leg_count: legRows.length,
    from_code: home.code, to_code: pts[1] ? pts[1].code : null,
    from_name: home.name, to_name: lastPt.name,
    custom_coords: m ? coordRaw : null, pax: pax, travel_date: $("#pt-date").value || null,
    mission: mission, aircraft_code: ac.code, aircraft: ac,
    distance_nm: +flightNm.toFixed(1), block_hours: +block.toFixed(2),
    day_stop: dayStop, night_stops: nights,
    rack_total: +rack.toFixed(2), net_total: +net.toFixed(2), margin: +(rack - net).toFixed(2),
    is_international: pts.some(function (p) { return p.country_code && p.country_code !== "UG"; }),
    method: method, nightUnknown: nightUnknown, allCoords: allCoords, id: null
  };

  $("#pt-r-route").textContent = names.join("  \u2192  ") + (backNm ? "  \u2192  " + home.name : "");
  $("#pt-r-ac").textContent = ac.name;
  $("#pt-r-dist").textContent = allCoords ? Math.round(flightNm) + " nm" : "\u2014";
  $("#pt-r-time").textContent = allCoords ? fmtHrs(flightHrs) + " airborne" : "on request";
  $("#pt-r-block").textContent = method === "book" ? "Rate book return price"
      : fmtHrs(block) + " block" + (backNm ? " incl. return to base" : "");
  $("#pt-r-rack").textContent = money(rack);
  $("#pt-r-net").textContent = money(net);
  $("#pt-r-margin").textContent = money(rack - net);
  $("#pt-r-band").textContent = method === "book" ? "fixed rate-book price"
      : money(rack * (1 - RANGE_PCT)) + " \u2013 " + money(rack * (1 + RANGE_PCT));
  var badge = $("#pt-r-method");
  badge.textContent = method === "book" ? "RATE BOOK" : "ESTIMATE";
  badge.className = "pt-pill " + (method === "book" ? "ok" : "");
  $("#pt-r-legs").innerHTML = legRows.map(function (l, k) {
    return "<div>" + (k + 1) + ". " + esc(l.from) + " \u2192 " + esc(l.to) + (l.nm != null ? " <b>" + Math.round(l.nm) + " nm</b>" : "") + "</div>";
  }).join("") + (backNm ? "<div style='color:var(--slate)'>\u21a9 positioning " + esc(lastPt.name) + " \u2192 " + esc(home.name) + " <b>" + Math.round(backNm) + " nm</b></div>" : "");
  $("#pt-r-nightwarn").hidden = !nightUnknown;
  $("#pt-r-intl").hidden = !LAST.is_international;
  $("#pt-result").hidden = false;
  saveQuote();
}

async function saveQuote() {
  if (!LAST) return;
  var r = await sb.from("quotes").insert({
    agent_id: IS_STAFF ? null : ME.id,
    from_code: LAST.from_code, to_code: LAST.to_code,
    from_name: LAST.from_name, to_name: LAST.to_name, custom_coords: LAST.custom_coords,
    pax: LAST.pax, travel_date: LAST.travel_date, mission: LAST.mission,
    aircraft_code: LAST.aircraft_code, distance_nm: LAST.distance_nm,
    block_hours: LAST.block_hours, day_stop: LAST.day_stop, night_stops: LAST.night_stops || 0,
    rack_total: LAST.rack_total, net_total: LAST.net_total, margin: LAST.margin,
    is_international: LAST.is_international, source: IS_STAFF ? "staff" : "portal",
    legs: LAST.legs, leg_count: LAST.leg_count
  }).select("id").single();
  if (r.error) { console.warn("saveQuote", r.error); toast("Quote not saved: " + r.error.message, true); return; }
  if (r.data) { LAST.id = r.data.id; QMAP[r.data.id] = null; }
}

/* ================= BOOKING ================= */
function openBookingFor(q) {
  LAST = {
    id: q.id, from_name: q.from_name, to_name: q.to_name, pax: q.pax,
    travel_date: q.travel_date, aircraft: { name: q.aircraft_code }, aircraft_code: q.aircraft_code,
    distance_nm: q.distance_nm, block_hours: q.block_hours, day_stop: q.day_stop,
    night_stops: q.night_stops, rack_total: q.rack_total, net_total: q.net_total,
    legs: q.legs, allCoords: true, method: "stored"
  };
  $("#pt-book-summary").innerHTML = "<b>" + esc(q.from_name) + " \u2192 " + esc(q.to_name) + "</b><br>" +
    esc(q.travel_date || "date flexible") + " \u00b7 " + q.pax + " pax \u00b7 " + esc(q.aircraft_code || "") +
    " \u00b7 " + money(q.rack_total);
  $("#pt-booked").hidden = true;
  show("book");
}

async function submitBooking(ev) {
  ev.preventDefault();
  if (!LAST) { toast("Pick a quote first.", true); return; }
  busy(true);
  var payload = {
    quote_id: LAST.id, agent_id: IS_STAFF ? null : ME.id,
    client_ref: $("#pt-b-ref").value || null,
    pax_details: $("#pt-b-pax").value || null,
    contact_phone: $("#pt-b-phone").value || (AGENT ? AGENT.phone : null),
    notes: $("#pt-b-notes").value || null,
    requested_date: LAST.travel_date, value_usd: LAST.rack_total
  };
  var r = await sb.from("booking_requests").insert(payload).select("ref,id").single();
  busy(false);
  if (r.error) { toast("Could not submit: " + r.error.message, true); return; }

  var who = AGENT || { agency_name: "KEA staff", contact_name: ME.email, email: ME.email };
  var body = [
    "NEW BOOKING REQUEST \u2014 " + (r.data.ref || ""),
    "Agency: " + who.agency_name,
    "Contact: " + (who.contact_name || "") + " (" + who.email + ")",
    "Phone: " + (payload.contact_phone || "-"), "",
    "Route: " + LAST.from_name + " -> " + LAST.to_name,
    (LAST.legs && LAST.legs.length > 1 ? "Legs: " + LAST.legs.map(function (l) { return l.from + ">" + l.to; }).join(", ") : ""),
    "Date: " + (LAST.travel_date || "flexible") + "   Pax: " + LAST.pax,
    "Aircraft: " + (LAST.aircraft.name || LAST.aircraft_code),
    "Distance: " + Math.round(LAST.distance_nm || 0) + " nm",
    (LAST.day_stop ? "Day stop: yes" : ""),
    (LAST.night_stops ? "Night stops: " + LAST.night_stops : ""),
    "Rack: " + money(LAST.rack_total) + "   Agent net: " + money(LAST.net_total), "",
    "Client ref: " + (payload.client_ref || "-"),
    "Pax details: " + (payload.pax_details || "-"),
    "Notes: " + (payload.notes || "-"), "",
    "Manage in the KEA Trade Portal -> Bookings queue."
  ].filter(Boolean).join("\n");
  try {
    await fetch("https://formsubmit.co/ajax/" + RESERVATIONS, {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({ _subject: "Booking request " + (r.data.ref || ""), message: body })
    });
  } catch (e) {}

  $("#pt-book-form").reset();
  $("#pt-booked-ref").textContent = r.data.ref || "";
  $("#pt-booked").hidden = false;
  mail("booking_submitted", r.data.id);
  toast("Booking request sent \u2014 " + (r.data.ref || ""));
}

function openWhyFor(q) {
  $("#pt-why-quote").value = q.id;
  $("#pt-why-label").textContent = q.from_name + " \u2192 " + q.to_name;
  $("#pt-why-reason").innerHTML = LOSS.map(function (l) { return '<option value="' + l.code + '">' + esc(l.label) + "</option>"; }).join("");
  $("#pt-whybox").hidden = false;
  $("#pt-whybox").scrollIntoView({ behavior: "smooth", block: "center" });
}
async function sendWhy() {
  var qid = $("#pt-why-quote").value;
  if (!qid) return;
  busy(true);
  var r = await sb.from("quote_feedback").insert({
    quote_id: qid, agent_id: IS_STAFF ? null : ME.id,
    reason_code: $("#pt-why-reason").value, notes: $("#pt-why-notes").value || null
  });
  busy(false);
  if (r.error) { toast(r.error.message, true); return; }
  $("#pt-whybox").hidden = true; $("#pt-why-notes").value = "";
  toast("Thanks \u2014 that feedback helps us price better.");
}

/* ================= MY QUOTES / BOOKINGS ================= */
async function loadMyQuotes() {
  var q = await sb.from("quotes").select("*").order("created_at", { ascending: false }).limit(100);
  if (q.error) { toast("Could not load quotes: " + q.error.message, true); return; }
  QMAP = {};
  var rows = (q.data || []).map(function (r) {
    QMAP[r.id] = r;
    var status = r.converted ? "<span class='pt-pill ok'>requested</span>"
                             : "<span class='pt-pill'>quote</span>";
    var book = r.converted ? "\u2014"
      : "<button class='pt-mini ok' data-book='" + r.id + "'>Book flight</button>";
    var dec  = r.converted ? "\u2014"
      : "<button class='pt-mini' data-nobook='" + r.id + "'>Don&rsquo;t book</button>";
    var del  = r.converted ? ""
      : " <button class='pt-mini pt-del' data-delq='" + r.id + "' title='Delete this quote'>&times;</button>";
    return "<tr><td>" + r.created_at.slice(0, 10) + "</td>" +
      "<td>" + esc(r.from_name) + " \u2192 " + esc(r.to_name) +
        (r.leg_count > 1 ? " <small>(" + r.leg_count + " legs)</small>" : "") + "</td>" +
      "<td>" + esc(r.aircraft_code || "") + "</td><td>" + r.pax + "</td>" +
      "<td>" + money(r.rack_total) + "</td><td>" + money(r.net_total) + "</td>" +
      "<td>" + status + "</td><td>" + book + "</td><td>" + dec + del + "</td></tr>";
  }).join("");
  $("#pt-quotes-body").innerHTML = rows ||
    "<tr><td colspan=9>No quotes yet. Run one on the Quote tab.</td></tr>";
}

/* rebuild LAST from a saved quote so the booking form can be reused */
function quoteToLast(row) {
  var ac = FLEET.filter(function (a) { return a.code === row.aircraft_code; })[0] || FLEET[0];
  LAST = {
    id: row.id, from_code: row.from_code, to_code: row.to_code,
    from_name: row.from_name, to_name: row.to_name, custom_coords: row.custom_coords,
    pax: row.pax, travel_date: row.travel_date, mission: row.mission,
    aircraft_code: row.aircraft_code, aircraft: ac,
    distance_nm: row.distance_nm, block_hours: row.block_hours,
    day_stop: row.day_stop, night_stops: row.night_stops || 0,
    rack_total: row.rack_total, net_total: row.net_total, margin: row.margin,
    is_international: row.is_international, lo: row.rack_total, hi: row.rack_total,
    oneWay: (row.block_hours || 1) / 2, method: "saved", hasCoords: row.distance_nm > 0
  };
}

function bookFromQuote(id) {
  var row = MYQ.filter(function (r) { return r.id === id; })[0];
  if (!row) return;
  quoteToLast(row);
  show("quote");
  $("#pt-r-route").textContent = row.from_name + "  →  " + row.to_name;
  $("#pt-r-ac").textContent = LAST.aircraft.name;
  $("#pt-r-dist").textContent = row.distance_nm ? Math.round(row.distance_nm) + " nm" : "—";
  $("#pt-r-time").textContent = fmtHrs((row.block_hours || 1) / 2);
  $("#pt-r-block").textContent = "Saved quote";
  $("#pt-r-rack").textContent = money(row.rack_total);
  $("#pt-r-net").textContent = money(row.net_total);
  $("#pt-r-margin").textContent = money(row.margin);
  $("#pt-r-band").textContent = "as quoted";
  var badge = $("#pt-r-method"); if (badge) { badge.textContent = "SAVED QUOTE"; badge.className = "pt-pill"; }
  $("#pt-result").hidden = false;
  setTimeout(function () {
    var f = $("#pt-book-form"); if (f) f.scrollIntoView({ behavior: "smooth", block: "center" });
  }, 120);
  toast("Complete the details and send the booking request.");
}

function askWhyNotBooked(id) {
  var row = MYQ.filter(function (r) { return r.id === id; })[0];
  if (row) openWhyFor(row);
}

async function deleteQuote(id) {
  var q = QMAP[id];
  if (!confirm("Delete this quote?" + (q ? "\n\n" + q.from_name + " \u2192 " + q.to_name : ""))) return;
  busy(true);
  var r = await sb.from("quotes").delete().eq("id", id);
  busy(false);
  if (r.error) { toast(r.error.message, true); return; }
  toast("Quote deleted.");
  loadMyQuotes();
}

async function loadMyBookings() {
  var b = await sb.from("booking_requests").select("*").order("created_at", { ascending: false }).limit(100);
  var rows = (b.data || []).map(function (r) {
    var cls = (r.status === "flown" || r.status === "confirmed") ? "ok"
            : (r.status === "lost" || r.status === "cancelled") ? "bad" : "";
    return "<tr><td>" + esc(r.ref || "") + "</td><td>" + r.created_at.slice(0, 10) + "</td><td>" +
      esc(r.client_ref || "-") + "</td><td>" + money(r.value_usd) + "</td>" +
      "<td><span class='pt-pill " + cls + "'>" + esc(r.status) + "</span></td>" +
      "<td>" + (r.confirmed_at ? "Confirmed " + r.confirmed_at.slice(0, 10) + (r.confirmation_ref ? " \u00b7 " + esc(r.confirmation_ref) : "") : "") +
      (r.ops_notes ? "<br><small>" + esc(r.ops_notes) + "</small>" : "") + "</td>" +
      "<td>" + (r.commission_usd == null ? "\u2014"
        : r.status === "flown"     ? "<b style='color:var(--green-ink)'>" + money(r.commission_usd) + "</b><br><small>earned</small>"
        : r.status === "confirmed" ? money(r.commission_usd) + "<br><small>on completion</small>"
        : (r.status === "lost" || r.status === "cancelled") ? "\u2014"
        : "<span style='color:var(--slate)'>" + money(r.commission_usd) + "</span><br><small>if booked</small>") +
      "</td></tr>";
  }).join("");
  $("#pt-bookings-body").innerHTML = rows || "<tr><td colspan=7>No booking requests yet.</td></tr>";
}

/* ================= AIRCRAFT ================= */
function renderFleetSpecs() {
  var wrap = $("#pt-specs"); if (!wrap) return;
  wrap.innerHTML = FLEET.map(function (a, ix) {
    var gal = Array.isArray(a.gallery) ? a.gallery : [];
    if (!gal.length && a.image_url) gal = [{ url: a.image_url, caption: "" }];

    var media;
    if (!gal.length) {
      media = '<div class="pt-spec-noimg"><span>' + esc(a.name) + '</span><small>photo coming soon</small></div>';
    } else if (gal.length === 1) {
      media = '<div class="pt-carousel"><div class="pt-track"><figure><img src="' + esc(gal[0].url) +
              '" alt="' + esc(a.name) + '" loading="lazy"></figure></div></div>';
    } else {
      var slides = gal.map(function (g, i) {
        return '<figure' + (i === 0 ? ' class="on"' : '') + '><img src="' + esc(g.url) + '" alt="' +
               esc(a.name + (g.caption ? " \u2014 " + g.caption : "")) + '" loading="lazy">' +
               (g.caption ? '<figcaption>' + esc(g.caption) + '</figcaption>' : '') + '</figure>';
      }).join("");
      var dots = gal.map(function (_, i) {
        return '<button class="pt-dot' + (i === 0 ? ' on' : '') + '" data-car="' + ix + '" data-slide="' + i +
               '" aria-label="Photo ' + (i + 1) + '"></button>';
      }).join("");
      media = '<div class="pt-carousel" data-carousel="' + ix + '" data-n="' + gal.length + '" data-i="0">' +
              '<div class="pt-track">' + slides + '</div>' +
              '<button class="pt-car-nav prev" data-car="' + ix + '" data-step="-1" aria-label="Previous photo">&#8249;</button>' +
              '<button class="pt-car-nav next" data-car="' + ix + '" data-step="1" aria-label="Next photo">&#8250;</button>' +
              '<div class="pt-dots">' + dots + '</div>' +
              '<span class="pt-car-count">' + gal.length + ' photos</span></div>';
    }

    return '<div class="pt-spec">' + media +
      '<div class="pt-spec-b"><h3>' + esc(a.name) + '</h3><dl>' +
      '<dt>Seats</dt><dd>' + a.seats + '</dd><dt>Cruise</dt><dd>' + a.cruise_kt + ' kt</dd>' +
      '<dt>Range</dt><dd>' + a.range_nm + ' nm</dd><dt>Baggage</dt><dd>' + esc(a.baggage || "\u2014") + '</dd>' +
      '<dt>Strip</dt><dd>' + esc(a.strip_requirement || "\u2014") + '</dd></dl>' +
      '<p>' + esc(a.spec_notes || "") + '</p></div></div>';
  }).join("");
}

function carouselGo(ix, target, isStep) {
  var car = document.querySelector('[data-carousel="' + ix + '"]');
  if (!car) return;
  var n = +car.dataset.n, cur = +car.dataset.i;
  var next = isStep ? (cur + target + n) % n : target;
  car.dataset.i = next;
  $$("figure", car).forEach(function (f, i) { f.classList.toggle("on", i === next); });
  $$(".pt-dot[data-car='" + ix + "']", car).forEach(function (d, i) { d.classList.toggle("on", i === next); });
}

/* ================= PROFILE ================= */
function fillProfileForm() {
  if (!AGENT) return;
  [["agency", "agency_name"], ["contact", "contact_name"], ["phone", "phone"], ["address", "address"],
   ["city", "city"], ["country", "country"], ["website", "website"]].forEach(function (p) {
    var n = $("#pf-" + p[0]); if (n) n.value = AGENT[p[1]] || "";
  });
  var img = $("#pf-logo-prev");
  if (AGENT.logo_url) { img.src = AGENT.logo_url; img.hidden = false; } else img.hidden = true;
}
async function saveProfile(ev) {
  ev.preventDefault(); busy(true);
  var patch = {
    agency_name: $("#pf-agency").value.trim(), contact_name: $("#pf-contact").value.trim(),
    phone: $("#pf-phone").value.trim(), address: $("#pf-address").value.trim(),
    city: $("#pf-city").value.trim(), country: $("#pf-country").value.trim(),
    website: $("#pf-website").value.trim()
  };
  var f = $("#pf-logo").files[0];
  if (f) {
    var path = ME.id + "/logo-" + Date.now() + "-" + f.name.replace(/[^\w.\-]/g, "");
    var up = await sb.storage.from("agent-logos").upload(path, f, { upsert: true });
    if (!up.error) patch.logo_url = sb.storage.from("agent-logos").getPublicUrl(path).data.publicUrl;
  }
  var r = await sb.from("agents").update(patch).eq("id", ME.id).select().single();
  busy(false);
  if (r.error) { toast(r.error.message, true); return; }
  AGENT = r.data; fillProfileForm(); toast("Profile saved.");
}

/* ================= CLIENT QUOTE (rack only) ================= */
function clientQuote() {
  if (!LAST) { toast("Run a quote first.", true); return; }
  var a = AGENT || {};
  var w = window.open("", "_blank");
  if (!w) { toast("Allow pop-ups to generate the quote.", true); return; }
  var ref = "Q-" + today().replace(/-/g, "") + "-" + Math.floor(Math.random() * 900 + 100);
  var validTo = new Date(Date.now() + 30 * 864e5).toISOString().slice(0, 10);
  var legHtml = (LAST.legs || []).map(function (l, i) {
    return '<tr><td>Leg ' + (i + 1) + '</td><td><b>' + esc(l.from) + ' &rarr; ' + esc(l.to) + '</b></td></tr>';
  }).join("");
  w.document.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>Charter Quote ' + ref + '</title><style>' +
  'body{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#1C2118;margin:0;padding:40px;max-width:800px}' +
  '.hd{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;border-bottom:3px solid #90B820;padding-bottom:18px}' +
  '.hd img{max-height:74px;max-width:230px;object-fit:contain}.ag{font-size:12px;line-height:1.6;text-align:right;color:#566058}' +
  '.ag b{color:#1C2118;font-size:15px;display:block;margin-bottom:3px}h1{font-size:23px;margin:26px 0 4px}' +
  '.sub{color:#566058;font-size:13px;margin:0 0 22px}table{width:100%;border-collapse:collapse;margin:18px 0}' +
  'td{padding:9px 0;border-bottom:1px solid #e6ebe1;font-size:14px}td:first-child{color:#566058;width:38%}' +
  '.tot{margin-top:26px;background:#F5F8EE;border-left:4px solid #90B820;padding:18px 22px}' +
  '.tot .lbl{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#56750F}.tot .amt{font-size:31px;font-weight:700;margin-top:4px}' +
  '.note{font-size:11.5px;color:#566058;line-height:1.65;margin-top:26px;border-top:1px solid #e6ebe1;padding-top:16px}' +
  '.ft{margin-top:30px;font-size:11px;color:#8a938a;text-align:center}@media print{body{padding:16px}.no-print{display:none}}' +
  'button{background:#90B820;border:0;padding:11px 20px;border-radius:6px;font-weight:600;cursor:pointer;font-size:14px}</style></head><body>' +
  '<div class="no-print" style="margin-bottom:18px"><button onclick="window.print()">Print / Save as PDF</button></div><div class="hd">' +
  (a.logo_url ? '<img src="' + esc(a.logo_url) + '" alt="">' : '<div style="font-size:20px;font-weight:700">' + esc(a.agency_name || "") + '</div>') +
  '<div class="ag"><b>' + esc(a.agency_name || "") + '</b>' + (a.address ? esc(a.address) + '<br>' : '') +
  (a.city ? esc(a.city) + '<br>' : '') + (a.country ? esc(a.country) + '<br>' : '') +
  (a.phone ? esc(a.phone) + '<br>' : '') + (a.email ? esc(a.email) + '<br>' : '') + (a.website ? esc(a.website) : '') + '</div></div>' +
  '<h1>Private Charter Quotation</h1><p class="sub">Reference ' + ref + ' &nbsp;&middot;&nbsp; Issued ' + today() + ' &nbsp;&middot;&nbsp; Valid until ' + validTo + '</p><table>' + legHtml +
  '<tr><td>Date of travel</td><td>' + esc(LAST.travel_date || "To be confirmed") + '</td></tr>' +
  '<tr><td>Passengers</td><td>' + LAST.pax + '</td></tr>' +
  '<tr><td>Aircraft</td><td>' + esc(LAST.aircraft.name || LAST.aircraft_code) + '</td></tr>' +
  (LAST.allCoords ? '<tr><td>Total distance</td><td>' + Math.round(LAST.distance_nm) + ' nautical miles</td></tr>' : '') +
  (LAST.day_stop ? '<tr><td>Aircraft waiting time</td><td>Included (day stop)</td></tr>' : '') +
  (LAST.night_stops ? '<tr><td>Night stops</td><td>' + LAST.night_stops + '</td></tr>' : '') +
  '</table><div class="tot"><div class="lbl">Total charter price</div><div class="amt">' + money(LAST.rack_total) + ' USD</div></div>' +
  '<div class="note"><b>Included:</b> aircraft, crew and fuel for the routing shown including positioning to and from base, landing fees, air navigation (ATNS) fees, passenger taxes, pilot fees and per diem, passenger legal liability and insurance, animal clearance where required, and crew transport.<br>' +
  '<b>Not included:</b> in-flight catering, passenger land transfers, ad-hoc and off-site landing costs, local authority fees and clearances, and pilot accommodation, meals and transport where the aircraft remains away from base.<br>' +
  '<b>Please note:</b> quoted flight time is an estimate and may change due to weather, diversion or air traffic control; flying time beyond the quoted time is charged additionally. Passenger names are required before the flight for legal and insurance purposes. On helicopter flights only soft luggage of 5kg per passenger is permitted, GPS coordinates and landowner permission must be obtained in advance, and no dust landings are permitted.<br>' +
  '<b>Terms:</b> valid 30 days. Subject to aircraft availability at time of booking, to final confirmation of routing, timings and payload, and to landing and overflight permissions being granted. Rates are subject to fuel price fluctuation.</div>' +
  '<div class="ft">Flight operated by Kampala Executive Aviation \u2014 Ugandan CAA AOC 097 \u00b7 Gate 1, Kajjansi Airfield, Kampala</div></body></html>');
  w.document.close();
}

/* ================= STAFF: bookings queue ================= */
async function loadQueue() {
  if (!IS_STAFF) return;
  var r = await sb.from("v_booking_queue").select("*").limit(200);
  var rows = (r.data || []).map(function (b) {
    var cls = (b.status === "confirmed" || b.status === "flown") ? "ok"
            : (b.status === "lost" || b.status === "cancelled") ? "bad" : "";
    var acts = "";
    if (b.status === "requested" || b.status === "quoted") {
      acts = "<button class='pt-mini ok' data-accept='" + b.id + "'>Accept booking</button>" +
             " <button class='pt-mini bad' data-decline='" + b.id + "'>Not proceeding</button>";
    } else if (b.status === "confirmed") {
      acts = "<button class='pt-mini' data-flown='" + b.id + "'>Mark flown</button>";
    }
    if (b.agent_email) acts += " <a class='pt-mini' target='_blank' href='" + mailtoConfirm(b) + "'>Email agent</a>";
    return "<tr><td><b>" + esc(b.ref || "") + "</b><br><small>" + b.created_at.slice(0, 10) + "</small></td>" +
      "<td>" + esc(b.agency_name || "KEA staff") + "<br><small>" + esc(b.agent_email || "") + " \u00b7 " + esc(b.agent_phone || b.contact_phone || "") + "</small></td>" +
      "<td>" + esc(b.from_name || "") + " \u2192 " + esc(b.to_name || "") + "<br><small>" + esc(b.requested_date || "flexible") +
      " \u00b7 " + (b.pax || "?") + " pax \u00b7 " + esc(b.aircraft_code || "") + "</small></td>" +
      "<td>" + money(b.value_usd) + "<br><small>net " + money(b.net_total) + "</small></td>" +
      "<td><small>" + esc(b.client_ref || "-") + "</small></td>" +
      "<td><span class='pt-pill " + cls + "'>" + esc(b.status) + "</span></td><td>" + acts + "</td></tr>";
  }).join("");
  $("#pt-queue-body").innerHTML = rows || "<tr><td colspan=7>No booking requests yet.</td></tr>";
  var open = (r.data || []).filter(function (b) { return b.status === "requested" || b.status === "quoted"; }).length;
  $("#pt-queue-count").textContent = open ? open + " request(s) awaiting action." : "Nothing outstanding.";
}

function mailtoConfirm(b) {
  var sub = "KEA booking " + (b.ref || "") + (b.status === "confirmed" ? " \u2014 confirmed" : " \u2014 update");
  var body = "Dear " + (b.contact_name || "colleague") + ",\n\n" +
    (b.status === "confirmed"
      ? "We are pleased to confirm your charter booking with Kampala Executive Aviation.\n\n"
      : "Thank you for your booking request. Details below.\n\n") +
    "Reference: " + (b.ref || "") + "\n" +
    "Route: " + (b.from_name || "") + " to " + (b.to_name || "") + "\n" +
    "Date: " + (b.requested_date || "to be confirmed") + "\n" +
    "Passengers: " + (b.pax || "") + "\n" +
    "Aircraft: " + (b.aircraft_code || "") + "\n" +
    "Price: " + money(b.value_usd) + " USD\n" +
    (b.ops_notes ? "Notes: " + b.ops_notes + "\n" : "") +
    "\nYou can view this booking any time in the KEA Trade Portal:\nhttps://www.flykea.com/agents/\n\n" +
    "Kind regards,\nReservations\nKampala Executive Aviation\n+256 776 333 114 \u00b7 reservations@flykea.com";
  return "mailto:" + encodeURIComponent(b.agent_email) + "?subject=" + encodeURIComponent(sub) + "&body=" + encodeURIComponent(body);
}

async function setBooking(id, status) {
  var patch = { status: status };
  if (status === "confirmed") {
    patch.confirmed_at = new Date().toISOString();
    patch.confirmation_ref = "KEA-CONF-" + Math.floor(Math.random() * 9000 + 1000);
    var n = prompt("Note for the agent? (aircraft reg, timings \u2014 optional)");
    if (n) patch.ops_notes = n;
  }
  if (status === "lost") {
    var c = prompt("Reason code \u2014 one of: " + LOSS.map(function (l) { return l.code; }).join(", "));
    if (!c) return;
    patch.loss_reason_code = c.trim();
    patch.loss_notes = prompt("Notes (optional)") || null;
  }
  busy(true);
  var r = await sb.from("booking_requests").update(patch).eq("id", id);
  busy(false);
  if (r.error) { toast(r.error.message, true); return; }
  if (status === "confirmed" || status === "flown") {
    var ok = await mail("booking_status", id);
    toast(ok ? "Booking " + status + " \u2014 the agent has been emailed."
             : "Booking " + status + ", but the email did not send (check RESEND_API_KEY).", !ok);
  } else { toast("Booking marked " + status + "."); }
  loadQueue();
}

/* ================= STAFF: applications ================= */
async function loadApplications() {
  if (!IS_STAFF) return;
  var r = await sb.from("agents").select("*").order("applied_at", { ascending: false });
  $("#pt-apps-body").innerHTML = (r.data || []).map(function (a) {
    var act = a.status === "pending"
      ? "<button class='pt-mini ok' data-approve='" + a.id + "'>Approve</button> <button class='pt-mini bad' data-reject='" + a.id + "'>Reject</button>"
      : (a.status === "approved" ? "<button class='pt-mini' data-suspend='" + a.id + "'>Suspend</button>"
                                 : "<button class='pt-mini ok' data-approve='" + a.id + "'>Approve</button>");
    act += " <a class='pt-mini' target='_blank' href='" + mailtoWelcome(a) + "'>Email agent</a>";
    return "<tr><td>" + esc(a.agency_name) + "<br><small>" + esc(a.contact_name) + " \u00b7 " + esc(a.email) + "</small></td>" +
      "<td>" + esc([a.city, a.country].filter(Boolean).join(", ")) + "</td><td>" + a.applied_at.slice(0, 10) + "</td>" +
      "<td><span class='pt-pill " + (a.status === "approved" ? "ok" : a.status === "pending" ? "" : "bad") + "'>" + esc(a.status) + "</span></td>" +
      "<td>" + act + "</td></tr>";
  }).join("") || "<tr><td colspan=5>No applications yet.</td></tr>";
}

function mailtoWelcome(a) {
  var body = "Dear " + (a.contact_name || "colleague") + ",\n\n" +
    "Good news \u2014 your trade account for " + (a.agency_name || "your agency") + " has been approved.\n\n" +
    "Sign in to the KEA Trade Portal here:\nhttps://www.flykea.com/agents/\n\n" +
    "Your username is: " + a.email + "\n(use the password you chose when you applied)\n\n" +
    "Inside the portal you can:\n" +
    "  \u2022 Run instant charter quotes showing your agency net rate and margin\n" +
    "  \u2022 Build multi-leg itineraries across several airfields\n" +
    "  \u2022 Produce branded quotations for your own clients\n" +
    "  \u2022 Send booking requests straight to our reservations desk\n" +
    "  \u2022 View aircraft specifications and our charter terms\n\n" +
    "Tip: add your agency logo and address under Profile \u2014 they appear on the client quotations you generate.\n\n" +
    "Any questions, reply to this email or call +256 776 333 114.\n\n" +
    "Kind regards,\nKampala Executive Aviation\nGate 1, Kajjansi Airfield, Kampala\nreservations@flykea.com";
  return "mailto:" + encodeURIComponent(a.email) + "?subject=" + encodeURIComponent("Your KEA trade account is approved") + "&body=" + encodeURIComponent(body);
}

async function setAgentStatus(id, status) {
  busy(true);
  var patch = { status: status };
  if (status === "approved") { patch.approved_at = new Date().toISOString(); patch.approved_by = ME.id; }
  var r = await sb.from("agents").update(patch).eq("id", id);
  busy(false);
  if (r.error) { toast(r.error.message, true); return; }
  if (status === "approved") {
    var sent = await mail("agent_approved", id);
    toast(sent ? "Approved \u2014 the agency has been emailed."
               : "Approved, but the email did not send (check RESEND_API_KEY).", !sent);
  } else { toast("Agent " + status + "."); }
  loadApplications();
}

/* ================= STAFF: rate book ================= */
async function loadRates() {
  if (!IS_STAFF) return;
  var r = await sb.from("route_rates").select("*").order("aircraft_code").order("to_name");
  $("#pt-rates-body").innerHTML = (r.data || []).map(function (x) {
    return "<tr><td>" + esc(x.aircraft_code) + "</td><td>" + esc(x.to_name) + "</td>" +
      "<td><input class='pt-rate-in' data-id='" + x.id + "' type='number' step='1' value='" + (+x.rack) + "'></td>" +
      "<td>" + (x.verified ? "<span class='pt-pill ok'>verified</span>" : "<span class='pt-pill bad'>unverified</span>") + "</td>" +
      "<td><small>" + esc(x.note || "") + "</small></td>" +
      "<td><button class='pt-mini ok' data-rate-save='" + x.id + "'>Save &amp; verify</button>" +
      (x.verified ? " <button class='pt-mini' data-rate-unverify='" + x.id + "'>Unverify</button>" : "") + "</td></tr>";
  }).join("") || "<tr><td colspan=6>No route rates loaded.</td></tr>";
  var n = (r.data || []).filter(function (x) { return !x.verified; }).length;
  $("#pt-rates-count").textContent = n ? n + " rate(s) still need verifying \u2014 agents cannot see these yet."
                                       : "All rates verified and live to agents.";
}
async function saveRate(id, verify) {
  var inp = document.querySelector(".pt-rate-in[data-id='" + id + "']");
  var patch = { verified: verify };
  if (inp) patch.rack = +inp.value;
  if (verify) patch.note = "verified by KEA";
  busy(true);
  var r = await sb.from("route_rates").update(patch).eq("id", id);
  busy(false);
  if (r.error) { toast(r.error.message, true); return; }
  toast(verify ? "Rate verified \u2014 now live to agents." : "Rate hidden from agents.");
  loadRates(); loadReference();
}

/* ================= STAFF: reports ================= */
async function loadReports() {
  if (!IS_STAFF) return;
  var f  = await sb.from("v_funnel_monthly").select("*").limit(12);
  var bf = await sb.from("v_booking_funnel_monthly").select("*").limit(12);
  var lr = await sb.from("v_loss_reasons").select("*");
  var ap = await sb.from("v_agent_performance").select("*").limit(25);
  var rd = await sb.from("v_route_demand").select("*").limit(20);
  var ap2 = await sb.from("v_aircraft_popularity").select("*");
  var acBody = $("#rp-aircraft");
  if (acBody) acBody.innerHTML = (ap2.data || []).map(function (r) {
    return "<tr><td>" + esc(r.aircraft) + "</td><td>" + r.times_quoted + "</td><td>" + r.times_requested +
      "</td><td><b>" + (r.conversion_pct == null ? "\u2014" : r.conversion_pct + "%") + "</b></td>" +
      "<td>" + (r.avg_pax || "\u2014") + "</td><td>" + money(r.avg_rack) + "</td></tr>";
  }).join("") || "<tr><td colspan=6>No aircraft data yet.</td></tr>";
  var qa = await sb.from("v_quote_abandon_reasons").select("*");

  $("#rp-funnel").innerHTML = (f.data || []).map(function (r) {
    return "<tr><td>" + r.month + "</td><td>" + r.quotes + "</td><td>" + r.requests + "</td><td><b>" +
      (r.quote_to_request_pct == null ? "\u2014" : r.quote_to_request_pct + "%") + "</b></td><td>" + money(r.quoted_value) + "</td></tr>";
  }).join("") || "<tr><td colspan=5>No quote data yet.</td></tr>";

  $("#rp-bookings").innerHTML = (bf.data || []).map(function (r) {
    return "<tr><td>" + r.month + "</td><td>" + r.requests + "</td><td>" + r.confirmed + "</td><td>" + r.flown +
      "</td><td>" + r.lost + "</td><td><b>" + (r.request_to_confirmed_pct == null ? "\u2014" : r.request_to_confirmed_pct + "%") +
      "</b></td><td>" + money(r.won_value) + "</td></tr>";
  }).join("") || "<tr><td colspan=7>No booking data yet.</td></tr>";

  $("#rp-loss").innerHTML = (lr.data || []).map(function (r) {
    return "<tr><td>" + esc(r.reason) + "</td><td>" + r.lost_count + "</td><td>" + money(r.lost_value) + "</td><td>" + (r.pct_of_losses || 0) + "%</td></tr>";
  }).join("") || "<tr><td colspan=4>No losses recorded.</td></tr>";

  $("#rp-abandon").innerHTML = (qa.data || []).map(function (r) {
    return "<tr><td>" + esc(r.reason) + "</td><td>" + r.times_cited + "</td></tr>";
  }).join("") || "<tr><td colspan=2>No feedback yet.</td></tr>";

  $("#rp-agents").innerHTML = (ap.data || []).map(function (r) {
    return "<tr><td>" + esc(r.agency_name) + "</td><td>" + esc(r.country || "") + "</td><td>" + (r.quotes || 0) +
      "</td><td>" + (r.requests || 0) + "</td><td>" + (r.won || 0) + "</td><td><b>" +
      (r.quote_to_won_pct == null ? "\u2014" : r.quote_to_won_pct + "%") + "</b></td><td>" + money(r.won_value) + "</td></tr>";
  }).join("") || "<tr><td colspan=7>No agent activity yet.</td></tr>";

  $("#rp-routes").innerHTML = (rd.data || []).map(function (r) {
    return "<tr><td>" + esc(r.route) + "</td><td>" + r.times_quoted + "</td><td>" + r.times_requested +
      "</td><td>" + (r.avg_nm || 0) + " nm</td><td>" + money(r.avg_rack) + "</td></tr>";
  }).join("") || "<tr><td colspan=5>No route data yet.</td></tr>";
}

function exportCSV(tableId, filename) {
  var rows = $$("#" + tableId + " tr").map(function (tr) {
    return $$("th,td", tr).map(function (c) { return '"' + c.textContent.replace(/"/g, '""').trim() + '"'; }).join(",");
  }).join("\n");
  var a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([rows], { type: "text/csv" }));
  a.download = filename; a.click();
}

/* ================= APPLY / LOGIN ================= */
async function doApply(ev) {
  ev.preventDefault();
  var err = $("#pt-apply-err"); if (err) { err.hidden = true; err.textContent = ""; }
  busy(true);
  var email = $("#ap-email").value.trim(), pw = $("#ap-pass").value;
  var meta = {
    agency_name: $("#ap-agency").value.trim(), contact_name: $("#ap-contact").value.trim(),
    phone: $("#ap-phone").value.trim(), country: $("#ap-country").value.trim(),
    city: $("#ap-city").value.trim(), website: $("#ap-website").value.trim(), tc_version: TC_VERSION
  };
  var su = await sb.auth.signUp({ email: email, password: pw,
    options: { data: meta, emailRedirectTo: location.origin + "/agents/" } });
  busy(false);
  if (su.error) { if (err) { err.textContent = su.error.message; err.hidden = false; } toast(su.error.message, true); return; }
  try {
    await fetch("https://formsubmit.co/ajax/" + RESERVATIONS, {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({ _subject: "New trade agent application \u2014 " + meta.agency_name,
        message: "Agency: " + meta.agency_name + "\nContact: " + meta.contact_name + "\nEmail: " + email +
                 "\nPhone: " + meta.phone + "\nCity: " + meta.city + "\nCountry: " + meta.country +
                 "\nWebsite: " + meta.website + "\n\nApprove in the KEA Trade Portal -> Agents tab." })
    });
  } catch (e) {}
  // Supabase returns a decoy user (empty identities) when the address is already
  // registered and sends NO email, so don't promise a link that will never arrive.
  var u = su.data && su.data.user;
  if (u && Array.isArray(u.identities) && u.identities.length === 0) {
    var msg = "An account already exists for " + email + ". Please sign in instead \u2014 " +
              "or use \u201CForgot password\u201D on the sign-in screen if you can\u2019t get in.";
    if (err) { err.textContent = msg; err.hidden = false; }
    toast("That email already has an account \u2014 sign in instead.", true);
    return;
  }
  if (su.data && su.data.session) { await onSession(su.data.session); return; }
  $("#pt-confirm-email").textContent = email;
  gate("confirm");
}

async function doLogin(ev) {
  ev.preventDefault(); busy(true);
  var r = await sb.auth.signInWithPassword({ email: $("#li-email").value.trim(), password: $("#li-pass").value });
  busy(false);
  if (r.error) toast(r.error.message, true);
}
async function doReset() {
  var em = ($("#li-email").value || "").trim();
  if (!em) { toast("Enter your email first.", true); return; }
  await sb.auth.resetPasswordForEmail(em, { redirectTo: location.origin + "/agents/" });
  toast("Password reset link sent.");
}

/* ================= WIRE UP ================= */
document.addEventListener("DOMContentLoaded", function () {
  if (!$("#pt-root")) return;
  var d = $("#pt-date"); if (d) d.value = new Date(Date.now() + 3 * 864e5).toISOString().slice(0, 10);

  $$(".pt-tab").forEach(function (t) { t.addEventListener("click", function () { show(t.dataset.go); }); });
  $$("[data-gateswap]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); gate(b.dataset.gateswap); }); });
  $$(".pt-signout").forEach(function (b) { b.addEventListener("click", async function () { await sb.auth.signOut(); location.reload(); }); });

  $("#pt-apply-form").addEventListener("submit", doApply);
  $("#pt-login-form").addEventListener("submit", doLogin);
  $("#pt-reset").addEventListener("click", function (e) { e.preventDefault(); doReset(); });

  $("#pt-calc").addEventListener("click", calculate);
  $("#pt-pin") && $("#pt-pin").addEventListener("click", openPinMap);
  $("#pt-pin-close") && $("#pt-pin-close").addEventListener("click", closePinMap);
  $("#pt-pin-use") && $("#pt-pin-use").addEventListener("click", function () {
    var v = this.dataset.coord;
    if (!v) { toast("Tap the map to drop a pin first.", true); return; }
    $("#pt-coord").value = v; closePinMap();
    toast("Coordinates set \u2014 recalculating."); calculate();
  });
  $("#pt-addleg").addEventListener("click", addLeg);
  $("#pt-swap").addEventListener("click", function () {
    readLegs();
    var a = LEGS[0].from; LEGS[0].from = LEGS[0].to; LEGS[0].to = a;
    renderLegs(); if (LAST) calculate();
  });
  $("#pt-clientquote").addEventListener("click", clientQuote);
  $("#pt-book-form").addEventListener("submit", submitBooking);
  $("#pt-profile-form").addEventListener("submit", saveProfile);
  $("#pt-why-send").addEventListener("click", sendWhy);
  $("#pt-why-cancel").addEventListener("click", function () { $("#pt-whybox").hidden = true; });

  $("#pt-town").addEventListener("change", function () {
    var v = this.value.trim().toLowerCase();
    var t = TOWNS.filter(function (x) { return x.name.toLowerCase() === v; })[0];
    if (t) { $("#pt-coord").value = t.lat.toFixed(4) + ", " + t.lng.toFixed(4); if (LAST) calculate(); }
  });

  ["pt-pax", "pt-mission", "pt-ac", "pt-daystop", "pt-nights", "pt-date"].forEach(function (id) {
    var n = $("#" + id); if (n) n.addEventListener("change", function () { if (LAST) calculate(); });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" || !e.target.classList) return;
    if (e.target.classList.contains("pt-leg-to") || e.target.classList.contains("pt-leg-from") || e.target.id === "pt-coord") {
      e.preventDefault(); calculate();
    }
  });

  document.addEventListener("click", function (e) {
    var t = e.target;
    var rm = t.closest("[data-rmleg]");         if (rm) removeLeg(+rm.dataset.rmleg);
    var bk = t.closest("[data-book]");          if (bk && QMAP[bk.dataset.book]) openBookingFor(QMAP[bk.dataset.book]);
    var cn = t.closest(".pt-car-nav");
    if (cn) { carouselGo(cn.dataset.car, +cn.dataset.step, true); return; }
    var cd = t.closest(".pt-dot");
    if (cd) { carouselGo(cd.dataset.car, +cd.dataset.slide, false); return; }
    var dq = t.closest("[data-delq]");            if (dq) deleteQuote(dq.dataset.delq);
    var nb = t.closest("[data-nobook]");        if (nb && QMAP[nb.dataset.nobook]) openWhyFor(QMAP[nb.dataset.nobook]);
    var ok = t.closest("[data-accept]");        if (ok) setBooking(ok.dataset.accept, "confirmed");
    var dc = t.closest("[data-decline]");       if (dc) setBooking(dc.dataset.decline, "lost");
    var fl = t.closest("[data-flown]");         if (fl) setBooking(fl.dataset.flown, "flown");
    var ap = t.closest("[data-approve]");       if (ap) setAgentStatus(ap.dataset.approve, "approved");
    var rj = t.closest("[data-reject]");        if (rj) setAgentStatus(rj.dataset.reject, "rejected");
    var sp = t.closest("[data-suspend]");       if (sp) setAgentStatus(sp.dataset.suspend, "suspended");
    var rs = t.closest("[data-rate-save]");     if (rs) saveRate(rs.dataset.rateSave, true);
    var ru = t.closest("[data-rate-unverify]"); if (ru) saveRate(ru.dataset.rateUnverify, false);
    var cs = t.closest("[data-csv]");           if (cs) exportCSV(cs.dataset.csv, cs.dataset.csv + ".csv");
  });

  boot();
});
})();
