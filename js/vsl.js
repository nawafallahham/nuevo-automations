/* ================= Video sales letter player =================
   Used by /wellness-brands/vsl/. Settings live on the #vsl element (see the
   comment above it in the page).

   - Autoplays muted with a "Click to unmute" overlay; the first unmute
     restarts the video from the top, so nobody misses the opening.
   - No seeking: there is no scrubber, and any jump past the furthest point
     watched is pulled back.
   - The progress bar is not linear: shown = real ^ curve, so it races at the
     start and slows down later.
   - The booking step (#vsl-gate, #book) stays locked until the share of the
     video in data-unlock has been watched. A returning visitor resumes where
     they stopped, and one who already finished finds it open.

   Tracking (each fires once per page view):
   - first-party dashboard (/api/track, cookieless, always on): video_play,
     video_unmute, video_resume, video_progress at 10..90%, video_complete.
     The path carries the video id, so each cut gets its own numbers.
   - GA4 (after consent): vsl_autoplay, video_start, video_progress {percent},
     video_complete, vsl_unlock.
   - Meta (after consent): custom events VSLPlay, VSLProgress {percent}
     at 25/50/75, VSLComplete, for audiences such as "watched 50%". Sent by
     the pixel and by our server (Conversions API) with one shared event id.
   - Microsoft Clarity (after consent, if set up): the same milestones as
     custom events, plus a vsl_video tag to filter recordings by video cut. */
