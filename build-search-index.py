#!/usr/bin/env python3
"""
Regenerate search-index.json for andrewlikoudis.com.

Run from the repo root after editing any page content:

    python3 build-search-index.py

Parses the site's static HTML and produces a compact JSON index consumed by
the search UI in site.js. No dependencies beyond the standard library.
"""

import html
import json
import os
import re
from collections import OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))

# page slug -> clean URL
PAGES = OrderedDict([
    ("index.html",          ("/",                 "Home")),
    ("about.html",          ("/about",            "About")),
    ("books.html",          ("/books",            "Books")),
    ("writing.html",        ("/writing",          "Articles")),
    ("speaking.html",       ("/speaking",         "Speaking")),
    ("work-with-me.html",   ("/work-with-me",     "Work With Me")),
    ("endorsements.html",   ("/endorsements",     "Endorsements")),
    ("gallery.html",        ("/gallery",          "Gallery")),
    ("faith-in-crisis.html", ("/faith-in-crisis", "Faith in Crisis")),
])

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
SCRIPT_RE = re.compile(r"<(script|style|noscript)\b.*?</\1>", re.S | re.I)
NAVCHROME_RE = re.compile(r"<(nav|footer)\b.*?</\1>", re.S | re.I)


def text_of(fragment):
    """Strip tags and collapse whitespace.

    Stripped twice on purpose: some pages carry escaped markup (&lt;img ...&gt;)
    inside inline handlers, which only becomes a tag after unescaping.
    """
    s = TAG_RE.sub(" ", fragment)
    s = html.unescape(s)
    s = TAG_RE.sub(" ", s)
    return WS_RE.sub(" ", s).strip()


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def attr(fragment, name):
    m = re.search(r"%s=[\"']([^\"']*)[\"']" % name, fragment)
    return html.unescape(m.group(1)) if m else ""


def span(fragment, cls):
    m = re.search(
        r"<span[^>]*class=[\"'][^\"']*\b%s\b[^\"']*[\"'][^>]*>(.*?)</span>" % cls,
        fragment, re.S)
    return text_of(m.group(1)) if m else ""


records = []
seen = set()


def clean(s):
    """Final scrub: drop any residual tag, and any tag left dangling by a
    truncation, so snippets never leak markup into the UI."""
    s = TAG_RE.sub(" ", s)
    s = re.sub(r"<[^>]*$", "", s)      # tag cut off by a length limit
    return WS_RE.sub(" ", s).strip()


def add(rec):
    rec.setdefault("kw", "")          # hidden keywords (authors, outlets, tags)
    rec["t"] = clean(rec["t"])
    rec["s"] = clean(rec["s"])
    rec["b"] = clean(rec["b"])
    rec["kw"] = clean(rec["kw"])
    key = (rec["t"].lower(), rec["u"])
    if rec["t"] and key not in seen:
        seen.add(key)
        records.append(rec)


# ------------------------------------------------------------- articles
def harvest_items(fname, kind, meta_default):
    if not os.path.exists(os.path.join(ROOT, fname)):
        return
    raw = read(fname)
    # outlet headings segment the grid
    outlets = [(m.start(), text_of(m.group(1))) for m in re.finditer(
        r"<div class=\"writing-section-header\">\s*<h3>(.*?)</h3>", raw, re.S)]

    for m in re.finditer(
            r"<a\b[^>]*class=\"[^\"]*\bwriting-item\b[^\"]*\"[^>]*>(.*?)</a>",
            raw, re.S):
        block = m.group(0)
        url = attr(block, "href")
        title = span(block, "writing-title")
        desc = span(block, "writing-desc")
        if desc and title.endswith(desc):
            title = title[: -len(desc)].strip()
        date = span(block, "writing-date")
        outlet = meta_default
        for pos, name in outlets:
            if pos < m.start():
                outlet = name
        if not title:
            continue
        add({"k": kind, "t": title, "s": desc, "u": url,
             "m": " · ".join(x for x in (outlet, date) if x),
             "kw": outlet,
             "b": " ".join((title, desc, outlet, date))})


