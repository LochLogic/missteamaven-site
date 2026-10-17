# Maven Coaching site (redesign preview)

A rebuilt, re-imagined version of [missteamaven.com](https://www.missteamaven.com), currently on Wix.
This repo is a **preview for feedback**. Nothing here replaces the live site yet.

- Live preview: published by GitHub Pages on every push to `main` (noindex, so it never competes with the real site in search)
- What changed and why, plus open questions: [REDESIGN-NOTES.md](REDESIGN-NOTES.md)

## How it works

Plain HTML, CSS and a little JavaScript. No framework, no dependencies beyond Python 3.

```
src/
  layout.html        shared header, footer, <head>
  pages/*.html       one file per page, with a small metadata comment on top
  partials/*.html    reusable blocks (closing call-to-action, logo wall)
  assets/            css, js, images (already web-sized)
  _redirects         old Wix URLs -> new pages (for Cloudflare Pages / Netlify)
build.py             wraps pages in the layout, writes dist/
tools/prep_images.py resizes the original Wix images (needs Pillow and the original download)
```

Build and preview locally:

```bash
python build.py
python -m http.server 8090 --directory dist
```

Preview build for a sub-path (what GitHub Pages runs):

```bash
BASE=/missteamaven-site PREVIEW=1 python build.py
```

## Editing content

- Text: edit the page in `src/pages/`, then rebuild.
- Calendar: the "On the calendar" block lives in `src/pages/contact.html`.
- Contact form: currently opens a pre-filled email to missteamaven@gmail.com. Swap in a form service before launch (see notes).
