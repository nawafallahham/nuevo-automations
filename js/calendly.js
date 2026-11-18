/* ================= Calendly booking embed =================
   Shared by /book/ and /consultation/. Expects a .cal-embed container
   (data-source) holding a .calendly-inline-widget div. Calendly's script
   loads only when the container nears the viewport. The scheduled booking
   reaches us twice: Calendly's signed webhook (the booking itself) and the
   beacon below (consent + first-touch attribution for Meta CAPI). */
(function () {
  'use strict';

  var EVENT_URL = 'https://calendly.com/nawaf-allahham02/30min';
  var WIDGET_JS = 'https://assets.calendly.com/assets/external/widget.js';
  var WIDGET_CSS = 'https://assets.calendly.com/assets/external/widget.css';
  var ORIGIN = 'https://calendly.com';

  var box = document.querySelector('.cal-embed');
  var widget = box && box.querySelector('.calendly-inline-widget');
  if (!box || !widget) return;

  var source = box.getAttribute('data-source') || 'site';
  var sent = {};          // analytics events fire once per page

  function consentGranted() {
    try { return localStorage.getItem('nuevo-consent') === 'granted'; } catch (e) { return false; }
  }
  function attribution() {
    try { return typeof window.nuevoAttribution === 'function' ? window.nuevoAttribution() : null; } catch (e) { return null; }
  }

  // Calendly only accepts the five utm_* params for tracking. Prefer the
  // stored first touch, fall back to this page's query string.
  function embedUrl() {
    var a = attribution() || {};
    var q = new URLSearchParams(location.search);
    var params = ['hide_gdpr_banner=1', 'primary_color=1a5fa0', 'text_color=101a2b'];
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
      var v = a[k] || q.get(k);
      if (v) params.push(k + '=' + encodeURIComponent(String(v).slice(0, 150)));
    });
    return EVENT_URL + '?' + params.join('&');
  }

  // --- lazy load ---------------------------------------------------
  var loading = false;
  function fail() {
    box.classList.add('is-failed');
    widget.innerHTML = '<p class="cal-embed__msg">The calendar didn’t load. ' +
      '<a href="' + embedUrl() + '" target="_blank" rel="noopener">Open it on Calendly</a> or message us on WhatsApp below.</p>';
  }
  function init() {
    if (!window.Calendly || typeof window.Calendly.initInlineWidget !== 'function') { fail(); return; }
    var url = embedUrl();
    widget.setAttribute('data-url', url);
    widget.innerHTML = '';
    window.Calendly.initInlineWidget({ url: url, parentElement: widget });
    box.classList.add('is-loaded');
  }
  function load() {
    if (loading) return;
    loading = true;
    var css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = WIDGET_CSS;
    document.head.appendChild(css);
    var s = document.createElement('script');
    s.src = WIDGET_JS;
    s.async = true;
    s.onload = init;
    s.onerror = fail;
    document.head.appendChild(s);
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); load(); }
    }, { rootMargin: '600px 0px' });
    io.observe(box);
  } else {
    load();
  }

  // --- Calendly events -----------------------------------------------
  function track(type) {
    if (sent[type] || typeof window.nuevoTrack !== 'function') return;
    sent[type] = true;
    window.nuevoTrack(type);
  }

  function scheduled(payload) {
    var inviteeUri = payload && payload.invitee && payload.invitee.uri;
    var eventUri = payload && payload.event && payload.event.uri;
    if (!inviteeUri || sent[inviteeUri]) return;
    sent[inviteeUri] = true;

    // The invitee uri is also the server's CAPI event_id -> deduplicated.
    if (typeof window.fbq === 'function') {
      window.fbq('track', 'Schedule', { content_name: 'calendly' }, { eventID: inviteeUri });
    }
    try {
      fetch('/api/calendly/scheduled', {
        method: 'POST',
        keepalive: true,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          invitee_uri: inviteeUri,
          event_uri: eventUri || null,
          consent: consentGranted(),
          attribution: attribution(),
          page_url: location.href,
          source: source
        })
      }).catch(function () {});
    } catch (e) {}
  }

  window.addEventListener('message', function (e) {
    if (e.origin !== ORIGIN || !e.data || typeof e.data.event !== 'string') return;
    switch (e.data.event) {
      case 'calendly.event_type_viewed': track('book_view'); break;
      case 'calendly.date_and_time_selected': track('book_start'); break;
      case 'calendly.event_scheduled': scheduled(e.data.payload); break;
    }
  });
}());
