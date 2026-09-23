# -*- coding: utf-8 -*-
"""Generates the static site from content.py. Run: python3 build.py"""
import json, os, re
from content import LANGS, EN

OUT = os.path.dirname(os.path.abspath(__file__))

PHONE      = "+41 76 409 62 42"
PHONE_HREF = "+41764096242"
EMAIL      = "info@stillbleu.ch"
YEAR       = "2026"

# ---------------------------------------------------------------------------
# Paste the Calendly scheduling link here, e.g.
#   CALENDLY_URL = "https://calendly.com/srijangupta/consultation"
# Until it is set, the booking page shows a placeholder instead of the widget.
CALENDLY_URL = "https://calendly.com/stillbleu-info/30min"
# ---------------------------------------------------------------------------

# --------------------------------------------------------------------------
# icons
# --------------------------------------------------------------------------
def svg(body, cls="", vb="0 0 24 24", extra=''):
    return (f'<svg class="{cls}" viewBox="{vb}" fill="none" stroke="currentColor" '
            f'stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" {extra}>{body}</svg>')

ICONS = {
 # hands / touch — external therapy
 "touch": '<path d="M8.5 13V5.4a1.4 1.4 0 0 1 2.8 0V11"/><path d="M11.3 11V4.2a1.4 1.4 0 0 1 2.8 0V11"/>'
          '<path d="M14.1 11.6V6.6a1.35 1.35 0 0 1 2.7 0V15c0 3.3-2.3 5.8-5.5 5.8-3 0-4.6-1.7-5.6-3.9'
          'l-1.5-3.3a1.4 1.4 0 0 1 2.3-1.5l1.4 1.7"/>',
 # needle — acupuncture
 "needle": '<path d="M20.5 3.5 9.8 14.2"/><path d="m7 17 2.8-2.8"/><path d="M4 20.5 6.4 18"/>'
           '<circle cx="16.4" cy="7.6" r="3.4"/>',
 # lotus / breath — yoga
 "lotus": '<path d="M12 4.5c1.9 2 2.8 4 2.8 6.2 0 2-.9 3.7-2.8 5.3-1.9-1.6-2.8-3.3-2.8-5.3 0-2.2.9-4.2 2.8-6.2Z"/>'
          '<path d="M12 16c-2.7 2-5.4 2.4-8.2 1.3 1-2.4 2.6-3.9 4.9-4.6"/>'
          '<path d="M12 16c2.7 2 5.4 2.4 8.2 1.3-1-2.4-2.6-3.9-4.9-4.6"/><path d="M4.5 20h15"/>',
 # sound waves
 "sound": '<path d="M4 10v4"/><path d="M8 6.5v11"/><path d="M12 3.5v17"/><path d="M16 7.5v9"/><path d="M20 10.5v3"/>',
 # energy
 "energy": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3"/><path d="M12 19v3"/><path d="M2 12h3"/>'
           '<path d="M19 12h3"/><path d="m5 5 2.1 2.1"/><path d="m16.9 16.9 2.1 2.1"/>'
           '<path d="m19 5-2.1 2.1"/><path d="m7.1 16.9-2.1 2.1"/>',
 # leaf — guidance
 "leaf": '<path d="M4.5 19.5C3 14 6 5.5 19.5 4.5c1 10.5-5 15.5-11 15"/><path d="M4.5 19.5c3.5-6 7-9 12-12.5"/>',
 "pin": '<path d="M12 21s7-5.7 7-11a7 7 0 1 0-14 0c0 5.3 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
 "phone": '<path d="M6.2 3.5h3l1.5 4-2 1.5a12 12 0 0 0 6.3 6.3l1.5-2 4 1.5v3a2 2 0 0 1-2.2 2A16.8 16.8 0 0 1 4.2 5.7a2 2 0 0 1 2-2.2Z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/>',
 "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.2V12l3 2"/>',
 "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.3 2.4 3.4 5.3 3.4 8.5S14.3 18.1 12 20.5c-2.3-2.4-3.4-5.3-3.4-8.5S9.7 5.9 12 3.5Z"/>',
}

BRAND_MARK = ('<img class="brand-mark logo" src="assets/img/logo-mark.png" width="52" height="52" alt="" loading="eager">')