(function () {
  'use strict';

  var root = document.getElementById('vsl');
  if (!root) return;

  var video = root.querySelector('.vsl__video');
  var overlay = root.querySelector('.vsl__overlay');
  var resumeBox = root.querySelector('.vsl__resume');
  var soon = root.querySelector('.vsl__soon');
  var barFill = root.querySelector('.vsl__bar span');
  var playBtn = root.querySelector('.vsl__play');
  var muteBtn = root.querySelector('.vsl__mute');
  var gate = document.getElementById('vsl-gate');
  var book = document.getElementById('book');

  var src = (root.getAttribute('data-src') || '').trim();
  var poster = (root.getAttribute('data-poster') || '').trim();
  var vid = ((root.getAttribute('data-video-id') || 'v1').replace(/[^\w-]/g, '') || 'v1').slice(0, 40);
  var curve = parseFloat(root.getAttribute('data-curve'));
  if (!(curve > 0 && curve <= 1)) curve = 0.5;
  var unlockAt = parseFloat(root.getAttribute('data-unlock'));
  if (!(unlockAt > 0 && unlockAt <= 1)) unlockAt = 1;

  var KEY = 'nuevo-vsl-' + vid;
  var sent = {};
  var engaged = false;   // true once the viewer unmuted or pressed play
  var maxWatched = 0;    // furthest point reached, in seconds
  var unlocked = false;

  // --- storage ---------------------------------------------------------
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null') || {}; } catch (e) { return {}; }
  }
  function save(v) {
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {}
  }
  var stored = load();

  // --- tracking ----------------------------------------------------------
  function once(key, fn) { if (sent[key]) return; sent[key] = true; fn(); }
  function first(type, what) {
    if (typeof window.nuevoTrack === 'function') window.nuevoTrack(type, '/vsl/' + vid + '/' + what);
  }
  function ga(name, params) {
    params = params || {};
    params.video_id = vid;
    if (typeof window.nuevoGa === 'function') window.nuevoGa(name, params);
  }
  // Meta: pixel + server copy with a shared event id, after consent only
  // (window.nuevoMeta in js/consent.js).
  function meta(name, params) {
    params = params || {};
    params.video_id = vid;
    if (typeof window.nuevoMeta === 'function') window.nuevoMeta(name, params);
  }
  function clarity(name) {
    if (typeof window.clarity === 'function') window.clarity('event', name);
  }
  if (typeof window.clarity === 'function') window.clarity('set', 'vsl_video', vid);
  window.addEventListener('nuevo:clarity', function () { window.clarity('set', 'vsl_video', vid); });

  function milestone(p) {
    once('p' + p, function () {
      first('video_progress', 'p' + p);
      ga('video_progress', { percent: p });
      clarity('vsl_' + p);
      if (p === 25 || p === 50 || p === 75) meta('VSLProgress', { percent: p });
    });
  }

  // --- the gate ----------------------------------------------------------
  function unlock(silent) {
    if (unlocked) return;
    unlocked = true;
    gate.querySelector('.vsl-gate__locked').hidden = true;
    gate.querySelector('.vsl-gate__open').hidden = false;
    book.hidden = false;
    gate.classList.add('is-open');
    if (!silent) {
      ga('vsl_unlock');
      clarity('vsl_unlock');
    }
  }

  // --- no video yet -----------------------------------------------------
  if (!src) {
    root.classList.add('is-soon');
    soon.hidden = false;
    root.querySelector('.vsl__controls').hidden = true;
    unlock(true);
    return;
  }

  // --- progress bar -----------------------------------------------------
  function shown(x) { return x <= 0 ? 0 : x >= 1 ? 1 : Math.pow(x, curve); }
  var raf = 0;
  function paint() {
    var d = video.duration;
    if (d && isFinite(d)) barFill.style.transform = 'scaleX(' + shown(video.currentTime / d) + ')';
    raf = video.paused ? 0 : requestAnimationFrame(paint);
  }
  function startPaint() { if (!raf) raf = requestAnimationFrame(paint); }

  // --- player state -----------------------------------------------------
  function setPlayIcon() {
    root.classList.toggle('is-paused', video.paused);
    playBtn.setAttribute('aria-label', video.paused ? 'Play' : 'Pause');
  }
  function setMuteIcon() {
    root.classList.toggle('is-muted', video.muted);
    muteBtn.setAttribute('aria-label', video.muted ? 'Unmute' : 'Mute');
  }
  function showOverlay(title, sub) {
    overlay.querySelector('.vsl__overlay-title').textContent = title;
    overlay.querySelector('.vsl__overlay-sub').textContent = sub;
    overlay.hidden = false;
  }

  function engage(fromStart) {
    var firstTime = !engaged;
    engaged = true;
    overlay.hidden = true;
    resumeBox.hidden = true;
    if (fromStart) { video.currentTime = 0; maxWatched = 0; }
    video.muted = false;
    setMuteIcon();
    var p = video.play();
    // If the browser still refuses (no real tap), ask for one more click.
    if (p && p.catch) p.catch(function () { setPlayIcon(); showOverlay('Your Video Is Ready', 'Click To Play'); });
    if (firstTime) {
      once('start', function () {
        first('video_unmute', 'unmute');
        ga('video_start');
        meta('VSLPlay');
        clarity('vsl_start');
      });
    }
  }

  overlay.addEventListener('click', function () {
    // The first click restarts from the top; later ones (after a pause) just resume.
    engage(!engaged && !(stored.t > 0 && video.currentTime > 1));
  });
  resumeBox.querySelector('.vsl__continue').addEventListener('click', function () {
    once('resume', function () { first('video_resume', 'resume'); ga('video_resume'); });
    engage(false);
  });
  resumeBox.querySelector('.vsl__restart').addEventListener('click', function () { engage(true); });

  playBtn.addEventListener('click', function () {
    if (!engaged) { engage(true); return; }
    if (video.paused) { var p = video.play(); if (p && p.catch) p.catch(function () {}); }
    else video.pause();
  });
  muteBtn.addEventListener('click', function () {
    if (!engaged) { engage(true); return; }
    video.muted = !video.muted;
    setMuteIcon();
  });
  // A tap on the picture pauses / resumes once the viewer is engaged.
  video.addEventListener('click', function () {
    if (!engaged) { engage(true); return; }
    if (video.paused) video.play(); else video.pause();
  });

  video.addEventListener('play', function () { setPlayIcon(); startPaint(); });
  video.addEventListener('pause', function () {
    setPlayIcon();
    if (engaged && !video.ended) showOverlay('Paused', 'Click to keep watching');
  });

  // No skipping ahead: pull any jump past the furthest point back.
  video.addEventListener('seeking', function () {
    if (video.currentTime > maxWatched + 1.5) video.currentTime = maxWatched;
  });
  // Keep the speed at 1x, whatever the browser offers.
  video.addEventListener('ratechange', function () { if (video.playbackRate !== 1) video.playbackRate = 1; });

  var lastSave = 0;
  video.addEventListener('timeupdate', function () {
    var t = video.currentTime, d = video.duration;
    if (!video.seeking && t > maxWatched && t - maxWatched < 3) maxWatched = t;
    if (!d || !isFinite(d)) return;
    if (!engaged) return; // muted autoplay before the click doesn't count
    var frac = maxWatched / d;
    for (var p = 10; p <= 90; p += 10) if (frac >= p / 100) milestone(p);
    if (frac >= unlockAt - 0.002) unlock();
    var now = Date.now();
    if (now - lastSave > 2000) { lastSave = now; save({ t: maxWatched, done: stored.done || false }); }
  });

  video.addEventListener('ended', function () {
    barFill.style.transform = 'scaleX(1)';
    setPlayIcon();
    if (!engaged) return;
    maxWatched = video.duration;
    stored.done = true;
    save({ t: 0, done: true });
    once('complete', function () {
      first('video_complete', 'complete');
      ga('video_complete');
      meta('VSLComplete');
      clarity('vsl_complete');
    });
    unlock();
    overlay.hidden = true;
  });

  video.addEventListener('error', function () {
    root.classList.add('is-error');
    soon.querySelector('.vsl__soon-title').textContent = 'The video didn’t load';
    soon.querySelector('p:last-child').textContent = 'Please refresh the page, or book your free audit below.';
    soon.hidden = false;
    overlay.hidden = true;
    unlock(true);
  });

  // --- start ---------------------------------------------------------------
  if (poster) video.poster = poster;
  video.src = src;
  setMuteIcon();
  setPlayIcon();

  if (stored.done) unlock(true);

  if (stored.t > 5 && !stored.done) {
    // Came back part-way through: offer to continue where they left off.
    maxWatched = stored.t;
    video.addEventListener('loadedmetadata', function () { video.currentTime = stored.t; startPaint(); paint(); }, { once: true });
    resumeBox.hidden = false;
  } else {
    var p = video.play();
    showOverlay('Your Video Is Playing', 'Click To Unmute');
    if (p && p.then) {
      p.then(function () {
        once('autoplay', function () { first('video_play', 'autoplay'); ga('vsl_autoplay'); });
      }).catch(function () {
        // Autoplay blocked (low-power mode, data saver): ask for a tap instead.
        showOverlay('Your Video Is Ready', 'Click To Play');
      });
    }
  }
}());
