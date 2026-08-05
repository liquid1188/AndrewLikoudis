#!/usr/bin/env python3
"""Append newly published Substack essays to tr-archive.json.

Substack's RSS feed only exposes the 20 most recent posts, so anything older
disappears from the feed permanently. This keeps a durable, version-controlled
copy. Run daily by .github/workflows/tr-archive.yml.
"""
import json, re, html, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEED = "https://traditionandrenewal.substack.com/feed"
PATH = "tr-archive.json"

def _norm(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())

def clean(s, n=280):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return (s[:n].rsplit(" ", 1)[0] + "\u2026") if len(s) > n else s

def main():
    req = urllib.request.Request(FEED, headers={"User-Agent": "tr-archive/1.0"})
    xml = urllib.request.urlopen(req, timeout=30).read()
    channel = ET.fromstring(xml).find("channel")

    data = json.load(open(PATH, encoding="utf-8"))
    entries = data["entries"]
    known = {(e.get("url") or "").split("?")[0] for e in entries}
    known |= {(a.get("url") or "").split("?")[0]
              for e in entries for a in e.get("also_at", [])}
    titles = {_norm(e["title"]): e for e in entries}

    added = 0
    for it in channel.findall("item"):
        link = (it.findtext("link") or "").split("?")[0]
        if not link or link in known:
            continue
        title_now = html.unescape(it.findtext("title") or "").strip()
        prior = titles.get(_norm(title_now))
        if prior is not None:
            # already published elsewhere first — record the cross-post, don't duplicate
            prior.setdefault("also_at", []).append(
                {"venue": "Tradition & Renewal", "url": link})
            known.add(link)
            added += 1
            continue
        try:
            dt = datetime.strptime(it.findtext("pubDate"), "%a, %d %b %Y %H:%M:%S %Z")
        except (TypeError, ValueError):
            continue
        entries.append({
            "title": title_now,
            "url": link,
            "date": dt.strftime("%Y-%m-%d"),
            "venue": "Tradition & Renewal",
            "sections": [],
            "excerpt": clean(it.findtext("description") or ""),
        })
        known.add(link)
        added += 1

    if not added:
        print("no new essays")
        return 0

    entries.sort(key=lambda e: e["date"], reverse=True)
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    data["entries"] = entries
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"added {added} essay(s); archive now {len(entries)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
