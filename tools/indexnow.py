#!/usr/bin/env python3
"""Tell Bing, Yandex and other IndexNow engines that pages changed.

Run after a deploy. With no arguments it submits every URL in sitemap.xml;
pass paths (/pricing/ /results/) to submit only those. The key file at the
site root proves we own the domain.

Usage: python3 tools/indexnow.py [/path/ ...]
"""
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = "nuevoautomations.com"
KEY = "21d17b9959b1de0b18f91842ae52f3aa"


def main():
    if sys.argv[1:]:
        urls = ["https://" + HOST + p for p in sys.argv[1:]]
    else:
        urls = re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text())
    body = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
        "urlList": urls,
    }).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=body,
        headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=20) as res:
        print(res.status, "submitted", len(urls), "URLs")


if __name__ == "__main__":
    main()
