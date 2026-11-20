(function () {
  'use strict';

  /* ---- Meta Pixel: count WhatsApp and booking CTA clicks as leads ----
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
    window.fbq('track', 'Lead', { content_name: where });
  });

  /* ---- Footer year ---- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
