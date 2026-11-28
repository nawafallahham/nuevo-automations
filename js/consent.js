/* Cookie consent + gated Meta Pixel loading.
 *
 * The pixel is deliberately NOT in the page markup. It is injected here only
 * after consent is granted, so declining actually prevents tracking rather
 * than just hiding a banner. Lead handlers elsewhere already guard on
 * `typeof fbq === 'function'`, so they no-op until this runs.
 */
(function () {
  'use strict';

  var PIXEL_ID = '997785509848718';
  var GA_ID = 'G-1FF7172KH1';
  // Microsoft Clarity (heatmaps + session recordings). Free; paste the
  // project id from clarity.microsoft.com -> Settings -> Setup. Empty = off.
  var CLARITY_ID = 'zk7ajob7cv';
  var STORE_KEY = 'nuevo-consent';

  function read() {
    try { return localStorage.getItem(STORE_KEY); } catch (e) { return null; }
  }
  function write(v) {
    try { localStorage.setItem(STORE_KEY, v); } catch (e) {}
  }

  function loadPixel() {
    if (window.fbq) return;
    /* eslint-disable */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
      n.queue = []; t = b.createElement(e); t.async = !0; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */
    window.fbq('init', PIXEL_ID);
    window.nuevoPixelId = PIXEL_ID;
    window.nuevoMeta('PageView');
  }

  /* Meta event helper: fires the pixel and sends the same event from our
     server (/api/meta-event, Conversions API) with one shared event id, so
     Meta counts it once and still gets it when an ad blocker stops the
     pixel. Does nothing until the visitor accepts cookies.
     nuevoMeta(name, params, custom) — custom=true for trackCustom events. */
  var metaSeq = 0;
  var pageKey = Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
  var STANDARD = { PageView: 1, Contact: 1, Lead: 1, Schedule: 1, SubmitApplication: 1 };
  window.nuevoMeta = function (name, params) {
    if (read() !== 'granted' || typeof window.fbq !== 'function') return;
    params = params || {};
    var eventId = 'ev.' + pageKey + '.' + (++metaSeq) + '.' + name;
    window.fbq(STANDARD[name] ? 'track' : 'trackCustom', name, params, { eventID: eventId });
    // Give the pixel a moment to set its _fbp cookie, then send the copy.
    setTimeout(function () {
      var attr = null;
      try { attr = typeof window.nuevoAttribution === 'function' ? window.nuevoAttribution() : null; } catch (e) {}
      var payload = JSON.stringify({
        name: name, event_id: eventId, consent: true, page_url: location.href,
        content_name: params.content_name || null, video_id: params.video_id || null,
        percent: params.percent || null,
        fbp: attr && attr.fbp || null, fbc: attr && attr.fbc || null
      });
      try {
        if (navigator.sendBeacon && navigator.sendBeacon('/api/meta-event', new Blob([payload], { type: 'application/json' }))) return;
      } catch (e) {}
      try { fetch('/api/meta-event', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: payload, keepalive: true }); } catch (e) {}
    }, name === 'PageView' ? 1500 : 0);
  };

  // Google Analytics 4, under the same consent as the pixel.
  function loadAnalytics() {
    if (window.gtag) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
    var t = document.createElement('script');
    t.async = true;
    t.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(t);
  }

  function loadClarity() {
    if (!CLARITY_ID || window.clarity) return;
    /* eslint-disable */
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
    /* eslint-enable */
    window.clarity('consent');
    // Tags to filter recordings by: where the visitor came from, the
    // campaign, the page they landed on, and their best outcome so far.
    try {
      var a = typeof window.nuevoAttribution === 'function' ? window.nuevoAttribution() : {};
      var src = a.utm_source || (a.fbclid ? 'facebook' : '') || hostOnly(a.referrer) || 'direct';
      window.clarity('set', 'source', src.slice(0, 50));
      if (a.utm_campaign) window.clarity('set', 'campaign', String(a.utm_campaign).slice(0, 100));
      if (a.utm_content) window.clarity('set', 'ad', String(a.utm_content).slice(0, 100));
      if (a.landing) window.clarity('set', 'landing', String(a.landing).split('?')[0].slice(0, 100));
      window.clarity('set', 'outcome', bestOutcome() || 'none');
    } catch (e) {}
    try { window.dispatchEvent(new Event('nuevo:clarity')); } catch (e) {}
  }
  function hostOnly(u) {
    try { return u ? new URL(u).hostname.replace(/^www\./, '') : ''; } catch (e) { return ''; }
  }

  /* Clarity conversion events: nuevoClarity('lead_contact') etc. Each one is
     a custom event (for funnels and filters), raises the session's
     "outcome" tag to the best step reached, and asks Clarity to keep the
     recording. Before consent (or with no Clarity) it does nothing. */
  var OUTCOMES = ['whatsapp_click', 'book_click', 'lead_declined', 'lead_contact', 'lead_qualified', 'booked'];
  var OUTCOME_KEY = 'nuevo-outcome';
  function bestOutcome() {
    try { return sessionStorage.getItem(OUTCOME_KEY) || ''; } catch (e) { return ''; }
  }
  window.nuevoClarity = function (name) {
    if (typeof window.clarity !== 'function') return;
    window.clarity('event', name);
    var rank = OUTCOMES.indexOf(name);
    if (rank < 0) return;
    if (rank > OUTCOMES.indexOf(bestOutcome())) {
      try { sessionStorage.setItem(OUTCOME_KEY, name); } catch (e) {}
      window.clarity('set', 'outcome', name);
    }
    if (rank >= OUTCOMES.indexOf('lead_contact')) window.clarity('upgrade', name);
  };

  function loadTrackers() { loadPixel(); loadAnalytics(); loadClarity(); }

  // The notice is a small card at the foot of the screen (styles in /css/site.css).
  // Accept and Decline carry equal weight. While it shows, the body is padded by
  // its height so it never covers the page's last lines.
  function banner() {
    var box = document.createElement('div');
    box.className = 'consent';
    box.setAttribute('role', 'region');
    // Arabic pages (/ar/) get the same notice in Arabic.
    var ar = document.documentElement.lang === 'ar';
    box.setAttribute('aria-label', ar ? 'الموافقة على ملفات تعريف الارتباط' : 'Cookie consent');
    box.innerHTML = ar
      ? '<p>نستخدم ملفات تعريف الارتباط لقياس إعلاناتنا وطريقة استخدام الموقع. <a href="/privacy/">سياسة الخصوصية</a></p>' +
        '<div class="consent-row">' +
        '<button type="button" class="btn btn--primary consent-yes">موافق</button>' +
        '<button type="button" class="btn btn--primary consent-no">رفض</button>' +
        '</div>'
      : '<p>We use cookies to measure our ads and how the site is used. <a href="/privacy/">Privacy policy</a></p>' +
        '<div class="consent-row">' +
        '<button type="button" class="btn btn--primary consent-yes">Accept</button>' +
        '<button type="button" class="btn btn--primary consent-no">Decline</button>' +
        '</div>';
    // after the header, so keyboard and screen reader users reach it early
    var header = document.querySelector('body > header');
    if (header) header.insertAdjacentElement('afterend', box);
    else document.body.insertBefore(box, document.body.firstChild);
    var pad = function () { document.body.style.paddingBottom = (box.offsetHeight + 32) + 'px'; };
    pad();
    window.addEventListener('resize', pad);
    // step aside while the footer is on screen, so its contact links stay readable and tappable
    var foot = document.querySelector('footer');
    var io = null;
    if (foot && 'IntersectionObserver' in window) {
      io = new IntersectionObserver(function (es) { box.hidden = es[es.length - 1].isIntersecting; });
      io.observe(foot);
    }

    function close(choice) {
      write(choice);
      // Don't strand keyboard focus on a button that's about to disappear.
      if (box.contains(document.activeElement)) {
        var main = document.querySelector('main');
        if (main) { main.setAttribute('tabindex', '-1'); main.focus({ preventScroll: true }); }
      }
      box.remove();
      window.removeEventListener('resize', pad);
      if (io) io.disconnect();
      document.body.style.paddingBottom = '';
      if (choice === 'granted') loadTrackers();
    }
    box.querySelector('.consent-yes').addEventListener('click', function () { close('granted'); });
    box.querySelector('.consent-no').addEventListener('click', function () { close('denied'); });
  }

  var choice = read();
  if (choice === 'granted') {
    loadTrackers();
  } else if (choice !== 'denied') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', banner);
    } else {
      banner();
    }
  }

  // GA4 event, a no-op until consent loads gtag.
  window.nuevoGa = function (name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
  };

  window.NuevoConsent = {
    state: function () { return read(); },
    reset: function () {
      try { localStorage.removeItem(STORE_KEY); } catch (e) {}
    }
  };
}());
