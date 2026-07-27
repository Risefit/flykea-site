/* ===== KEA Trade Portal =====================================================
   Agent accounts, charter calculator (rack / net / margin), booking requests,
   branded client quotes, and reservations/marketing funnel reports.
   Backend: Supabase (auth + Postgres + storage). Static-site friendly.
   ========================================================================== */
(function () {
"use strict";

/* ---------- CONFIG (safe to publish: publishable key + RLS) ---------- */
var SUPABASE_URL = "https://utlynkvxqdplfrsxxrez.supabase.co";
var SUPABASE_KEY = "sb_publishable_f28aljVLZ6dEx2NUOdZqEg_bvosgf0d";
var RESERVATIONS = "reservations@flykea.com";
var WA_NUMBER    = "256776333114";
var TC_VERSION   = "2026.1";
var TAXI_HRS     = 0.5;      // taxi/climb allowance added to block time
var RANGE_PCT    = 0.10;     // +/- band on indicative pricing

var sb = null, ME = null, AGENT = null, IS_STAFF = false;
var PORTS = [], FLEET = [], LOSS = [], RATES = [], LAST = null;

/* ---------- tiny helpers ---------- */
function $(s, r) { return (r || document).querySelector(s); }
function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]; }); }
function money(n) { return n == null ? "—" : "$" + Math.round(n).toLocaleString("en-US"); }
function fmtHrs(h) { var m = Math.round(h * 60); return Math.floor(m / 60) + "h " + ("0" + (m % 60)).slice(-2) + "m"; }
function today() { return new Date().toISOString().slice(0, 10); }
function toast(msg, bad) {
  var t = el("div", "pt-toast" + (bad ? " bad" : ""), esc(msg));
  document.body.appendChild(t);
  setTimeout(function () { t.classList.add("go"); }, 10);
  setTimeout(function () { t.remove(); }, 4200);
}
function busy(on) { document.body.classList.toggle("pt-busy", !!on); }