LEAFRULE = svg(
  '<path d="M2 8h30" stroke-width="1"/><path d="M60 8H90" stroke-width="1"/>'
  '<path d="M46 2.4c3.2 1.5 4.6 3.6 4.6 5.6 0 2-1.4 4.1-4.6 5.6-3.2-1.5-4.6-3.6-4.6-5.6 0-2 1.4-4.1 4.6-5.6Z" stroke-width="1"/>'
  '<path d="M46 3.2v9.6" stroke-width=".8"/>',
  cls="leafrule", vb="0 0 92 16")

HERO_ART = ('<img class="hero-emblem" src="assets/img/logo-mark-gentle.gif" width="264" height="264" alt="" loading="eager">')

# --------------------------------------------------------------------------
# helpers — emit English text with a data-i18n hook
# --------------------------------------------------------------------------
def t(key):
    return EN[key]

def E(tag, key, cls=None, attrs=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-i18n="{key}"{(" " + attrs) if attrs else ""}>{t(key)}</{tag}>'

def LI(key, cls="ticklist"):
    items = "".join(f"<li>{i}</li>" for i in EN[key])
    return f'<ul class="{cls}" data-i18n-list="{key}">{items}</ul>'

def STEPS(key):
    items = "".join(f"<li>{i}</li>" for i in EN[key])
    return f'<ol class="steps" data-i18n-list="{key}">{items}</ol>'

def PILLS(key):
    items = "".join(f"<li>{i}</li>" for i in EN[key])
    return f'<ul class="pill-row" data-i18n-list="{key}">{items}</ul>'

# --------------------------------------------------------------------------
# chrome
# --------------------------------------------------------------------------
NAVITEMS = [("index.html", "nav.home"), ("about.html", "nav.about"),
            ("approach.html", "nav.approach"), ("therapies.html", "nav.therapies"),
            ("contact.html", "nav.contact")]

def header(page):
    links = ""
    for href, key in NAVITEMS:
        cur = ' aria-current="page"' if href == page else ""
        links += f'<a href="{href}"{cur} data-i18n="{key}">{t(key)}</a>'
    langs = "".join(
        f'<button class="lang-btn" type="button" data-lang="{c}" aria-pressed="{"true" if c=="en" else "false"}">{c.upper()}</button>'
        for c in ("en", "fr"))
    return f'''<a class="skip" href="#main" data-i18n="skip">{t("skip")}</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">
      {BRAND_MARK}
      <span class="brand-text">
        <span class="brand-name">StillBleu</span>
        <span class="brand-sub" data-i18n="brand.sub">{t("brand.sub")}</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="{t("menu")}">
      {svg('<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>', vb="0 0 24 24", extra='width="22" height="22"')}
    </button>
    <nav class="nav" id="nav">
      {links}
      <a class="btn btn-primary btn-sm header-cta" href="booking.html" data-i18n="cta.book">{t("cta.book")}</a>
      <div class="langs">{langs}</div>
    </nav>
  </div>
</header>'''

def footer():
    navlinks = "".join(f'<li><a href="{h}" data-i18n="{k}">{t(k)}</a></li>'
                       for h, k in NAVITEMS + [("booking.html", "nav.book")])
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <div class="footer-brand">StillBleu</div>
      <p class="footer-quote" data-i18n="foot.quote">{t("foot.quote")}</p>
    </div>
    <div>
      <h4 data-i18n="foot.nav">{t("foot.nav")}</h4>
      <ul>{navlinks}</ul>
    </div>
    <div>
      <h4 data-i18n="foot.visit">{t("foot.visit")}</h4>
      <ul>
        <li data-i18n="foot.addr">{t("foot.addr")}</li>
        <li><a href="tel:{PHONE_HREF}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© {YEAR} StillBleu. <span data-i18n="foot.rights">{t("foot.rights")}</span></span>
    <span data-i18n="foot.hosted">{t("foot.hosted")}</span>
  </div>
</footer>'''

def page(fname, title_key, desc_key, body, cur, extra_js=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-i18n="{title_key}">{t(title_key)}</title>
<meta name="description" data-i18n-attr="content:{desc_key}" content="{t(desc_key)}">
<meta name="theme-color" content="#1D3A52">
<meta property="og:title" content="{t(title_key)}">
<meta property="og:description" content="{t(desc_key)}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/img/favicon-64.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Prata&family=Poppins:wght@400;500&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Karla:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=3">
<script src="assets/js/i18n.js?v=2"></script>
<style>html.lang-pending body{{visibility:hidden}}</style>
<script>
(function(){{var h=document.documentElement;h.classList.add('lang-pending');
setTimeout(function(){{h.classList.remove('lang-pending');}},700);}})();
</script>
<noscript><style>.reveal{{opacity:1;transform:none}}html.lang-pending body{{visibility:visible}}</style></noscript>
</head>
<body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
{extra_js}
<script src="assets/js/main.js"></script>
</body>
</html>
'''

def bookcta():
    return f'''<section class="sec-deep">
  <div class="wrap narrow center">
    {E("p","bcta.head".replace("head","head"),"eyebrow") if False else ""}
    <h2 data-i18n="bcta.head">{t("bcta.head")}</h2>
    <p data-i18n="bcta.text">{t("bcta.text")}</p>
    <p style="margin-top:1.3rem;margin-bottom:0"><a class="btn btn-light" href="booking.html" data-i18n="cta.book">{t("cta.book")}</a></p>
  </div>
</section>'''

# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def home():
    cards = ""
    # row 1: the three services featured on the home page
    featured = [("touch", 1), ("leaf", 6), ("energy", 5)]
    for pos, (ic, n) in enumerate(featured):
        lead = ' lead-card' if pos == 0 else ''
        cards += f'''<article class="card{lead} reveal">
        {svg(ICONS[ic], cls="card-icon")}
        <h3 data-i18n="serv.{n}.h">{t(f"serv.{n}.h")}</h3>
        <p data-i18n="serv.{n}.p">{t(f"serv.{n}.p")}</p>
      </article>'''
    body = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>StillBleu</h1>
      <p class="hero-sub" data-i18n="hero.sub">{t("hero.sub")}</p>
      <p class="hero-tag" data-i18n="hero.tag">{t("hero.tag")}</p>
      <p class="lead" data-i18n="hero.text">{t("hero.text")}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="booking.html" data-i18n="cta.book">{t("cta.book")}</a>
        <a class="btn btn-ghost" href="therapies.html" data-i18n="cta.therapies">{t("cta.therapies")}</a>
        <a class="btn btn-ghost" href="{t('flyer.file')}" download data-i18n="flyer.download" data-i18n-attr="href:flyer.file">{t("flyer.download")}</a>
      </div>
    </div>
    <div>{HERO_ART}</div>
  </div>
</section>

<div class="locbar"><div class="wrap"><p data-i18n="loc.text">{t("loc.text")}</p></div></div>

<section>
  <div class="wrap split">
    <div>
      <p class="eyebrow" data-i18n="who.eyebrow">{t("who.eyebrow")}</p>
      <h2 data-i18n="who.head">{t("who.head")}</h2>
      <p data-i18n="who.lead">{t("who.lead")}</p>
      <p style="color:var(--ink-mute);font-size:.95rem" data-i18n="who.note">{t("who.note")}</p>
    </div>
    <div>{LI("who.items")}</div>
  </div>
</section>

<section>
  <div class="wrap split">
    <div>
      <p class="eyebrow" data-i18n="core.eyebrow">{t("core.eyebrow")}</p>
      <h2 data-i18n="core.head">{t("core.head")}</h2>
      <p data-i18n="core.lead">{t("core.lead")}</p>
      <p style="color:var(--ink-mute);font-size:.95rem" data-i18n="core.note">{t("core.note")}</p>
    </div>
    <div>
      <p style="font-weight:700;letter-spacing:.04em" data-i18n="core.sub">{t("core.sub")}</p>
      {LI("core.items")}
      <a class="btn btn-ghost btn-sm" href="approach.html" data-i18n="cta.more">{t("cta.more")}</a>
    </div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap">
    <div class="center" style="max-width:640px;margin-inline:auto">
      <p class="eyebrow" data-i18n="serv.eyebrow">{t("serv.eyebrow")}</p>
      <h2 data-i18n="serv.head">{t("serv.head")}</h2>
      <p data-i18n="serv.lead">{t("serv.lead")}</p>
      {LEAFRULE}
    </div>
    <div class="grid grid-3">{cards}</div>
    <p class="center" style="margin-top:34px"><a class="btn btn-ghost" href="therapies.html" data-i18n="cta.therapies">{t("cta.therapies")}</a></p>
  </div>
</section>

{bookcta()}'''
    return page("index.html", "home.title", "home.desc", body, "index.html")

def about():
    body = f'''<section class="pagehead">
  <div class="wrap narrow">
    <p class="eyebrow" data-i18n="phil.eyebrow">{t("phil.eyebrow")}</p>
    <h1 style="font-size:clamp(2.2rem,4.6vw,3.4rem)" data-i18n="phil.head">{t("phil.head")}</h1>
    <p class="lead" data-i18n="phil.p1">{t("phil.p1")}</p>
    <p data-i18n="phil.p2">{t("phil.p2")}</p>
    <p data-i18n="phil.p3">{t("phil.p3")}</p>
  </div>
</section>

<section>
  <div class="wrap split">
    <div>
      <p class="eyebrow" data-i18n="about.eyebrow">{t("about.eyebrow")}</p>
      <h2 style="font-size:clamp(2rem,4.2vw,3rem);margin-bottom:.2em" data-i18n="about.head">{t("about.head")}</h2>
      <p class="about-role" data-i18n="about.role">{t("about.role")}</p>
      <p class="lead" data-i18n="about.lead">{t("about.lead")}</p>
      <p data-i18n="about.p2">{t("about.p2")}</p>
      <p data-i18n="about.p3">{t("about.p3")}</p>
      <p data-i18n="about.p4">{t("about.p4")}</p>
      <p style="color:var(--ink-mute);font-size:.95rem" data-i18n="about.accred">{t("about.accred")}</p>
    </div>
    <div>
      <figure class="portrait" id="portrait">
        <img src="assets/img/srijan.jpg" width="900" height="1125" loading="lazy"
             alt="Dr Srijan Gupta"
             onerror="document.getElementById('portrait').remove()">
        <figcaption data-i18n="about.portrait.cap">{t("about.portrait.cap")}</figcaption>
      </figure>
      <blockquote class="quote" data-i18n="about.quote">{t("about.quote")}</blockquote>
    </div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap narrow">
    <h2 data-i18n="jour.head">{t("jour.head")}</h2>
    <p data-i18n="jour.p1">{t("jour.p1")}</p>
    <p data-i18n="jour.p2">{t("jour.p2")}</p>
    <p data-i18n="jour.p3">{t("jour.p3")}</p>
    <p data-i18n="jour.p4">{t("jour.p4")}</p>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div>
      <h2 data-i18n="work.head">{t("work.head")}</h2>
      <p class="lead" data-i18n="work.p1">{t("work.p1")}</p>
      <p data-i18n="work.p2">{t("work.p2")}</p>
      <p data-i18n="work.p3">{t("work.p3")}</p>
      <p data-i18n="work.p4">{t("work.p4")}</p>
      <p data-i18n="work.p5">{t("work.p5")}</p>
      <p data-i18n="work.p6">{t("work.p6")}</p>
    </div>
    <div>
      <p style="font-weight:700;letter-spacing:.04em" data-i18n="work.lead">{t("work.lead")}</p>
      {LI("work.items")}
    </div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap split" style="align-items:start">
    <div>
      <h2 data-i18n="about.train.head">{t("about.train.head")}</h2>
      {LI("about.train.items")}
      <h3 style="margin-top:2.2rem" data-i18n="about.comp.head">{t("about.comp.head")}</h3>
      <p style="font-size:.95rem;color:var(--ink-mute)" data-i18n="about.comp.note">{t("about.comp.note")}</p>
      {LI("about.comp.items")}
    </div>
    <div>
      <h2 data-i18n="about.exp.head">{t("about.exp.head")}</h2>
      <p data-i18n="about.exp.p">{t("about.exp.p")}</p>
      <p style="font-size:.9rem;color:var(--ink-mute)" data-i18n="about.certnote">{t("about.certnote")}</p>
    </div>
  </div>
</section>

{bookcta()}'''
    return page("about.html", "about.title", "about.desc", body, "about.html")

def approach():
    cards = ""
    for n in range(1, 6):
        cards += f'''<article class="card reveal">
        <h3 data-i18n="appr.p{n}.h">{t(f"appr.p{n}.h")}</h3>
        <p data-i18n="appr.p{n}.p">{t(f"appr.p{n}.p")}</p>
      </article>'''
    body = f'''<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow" data-i18n="appr.eyebrow">{t("appr.eyebrow")}</p>
    <h1 style="font-size:clamp(2.2rem,4.6vw,3.4rem)" data-i18n="appr.head">{t("appr.head")}</h1>
    <p class="epigraph" data-i18n="appr.epigraph">{t("appr.epigraph")}</p>
    <p class="lead" data-i18n="appr.lead">{t("appr.lead")}</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2 class="center" data-i18n="appr.prin.head">{t("appr.prin.head")}</h2>
    {LEAFRULE}
    <div class="grid grid-3">{cards}</div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap narrow center">
    <h2 data-i18n="diag.head">{t("diag.head")}</h2>
    <div class="diagram">
      <div class="ring ring-outer"><span class="ring-label" data-i18n="diag.outer">{t("diag.outer")}</span>
        <div class="ring ring-mid"><span class="ring-label" data-i18n="diag.mid">{t("diag.mid")}</span>
          <div class="ring ring-core"><span data-i18n="diag.core">{t("diag.core")}</span></div>
        </div>
      </div>
    </div>
    <p class="diagram-note" data-i18n="diag.note">{t("diag.note")}</p>
  </div>
</section>

<section>
  <div class="wrap narrow">
    <h2 data-i18n="appr.close.head">{t("appr.close.head")}</h2>
    <p data-i18n="appr.close.p">{t("appr.close.p")}</p>
  </div>
</section>

{bookcta()}'''
    return page("approach.html", "appr.title", "appr.desc", body, "approach.html")

def therapies():
    comp = ""
    icons = ["needle", "lotus", "sound", "energy", "leaf"]
    for n, ic in enumerate(icons, start=1):
        comp += f'''<article class="card reveal">
        {svg(ICONS[ic], cls="card-icon")}
        <h3 data-i18n="ther.c{n}.h">{t(f"ther.c{n}.h")}</h3>
        <p data-i18n="ther.c{n}.p">{t(f"ther.c{n}.p")}</p>
      </article>'''
    body = f'''<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow" data-i18n="ther.eyebrow">{t("ther.eyebrow")}</p>
    <h1 style="font-size:clamp(2.2rem,4.6vw,3.4rem)" data-i18n="ther.head">{t("ther.head")}</h1>
    <p class="lead" data-i18n="ther.lead">{t("ther.lead")}</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="feature">
      <div class="feature-head">
        {svg(ICONS["touch"])}
        <h2 style="margin:0" data-i18n="ther.aet.head">{t("ther.aet.head")}</h2>
      </div>
      <p data-i18n="ther.aet.p">{t("ther.aet.p")}</p>
      <p data-i18n="ther.aet.p2">{t("ther.aet.p2")}</p>
      {PILLS("ther.aet.items")}
    </div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap">
    <div class="center" style="max-width:620px;margin-inline:auto">
      <h2 data-i18n="ther.comp.head">{t("ther.comp.head")}</h2>
      <p data-i18n="ther.comp.lead">{t("ther.comp.lead")}</p>
      {LEAFRULE}
    </div>
    <div class="grid grid-3">{comp}</div>
  </div>
</section>

<section>
  <div class="wrap narrow center">
    <h2 data-i18n="ther.note.head">{t("ther.note.head")}</h2>
    <p data-i18n="ther.note.p">{t("ther.note.p")}</p>
    <p style="margin-top:1.6rem"><a class="btn btn-primary" href="booking.html" data-i18n="cta.book">{t("cta.book")}</a></p>
  </div>
</section>'''
    return page("therapies.html", "ther.title", "ther.desc", body, "therapies.html")

def booking():
    rows = [
      ("book.det.location", "book.det.location.v", None),
      ("book.det.duration", "book.det.duration.v", None),
      ("book.det.format",   "book.det.format.v", None),
      ("book.det.online",   "book.det.online.v", None),
      ("book.det.lang",     "book.det.lang.v", None),
      ("book.det.fees",     "book.det.fees.v", None),
      ("book.det.pay",      "book.det.pay.v", None),
      ("book.det.cancel",   "book.det.cancel.v", None),
    ]
    WIDE = {"book.det.fees", "book.det.cancel"}
    dl = ""
    for key, val, todo in rows:
        if todo is None:
            dd = f'<dd data-i18n="{val}">{t(val)}</dd>'
        else:
            dd = f'<dd>{val}</dd>'
        cls = "dl-row dl-wide" if key in WIDE else "dl-row"
        dl += (f'<div class="{cls}"><dt data-i18n="{key}">{t(key)}</dt>{dd}</div>')

    body = f'''<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow" data-i18n="book.eyebrow">{t("book.eyebrow")}</p>
    <h1 style="font-size:clamp(2.2rem,4.6vw,3.4rem)" data-i18n="book.head">{t("book.head")}</h1>
    <p class="lead" data-i18n="book.lead">{t("book.lead")}</p>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div>
      <h2 data-i18n="book.first.head">{t("book.first.head")}</h2>
      <p data-i18n="book.first.p">{t("book.first.p")}</p>
      <h2 style="margin-top:2.4rem" data-i18n="book.exp.head">{t("book.exp.head")}</h2>
      {LI("book.exp.items")}
      <h2 style="margin-top:2.4rem" data-i18n="book.steps.head">{t("book.steps.head")}</h2>
      {STEPS("book.steps.items")}
    </div>
    <div>
      <h2 data-i18n="book.det.head">{t("book.det.head")}</h2>
      <dl class="dl">{dl}</dl>
    </div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap narrow">
    <h2 data-i18n="book.cal.head">{t("book.cal.head")}</h2>
    <p data-i18n="book.cal.text">{t("book.cal.text")}</p>
    <div class="calwrap">
      <div class="calendly-inline-widget" id="calendly"
           data-url="{CALENDLY_URL}?hide_gdpr_banner=1&amp;background_color=fdfbf7&amp;primary_color=35688e&amp;text_color=2c2a26"
           style="min-width:320px;height:760px"></div>
      <noscript><p data-i18n="book.nojs">{t("book.nojs")}</p></noscript>
    </div>
  </div>
</section>'''
    return page("booking.html", "book.title", "book.desc", body, "booking.html",
                extra_js='<script src="https://assets.calendly.com/assets/external/widget.js" async></script>')

def thankyou():
    body = f'''<section class="pagehead" style="min-height:52vh;display:flex;align-items:center">
  <div class="wrap narrow center">
    {LEAFRULE}
    <h1 style="font-size:clamp(2.4rem,5vw,3.6rem)" data-i18n="ty.head">{t("ty.head")}</h1>
    <p class="lead" data-i18n="ty.p">{t("ty.p")}</p>
    <p data-i18n="ty.p2">{t("ty.p2")}</p>
    <p style="margin-top:2rem"><a class="btn btn-primary" href="index.html" data-i18n="ty.btn">{t("ty.btn")}</a></p>
  </div>
</section>'''
    return page("thank-you.html", "ty.title", "ty.desc" if "ty.desc" in EN else "home.desc", body, "")

def contact():
    body = f'''<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow" data-i18n="cont.eyebrow">{t("cont.eyebrow")}</p>
    <h1 style="font-size:clamp(2.2rem,4.6vw,3.4rem)" data-i18n="cont.head">{t("cont.head")}</h1>
    <p class="lead" data-i18n="cont.lead">{t("cont.lead")}</p>
  </div>
</section>

<section>
  <div class="wrap contact-grid">
    <div>
      <h2 data-i18n="cont.addr.head">{t("cont.addr.head")}</h2>
      <ul class="contact-list">
        <li>{svg(ICONS["pin"])}<span data-i18n="cont.addr.v">{t("cont.addr.v")}</span></li>
        <li>{svg(ICONS["phone"])}<a href="tel:{PHONE_HREF}">{PHONE}</a></li>
        <li>{svg(ICONS["mail"])}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{svg(ICONS["clock"])}<span><span data-i18n="book.det.duration">{t("book.det.duration")}</span>: <span data-i18n="book.det.duration.v">{t("book.det.duration.v")}</span></span></li>
        <li>{svg(ICONS["globe"])}<span><span data-i18n="book.det.lang">{t("book.det.lang")}</span>: <span data-i18n="book.det.lang.v">{t("book.det.lang.v")}</span></span></li>
      </ul>

      <h2 style="margin-top:2.2rem" data-i18n="cont.get.head">{t("cont.get.head")}</h2>
      <dl class="dl">
        <div class="dl-row"><dt data-i18n="cont.get.car">{t("cont.get.car")}</dt><dd data-i18n="cont.get.car.v">{t("cont.get.car.v")}</dd></div>
        <div class="dl-row"><dt data-i18n="cont.get.pt">{t("cont.get.pt")}</dt><dd data-i18n="cont.get.pt.v">{t("cont.get.pt.v")}</dd></div>
        <div class="dl-row"><dt data-i18n="cont.get.park">{t("cont.get.park")}</dt><dd data-i18n="cont.get.park.v">{t("cont.get.park.v")}</dd></div>
      </dl>
      <p style="margin-top:1.4rem;font-size:.94rem" data-i18n="cont.aubier">{t("cont.aubier")}</p>
      <p style="margin-top:1.8rem"><a class="btn btn-primary" href="booking.html" data-i18n="cta.book">{t("cta.book")}</a></p>
    </div>

    <div>
      <h2 data-i18n="cont.map.head">{t("cont.map.head")}</h2>
      <div class="map">
        <iframe title="Map — StillBleu, Montézillon (NE)" loading="lazy"
          src="https://www.openstreetmap.org/export/embed.html?bbox=6.8137%2C46.9740%2C6.8617%2C46.9980&amp;layer=mapnik&amp;marker=46.98602%2C6.83770"></iframe>
      </div>
      <p style="margin-top:.9rem;font-size:.86rem;color:var(--ink-mute)">
        <a href="https://www.openstreetmap.org/?mlat=46.98602&amp;mlon=6.83770#map=15/46.98602/6.83770"
           target="_blank" rel="noopener">OpenStreetMap</a> · Les Murailles 5, 2037 Montézillon (NE)
      </p>
    </div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap narrow">
    <h2 data-i18n="cont.form.head">{t("cont.form.head")}</h2>
    <div class="formcard">
      <p class="formnote" data-i18n="cont.form.note">{t("cont.form.note")}</p>
      <form name="contact" method="POST" action="/thank-you.html"
            data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="contact">
        <p hidden><label>Leave this empty: <input name="bot-field"></label></p>
        <div class="field-row">
          <div class="field">
            <label for="cname" data-i18n="f.name">{t("f.name")}</label>
            <input type="text" id="cname" name="name" required>
          </div>
          <div class="field">
            <label for="cemail" data-i18n="f.email">{t("f.email")}</label>
            <input type="email" id="cemail" name="email" required>
          </div>
        </div>
        <div class="field">
          <label for="cmessage" data-i18n="f.msg2">{t("f.msg2")}</label>
          <textarea id="cmessage" name="message" required></textarea>
        </div>
        <div class="check">
          <input type="checkbox" id="cconsent" name="consent" required value="yes">
          <label for="cconsent" data-i18n="f.consent2">{t("f.consent2")}</label>
        </div>
        <button class="btn btn-primary" type="submit" data-i18n="cta.send">{t("cta.send")}</button>
      </form>
    </div>
  </div>
</section>

<section class="sec-deep">
  <div class="wrap narrow center">
    <p class="quote" style="border:0;padding:0;margin:0 auto;max-width:46ch;text-align:center"
       data-i18n="cont.close">{t("cont.close")}</p>
  </div>
</section>'''
    return page("contact.html", "cont.title", "cont.desc", body, "contact.html")

# --------------------------------------------------------------------------
# write everything
# --------------------------------------------------------------------------
def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✓", name)

# thank-you needs a description key
EN["ty.desc"] = "Your appointment request has been received."
LANGS["fr"]["ty.desc"] = "Votre demande de rendez-vous a bien été reçue."

print("Building site…")
write("index.html",      home())
write("about.html",      about())
write("approach.html",   approach())
write("therapies.html",  therapies())
write("booking.html",    booking())
write("contact.html",    contact())
write("thank-you.html",  thankyou())

# i18n bundle
bundle = "window.I18N = " + json.dumps(LANGS, ensure_ascii=False, indent=1) + ";\n"
bundle += open(os.path.join(OUT, "assets", "js", "_i18n_runtime.js"), encoding="utf-8").read()
write(os.path.join("assets", "js", "i18n.js"), bundle)


print("Done.")
