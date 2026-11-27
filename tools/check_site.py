#!/usr/bin/env python3
"""Validate the static site in the repository root.

Checks every HTML page for: resolvable internal links/assets/fragments, valid
JSON-LD, one <h1>, title/description/canonical, image width/height/alt,
reciprocal hreflang (incl. x-default) matching <html lang>, and that
sitemap.xml lists exactly the indexable canonical pages with the same
alternates. Exits non-zero on any error.

Usage: python3 tools/check_site.py [--external]   (--external also fetches external links)
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://nakas-hotel.com"
SKIP_DIRS = {".git", "tools", "node_modules"}
errors = []


def err(msg):
    errors.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self._in_title = False
        self._in_jsonld = False
        self._jsonld_buf = ""
        self.jsonld = []
        self.meta = {}
        self.canonical = None
        self.alternates = {}
        self.ids = set()
        self.refs = []  # (attr, url)
        self.h1 = 0
        self.imgs = []
        self.refresh = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                err(f"{self.name}: duplicate id #{a['id']}")
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
            if a.get("http-equiv", "").lower() == "refresh":
                self.refresh = a.get("content")
        elif tag == "link":
            rel = a.get("rel", "")
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel == "alternate" and "hreflang" in a:
                self.alternates[a["hreflang"]] = a.get("href")
            elif rel == "preload" and a.get("imagesrcset"):
                self.refs += [("imagesrcset", u.split()[0]) for u in a["imagesrcset"].split(",")]
            elif a.get("href"):
                self.refs.append(("href", a["href"]))
        elif tag == "script":
            if a.get("type") == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = ""
            elif a.get("src"):
                self.refs.append(("src", a["src"]))
        elif tag in ("a", "area") and a.get("href"):
            self.refs.append(("href", a["href"]))
        elif tag in ("img", "source", "iframe"):
            if a.get("src"):
                self.refs.append(("src", a["src"]))
            if a.get("srcset"):
                self.refs += [("srcset", u.split()[0]) for u in a["srcset"].split(",")]
            if tag == "img":
                self.imgs.append(a)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld.append(self._jsonld_buf)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_jsonld:
            self._jsonld_buf += data


def url_for(rel_path):
    p = rel_path.as_posix()
    if p == "index.html":
        return BASE + "/"
    if p.endswith("/index.html"):
        return BASE + "/" + p[: -len("index.html")]
    return BASE + "/" + p


def file_for(url):
    path = urlparse(url).path
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    return target


def collect_pages():
    pages = {}
    for f in sorted(ROOT.rglob("*.html")):
        rel = f.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        p = Page()
        p.name = rel.as_posix()
        p.url = url_for(rel)
        p.feed(f.read_text(encoding="utf-8"))
        pages[p.url] = p
    return pages


def check_jsonld(p):
    for raw in p.jsonld:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            err(f"{p.name}: invalid JSON-LD: {e}")
            continue
        if data.get("@context") != "https://schema.org":
            err(f"{p.name}: JSON-LD @context missing")
        nodes = data.get("@graph", [data])
        types = [n.get("@type") for n in nodes]
        hotels = [n for n in nodes if n.get("@type") == "Hotel"]
        if not hotels:
            err(f"{p.name}: no Hotel node in JSON-LD ({types})")
        for h in hotels:
            for key in ("name", "address", "geo", "telephone", "contactPoint", "numberOfRooms", "amenityFeature",
                        "potentialAction"):
                if key not in h:
                    err(f"{p.name}: Hotel JSON-LD lacks {key}")
            if "aggregateRating" in h or "review" in h:
                err(f"{p.name}: Hotel JSON-LD contains rating/review markup")
        for n in nodes:
            if n.get("@type") == "WebPage" and n.get("url") != p.canonical:
                err(f"{p.name}: WebPage url {n.get('url')} != canonical {p.canonical}")


def check_page(p, pages, external):
    noindex = "noindex" in p.meta.get("robots", "")
    if not p.lang:
        err(f"{p.name}: <html lang> missing")
    if not p.title.strip():
        err(f"{p.name}: <title> missing")
    if p.refresh:
        return noindex
    if not noindex:
        if p.h1 != 1:
            err(f"{p.name}: expected exactly one <h1>, found {p.h1}")
        if not p.meta.get("description"):
            err(f"{p.name}: meta description missing")
        if p.canonical != p.url:
            err(f"{p.name}: canonical {p.canonical} != {p.url}")
        if not p.jsonld:
            err(f"{p.name}: no JSON-LD")
    check_jsonld(p)
    for img in p.imgs:
        if "alt" not in img:
            err(f"{p.name}: <img src={img.get('src')}> without alt")
        if img.get("src", "").startswith("data:"):
            continue
        if not (img.get("width") and img.get("height")):
            err(f"{p.name}: <img src={img.get('src')}> without width/height")
    for attr, ref in p.refs:
        absolute = urljoin(p.url, ref)
        target, frag = urldefrag(absolute)
        parsed = urlparse(absolute)
        if parsed.scheme in ("mailto", "tel", "data"):
            continue
        if not absolute.startswith(BASE):
            external.add(target)
            continue
        f = file_for(target)
        if not f.is_file():
            err(f"{p.name}: broken {attr} -> {ref}")
            continue
        if frag:
            tp = pages.get(target) or pages.get(target.removesuffix("index.html"))
            if tp is not None and frag not in tp.ids:
                err(f"{p.name}: missing fragment {ref}")
    return noindex


def check_hreflang(pages):
    for url, p in pages.items():
        if not p.alternates:
            continue
        if "x-default" not in p.alternates:
            err(f"{p.name}: hreflang x-default missing")
        own = [h for h, u in p.alternates.items() if u == p.canonical and h != "x-default"]
        if own != [p.lang]:
            err(f"{p.name}: self hreflang {own} does not match <html lang={p.lang}>")
        for h, alt_url in p.alternates.items():
            other = pages.get(alt_url)
            if other is None:
                err(f"{p.name}: hreflang {h} -> {alt_url} is not a page in the site")
                continue
            if other.alternates != p.alternates:
                err(f"{p.name}: hreflang set differs from {other.name} (not reciprocal)")
            if h != "x-default" and other.lang != h:
                err(f"{p.name}: hreflang {h} -> {other.name} which has lang={other.lang}")


def check_sitemap(pages, indexable):
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    tree = ET.parse(ROOT / "sitemap.xml")
    locs = {}
    for u in tree.getroot().findall("s:url", ns):
        loc = u.find("s:loc", ns).text
        alts = {l.get("hreflang"): l.get("href") for l in u.findall("x:link", ns)}
        locs[loc] = alts
    for loc, alts in locs.items():
        p = pages.get(loc)
        if p is None:
            err(f"sitemap: {loc} is not a page")
            continue
        if loc not in indexable:
            err(f"sitemap: {loc} is not indexable/canonical")
        if alts != p.alternates:
            err(f"sitemap: alternates for {loc} differ from page hreflang")
    for url in indexable:
        if url not in locs:
            err(f"sitemap: indexable page {url} missing")
    robots = (ROOT / "robots.txt").read_text()
    if f"Sitemap: {BASE}/sitemap.xml" not in robots:
        err("robots.txt does not reference the sitemap")
    return locs


def check_titles(pages, indexable):
    seen = defaultdict(list)
    for url in indexable:
        seen[pages[url].title].append(url)
        seen["desc:" + pages[url].meta.get("description", "")].append(url)
    for k, urls in seen.items():
        if len(urls) > 1:
            err(f"duplicate title/description {k!r}: {urls}")


def check_external(urls):
    for u in sorted(urls):
        if "fonts.g" in u or "gc.zgo.at" in u or "goatcounter" in u:
            continue
        try:
            req = urllib.request.Request(u, method="GET", headers={"User-Agent": "Mozilla/5.0 link-check"})
            with urllib.request.urlopen(req, timeout=15) as r:
                print(f"  {r.status} {u}")
        except Exception as e:  # noqa: BLE001
            print(f"  WARN {u}: {e}")


def main():
    pages = collect_pages()
    external = set()
    indexable = set()
    for url, p in pages.items():
        noindex = check_page(p, pages, external)
        if not noindex and not p.refresh and p.name != "404.html" and p.canonical == url:
            indexable.add(url)
    check_hreflang(pages)
    locs = check_sitemap(pages, indexable)
    check_titles(pages, indexable)
    print(f"{len(pages)} HTML files, {len(indexable)} indexable, {len(locs)} sitemap URLs, "
          f"{len(external)} external URLs")
    if "--external" in sys.argv:
        check_external(external)
    if errors:
        print(f"\n{len(errors)} error(s):")
        print("\n".join(f"  - {e}" for e in errors))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
