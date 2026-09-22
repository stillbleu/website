
/* ------------------------------------------------------------------ *
 * Language switching. English is rendered in the HTML; other languages
 * are swapped in from window.I18N above.
 * ------------------------------------------------------------------ */
(function () {
  var SUPPORTED = ['en', 'fr'];
  var KEY = 'sg-lang';

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(l) {
    try { localStorage.setItem(KEY, l); } catch (e) {}
  }

  var DEFAULT = 'fr';

  function detect() {
    var q = new URLSearchParams(location.search).get('lang');
    if (q && SUPPORTED.indexOf(q) > -1) return q;
    var s = stored();
    if (s && SUPPORTED.indexOf(s) > -1) return s;
    return DEFAULT;
  }

  function apply(lang) {
    var dict = window.I18N[lang] || window.I18N.en;
    var en = window.I18N.en;

    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var v = dict[el.dataset.i18n];
      if (v == null) v = en[el.dataset.i18n];
      if (typeof v === 'string') el.innerHTML = v;
    });

    document.querySelectorAll('[data-i18n-list]').forEach(function (el) {
      var v = dict[el.dataset.i18nList] || en[el.dataset.i18nList];
      if (!Array.isArray(v)) return;
      el.innerHTML = v.map(function (i) { return '<li>' + i + '</li>'; }).join('');
    });

    document.querySelectorAll('[data-i18n-attr]').forEach(function (el) {
      el.dataset.i18nAttr.split('|').forEach(function (pair) {
        var bits = pair.split(':');
        var v = dict[bits[1]] || en[bits[1]];
        if (typeof v === 'string') el.setAttribute(bits[0], v);
      });
    });

    document.querySelectorAll('.lang-btn').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
    });

    remember(lang);
  }

  function reveal() {
    document.documentElement.classList.remove('lang-pending');
  }

  function init() {
    try {
      var current = detect();
      if (current !== 'en') apply(current);
      else document.querySelectorAll('.lang-btn').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b.dataset.lang === 'en'));
      });

      document.querySelectorAll('.lang-btn').forEach(function (b) {
        b.addEventListener('click', function () { apply(b.dataset.lang); });
      });
    } finally {
      reveal();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
