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
    });
    mainNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        header.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('is-open')) {
        header.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
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

  /* ---- Animated M2S conversation (home hero) ----
     Plays one ad-to-sale story: the ad chip, the question, the AI reply,
     the payment link and the paid confirmation, then loops. */
  var chat = document.getElementById('m2s-chat');
  if (!chat) return;

  var story = [
    { type: 'chip', cls: 'chip--ad', text: 'Opened from your Instagram ad · Linen collection' },
    { type: 'in', text: 'Hi, is the linen set still available in M? How much?', time: '11:48 PM' },
    { type: 'out', text: 'Hi! Yes, the linen set is in stock in M for AED 289, with free delivery in Dubai tomorrow. Shall I reserve one for you?', time: '11:48 PM' },
    { type: 'in', text: 'Yes please. Can I pay by card?', time: '11:49 PM' },
    { type: 'out', text: 'Of course. Here is your secure payment link:', time: '11:49 PM' },
    { type: 'pay', amount: 'AED 289.00', label: 'Linen set · M' },
    { type: 'chip', cls: 'chip--win', text: '✓ Paid · Order #1042 sent to your team' }
  ];

  function node(item) {
    var el = document.createElement('div');
    if (item.type === 'chip') {
      el.className = 'chip ' + (item.cls || '');
      el.textContent = item.text;
    } else if (item.type === 'pay') {
      el.className = 'pay-card';
      el.innerHTML = '<div class="pay-card-head"><span></span><strong></strong></div><span class="pay-card-btn">Pay securely</span>';
      el.querySelector('span').textContent = item.label;
      el.querySelector('strong').textContent = item.amount;
    } else {
      el.className = 'msg msg--' + item.type;
      var text = document.createElement('span');
      text.textContent = item.text;
      var time = document.createElement('time');
      time.textContent = item.time;
      el.appendChild(text);
      el.appendChild(time);
    }
    return el;
  }

  function typing() {
    var t = document.createElement('div');
    t.className = 'typing';
    t.setAttribute('aria-hidden', 'true');
    t.innerHTML = '<span></span><span></span><span></span>';
    return t;
  }

  var timers = [];
  function later(fn, ms) { timers.push(setTimeout(fn, ms)); }

  function play() {
    timers.forEach(clearTimeout);
    timers = [];
    chat.innerHTML = '';
    var t = 300;
    story.forEach(function (item) {
      var aiSide = item.type === 'out' || item.type === 'pay';
      if (aiSide) {
        later(function () {
          var dots = typing();
          chat.appendChild(dots);
          chat.scrollTop = chat.scrollHeight;
          later(function () {
            dots.remove();
            chat.appendChild(node(item));
            chat.scrollTop = chat.scrollHeight;
          }, 1100);
        }, t);
        t += 1100 + 900;
      } else {
        later(function () {
          chat.appendChild(node(item));
          chat.scrollTop = chat.scrollHeight;
        }, t);
        t += item.type === 'chip' ? 900 : 1300;
      }
    });
    later(play, t + 4200);
  }

  if (prefersReducedMotion) {
    story.forEach(function (item) { chat.appendChild(node(item)); });
  } else if ('IntersectionObserver' in window) {
    var chatObserver = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { play(); chatObserver.disconnect(); }
    }, { threshold: 0.3 });
    chatObserver.observe(chat);
  } else {
    play();
  }
})();
