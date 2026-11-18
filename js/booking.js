/* ================= Booking widget =================
   Shared by /book/ and /consultation/. Expects the #bk-form markup.
   Slots run 14:00-18:30 Dubai time (GST, UTC+4, no DST). Availability
   comes from the booking API; if that's unreachable the widget still
   works and hands off to WhatsApp, so the page never dead-ends. */
(function () {
  'use strict';

  // Same-origin API, served by the site's Cloudflare Worker (/api/*).
  var API = '';
  var WA = '971508549171';
  var OPEN = 14 * 60, CLOSE = 18 * 60 + 30, STEP = 30;
  var LEAD_MIN = 45;   // don't offer a slot less than 45 min away
  var DAYS = 7;

  var elDays = document.getElementById('bk-days');
  var elTimes = document.getElementById('bk-times');
  var elSummary = document.getElementById('bk-summary');
  var elConfirm = document.getElementById('bk-confirm');
  var elForm = document.getElementById('bk-form');
  var elDone = document.getElementById('bk-done');
  if (!elDays || !elForm) return;

  var source = elForm.getAttribute('data-source') || 'site';
  var taken = {};          // { 'YYYY-MM-DD': ['14:00', ...] }
  var days = [];
  var sel = { date: null, time: null };
  var startSent = false;   // book_start analytics fires once per page

  // One id per booking attempt, shared by the browser pixel and the
  // server-side Conversions API so Meta counts the Schedule only once.
  function newEventId() {
    try { if (window.crypto && crypto.randomUUID) return crypto.randomUUID(); } catch (e) {}
    return 'ev-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
  }
  function consentGranted() {
    try { return localStorage.getItem('nuevo-consent') === 'granted'; } catch (e) { return false; }
  }

  // --- Dubai clock -------------------------------------------------
  function dubaiParts() {
    var p = {};
    new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Asia/Dubai', year: 'numeric', month: '2-digit',
      day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false
    }).formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    return p;
  }
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function iso(d) {
    return d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1) + '-' + pad(d.getUTCDate());
  }
  function label12(mins) {
    var h = Math.floor(mins / 60), m = mins % 60;
    var ap = h >= 12 ? 'PM' : 'AM';
    var h12 = h % 12 === 0 ? 12 : h % 12;
    return h12 + ':' + pad(m) + ' ' + ap;
  }

  var p = dubaiParts();
  var todayISO = p.year + '-' + p.month + '-' + p.day;
  var nowMins = Number(p.hour) * 60 + Number(p.minute);

  // --- build the day list, skipping days with nothing left ---------
  function buildDays() {
    days = [];
    var base = new Date(Date.UTC(Number(p.year), Number(p.month) - 1, Number(p.day)));
    for (var i = 0; days.length < DAYS && i < DAYS + 5; i++) {
      var d = new Date(base);
      d.setUTCDate(d.getUTCDate() + i);
      var key = iso(d);
      if (slotsFor(key).some(function (s) { return !s.disabled; })) {
        days.push({ key: key, date: d });
      }
    }
  }

  function slotsFor(dateKey) {
    var out = [];
    for (var m = OPEN; m <= CLOSE; m += STEP) {
      var hhmm = pad(Math.floor(m / 60)) + ':' + pad(m % 60);
      var isTaken = (taken[dateKey] || []).indexOf(hhmm) !== -1;
      var tooSoon = dateKey === todayISO && m < nowMins + LEAD_MIN;
      out.push({ value: hhmm, mins: m, label: label12(m), disabled: isTaken || tooSoon, taken: isTaken });
    }
    return out;
  }

  // --- rendering ---------------------------------------------------
  function renderDays() {
    elDays.innerHTML = '';
    if (!days.length) {
      elDays.innerHTML = '<p class="bk-empty">No slots left this week. Message us on WhatsApp and we\'ll find a time.</p>';
      return;
    }
    var keep = days.some(function (d) { return d.key === sel.date; }) ? sel.date : days[0].key;
    days.forEach(function (d) {
      var q = {};
      new Intl.DateTimeFormat('en-GB', { timeZone: 'UTC', weekday: 'short', day: 'numeric', month: 'short' })
        .formatToParts(d.date).forEach(function (x) { q[x.type] = x.value; });
      var on = d.key === keep;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'bk-day' + (on ? ' is-on' : '');
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.innerHTML = (d.key === todayISO ? 'Today' : q.weekday) + '<strong>' + q.day + ' ' + q.month + '</strong>';
      btn.addEventListener('click', function () {
        sel.date = d.key; sel.time = null;
        [].forEach.call(elDays.children, function (c) {
          c.classList.remove('is-on'); c.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('is-on'); btn.setAttribute('aria-pressed', 'true');
        renderTimes(); update();
      });
      elDays.appendChild(btn);
    });
    sel.date = keep;
  }

  function renderTimes() {
    elTimes.innerHTML = '';
    if (!sel.date) return;
    var list = slotsFor(sel.date);
    if (!list.some(function (s) { return !s.disabled; })) {
      elTimes.innerHTML = '<p class="bk-empty">Nothing left on this day. Try another.</p>';
      return;
    }
    list.forEach(function (s) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'bk-time' + (sel.time === s.value ? ' is-on' : '');
      btn.textContent = s.label;
      btn.disabled = s.disabled;
      if (s.taken) btn.title = 'Already booked';
      btn.addEventListener('click', function () {
        sel.time = s.value;
        [].forEach.call(elTimes.children, function (c) { c.classList && c.classList.remove('is-on'); });
        btn.classList.add('is-on');
        if (!startSent && typeof window.nuevoTrack === 'function') {
          startSent = true;
          window.nuevoTrack('book_start');
        }
        update();
      });
      elTimes.appendChild(btn);
    });
  }

  function prettySel() {
    if (!sel.date || !sel.time) return '';
    var d = new Date(sel.date + 'T00:00:00Z');
    var q = {};
    new Intl.DateTimeFormat('en-GB', { timeZone: 'UTC', weekday: 'long', day: 'numeric', month: 'long' })
      .formatToParts(d).forEach(function (x) { q[x.type] = x.value; });
    var mins = Number(sel.time.slice(0, 2)) * 60 + Number(sel.time.slice(3));
    return q.weekday + ' ' + q.day + ' ' + q.month + ' at ' + label12(mins) + ' (Dubai time)';
  }

  function update() {
    var ready = Boolean(sel.date && sel.time);
    elConfirm.disabled = !ready;
    elSummary.classList.remove('is-bad');
    elSummary.innerHTML = ready
      ? 'Your audit: <strong>' + prettySel() + '</strong>'
      : 'Select a day and a time to continue.';
  }

  function waLink(extra) {
    var msg = 'Hi, I would like to book my free M2S audit on ' + prettySel() + '.' + (extra || '');
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
  }

  // --- submit ------------------------------------------------------
  elForm.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!sel.date || !sel.time) return;

    var name = document.getElementById('bk-name');
    var phone = document.getElementById('bk-phone');
    var business = document.getElementById('bk-business');
    var email = document.getElementById('bk-email');          // optional
    var honey = elForm.querySelector('input[name="website"]');  // bots only
    var bad = false;
    [name, phone, business].forEach(function (f) {
      var ok = f === phone
        ? f.value.replace(/\D/g, '').length >= 7
        : f.value.trim().length >= 2;
      f.classList.toggle('is-bad', !ok);
      if (!ok) bad = true;
    });
    var emailVal = email ? email.value.trim() : '';
    var emailOk = !emailVal || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(emailVal);
    if (email) email.classList.toggle('is-bad', !emailOk);
    if (bad || !emailOk) {
      elSummary.classList.add('is-bad');
      elSummary.textContent = bad
        ? 'Please add your name, business name and a valid WhatsApp number.'
        : 'That email address doesn\'t look right. Fix it or leave it empty.';
      return;
    }
    var eventId = newEventId();

    elConfirm.disabled = true;
    elConfirm.textContent = 'Booking…';

    function finish(stored) {
      // Same eventID as the server's Conversions API call -> deduplicated.
      if (stored && typeof window.fbq === 'function') {
        window.fbq('track', 'Schedule', { content_name: sel.date + ' ' + sel.time }, { eventID: eventId });
      }
      elForm.hidden = true;
      elDone.hidden = false;
      document.getElementById('bk-done-title').textContent = stored ? "You're booked in" : 'Almost there';
      document.getElementById('bk-done-msg').textContent = stored
        ? prettySel() + '. We\'ll message you on WhatsApp shortly to confirm.'
        : 'Tap below to send us your slot on WhatsApp and we\'ll confirm it: ' + prettySel() + '.';
      document.getElementById('bk-done-wa').href = waLink(
        ' Name: ' + name.value.trim() + '. Business: ' + business.value.trim() + '.'
      );
      elDone.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // Always attempt the real booking. Availability lookup and booking are
    // separate endpoints, so a failure to pre-load taken slots must not
    // stop someone actually booking - the server's atomic write is what
    // guarantees correctness, and a 409 covers any collision.
    fetch(API + '/api/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date: sel.date, time: sel.time,
        name: name.value.trim(), phone: phone.value.trim(),
        business: business.value.trim(),
        email: emailVal,
        website: honey ? honey.value : '',
        note: 'M2S audit · booked from ' + source,
        source: source,
        attribution: typeof window.nuevoAttribution === 'function' ? window.nuevoAttribution() : null,
        event_id: eventId,
        consent: consentGranted()
      })
    })
      .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (r) {
        if (r.body && r.body.ok) { finish(true); return; }
        if (r.status === 409) {
          // Someone took it first — refresh availability and let them repick.
          elConfirm.disabled = false;
          elConfirm.textContent = 'Confirm my audit';
          elSummary.classList.add('is-bad');
          elSummary.textContent = 'Sorry, that slot was just taken. Please pick another.';
          return loadAvailability().then(function () { buildDays(); renderDays(); renderTimes(); });
        }
        finish(false);
      })
      .catch(function () { finish(false); });
  });

  // --- availability ------------------------------------------------
  function loadAvailability() {
    return fetch(API + '/api/slots?days=14', { cache: 'no-store' })
      .then(function (r) { return r.json(); })
      .then(function (j) { taken = (j && j.taken) || {}; })
      .catch(function () { taken = {}; });
  }

  // Render immediately from local rules, then refine once the API answers,
  // so the widget is usable even on a slow or failed request.
  buildDays(); renderDays(); renderTimes(); update();
  loadAvailability().then(function () {
    buildDays(); renderDays(); renderTimes(); update();
  });
}());
