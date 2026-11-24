/* ================= Calendly booking embed =================
   Shared by /book/, /consultation/ and /wellness-brands/. Expects a
   .cal-embed container (data-source) holding a .calendly-inline-widget div.
   Before the calendar shows, the visitor answers the qualifying questions
   below (QUESTIONS); only a qualified visitor gets the calendar, with the
   answers passed into Calendly. Calendly's script loads only when the
   container nears the viewport or a "#book" button is tapped. The scheduled booking
   reaches us twice: Calendly's signed webhook (the booking itself) and the
   beacon below (consent + first-touch attribution for Meta CAPI). */
(function () {
  'use strict';

  var EVENT_URL = 'https://calendly.com/nawaf-allahham02/30min';
  var WIDGET_JS = 'https://assets.calendly.com/assets/external/widget.js';
  var WIDGET_CSS = 'https://assets.calendly.com/assets/external/widget.css';
  var ORIGIN = 'https://calendly.com';

  /* ---- Qualifying questions ---------------------------------------
     One tap each. An option with pass: false ends the check; the visitor
     sees the decline message and no calendar. Answers go to Calendly as
     a1..a4 (custom invitee questions 1-4 on the event type, in this order). */
  var QUESTIONS = [
    {
      "q": "What’s your role at the brand?",
      "options": [
        {
          "label": "Founder or owner"
        },
        {
          "label": "Co-founder or partner"
        },
        {
          "label": "Head of marketing or e‑commerce"
        },
        {
          "label": "Other (agency, freelancer or staff)",
          "pass": false,
          "why": "The audit is a planning call with the person who decides on the brand’s marketing. Please ask the founder or marketing lead to book it."
        }
      ]
    },
    {
      "q": "How many orders do you get in a typical week?",
      "options": [
        {
          "label": "Not selling yet",
          "pass": false,
          "why": "We work with brands that already sell online every week, so the ads have a live store and real products behind them. Once you’re selling, we’d love to talk."
        },
        {
          "label": "1 to 10"
        },
        {
          "label": "11 to 50"
        },
        {
          "label": "51 to 200"
        },
        {
          "label": "More than 200"
        }
      ]
    },
    {
      "q": "What’s your average order value?",
      "options": [
        {
          "label": "Under AED 100",
          "pass": false,
          "why": "With orders under AED 100, the ad spend rarely pays back through WhatsApp sales, so we’d be taking your budget without a fair chance of profit."
        },
        {
          "label": "AED 100 to 149"
        },
        {
          "label": "AED 150 to 300"
        },
        {
          "label": "AED 300 to 600"
        },
        {
          "label": "More than AED 600"
        }
      ]
    },
    {
      "q": "How do you run Meta ads today?",
      "options": [
        {
          "label": "From our own ad account"
        },
        {
          "label": "Our own account, paused for now"
        },
        {
          "label": "An agency runs them in their account"
        },
        {
          "label": "We don’t have a Meta ad account yet",
          "pass": false,
          "why": "We run the ads from your own Meta ad account, so you keep the ads, data and results. Set one up in Meta Business Suite, then come back and book."
        }
      ]
    }
  ];
  var STORE_KEY = 'nuevo-qualify';
  var STORE_DAYS = 30;

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
    var params = ['primary_color=0d518d', 'text_color=18213a'];
    if (person.name) params.push('name=' + encodeURIComponent(person.name));
    answers.forEach(function (a, i) { params.push('a' + (i + 1) + '=' + encodeURIComponent(a)); });
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
      var v = a[k] || q.get(k);
      if (v) params.push(k + '=' + encodeURIComponent(String(v).slice(0, 150)));
    });
    return EVENT_URL + '?' + params.join('&');
  }

  // --- lazy load ---------------------------------------------------
  // The script may load early (near the viewport, or on a "#book" tap);
  // the widget itself is only drawn once the visitor has qualified.
  var loading = false, scriptReady = false, qualified = false;
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
  function maybeInit() { if (scriptReady && qualified) init(); }
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
    s.onload = function () { scriptReady = true; maybeInit(); };
    s.onerror = function () { if (qualified) fail(); else loading = false; };
    document.head.appendChild(s);
  }

  // A tap on any "#book" button starts the load at once, so the calendar is
  // ready (or nearly) by the time the visitor has answered.
  document.addEventListener('pointerdown', function (e) {
    var a = e.target.closest && e.target.closest('a[href="#book"]');
    if (a) load();
  }, { passive: true });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); load(); }
    }, { rootMargin: '600px 0px' });
    io.observe(box);
  } else {
    load();
  }

  // --- qualifying questions ------------------------------------------
  // Each step is reported to /api/lead (the dashboard funnel). The visitor
  // gives their name and WhatsApp number first, then answers; one who
  // qualifies adds their company and gets the calendar.
  var answers = [];
  var person = { name: '', phone: '', company: '' };
  var leadId = '';
  function readStore() {
    try {
      var v = JSON.parse(localStorage.getItem(STORE_KEY) || 'null');
      if (v && Date.now() - v.t < STORE_DAYS * 864e5) return v;
    } catch (e) {}
    return null;
  }
  function writeStore(v) {
    v.id = leadId;
    try { v.t = Date.now(); localStorage.setItem(STORE_KEY, JSON.stringify(v)); } catch (e) {}
  }
  function newLeadId() {
    var a = new Uint8Array(12);
    (window.crypto || window.msCrypto).getRandomValues(a);
    return 'ld_' + Array.prototype.map.call(a, function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
  }
  function report(status, extra) {
    if (!leadId) return;
    var body = { id: leadId, page: source, status: status, answers: answers, attribution: attribution(),
      name: person.name || null, phone: person.phone || null, consent: consentGranted(), page_url: location.href };
    for (var k in extra) body[k] = extra[k];
    try {
      fetch('/api/lead', { method: 'POST', keepalive: true, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .catch(function () {});
    } catch (e) {}
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var panel = document.createElement('div');
  panel.className = 'qualify';
  panel.setAttribute('aria-live', 'polite');
  box.insertBefore(panel, widget);
  box.classList.add('is-gated');

  function pass() {
    qualified = true;
    panel.remove();
    box.classList.remove('is-gated');
    widget.innerHTML = '<p class="cal-embed__msg">Loading the calendar&hellip;</p>';
    load();
    maybeInit();
  }
  function decline(why) {
    box.classList.add('is-declined');
    panel.innerHTML =
      '<p class="qualify__step">Thanks for your answers</p>' +
      '<h3 class="qualify__q" tabindex="-1">We’re not the right fit just yet</h3>' +
      '<p class="qualify__note">' + esc(why || 'The free audit is for brands that already sell online every week and run Meta ads from their own account.') + '</p>' +
      '<p class="qualify__note">Have a question in the meantime? Message us on WhatsApp.</p>' +
      '<div class="btn-row"><a class="btn btn--secondary" href="https://wa.me/15557738409" target="_blank" rel="noopener" data-lead="qualify-wa">Message us on WhatsApp</a></div>';
    panel.querySelector('h3').focus({ preventScroll: true });
  }
  function details() {
    panel.innerHTML =
      '<p class="qualify__step">You’re a fit · last step</p>' +
      '<div class="qualify__bar" aria-hidden="true"><span style="width:100%"></span></div>' +
      '<h3 class="qualify__q" tabindex="-1">Which brand is the audit for?</h3>' +
      '<form class="qualify__form" novalidate>' +
      '<label class="field">Company or brand name<input name="company" autocomplete="organization" required maxlength="120" value="' + esc(person.company) + '"></label>' +
      '<p class="field__error qualify__err" hidden>Please add your brand name, so we can prepare your audit.</p>' +
      '<button class="btn btn--primary" type="submit">Show available times</button>' +
      '<p class="t-small muted">We only use this to prepare your call. <a href="/privacy/">Privacy policy</a></p>' +
      '</form>';
    var form = panel.querySelector('form');
    panel.querySelector('h3').focus({ preventScroll: true });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var c = form.elements.company.value.trim();
      form.elements.company.setAttribute('aria-invalid', String(!c));
      panel.querySelector('.qualify__err').hidden = !!c;
      if (!c) { form.elements.company.focus(); return; }
      person.company = c.slice(0, 120);
      writeStore({ ok: true, answers: answers.slice(), name: person.name, phone: person.phone, company: person.company });
      report('details', { company: person.company });
      if (typeof window.fbq === 'function') window.fbq('track', 'SubmitApplication', { content_name: 'audit-qualified' }, { eventID: leadId + '-q' });
      if (window.nuevoGa) window.nuevoGa('qualify_lead');
      pass();
    });
  }
  // Advanced matching: the pixel hashes these before sending, and they match
  // the server's CAPI user data (phone, first name, external_id = lead id).
  function matchUser() {
    if (typeof window.fbq !== 'function' || !window.nuevoPixelId || !person.phone) return;
    var d = person.phone.replace(/\D/g, '').replace(/^00/, '');
    if (d.length === 10 && d.charAt(0) === '0' && d.charAt(1) === '5') d = '971' + d.slice(1);
    else if (d.length === 9 && d.charAt(0) === '5') d = '971' + d;
    var m = { ph: d, external_id: leadId, country: 'ae' };
    var fn = person.name.trim().split(/\s+/)[0].toLowerCase();
    if (fn) m.fn = fn;
    window.fbq('init', window.nuevoPixelId, m);
  }

  // First step: name and WhatsApp number. Sends the one real Lead event to
  // Meta (pixel here, CAPI from /api/lead, same event id).
  function contact() {
    panel.innerHTML =
      '<p class="qualify__step">Free audit · takes under a minute</p>' +
      '<div class="qualify__bar" aria-hidden="true"><span style="width:0%"></span></div>' +
      '<h3 class="qualify__q" tabindex="-1">Who are we talking to?</h3>' +
      '<form class="qualify__form" novalidate>' +
      '<label class="field">Your name<input name="name" autocomplete="name" required maxlength="100" value="' + esc(person.name) + '"></label>' +
      '<label class="field">WhatsApp number<input name="phone" type="tel" inputmode="tel" autocomplete="tel" required maxlength="24" placeholder="+971 50 123 4567" value="' + esc(person.phone) + '"></label>' +
      '<p class="field__error qualify__err" hidden>Please add your name and a WhatsApp number we can reach.</p>' +
      '<button class="btn btn--primary" type="submit">Next: 4 quick questions</button>' +
      '<p class="t-small muted">We only use this to prepare and confirm your call. <a href="/privacy/">Privacy policy</a></p>' +
      '</form>';
    var form = panel.querySelector('form');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var n = form.elements.name.value.trim(), p = form.elements.phone.value.trim();
      var digits = p.replace(/\D/g, '');
      var okP = digits.length >= 7 && digits.length <= 15;
      form.elements.name.setAttribute('aria-invalid', String(!n));
      form.elements.phone.setAttribute('aria-invalid', String(!okP));
      panel.querySelector('.qualify__err').hidden = !!(n && okP);
      if (!n || !okP) { (n ? form.elements.phone : form.elements.name).focus(); return; }
      if (!leadId) leadId = newLeadId();
      person.name = n.slice(0, 100);
      person.phone = p.slice(0, 24);
      var done = answers.length === QUESTIONS.length;
      writeStore(done ? { ok: true, answers: answers.slice(), name: person.name, phone: person.phone, company: person.company }
                      : { contact: true, name: person.name, phone: person.phone });
      report(done ? 'qualified' : 'started');
      matchUser();
      if (typeof window.fbq === 'function') window.fbq('track', 'Lead', { content_name: 'audit-contact' }, { eventID: leadId });
      if (window.nuevoGa) window.nuevoGa('generate_lead');
      if (done) { if (person.company) pass(); else details(); return; }
      ask(0);
      panel.querySelector('h3').focus({ preventScroll: true });
    });
  }

  function ask(i) {
    var q = QUESTIONS[i];
    panel.innerHTML =
      '<p class="qualify__step">' + (i ? '' : 'Thanks, ' + esc(person.name.split(' ')[0]) + ' · ') + (i + 1) + ' of ' + QUESTIONS.length + '</p>' +
      '<div class="qualify__bar" aria-hidden="true"><span style="width:' + Math.round(i / QUESTIONS.length * 100) + '%"></span></div>' +
      '<h3 class="qualify__q" id="qualify-q" tabindex="-1">' + esc(q.q) + '</h3>' +
      '<div class="qualify__opts" role="group" aria-labelledby="qualify-q">' +
      q.options.map(function (o, j) { return '<button type="button" class="qualify__opt" data-j="' + j + '">' + esc(o.label) + '</button>'; }).join('') +
      '</div>' +
      (i ? '<button type="button" class="qualify__back">Back</button>' : '');
    panel.querySelectorAll('.qualify__opt').forEach(function (b) {
      b.addEventListener('click', function () {
        var o = q.options[+b.getAttribute('data-j')];
        if (!leadId) leadId = newLeadId();
        answers[i] = o.label;
        answers.length = i + 1;
        if (o.pass === false) {
          writeStore({ ok: false, why: o.why });
          report('declined', { declined_at_q: i + 1 });
          decline(o.why);
          return;
        }
        if (i + 1 < QUESTIONS.length) { report('started'); ask(i + 1); }
        else { writeStore({ ok: true, answers: answers.slice() }); report('qualified'); details(); }
      });
    });
    var back = panel.querySelector('.qualify__back');
    if (back) back.addEventListener('click', function () { ask(i - 1); });
    if (i) panel.querySelector('h3').focus({ preventScroll: true });
  }

  var prior = readStore();
  if (prior && prior.id) leadId = prior.id;
  if (prior) person = { name: prior.name || '', phone: prior.phone || '', company: prior.company || '' };
  if (leadId && person.phone) matchUser();
  if (prior && prior.ok && Array.isArray(prior.answers) && prior.answers.length === QUESTIONS.length) {
    answers = prior.answers;
    if (!person.name || !person.phone) contact();
    else if (person.company) pass(); else details();
  }
  else if (prior && prior.ok === false) decline(prior.why);
  else if (person.name && person.phone) { widget.innerHTML = ''; ask(0); }
  else { widget.innerHTML = ''; contact(); }

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
    if (window.nuevoGa) {
      window.nuevoGa('book_appointment');
      // Google Ads conversion (linked to the same Google tag).
      window.nuevoGa('ads_conversion_Book_appointment_1', { transaction_id: inviteeUri });
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
          lead_id: leadId || null,
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
