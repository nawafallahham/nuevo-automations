#!/usr/bin/env python3
"""Build /llms-full.txt: one Markdown file with every indexed page's title, URL,
description, short answer and FAQs, for AI assistants and answer engines.

It reads sitemap.xml for the page list and llms.txt for the summary at the top,
so run it after either changes (and after editing a page's answer box or FAQs).

Usage: python3 tools/build_llms_full.py
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = "https://nuevoautomations.com"


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def main():
    intro = (ROOT / "llms.txt").read_text().split("\n## ", 1)[0].strip()
    out = [intro, ""]
    for url in re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text()):
        path = url[len(HOST):].strip("/")
        src = (ROOT / path / "index.html") if path else ROOT / "index.html"
        page = src.read_text()
        title = text(re.search(r"<title>(.*?)</title>", page, re.S).group(1))
        desc = re.search(r'name="description" content="([^"]*)"', page)
        out += ["", f"## {title}", "", f"URL: {url}"]
        if desc:
            out += ["", html.unescape(desc.group(1))]
        answer = re.search(r'<div class="answer">(.*?)</div>', page, re.S)
        if answer:
            out += ["", text(answer.group(1))]
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
            try:
                data = json.loads(block)
            except ValueError:
                continue
            if data.get("@type") == "FAQPage":
                for q in data["mainEntity"]:
                    out += ["", f"Q: {q['name']}", f"A: {q['acceptedAnswer']['text']}"]
    (ROOT / "llms-full.txt").write_text("\n".join(out).strip() + "\n")
    print("wrote llms-full.txt", len("\n".join(out)) // 1024, "KB")


if __name__ == "__main__":
    main()
