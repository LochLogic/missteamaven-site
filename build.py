"""Tiny static-site build: wraps each page in the shared layout.

Pages live in src/pages/*.html and start with a metadata comment:

    <!--
    title: League Training
    description: One-sentence summary for search results.
    path: /leagues/
    nav: leagues
    -->

`<!-- include: name -->` pulls in src/partials/name.html.
Output goes to dist/, one folder per page so URLs stay clean (/leagues/).

Usage: python build.py
Preview build (e.g. GitHub Pages under /repo-name):
    BASE=/repo-name PREVIEW=1 python build.py
BASE prefixes every root-relative link; PREVIEW adds noindex so search engines
never treat the preview as a duplicate of the real site.
"""
import os
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
SITE_URL = "https://www.missteamaven.com"

META_RE = re.compile(r"^\s*<!--(.*?)-->", re.S)
INCLUDE_RE = re.compile(r"<!--\s*include:\s*([\w-]+)\s*-->")
NAV_KEYS = ["leagues", "skaters", "juniors", "coaches", "about", "reviews"]
BASE = os.environ.get("BASE", "").rstrip("/")
PREVIEW = bool(os.environ.get("PREVIEW"))
ROOT_LINK_RE = re.compile(r'((?:href|src)=")/(?!/)')


def rebase(html):
    if PREVIEW:
        html = html.replace("<head>", '<head>\n  <meta name="robots" content="noindex, nofollow">', 1)
    return ROOT_LINK_RE.sub(lambda m: f"{m.group(1)}{BASE}/", html) if BASE else html


def includes(html):
    return INCLUDE_RE.sub(lambda m: includes((SRC / "partials" / f"{m.group(1)}.html").read_text("utf-8")), html)


def parse(page):
    text = page.read_text("utf-8")
    m = META_RE.match(text)
    meta = dict(line.split(":", 1) for line in m.group(1).strip().splitlines())
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    return meta, text[m.end():]


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC / "assets", DIST / "assets")
    for extra in ["_redirects", "robots.txt"]:
        shutil.copy(SRC / extra, DIST / extra)
    if PREVIEW:
        (DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n", "utf-8")
        (DIST / ".nojekyll").write_text("", "utf-8")

    layout = includes((SRC / "layout.html").read_text("utf-8"))
    urls = []
    for page in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse(page)
        html = layout.replace("{{content}}", includes(body))
        for key in ["title", "description", "path", "bodyclass", "ogimage"]:
            html = html.replace("{{" + key + "}}", meta.get(key, ""))
        for key in NAV_KEYS:
            html = html.replace("{{nav-" + key + "}}", ' aria-current="page"' if meta.get("nav") == key else "")
        html = html.replace("{{year}}", str(date.today().year))
        out = DIST / meta["path"].strip("/") / "index.html" if meta["path"] != "/" else DIST / "index.html"
        if meta["path"] == "/404/":
            out = DIST / "404.html"
        else:
            urls.append(meta["path"])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rebase(html), "utf-8")
        print(f"built {meta['path']}")

    sitemap = "".join(f"<url><loc>{SITE_URL}{u}</loc></url>" for u in urls)
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>',
        "utf-8",
    )


if __name__ == "__main__":
    main()
