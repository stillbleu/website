# Editing the StillBleu website yourself

Everything on the site — every sentence, price and address, in both English and
French — lives in **one file: `content.py`**. You change the text there, run one
command, and the whole site is rebuilt in both languages.

You never need to touch HTML.

---

## The 5-minute version

1. Open `content.py` in any plain-text editor (TextEdit on Mac, Notepad on
   Windows, or the free [VS Code](https://code.visualstudio.com)).
2. Find the line you want to change (see the table below for which line).
3. Change the text **between the quote marks** — never the part before the `:`.
4. Save the file.
5. Open a Terminal in this folder and run:

   ```
   python3 build.py
   ```

6. Upload the folder to Netlify (see "Publishing" at the end).

That's it. Step 5 rewrites all seven `.html` pages and the translations file.

---

## How `content.py` is organised

The file has two halves:

```python
EN = {                                  # ← English — lines 4 to ~265
 "book.det.pay.v": "Cash and TWINT",
 ...
}

FR = {                                  # ← French — line 267 to the end
 "book.det.pay.v": "Espèces et TWINT",
 ...
}
```

Every piece of text has a **key** (`"book.det.pay.v"`) that appears **twice** —
once in the English half, once in the French half. When you change something,
change it in **both halves**, or the site will still show the old wording to
French visitors.

> **Tip:** to find both copies at once, search the file for the key
> (`Cmd+F` / `Ctrl+F`) and use "Find next".

### The rules

- Only edit what is **inside the double quotes**.
- Keep the comma at the end of the line.
- If your text contains a `"`, write it as `\"`.
- Apostrophes are fine (`l'Aubier`), accents are fine (`é`, `à`, `ê`).
- Text in `<strong>…</strong>` or `<em>…</em>` is bold / italic — you can keep
  it, move it, or drop it.

---

## Where to change the most common things

| What you want to change | Key to search for in `content.py` |
|---|---|
| **Prices** | `book.det.fees.v` |
| **Cancellation policy** | `book.det.cancel.v` |
| **Payment methods** | `book.det.pay.v` |
| **Session length** | `book.det.duration.v` |
| **Languages spoken** | `book.det.lang.v` |
| **Postal address** | `cont.addr.v` (contact page), `foot.addr` (footer), `book.det.location.v` (booking page) |
| **Directions by car** | `cont.get.car.v` |
| **Directions by public transport** | `cont.get.pt.v` |
| **Parking** | `cont.get.park.v` |
| **Home page headline text** | `hero.sub`, `hero.tag`, `hero.text` |
| **The list of therapies** | `serv.1.h` … `serv.6.p` (`.h` = heading, `.p` = paragraph) |
| **Your biography** | `about.lead`, `about.p2`, `about.p3`, `about.p4` |
| **Photo caption** | `about.portrait.cap` |

**Phone number and email** are not in `content.py` — they are at the top of
`build.py`:

```python
PHONE      = "+41 76 409 62 42"
PHONE_HREF = "+41764096242"      # the same number, no spaces — for click-to-call
EMAIL      = "info@stillbleu.ch"
```

---

## Changing the prices — a worked example

Search `content.py` for `book.det.fees.v`. You will find this in the English
half:

```python
"book.det.fees.v": "<ul class=\"fee-list\"><li><span>First consultation, 60 minutes</span><b>CHF 120</b></li>…",
```

Each appointment is one `<li>` block, built the same way:

```
<li><span>WHAT IT IS</span><b>WHAT IT COSTS</b></li>
```

- To **change a price**, edit the number between `<b>` and `</b>`.
- To **remove a line**, delete the whole `<li>…</li>`.
- To **add a line**, copy an existing `<li>…</li>` and paste it just before the
  closing `</ul>`, then edit it.

Then do exactly the same in the French half (search for `book.det.fees.v`
again — the second match).

The cancellation policy (`book.det.cancel.v`) works identically.

---

## Adding your photo

Save your photo as **`assets/img/srijan.jpg`**. That's the only step — the
About page already has a place for it and will show it as soon as the file
exists. (If the file is missing, the page simply leaves the space out, which is
why you don't see a broken image today.)

- Portrait orientation works best, roughly 900 × 1125 pixels.
- Keep it under about 400 KB so pages stay fast. On a Mac: open the photo in
  Preview → *Tools → Adjust Size*, set the width to 900, then *File → Export*
  as JPEG at around 70% quality.
- The caption under the photo is the key `about.portrait.cap`.

To change the caption or remove it, edit that key in both halves of
`content.py`.

---

## Adding or changing images and the logo

All images live in `assets/img/`. To replace one, **save the new file over the
old one using the same filename** — nothing else needs changing.

| File | Where it appears |
|---|---|
| `logo-full.png` | Large logo on the home page |
| `logo-mark.png` | Small logo in the header |
| `favicon-64.png`, `apple-touch-icon.png` | Browser tab icon |
| `srijan.jpg` | Your photo on the About page (add this one) |

---

## Which language visitors see

The site opens in **French** by default. Visitors can switch with the EN / FR
buttons in the top right, and their choice is remembered on their device.

You can link straight to one language by adding `?lang=en` or `?lang=fr` to any
address, e.g. `https://stillbleu.ch/booking.html?lang=en` — useful when you send
a link to an English-speaking patient.

To change the default back to English, open
`assets/js/_i18n_runtime.js` and change this line:

```javascript
var DEFAULT = 'fr';
```

then run `python3 build.py` again.

---

## Publishing your changes

The site is hosted on **Netlify**, which is free for a site this size.

**To put a change online:**

1. Sign in at [app.netlify.com](https://app.netlify.com).
2. Open the StillBleu site, go to the **Deploys** tab.
3. Drag this whole `website` folder onto the drop zone that says
   *"Drag and drop your site output folder here"*.
4. Wait about thirty seconds. The new version is live.

Nothing is ever lost: Netlify keeps every past version under **Deploys**, and
you can click any older one and choose **Publish deploy** to roll back.

### About the login

I can't create the account or set a password for you — Netlify needs you to do
that yourself, and it's better that the password only ever exists in your own
password manager.

**To set it up (once, about five minutes):**

1. Go to [netlify.com](https://www.netlify.com) and click **Sign up**.
2. Choose **Email** and use `info@stillbleu.ch` (or whichever address you want
   to own the site).
3. Pick a strong password and save it in your password manager.
4. Confirm the address from the email Netlify sends you.
5. On the Netlify dashboard, drag this `website` folder onto the page — the
   site is live at a temporary address within a minute.
6. Go to **Site configuration → Domain management** to point `stillbleu.ch` at
   it. Netlify issues the HTTPS certificate automatically.

If the site is **already online** and someone else set it up, ask them to go to
**Team settings → Members → Invite members** and invite `info@stillbleu.ch` as
an **Owner**. You will then set your own password from the invitation email.

### Form submissions

Both forms (appointment requests and contact messages) are handled by Netlify.
Submissions are stored in the dashboard, but **no email is sent until you turn
that on**:

**Site configuration → Forms → Form notifications → Add notification → Email
notification**, then enter the address that should receive them.

---

## If something breaks

Nothing you do in `content.py` can break the live site — the site only changes
when you upload the folder to Netlify.

If `python3 build.py` prints an error instead of the list of pages, it is almost
always one of three things:

| Error mentions | What to look for |
|---|---|
| `SyntaxError` / `unterminated string` | A missing `"` or a missing comma at the end of the line you edited |
| `KeyError` | A key name was changed — restore the text before the `:` |
| `command not found: python3` | Python isn't installed. On a Mac, run `xcode-select --install` once |

A `SyntaxError` stops the build before anything is written. Fix the line and
run the command again — and if a build ever stops halfway, just run it again
once the error is fixed; it always rewrites every page from scratch.

**Before a big edit,** duplicate the whole `website` folder and keep the copy.
That is the simplest possible backup.

---

## Seeing your changes before publishing

To look at the site on your own computer first:

```
cd /path/to/website
python3 -m http.server 8777
```

Then open <http://localhost:8777> in your browser. Press `Ctrl+C` in the
Terminal to stop it. Nothing here is visible to anyone else.
