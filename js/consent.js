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
    window.fbq('track', 'PageView');
  }

  // The notice is a small card at the foot of the screen (styles in /css/site.css).
  // Accept and Decline carry equal weight. While it shows, the body is padded by
  // its height so it never covers the page's last lines.
  function banner() {
    var box = document.createElement('div');
    box.className = 'consent';
    box.setAttribute('role', 'region');
    box.setAttribute('aria-label', 'Cookie consent');
    box.innerHTML =
      '<p>We use cookies to measure how our ads perform. <a href="/privacy/">Privacy policy</a></p>' +
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
      if (choice === 'granted') loadPixel();
    }
    box.querySelector('.consent-yes').addEventListener('click', function () { close('granted'); });
    box.querySelector('.consent-no').addEventListener('click', function () { close('denied'); });
  }

  var choice = read();
  if (choice === 'granted') {
    loadPixel();
  } else if (choice !== 'denied') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', banner);
    } else {
      banner();
    }
  }

  window.NuevoConsent = {
    state: function () { return read(); },
    reset: function () {
      try { localStorage.removeItem(STORE_KEY); } catch (e) {}
    }
  };
}());
