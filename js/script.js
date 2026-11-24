(function () {
  'use strict';

  /* ---- Meta Pixel: WhatsApp taps are Contact, booking-button taps a custom
     BookClick. The real Lead is the name + number step (js/calendly.js), so
     campaigns optimising for Lead learn from people who gave their details.
     Guarded on fbq so it no-ops until consent loads the pixel. */
  document.addEventListener('click', function (e) {
    if (typeof window.fbq !== 'function' || !e.target.closest) return;
    var link = e.target.closest('a[href*="wa.me/"], .js-lead');
    if (!link) return;
    var where = link.getAttribute('data-lead')
              || (link.classList.contains('wa-float') ? 'wa-float'
              : link.closest('.actionbar') ? 'mobile-bar'
              : link.closest('header') ? 'header'
              : link.closest('.hero, .page-head') ? 'hero'
              : link.closest('footer') ? 'footer'
              : 'other');
    if (/wa\.me\//.test(link.getAttribute('href') || '')) window.fbq('track', 'Contact', { content_name: where });
    else window.fbq('trackCustom', 'BookClick', { content_name: where });
    if (window.nuevoGa) window.nuevoGa(/wa\.me\//.test(link.getAttribute('href') || '') ? 'whatsapp_click' : 'book_click', { location: where });
  });

  /* ---- Footer year ---- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
