#!/usr/bin/env python3
"""Append newly published Substack essays to tr-archive.json.

Substack's RSS feed only exposes the 20 most recent posts, so anything older
disappears from the feed permanently. This keeps a durable, version-controlled
copy. Run daily by .github/workflows/tr-archive.yml.
"""
import json, re, html, sys, urllib.request
from datetime import datetime, timezone

API = "https://traditionandrenewal.substack.com/api/v1/archive?sort=new&limit=50&offset="
PATH = "tr-archive.json"

def _norm(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())

def clean(s, n=280):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return (s[:n].rsplit(" ", 1)[0] + "\u2026") if len(s) > n else s

def main():
    posts, offset = [], 0
    while True:
        req = urllib.request.Request(API + str(offset), headers={"User-Agent": "tr-archive/1.0"})
        batch = json.load(urllib.request.urlopen(req, timeout=30))
        if not batch:
            break
        posts += batch
        offset += 50
        if len(batch) < 50:
            break

    data = json.load(open(PATH, encoding="utf-8"))
    entries = data["entries"]
    known = {(e.get("url") or "").split("?")[0] for e in entries}
    known |= {(a.get("url") or "").split("?")[0]
              for e in entries for a in e.get("also_at", [])}
    titles = {_norm(e["title"]): e for e in entries}

    added = 0
    for p in posts:
        link = (p.get("canonical_url") or "").split("?")[0]
        title_now = (p.get("title") or "").strip()
        date_str = (p.get("post_date") or "")[:10]
        if not link or link in known or not date_str:
            continue
        if title_now.lower() == "test":
            continue
        prior = titles.get(_norm(title_now))
        if prior is not None:
            # published elsewhere first — record the cross-post rather than duplicating
            prior.setdefault("also_at", []).append(
                {"venue": "Tradition & Renewal", "url": link})
            known.add(link)
            added += 1
            continue
        entries.append({
            "title": title_now,
            "url": link,
            "date": date_str,
            "venue": "Tradition & Renewal",
            "sections": [],
            "excerpt": clean(p.get("subtitle") or ""),
        })
        known.add(link)
        titles[_norm(title_now)] = entries[-1]
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
