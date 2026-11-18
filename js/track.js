/* ================= First-party analytics + attribution =================
   Cookieless and anonymous: sends small beacons to /api/track (the server
   stores a daily-rotating hash, never the IP). Also remembers where the
   visitor first came from (utm_*, fbclid, referrer) so a booking can be
   credited to the right ad, and exposes window.nuevoAttribution(). */
(function () {
  'use strict';

  var KEY = 'nuevo-attr';
  var TTL = 30 * 24 * 60 * 60 * 1000; // keep first touch for 30 days
  var ENDPOINT = '/api/track';

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {}
  }
  function cookie(name) {
    var m = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
  }
  function externalRef() {
    var r = document.referrer || '';
    try { return r && new URL(r).hostname !== location.hostname ? r.slice(0, 300) : ''; } catch (e) { return ''; }
  }

  // --- first-touch attribution --------------------------------------
  var q = new URLSearchParams(location.search);
  var fields = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'fbclid'];
  var fromUrl = {};
  var hasUrl = false;
  fields.forEach(function (f) {
    var v = q.get(f);
    if (v) { fromUrl[f] = v.slice(0, 300); hasUrl = true; }
  });

  var now = Date.now();
  var attr = read();
  if (attr && (!attr.ts || now - attr.ts > TTL)) attr = null;

  if (!attr) {
    // First visit (or expired): record whatever we know, even if direct.
    attr = fromUrl;
    attr.landing = (location.pathname + location.search).slice(0, 300);
    attr.referrer = externalRef();
    attr.ts = now;
    if (fromUrl.fbclid) attr.fbc = 'fb.1.' + now + '.' + fromUrl.fbclid;
    write(attr);
  } else if (fromUrl.fbclid && fromUrl.fbclid !== attr.fbclid) {
    // Keep the first-touch source, but a fresh ad click id is what Meta
    // needs to match the conversion, so refresh only that.
    attr.fbclid = fromUrl.fbclid;
    attr.fbc = 'fb.1.' + now + '.' + fromUrl.fbclid;
    write(attr);
  }

  window.nuevoAttribution = function () {
    var a = read() || attr || {};
    var out = {};
    for (var k in a) if (Object.prototype.hasOwnProperty.call(a, k) && k !== 'ts') out[k] = a[k];
    var fbp = cookie('_fbp');
    var fbc = cookie('_fbc');
    if (fbp) out.fbp = fbp;
    if (fbc) out.fbc = fbc; // the pixel's own cookie wins over our rebuilt value
    return out;
  };

  // --- beacons --------------------------------------------------------
  function send(type, path) {
    var body = JSON.stringify({
      type: type,
      path: (path || location.pathname).slice(0, 200),
      ref: externalRef(),
      utm_source: attr.utm_source || '',
      utm_campaign: attr.utm_campaign || ''
    });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon(ENDPOINT, body)) return;
    } catch (e) {}
    try {
      fetch(ENDPOINT, { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'text/plain' } })
        .catch(function () {});
    } catch (e) {}
  }
  send('pageview');

  // book_view: once per page, on /book/ or when a #book section is seen.
  // The booking embed may report it too; both go through bookView().
  var bookSent = false;
  function bookView() {
    if (bookSent) return;
    bookSent = true;
    send('book_view');
  }
  window.nuevoTrack = function (type, path) {
    if (type === 'book_view') bookView(); else send(type, path);
  };
  if (/^\/book\/?$/.test(location.pathname)) {
    bookView();
  } else {
    var target = document.getElementById('book');
    var watch = function () {
      target = target || document.getElementById('book');
      if (!target) return;
      if (!('IntersectionObserver' in window)) { bookView(); return; }
      var io = new IntersectionObserver(function (entries) {
        if (entries.some(function (e) { return e.isIntersecting; })) { bookView(); io.disconnect(); }
      }, { threshold: 0.25 });
      io.observe(target);
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', watch);
    else watch();
  }

  // CTA clicks: booking buttons (.js-lead) and any WhatsApp link.
  document.addEventListener('click', function (e) {
    if (!e.target || !e.target.closest) return;
    var el = e.target.closest('.js-lead, a[href*="wa.me/"]');
    if (!el) return;
    var lead = el.getAttribute('data-lead') || (/wa\.me\//.test(el.getAttribute('href') || '') ? 'whatsapp' : 'other');
    send('cta', '/cta/' + lead.replace(/[^\w-]/g, '').slice(0, 60));
  }, true);
}());