harvest_items("writing.html", "article", "Article")
harvest_items("speaking.html", "talk", "Appearance")


# ---------------------------------------------------------------- books
if os.path.exists(os.path.join(ROOT, "books.html")):
    raw = read("books.html")
    for m in re.finditer(
            r"<div class=\"book-edited-card\"[^>]*onclick=\"openBookModal\('([^']+)'\)\"(.*?)"
            r"(?=<div class=\"book-edited-card\"|</div>\s*</section>|$)",
            raw, re.S):
        slug, block = m.group(1), m.group(2)
        title = text_of(re.search(r"<h4>(.*?)</h4>", block, re.S).group(1)) \
            if re.search(r"<h4>(.*?)</h4>", block, re.S) else ""
        def p(cls):
            mm = re.search(r"<p class=\"%s\">(.*?)</p>" % cls, block, re.S)
            return text_of(mm.group(1)) if mm else ""
        sub, author = p("book-subtitle"), p("book-author")
        role, pub, fwd = p("book-role"), p("book-publisher"), p("book-foreword")
        if not title:
            continue
        add({"k": "book", "t": title, "s": sub,
             "u": "/books#" + slug if slug else "/books",
             "m": " · ".join(x for x in (role, pub) if x),
             "kw": " ".join(x for x in (author, fwd, pub) if x),
             "b": " ".join((title, sub, author, role, pub, fwd))})


rich_titles = {r["t"].lower() for r in records}

# ---------------------------------------------------------------- pages
for fname, (url, label) in PAGES.items():
    if not os.path.exists(os.path.join(ROOT, fname)):
        continue
    raw = read(fname)
    title = text_of(re.search(r"<title>(.*?)</title>", raw, re.S).group(1)) \
        if re.search(r"<title>(.*?)</title>", raw, re.S) else label
    desc = attr(re.search(r'<meta name="description"[^>]*>', raw).group(0), "content") \
        if re.search(r'<meta name="description"[^>]*>', raw) else ""

    body = SCRIPT_RE.sub(" ", raw)
    body = NAVCHROME_RE.sub(" ", body)

    # Mark headings with sentinels, THEN strip tags once. Slicing raw HTML and
    # stripping afterwards leaves partial tags wherever the cut lands.
    def mark(m):
        hid = attr(m.group(0), "id")
        return "\x00%s\x02%s\x01" % (hid, text_of(m.group(2)))

    marked = re.sub(r"<h([23])\b[^>]*>(.*?)</h\1>", mark, body, flags=re.S)
    flat = text_of(marked)
    body_text = flat.replace("\x00", " ").replace("\x01", " ").replace("\x02", " ")
    body_text = WS_RE.sub(" ", body_text).strip()

    add({"k": "page", "t": label, "s": desc, "u": url,
         "m": "Page", "b": body_text[:600]})

    parts = flat.split("\x00")[1:]
    for part in parts:
        head_seg, _, tail = part.partition("\x01")
        hid, _, heading = head_seg.partition("\x02")
        heading = heading.strip()
        tail = WS_RE.sub(" ", tail.split("\x00")[0]).strip()
        if not heading or len(heading) > 90:
            continue
        if heading.lower() in rich_titles:
            continue          # already indexed as a book, article or talk
        if len(tail) < 40:
            continue          # heading with no substance beneath it
        add({"k": "section", "t": heading, "s": tail[:180], "m": label,
             "u": url + ("#" + hid if hid else ""), "b": tail[:900]})


