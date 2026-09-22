# Dr. Srijan Gupta — clinic website

Static site for the practice at L'Aubier, Montézillon. No build tools, no
dependencies: plain HTML, one CSS file, two small JS files.

## What's here

```
index.html        Home
about.html        About
approach.html     Approach (salutogenesis)
therapies.html    Therapies
booking.html      Book an appointment (Calendly + request form)
contact.html      Contact (address, map, message form)
thank-you.html    Shown after a form is submitted
assets/css/style.css
assets/js/i18n.js   translations for EN / FR + language switcher
assets/js/_i18n_runtime.js  the switcher alone; build.py appends it to i18n.js
assets/js/main.js   mobile menu, scroll reveal, Calendly placeholder
netlify.toml, robots.txt, sitemap.xml
build.py, content.py   optional: regenerate the HTML from source copy
```

**To change anything on the site, edit `content.py` and run `python3 build.py`.**
See **[EDITING-GUIDE.md](EDITING-GUIDE.md)** — a step-by-step guide written for
someone who has never edited a website, covering prices, the cancellation
policy, the address, the photo and publishing.

The `.html` files are generated; edits made directly to them are overwritten by
the next build.

---

## 1. Before going live — things to fill in

Every unknown is marked on the page with a yellow **TO FILL** badge, so you can
find them by opening each page, or by searching the files for `class="todo"`.

| Where | What's needed |
|---|---|
| `assets/img/srijan.jpg` | **Your photo** — drop the file in and the About page shows it (see EDITING-GUIDE.md) |
| `booking.html` | The Calendly link (see below) |
| `therapies.html` | Confirm which external therapies you actually offer — delete the rest from the list |

Fees, cancellation policy, session duration, languages, payment, address,
directions and parking are all filled in (September 2026). Please check the map
pin (`build.py`, the OpenStreetMap `iframe` — replace the `marker=` and `bbox=`
coordinates if it's off).

---

## 2. Calendly

Open `booking.html`, find:

```html
<div class="calendly-inline-widget" id="calendly"
     data-url="https://calendly.com/YOUR-CALENDLY-LINK?hide_gdpr_banner=1&..."
```

Replace `YOUR-CALENDLY-LINK` with your own scheduling link, e.g.
`srijangupta/first-consultation`. Keep the `?...` parameters — they match the
site's colours. Until you do, the page shows a neutral placeholder box instead
of a broken widget.

In Calendly, create one event type per appointment kind (first consultation,
external therapy, acupuncture) and set the durations there.

---

## 3. Deploying to Netlify

1. Create a free account at netlify.com.
2. Drag this whole folder onto the Netlify "Sites" page — that's the entire
   deploy. (Or connect a Git repository; no build command is needed.)
3. **Forms:** Netlify detects the two forms automatically (`appointment` and
   `contact`). Go to **Site configuration → Forms → Form notifications → Add
   notification → Email notification** and enter the address that should
   receive submissions. Without this step, submissions are stored in the
   Netlify dashboard but no email is sent.
4. **Domain:** Site configuration → Domain management. HTTPS is automatic.
5. After you have a domain, replace `REPLACE-WITH-YOUR-DOMAIN` in
   `robots.txt` and `sitemap.xml`.

Spam protection: both forms carry a hidden honeypot field. If spam gets
through, enable reCAPTCHA in the Netlify form settings.

---

## 4. Languages

The site ships in English and French. English is written into the HTML;
French is swapped in by `assets/js/i18n.js`.

- **French is the default.** Every visitor lands on the French version; the
  default lives in `assets/js/_i18n_runtime.js` as `var DEFAULT = 'fr'`.
- To avoid a flash of the English source text, `page()` in `build.py` hides the
  body until the swap has run (`html.lang-pending`), with a 700 ms safety timer
  and a `<noscript>` fallback so the page always appears.
- The choice is remembered and can be forced with `?lang=fr` (or `?lang=en`).
- To change wording: edit the string in `assets/js/i18n.js` (both languages
  live in the `window.I18N` object at the top) **and** the matching English
  text in the `.html` file — or edit `content.py` and re-run `python3 build.py`,
  which keeps both in sync for you.

The French text is a careful translation of the English, but it has not been
reviewed by a native speaker — worth a read-through before launch, since most
local visitors will see it.

---

## 5. Look and feel

The design follows the CV, so the site and the CV read as one identity:

- **Colours** sampled directly from the CV — warm cream `#FDF7EA`, olive green
  `#3D4A12`, rust `#B4470F`, gold `#C79A4E`. They live as CSS variables at the
  top of `assets/css/style.css`; change one there and it updates everywhere.
- **Type** — Cinzel (roman capitals) for the name, as on the CV; Cormorant
  Garamond for headings and italic quotes; Karla for body text.
- **Logo** — `assets/img/emblem.png` is the emblem from the CV, cut out of the
  PDF with a transparent background. It is 215 × 242 px, which is all the
  source contains; it is sharp at header size but would go soft if enlarged
  much beyond ~150 px. **If you have the original logo file, drop it in over
  this one** — same filename, and nothing else needs changing.
- `assets/img/emblem-line.svg` is a line-drawn version of the same emblem
  (used large in the hero); it stays crisp at any size.
- Two lines from the CV are used verbatim: "Integrating science, wisdom and
  compassion for conscious care." in the footer, and "The art of healing is to
  nourish the body, calm the mind and uplift the soul." on the Approach page.

## 6. Notes

- The About page has a portrait slot at `assets/img/srijan.jpg`. It is empty
  today: the `<figure>` removes itself if the file is missing, so nothing
  breaks until the photo is added.
- Apart from the portrait, the imagery is drawn line-work so the site stays
  fast and has no licensing issues. Photos of the practice rooms or of L'Aubier
  would fit well at the top of the Therapies page.
- Certificates are deliberately not published — the About page lists the
  qualifications and says they are available on request.
- Nothing on the site claims medical cures; the Approach page states that
  anthroposophic medicine extends rather than replaces conventional medicine.
  Please check the wording against Swiss rules on medical advertising and
  against what you may call yourself before your MEBEKO recognition is complete.
