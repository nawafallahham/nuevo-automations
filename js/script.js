(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Meta Pixel: count WhatsApp and booking CTA clicks as leads ----
     Guarded on fbq so it no-ops until consent loads the pixel. */
  document.addEventListener('click', function (e) {
    if (typeof window.fbq !== 'function' || !e.target.closest) return;
    var link = e.target.closest('a[href*="wa.me/"], .js-lead');
    if (!link) return;
    var where = link.getAttribute('data-lead')
              || (link.classList.contains('wa-float') ? 'wa-float'
              : link.closest('.mobile-cta') ? 'mobile-bar'
              : link.closest('.site-header') ? 'header'
              : link.closest('.hero, .page-hero') ? 'hero'
              : link.closest('.cta-band') ? 'cta-band'
              : 'other');
    window.fbq('track', 'Lead', { content_name: where });
  });

  /* ---- Footer year ---- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- Header: shadow once scrolled, mobile nav toggle ---- */
  var header = document.querySelector('.site-header');
  var navToggle = document.getElementById('nav-toggle');
  var mainNav = document.getElementById('main-nav');

  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.pageYOffset > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  if (navToggle && header && mainNav) {
    navToggle.addEventListener('click', function () {
      var isOpen = header.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      navToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });
    mainNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        header.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Open menu');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('is-open')) {
        header.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Open menu');
        navToggle.focus();
      }
    });
  }

  /* ---- Scroll reveal (blocks + staggered grids) ---- */
  var revealEls = document.querySelectorAll('.reveal, .reveal-stagger');

  if (!prefersReducedMotion) {
    document.querySelectorAll('.reveal-stagger').forEach(function (group) {
      Array.prototype.forEach.call(group.children, function (child, i) {
        child.style.transitionDelay = (i * 70) + 'ms';
      });
    });
  }

  if (revealEls.length) {
    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
      revealEls.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
      revealEls.forEach(function (el) { observer.observe(el); });
    }
  }

  /* ---- Partners wheel: duplicate the set for a seamless loop ---- */
  var partnersTrack = document.getElementById('partners-track');
  if (partnersTrack && !prefersReducedMotion) {
    Array.prototype.slice.call(partnersTrack.children).forEach(function (item) {
      var clone = item.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      clone.querySelectorAll('img').forEach(function (img) { img.alt = ''; });
      partnersTrack.appendChild(clone);
    });
    partnersTrack.classList.add('is-looping');
  }
})();
