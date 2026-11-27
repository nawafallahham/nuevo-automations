(function () {
  'use strict';

  /* ---- Meta Pixel: WhatsApp taps are Contact, booking-button taps a custom
     BookClick. The real Lead is the name + number step (js/calendly.js), so
     campaigns optimising for Lead learn from people who gave their details.
     Sent through nuevoMeta (js/consent.js): pixel + server copy, only after
     consent. */
  document.addEventListener('click', function (e) {
    if (!e.target.closest) return;
    var link = e.target.closest('a[href*="wa.me/"], .js-lead');
    if (!link) return;
    var where = link.getAttribute('data-lead')
              || (link.classList.contains('wa-float') ? 'wa-float'
              : link.closest('.actionbar') ? 'mobile-bar'
              : link.closest('header') ? 'header'
              : link.closest('.hero, .page-head') ? 'hero'
              : link.closest('footer') ? 'footer'
              : 'other');
    if (window.nuevoMeta) window.nuevoMeta(/wa\.me\//.test(link.getAttribute('href') || '') ? 'Contact' : 'BookClick', { content_name: where });
    if (window.nuevoClarity) window.nuevoClarity(/wa\.me\//.test(link.getAttribute('href') || '') ? 'whatsapp_click' : 'book_click');
    if (window.nuevoGa) window.nuevoGa(/wa\.me\//.test(link.getAttribute('href') || '') ? 'whatsapp_click' : 'book_click', { location: where });
  });

  /* ---- Footer year ---- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
