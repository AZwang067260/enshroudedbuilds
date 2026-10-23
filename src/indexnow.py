"""Submit changed sitemap URLs to IndexNow (Bing, Yandex and others share submissions).

Usage: python3 src/indexnow.py [old_sitemap.xml]
With an old sitemap, only URLs that are new or have a newer <lastmod> are sent; without one, every URL is sent.
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from layout import INDEXNOW_KEY, SITE  # noqa: E402


def entries(xml):
    return dict(re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", xml))


def main():
    new = entries(open(os.path.join(ROOT, "public", "sitemap.xml"), encoding="utf-8").read())
    old = entries(open(sys.argv[1], encoding="utf-8").read()) if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else {}
    urls = [u for u, lm in new.items() if not old or old.get(u) != lm]
    if not urls:
        print("IndexNow: nothing changed")
        return
    host = SITE.split("//", 1)[1]
    body = json.dumps({"host": host, "key": INDEXNOW_KEY, "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt", "urlList": urls[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow: HTTP {r.status} for {len(urls)} URLs")
    for u in urls:
        print(" ", u)


if __name__ == "__main__":
    main()