/* ---------- pricing (mirrors KEA charter model: return positioning) ---------- */
function haversineNm(a, b) {
  var R = 6371, r = Math.PI / 180;
  var dLa = (b[0] - a[0]) * r, dLo = (b[1] - a[1]) * r, la1 = a[0] * r, la2 = b[0] * r;
  var x = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(la1) * Math.cos(la2) * Math.sin(dLo / 2) * Math.sin(dLo / 2);
  return (R * 2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x))) / 1.852;
}
function bookRate(acCode, fromName, toName) {
  var f = (fromName || "").toLowerCase(), t = (toName || "").toLowerCase();
  if (f.indexOf("kajjansi") < 0) return null;               // book row is Kajjansi return
  for (var i = 0; i < RATES.length; i++) {
    var r = RATES[i];
    if (r.aircraft_code !== acCode || !r.verified) continue;
    var rt = (r.to_name || "").toLowerCase();
    if (t === rt || t.indexOf(rt) === 0) return r;
  }
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
function price(ac, oneWayHrs, dayStop) {
  var block = oneWayHrs * 2 + TAXI_HRS;                 // aircraft returns to base
  var rack  = Math.max(+ac.min_charge || 0, block * +ac.hourly_rack);
  if (dayStop) rack += (+ac.day_stop || 0);
  var net    = rack * (+ac.net_factor || 0.9);
  return { block: block, rack: rack, net: net, margin: rack - net,
           lo: rack * (1 - RANGE_PCT), hi: rack * (1 + RANGE_PCT) };
}

/* ---------- view routing ---------- */
function show(view) {
  $$(".pt-view").forEach(function (v) { v.hidden = v.dataset.view !== view; });
  $$(".pt-tab").forEach(function (t) { t.classList.toggle("on", t.dataset.go === view); });
  if (view === "quotes")   loadMyQuotes();
  if (view === "bookings") loadMyBookings();
  if (view === "reports")  loadReports();
  if (view === "admin")    loadApplications();
  if (view === "rates")    loadRates();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ================= AUTH ================= */
async function boot() {
  if (!window.supabase) { console.warn("Supabase SDK missing"); return; }
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
  IS_STAFF = !!(st.data);
  if (!AGENT && !IS_STAFF) {
    var md = (ME.user_metadata || {});
    if (md.agency_name) {                       // confirmed but record missing - create it now
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
  $("#pt-app").hidden = true;
  $("#pt-gates").hidden = false;
  if (which === "pending" && AGENT) $("#pt-pending-name").textContent = AGENT.agency_name || "";
}

async function enterPortal() {
  $("#pt-gates").hidden = true;
  $("#pt-app").hidden = false;
  $("#pt-who").textContent = IS_STAFF ? "KEA staff" : (AGENT.agency_name || ME.email);
  $$(".pt-staff-only").forEach(function (n) { n.hidden = !IS_STAFF; });
  await loadReference();
  if (!IS_STAFF) fillProfileForm();
  show(IS_STAFF ? "reports" : "quote");
}

async function loadReference() {
  var a = await sb.from("aircraft").select("*").eq("active", true).order("sort_order");
  FLEET = a.data || [];
  var p = await sb.from("airfields").select("*").eq("active", true).order("sort_order").order("name");
  PORTS = p.data || [];
  var l = await sb.from("loss_reasons").select("*").eq("active", true).order("sort_order");
  LOSS = l.data || [];
  var rr = await sb.from("route_rates").select("*").order("to_name");
  RATES = rr.data || [];
  var dl = $("#pt-ports"); dl.innerHTML = "";
  PORTS.forEach(function (x) { var o = document.createElement("option"); o.value = x.name; dl.appendChild(o); });
  var ov = $("#pt-ac"); ov.innerHTML = '<option value="">Best match (automatic)</option>';
  FLEET.forEach(function (x) { var o = document.createElement("option"); o.value = x.code; o.textContent = x.name; ov.appendChild(o); });
  renderFleetSpecs();
  try { localStorage.setItem("kea_ref", JSON.stringify({ FLEET: FLEET, PORTS: PORTS, at: Date.now() })); } catch (e) {}
}

/* offline fallback for the calculator */
(function preloadOffline() {
  try {
    var c = JSON.parse(localStorage.getItem("kea_ref") || "null");
    if (c && c.FLEET) { FLEET = c.FLEET; PORTS = c.PORTS; }
  } catch (e) {}
})();

/* ================= CALCULATOR ================= */
function findPort(name) {
  name = (name || "").trim().toLowerCase();
  if (!name) return null;
  var f = PORTS.filter(function (p) { return p.name.toLowerCase() === name; });
  if (!f.length) f = PORTS.filter(function (p) { return p.name.toLowerCase().indexOf(name) >= 0; });
  return f[0] || null;
}

function calculate() {
  var A = findPort($("#pt-from").value), B = findPort($("#pt-to").value);
  var coordRaw = ($("#pt-coord").value || "").trim();
  var m = coordRaw.match(/(-?\d+\.?\d*)[ ,]+(-?\d+\.?\d*)/);
  if (m) B = { code: null, name: "Custom site " + (+m[1]).toFixed(3) + ", " + (+m[2]).toFixed(3), lat: +m[1], lng: +m[2], country_code: "XX" };
  if (!A || !B) { toast("Choose an origin and destination from the list.", true); return; }
  var pax = Math.max(1, +$("#pt-pax").value || 1);
  var mission = $("#pt-mission").value;
  var heli = mission === "site" || !!m;
  var hasCoords = A.lat != null && A.lng != null && B.lat != null && B.lng != null;
  var dist = hasCoords ? haversineNm([A.lat, A.lng], [B.lat, B.lng]) : 0;
  var forced = $("#pt-ac").value;
  var ac = forced ? FLEET.filter(function (x) { return x.code === forced; })[0] : pickAircraft(dist, pax, heli);
  if (!ac) { toast("No suitable aircraft found.", true); return; }
  var oneWay = hasCoords ? dist / (+ac.cruise_kt || 150) : 0;
  var dayStop = $("#pt-daystop").checked;
  var P = price(ac, oneWay, dayStop);

  // exact rate-book price wins over the hourly estimate
  var book = bookRate(ac.code, A.name, B.name), method = "estimate";
  if (book) {
    var rack = +book.rack + (dayStop ? (+ac.day_stop || 0) : 0);
    P = { block: P.block, rack: rack, net: rack * (+ac.net_factor || 0.9),
          margin: rack - rack * (+ac.net_factor || 0.9),
          lo: rack, hi: rack };
    method = "book";
  }
  var intl = (A.country_code !== "UG") || (B.country_code !== "UG");

  LAST = {
    from_code: A.code, to_code: B.code || null, from_name: A.name, to_name: B.name,
    custom_coords: m ? coordRaw : null, pax: pax, travel_date: $("#pt-date").value || null,
    mission: mission, aircraft_code: ac.code, aircraft: ac,
    distance_nm: +dist.toFixed(1), block_hours: +P.block.toFixed(2), day_stop: dayStop,
    rack_total: +P.rack.toFixed(2), net_total: +P.net.toFixed(2), margin: +P.margin.toFixed(2),
    is_international: intl, lo: P.lo, hi: P.hi, oneWay: oneWay, id: null,
    method: method, hasCoords: hasCoords
  };

  $("#pt-r-route").textContent = A.name + "  →  " + B.name;
  $("#pt-r-ac").textContent = ac.name;
  $("#pt-r-dist").textContent = hasCoords ? Math.round(dist) + " nm" : "—";
  $("#pt-r-time").textContent = hasCoords ? fmtHrs(oneWay + TAXI_HRS / 2) + " each way" : "on request";
  $("#pt-r-block").textContent = method === "book" ? "Rate book return price" : fmtHrs(P.block) + " block (return positioning)";
  $("#pt-r-rack").textContent = money(P.rack);
  $("#pt-r-net").textContent = money(P.net);
  $("#pt-r-margin").textContent = money(P.margin);
  $("#pt-r-band").textContent = method === "book" ? "fixed rate-book price" : money(P.lo) + " – " + money(P.hi);
  var badge = $("#pt-r-method");
  if (badge) {
    badge.textContent = method === "book" ? "RATE BOOK" : "ESTIMATE";
    badge.className = "pt-pill " + (method === "book" ? "ok" : "");
  }
  $("#pt-r-intl").hidden = !intl;
  $("#pt-result").hidden = false;
  $("#pt-result").scrollIntoView({ behavior: "smooth", block: "nearest" });
  saveQuote();
}

async function saveQuote() {
  if (!LAST || IS_STAFF || !navigator.onLine) return;
  var row = {
    agent_id: ME.id, from_code: LAST.from_code, to_code: LAST.to_code,
    from_name: LAST.from_name, to_name: LAST.to_name, custom_coords: LAST.custom_coords,
    pax: LAST.pax, travel_date: LAST.travel_date, mission: LAST.mission,
    aircraft_code: LAST.aircraft_code, distance_nm: LAST.distance_nm,
    block_hours: LAST.block_hours, day_stop: LAST.day_stop,
    rack_total: LAST.rack_total, net_total: LAST.net_total, margin: LAST.margin,
    is_international: LAST.is_international, source: "portal"
  };
  var r = await sb.from("quotes").insert(row).select("id").single();
  if (!r.error && r.data) LAST.id = r.data.id;
}

/* ================= BOOKING REQUEST ================= */
async function submitBooking(ev) {
  ev.preventDefault();
  if (!LAST) { toast("Run a quote first.", true); return; }
  busy(true);
  var payload = {
    quote_id: LAST.id, agent_id: ME.id,
    client_ref: $("#pt-b-ref").value || null,
    pax_details: $("#pt-b-pax").value || null,
    contact_phone: $("#pt-b-phone").value || AGENT.phone || null,
    notes: $("#pt-b-notes").value || null,
    requested_date: LAST.travel_date, value_usd: LAST.rack_total
  };
  var r = await sb.from("booking_requests").insert(payload).select("ref").single();
  busy(false);
  if (r.error) { toast("Could not submit: " + r.error.message, true); return; }

  // mirror to reservations@ so the desk sees it immediately
  var body = [
    "NEW TRADE BOOKING REQUEST — " + (r.data.ref || ""),
    "Agency: " + AGENT.agency_name, "Contact: " + AGENT.contact_name + " (" + AGENT.email + ")",
    "Phone: " + (payload.contact_phone || "-"),
    "", "Route: " + LAST.from_name + " -> " + LAST.to_name,
    "Date: " + (LAST.travel_date || "flexible") + "   Pax: " + LAST.pax,
    "Aircraft: " + LAST.aircraft.name, "Distance: " + Math.round(LAST.distance_nm) + " nm",
    "Block: " + fmtHrs(LAST.block_hours) + (LAST.day_stop ? " + day stop" : ""),
    "Rack: " + money(LAST.rack_total) + "   Agent net: " + money(LAST.net_total),
    "", "Client ref: " + (payload.client_ref || "-"),
    "Pax details: " + (payload.pax_details || "-"),
    "Notes: " + (payload.notes || "-")
  ].join("\n");
  try {
    await fetch("https://formsubmit.co/ajax/" + RESERVATIONS, {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({ _subject: "Trade booking request " + (r.data.ref || ""), message: body })
    });
  } catch (e) { /* database record is the source of truth */ }

  $("#pt-book-form").reset();
  $("#pt-booked-ref").textContent = r.data.ref || "";
  $("#pt-booked").hidden = false;
  toast("Booking request sent — reference " + (r.data.ref || ""));
}

/* agent tells us why a quote didn't convert */
async function sendFeedback(code, notes) {
  if (!LAST || !LAST.id) return;
  await sb.from("quote_feedback").insert({ quote_id: LAST.id, agent_id: ME.id, reason_code: code, notes: notes || null });
  toast("Thanks — that helps us price better.");
  $("#pt-why").hidden = true;
}

/* ================= MY QUOTES / BOOKINGS ================= */
async function loadMyQuotes() {
  var q = await sb.from("quotes").select("*").order("created_at", { ascending: false }).limit(100);
  var rows = (q.data || []).map(function (r) {
    return "<tr><td>" + r.created_at.slice(0, 10) + "</td><td>" + esc(r.from_name) + " → " + esc(r.to_name) +
      "</td><td>" + esc(r.aircraft_code || "") + "</td><td>" + r.pax + "</td><td>" + money(r.rack_total) +
      "</td><td>" + money(r.net_total) + "</td><td>" + (r.converted ? "<span class='pt-pill ok'>requested</span>" : "<span class='pt-pill'>quote</span>") + "</td></tr>";
  }).join("");
  $("#pt-quotes-body").innerHTML = rows || "<tr><td colspan=7>No quotes yet.</td></tr>";
}

async function loadMyBookings() {
  var b = await sb.from("booking_requests").select("*").order("created_at", { ascending: false }).limit(100);
  var rows = (b.data || []).map(function (r) {
    return "<tr><td>" + esc(r.ref || "") + "</td><td>" + r.created_at.slice(0, 10) + "</td><td>" +
      esc(r.client_ref || "-") + "</td><td>" + money(r.value_usd) + "</td><td><span class='pt-pill " +
      (r.status === "flown" || r.status === "confirmed" ? "ok" : (r.status === "lost" || r.status === "cancelled" ? "bad" : "")) +
      "'>" + esc(r.status) + "</span></td></tr>";
  }).join("");
  $("#pt-bookings-body").innerHTML = rows || "<tr><td colspan=5>No booking requests yet.</td></tr>";
}

/* ================= AIRCRAFT SPECS ================= */
function renderFleetSpecs() {
  var wrap = $("#pt-specs"); if (!wrap) return;
  wrap.innerHTML = FLEET.map(function (a) {
    return '<div class="pt-spec">' +
      (a.image_url ? '<img src="' + esc(a.image_url) + '" alt="' + esc(a.name) + '" loading="lazy">' : '<div class="pt-spec-noimg">' + esc(a.name) + '</div>') +
      '<div class="pt-spec-b"><h3>' + esc(a.name) + '</h3><dl>' +
      '<dt>Seats</dt><dd>' + a.seats + '</dd>' +
      '<dt>Cruise</dt><dd>' + a.cruise_kt + ' kt</dd>' +
      '<dt>Range</dt><dd>' + a.range_nm + ' nm</dd>' +
      '<dt>Baggage</dt><dd>' + esc(a.baggage || "—") + '</dd>' +
      '<dt>Strip</dt><dd>' + esc(a.strip_requirement || "—") + '</dd>' +
      '</dl><p>' + esc(a.spec_notes || "") + '</p></div></div>';
  }).join("");
}

/* ================= PROFILE (branding for client quotes) ================= */
function fillProfileForm() {
  if (!AGENT) return;
  $("#pf-agency").value  = AGENT.agency_name || "";
  $("#pf-contact").value = AGENT.contact_name || "";
  $("#pf-phone").value   = AGENT.phone || "";
  $("#pf-address").value = AGENT.address || "";
  $("#pf-city").value    = AGENT.city || "";
  $("#pf-country").value = AGENT.country || "";
  $("#pf-website").value = AGENT.website || "";
  if (AGENT.logo_url) $("#pf-logo-prev").src = AGENT.logo_url;
  $("#pf-logo-prev").hidden = !AGENT.logo_url;
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

/* ================= BRANDED CLIENT QUOTE (print / save as PDF) =================
   Deliberately shows the CLIENT price (rack) only — never net or margin.        */
function clientQuote() {
  if (!LAST) { toast("Run a quote first.", true); return; }
  var a = AGENT || {};
  var w = window.open("", "_blank");
  if (!w) { toast("Allow pop-ups to generate the quote.", true); return; }
  var ref = "Q-" + new Date().toISOString().slice(0, 10).replace(/-/g, "") + "-" + Math.floor(Math.random() * 900 + 100);
  var validTo = new Date(Date.now() + 14 * 864e5).toISOString().slice(0, 10);
  w.document.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>Charter Quote ' + ref + '</title>' +
  '<style>' +
  'body{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#1C2118;margin:0;padding:40px;max-width:800px}' +
  '.hd{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;border-bottom:3px solid #90B820;padding-bottom:18px}' +
  '.hd img{max-height:74px;max-width:230px;object-fit:contain}' +
  '.ag{font-size:12px;line-height:1.6;text-align:right;color:#566058}' +
  '.ag b{color:#1C2118;font-size:15px;display:block;margin-bottom:3px}' +
  'h1{font-size:23px;margin:26px 0 4px}.sub{color:#566058;font-size:13px;margin:0 0 22px}' +
  'table{width:100%;border-collapse:collapse;margin:18px 0}' +
  'td{padding:9px 0;border-bottom:1px solid #e6ebe1;font-size:14px}' +
  'td:first-child{color:#566058;width:38%}' +
  '.tot{margin-top:26px;background:#F5F8EE;border-left:4px solid #90B820;padding:18px 22px}' +
  '.tot .lbl{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#56750F}' +
  '.tot .amt{font-size:31px;font-weight:700;margin-top:4px}' +
  '.note{font-size:11.5px;color:#566058;line-height:1.65;margin-top:26px;border-top:1px solid #e6ebe1;padding-top:16px}' +
  '.ft{margin-top:30px;font-size:11px;color:#8a938a;text-align:center}' +
  '@media print{body{padding:16px}.no-print{display:none}}' +
  'button{background:#90B820;border:0;padding:11px 20px;border-radius:6px;font-weight:600;cursor:pointer;font-size:14px}' +
  '</style></head><body>' +
  '<div class="no-print" style="margin-bottom:18px"><button onclick="window.print()">Print / Save as PDF</button></div>' +
  '<div class="hd">' +
    (a.logo_url ? '<img src="' + esc(a.logo_url) + '" alt="">' : '<div style="font-size:20px;font-weight:700">' + esc(a.agency_name || "") + '</div>') +
    '<div class="ag"><b>' + esc(a.agency_name || "") + '</b>' +
      (a.address ? esc(a.address) + '<br>' : '') + (a.city ? esc(a.city) + '<br>' : '') +
      (a.country ? esc(a.country) + '<br>' : '') + (a.phone ? esc(a.phone) + '<br>' : '') +
      (a.email ? esc(a.email) + '<br>' : '') + (a.website ? esc(a.website) : '') +
    '</div></div>' +
  '<h1>Private Charter Quotation</h1>' +
  '<p class="sub">Reference ' + ref + ' &nbsp;·&nbsp; Issued ' + today() + ' &nbsp;·&nbsp; Valid until ' + validTo + '</p>' +
  '<table>' +
  '<tr><td>Route</td><td><b>' + esc(LAST.from_name) + ' &rarr; ' + esc(LAST.to_name) + '</b></td></tr>' +
  '<tr><td>Date of travel</td><td>' + esc(LAST.travel_date || "To be confirmed") + '</td></tr>' +
  '<tr><td>Passengers</td><td>' + LAST.pax + '</td></tr>' +
  '<tr><td>Aircraft</td><td>' + esc(LAST.aircraft.name) + ' &nbsp;(' + LAST.aircraft.seats + ' seats)</td></tr>' +
  '<tr><td>Flight time</td><td>' + fmtHrs(LAST.oneWay + TAXI_HRS / 2) + ' each way</td></tr>' +
  '<tr><td>Distance</td><td>' + Math.round(LAST.distance_nm) + ' nautical miles</td></tr>' +
  (LAST.day_stop ? '<tr><td>Aircraft waiting time</td><td>Same-day wait included</td></tr>' : '') +
  '</table>' +
  '<div class="tot"><div class="lbl">Total charter price</div><div class="amt">' + money(LAST.rack_total) + ' USD</div></div>' +
  '<div class="note"><b>Included:</b> aircraft, crew, fuel and standard insurance for the routing shown. ' +
  'The aircraft is chartered for the whole journey including positioning to and from base.<br>' +
  '<b>Not included:</b> landing, parking and handling fees, navigation charges, government taxes, ' +
  'passenger service charges, catering, ground transfers and any overnight crew costs, unless stated.<br>' +
  '<b>Terms:</b> quotation subject to aircraft availability at time of booking and to final confirmation of ' +
  'routing, timings and payload. Weather, air traffic control and operational requirements may affect timings. ' +
  'Prices are indicative and may vary by approximately 10% pending final routing and fees.</div>' +
  '<div class="ft">Flight operated by Kampala Executive Aviation — Ugandan CAA AOC 097 · Gate 1, Kajjansi Airfield, Kampala</div>' +
  '</body></html>');
  w.document.close();
}

/* ================= STAFF: applications ================= */
async function loadApplications() {
  if (!IS_STAFF) return;
  var r = await sb.from("agents").select("*").order("applied_at", { ascending: false });
  var rows = (r.data || []).map(function (a) {
    var act = a.status === "pending"
      ? '<button class="pt-mini ok" data-approve="' + a.id + '">Approve</button> <button class="pt-mini bad" data-reject="' + a.id + '">Reject</button>'
      : (a.status === "approved" ? '<button class="pt-mini" data-suspend="' + a.id + '">Suspend</button>'
                                 : '<button class="pt-mini ok" data-approve="' + a.id + '">Approve</button>');
    return "<tr><td>" + esc(a.agency_name) + "<br><small>" + esc(a.contact_name) + " · " + esc(a.email) + "</small></td>" +
      "<td>" + esc([a.city, a.country].filter(Boolean).join(", ")) + "</td>" +
      "<td>" + a.applied_at.slice(0, 10) + "</td>" +
      "<td><span class='pt-pill " + (a.status === "approved" ? "ok" : a.status === "pending" ? "" : "bad") + "'>" + esc(a.status) + "</span></td>" +
      "<td>" + act + "</td></tr>";
  }).join("");
  $("#pt-apps-body").innerHTML = rows || "<tr><td colspan=5>No applications yet.</td></tr>";
}

async function setAgentStatus(id, status) {
  busy(true);
  var patch = { status: status };
  if (status === "approved") { patch.approved_at = new Date().toISOString(); patch.approved_by = ME.id; }
  var r = await sb.from("agents").update(patch).eq("id", id);
  busy(false);
  if (r.error) { toast(r.error.message, true); return; }
  toast("Agent " + status + ".");
  loadApplications();
}

/* ================= STAFF: rate-book verification ================= */
async function loadRates() {
  if (!IS_STAFF) return;
  var r = await sb.from("route_rates").select("*").order("aircraft_code").order("to_name");
  var rows = (r.data || []).map(function (x) {
    return "<tr><td>" + esc(x.aircraft_code) + "</td><td>" + esc(x.to_name) + "</td>" +
      "<td><input class='pt-rate-in' data-id='" + x.id + "' type='number' step='1' value='" + (+x.rack) + "' style='width:110px;padding:.35rem;border:1px solid var(--line-dark);border-radius:5px'></td>" +
      "<td>" + (x.verified ? "<span class='pt-pill ok'>verified</span>" : "<span class='pt-pill bad'>unverified</span>") + "</td>" +
      "<td><small>" + esc(x.note || "") + "</small></td>" +
      "<td><button class='pt-mini ok' data-rate-save='" + x.id + "'>Save &amp; verify</button>" +
      (x.verified ? " <button class='pt-mini' data-rate-unverify='" + x.id + "'>Unverify</button>" : "") + "</td></tr>";
  }).join("");
  $("#pt-rates-body").innerHTML = rows || "<tr><td colspan=6>No route rates loaded.</td></tr>";
  var n = (r.data || []).filter(function (x) { return !x.verified; }).length;
  $("#pt-rates-count").textContent = n ? n + " rate(s) still need verifying — agents cannot see these yet." : "All rates verified and live to agents.";
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
  toast(verify ? "Rate verified — now live to agents." : "Rate hidden from agents.");
  loadRates(); loadReference();
}

/* ================= STAFF: funnel reports ================= */
async function loadReports() {
  if (!IS_STAFF) return;
  var f  = await sb.from("v_funnel_monthly").select("*").limit(12);
  var bf = await sb.from("v_booking_funnel_monthly").select("*").limit(12);
  var lr = await sb.from("v_loss_reasons").select("*");
  var ap = await sb.from("v_agent_performance").select("*").limit(25);
  var rd = await sb.from("v_route_demand").select("*").limit(20);
  var qa = await sb.from("v_quote_abandon_reasons").select("*");

  $("#rp-funnel").innerHTML = (f.data || []).map(function (r) {
    return "<tr><td>" + r.month + "</td><td>" + r.quotes + "</td><td>" + r.requests + "</td><td><b>" +
      (r.quote_to_request_pct == null ? "—" : r.quote_to_request_pct + "%") + "</b></td><td>" + money(r.quoted_value) + "</td></tr>";
  }).join("") || "<tr><td colspan=5>No quote data yet.</td></tr>";

  $("#rp-bookings").innerHTML = (bf.data || []).map(function (r) {
    return "<tr><td>" + r.month + "</td><td>" + r.requests + "</td><td>" + r.confirmed + "</td><td>" + r.flown +
      "</td><td>" + r.lost + "</td><td><b>" + (r.request_to_confirmed_pct == null ? "—" : r.request_to_confirmed_pct + "%") +
      "</b></td><td>" + money(r.won_value) + "</td></tr>";
  }).join("") || "<tr><td colspan=7>No booking data yet.</td></tr>";

  $("#rp-loss").innerHTML = (lr.data || []).map(function (r) {
    return "<tr><td>" + esc(r.reason) + "</td><td>" + r.lost_count + "</td><td>" + money(r.lost_value) +
      "</td><td>" + (r.pct_of_losses || 0) + "%</td></tr>";
  }).join("") || "<tr><td colspan=4>No losses recorded.</td></tr>";

  $("#rp-abandon").innerHTML = (qa.data || []).map(function (r) {
    return "<tr><td>" + esc(r.reason) + "</td><td>" + r.times_cited + "</td></tr>";
  }).join("") || "<tr><td colspan=2>No feedback yet.</td></tr>";

  $("#rp-agents").innerHTML = (ap.data || []).map(function (r) {
    return "<tr><td>" + esc(r.agency_name) + "</td><td>" + esc(r.country || "") + "</td><td>" + (r.quotes || 0) +
      "</td><td>" + (r.requests || 0) + "</td><td>" + (r.won || 0) + "</td><td><b>" +
      (r.quote_to_won_pct == null ? "—" : r.quote_to_won_pct + "%") + "</b></td><td>" + money(r.won_value) + "</td></tr>";
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

/* ================= FORMS: apply / login ================= */
async function doApply(ev) {
  ev.preventDefault();
  var err = $("#pt-apply-err"); if (err) { err.hidden = true; err.textContent = ""; }
  busy(true);
  var email = $("#ap-email").value.trim(), pw = $("#ap-pass").value;
  var meta = {
    agency_name: $("#ap-agency").value.trim(), contact_name: $("#ap-contact").value.trim(),
    phone: $("#ap-phone").value.trim(), country: $("#ap-country").value.trim(),
    city: $("#ap-city").value.trim(), website: $("#ap-website").value.trim(),
    tc_version: TC_VERSION
  };
  var su = await sb.auth.signUp({
    email: email, password: pw,
    options: { data: meta, emailRedirectTo: location.origin + "/agents/" }
  });
  busy(false);
  if (su.error) {
    if (err) { err.textContent = su.error.message; err.hidden = false; }
    toast(su.error.message, true);
    return;
  }
  // let reservations know an application has landed
  try {
    await fetch("https://formsubmit.co/ajax/" + RESERVATIONS, {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({ _subject: "New trade agent application — " + meta.agency_name,
        message: "Agency: " + meta.agency_name + "\nContact: " + meta.contact_name +
                 "\nEmail: " + email + "\nPhone: " + meta.phone +
                 "\nCity: " + meta.city + "\nCountry: " + meta.country +
                 "\nWebsite: " + meta.website +
                 "\n\nApprove in the KEA Trade Portal -> Agents tab." })
    });
  } catch (e) {}

  if (su.data && su.data.session) { await onSession(su.data.session); return; }  // confirmation off
  var em = $("#pt-confirm-email"); if (em) em.textContent = email;
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

/* ================= wire up ================= */
document.addEventListener("DOMContentLoaded", function () {
  if (!$("#pt-root")) return;

  $("#pt-date") && ($("#pt-date").value = new Date(Date.now() + 3 * 864e5).toISOString().slice(0, 10));

  $$(".pt-tab").forEach(function (t) { t.addEventListener("click", function () { show(t.dataset.go); }); });
  $$("[data-gateswap]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); gate(b.dataset.gateswap); }); });

  $("#pt-apply-form") && $("#pt-apply-form").addEventListener("submit", doApply);
  $("#pt-login-form") && $("#pt-login-form").addEventListener("submit", doLogin);
  $("#pt-reset") && $("#pt-reset").addEventListener("click", function (e) { e.preventDefault(); doReset(); });
  $$(".pt-signout").forEach(function (b) { b.addEventListener("click", async function () { await sb.auth.signOut(); location.reload(); }); });

  $("#pt-calc") && $("#pt-calc").addEventListener("click", calculate);
  $("#pt-swap") && $("#pt-swap").addEventListener("click", function () {
    var f = $("#pt-from"), t = $("#pt-to"), x = f.value; f.value = t.value; t.value = x; calculate();
  });
  ["pt-from", "pt-to", "pt-coord"].forEach(function (id) {
    var n = $("#" + id); n && n.addEventListener("keydown", function (e) { if (e.key === "Enter") calculate(); });
  });
  ["pt-ac", "pt-daystop", "pt-pax", "pt-mission"].forEach(function (id) {
    var n = $("#" + id); n && n.addEventListener("change", function () { if (LAST) calculate(); });
  });

  $("#pt-clientquote") && $("#pt-clientquote").addEventListener("click", clientQuote);
  $("#pt-book-form") && $("#pt-book-form").addEventListener("submit", submitBooking);
  $("#pt-profile-form") && $("#pt-profile-form").addEventListener("submit", saveProfile);

  $("#pt-nobook") && $("#pt-nobook").addEventListener("click", function () {
    var sel = $("#pt-why-reason");
    sel.innerHTML = LOSS.map(function (l) { return '<option value="' + l.code + '">' + esc(l.label) + "</option>"; }).join("");
    $("#pt-why").hidden = false;
  });
  $("#pt-why-send") && $("#pt-why-send").addEventListener("click", function () {
    sendFeedback($("#pt-why-reason").value, $("#pt-why-notes").value);
  });

  $("#pt-wa") && $("#pt-wa").addEventListener("click", function () {
    if (!LAST) { toast("Run a quote first.", true); return; }
    var msg = "KEA trade enquiry\nAgency: " + (AGENT ? AGENT.agency_name : "") +
      "\nRoute: " + LAST.from_name + " -> " + LAST.to_name +
      "\nDate: " + (LAST.travel_date || "flexible") + "\nPax: " + LAST.pax +
      "\nAircraft: " + LAST.aircraft.name;
    window.open("https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(msg), "_blank");
  });

  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-approve]"), r = e.target.closest("[data-reject]"), s = e.target.closest("[data-suspend]");
    if (a) setAgentStatus(a.dataset.approve, "approved");
    if (r) setAgentStatus(r.dataset.reject, "rejected");
    if (s) setAgentStatus(s.dataset.suspend, "suspended");
    var rs = e.target.closest("[data-rate-save]"), ru = e.target.closest("[data-rate-unverify]");
    if (rs) saveRate(rs.dataset.rateSave, true);
    if (ru) saveRate(ru.dataset.rateUnverify, false);
    var x = e.target.closest("[data-csv]");
    if (x) exportCSV(x.dataset.csv, x.dataset.csv + ".csv");
  });

  boot();
});
})();
