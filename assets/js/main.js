/* Mobile navigation + gentle reveal on scroll + Calendly placeholder */
(function () {
  var cal = document.getElementById('calendly');
  if (!cal) return;
  if (cal.dataset.url.indexOf('YOUR-CALENDLY-LINK') === -1) return;
  // No Calendly link configured yet — show a friendly placeholder instead.
  cal.classList.remove('calendly-inline-widget');
  cal.removeAttribute('style');
  cal.className = 'cal-placeholder';
  cal.innerHTML =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"' +
    ' stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/>' +
    '<path d="M3 10h18"/><path d="M8 3v4"/><path d="M16 3v4"/></svg>' +
    '<p style="margin:0" data-i18n="book.cal.ph">' +
    (window.I18N && window.I18N[document.documentElement.lang || 'en'] || window.I18N.en)['book.cal.ph'] +
    '</p><code>build.py → CALENDLY_URL</code>';
})();


(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  var items = document.querySelectorAll('.reveal');
  if (!items.length) return;

  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry, i) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      setTimeout(function () { el.classList.add('in'); }, i * 70);
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -60px 0px', threshold: 0.08 });

  items.forEach(function (el) { io.observe(el); });
})();