# ------------------------------------------------------------- articles
def harvest_items(fname, kind, meta_default):
    if not os.path.exists(os.path.join(ROOT, fname)):
        return
    raw = read(fname)
    # outlet headings segment the grid
    outlets = [(m.start(), text_of(m.group(1))) for m in re.finditer(
        r"<div class=\"writing-section-header\">\s*<h3>(.*?)</h3>", raw, re.S)]

    for m in re.finditer(
            r"<a\b[^>]*class=\"[^\"]*\bwriting-item\b[^\"]*\"[^>]*>(.*?)</a>",
            raw, re.S):
        block = m.group(0)
        url = attr(block, "href")
        title = span(block, "writing-title")
        desc = span(block, "writing-desc")
        if desc and title.endswith(desc):
            title = title[: -len(desc)].strip()
        date = span(block, "writing-date")
        outlet = meta_default
        for pos, name in outlets:
            if pos < m.start():
                outlet = name
        if not title:
            continue
        add({"k": kind, "t": title, "s": desc, "u": url,
             "m": " · ".join(x for x in (outlet, date) if x),
             "kw": outlet,
             "b": " ".join((title, desc, outlet, date))})


harvest_items("writing.html", "article", "Article")
harvest_items("speaking.html", "talk", "Appearance")


# ---------------------------------------------------------------- books
if os.path.exists(os.path.join(ROOT, "books.html")):
    raw = read("books.html")
    for m in re.finditer(
            r"<div class=\"book-edited-card\"[^>]*onclick=\"openBookModal\('([^']+)'\)\"(.*?)"
            r"(?=<div class=\"book-edited-card\"|</div>\s*</section>|$)",
            raw, re.S):
        slug, block = m.group(1), m.group(2)
        title = text_of(re.search(r"<h4>(.*?)</h4>", block, re.S).group(1)) \
            if re.search(r"<h4>(.*?)</h4>", block, re.S) else ""
        def p(cls):
            mm = re.search(r"<p class=\"%s\">(.*?)</p>" % cls, block, re.S)
            return text_of(mm.group(1)) if mm else ""
        sub, author = p("book-subtitle"), p("book-author")
        role, pub, fwd = p("book-role"), p("book-publisher"), p("book-foreword")
        if not title:
            continue
        add({"k": "book", "t": title, "s": sub,
             "u": "/books#" + slug if slug else "/books",
             "m": " · ".join(x for x in (role, pub) if x),
             "kw": " ".join(x for x in (author, fwd, pub) if x),
             "b": " ".join((title, sub, author, role, pub, fwd))})


rich_titles = {r["t"].lower() for r in records}

# ---------------------------------------------------------------- pages
for fname, (url, label) in PAGES.items():
    if not os.path.exists(os.path.join(ROOT, fname)):
        continue
    raw = read(fname)
    title = text_of(re.search(r"<title>(.*?)</title>", raw, re.S).group(1)) \
        if re.search(r"<title>(.*?)</title>", raw, re.S) else label
    desc = attr(re.search(r'<meta name="description"[^>]*>', raw).group(0), "content") \
        if re.search(r'<meta name="description"[^>]*>', raw) else ""

    body = SCRIPT_RE.sub(" ", raw)
    body = NAVCHROME_RE.sub(" ", body)
    body_text = text_of(body)

    add({"k": "page", "t": label, "s": desc, "u": url,
         "m": "Page", "b": body_text[:600]})

    # headings become their own jump targets where they carry an id
    for m in re.finditer(r"<h([23])[^>]*>(.*?)</h\1>", body, re.S):
        heading = text_of(m.group(2))
        if not heading or len(heading) > 90:
            continue
        if heading.lower() in rich_titles:
            continue          # already indexed as a book, article or talk
        tail = text_of(body[m.end():m.end() + 1800])
        if len(tail) < 40:
            continue          # heading with no substance beneath it
        hid = attr(m.group(0), "id")
        add({"k": "section", "t": heading, "s": tail[:180], "m": label,
             "u": url + ("#" + hid if hid else ""), "b": tail[:900]})


out = {"generated": True, "count": len(records), "records": records}
path = os.path.join(ROOT, "search-index.json")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))

by_kind = {}
for r in records:
    by_kind[r["k"]] = by_kind.get(r["k"], 0) + 1
print("wrote %s (%d records, %.1f KB)" % (
    os.path.relpath(path, ROOT), len(records), os.path.getsize(path) / 1024))
for k, v in sorted(by_kind.items()):
    print("   %-9s %d" % (k, v))
