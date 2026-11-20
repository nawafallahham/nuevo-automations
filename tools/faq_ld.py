#!/usr/bin/env python3
"""Rebuild each page's FAQPage JSON-LD from the questions shown on the page.

A page's visible FAQ is a .faq block of .faq__item elements, each an <h3> question and
<p> answers. Google wants the structured data to match what visitors read, so after
editing an FAQ run this; it rewrites mainEntity of the page's FAQPage node (top level
or inside @graph). Pages without both are left alone.

Usage: python3 tools/faq_ld.py [page ...]   (default: every page) [--check]
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ITEM = re.compile(r'<div class="faq__item[^"]*"><h3>(.*?)</h3>(.*?)</div>', re.S)
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def faq_nodes(data):
    nodes = data.get("@graph", [data]) if isinstance(data, dict) else []
    return [n for n in nodes if isinstance(n, dict) and n.get("@type") == "FAQPage"]


def main():
    check = "--check" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pages = [ROOT / a for a in args] or [ROOT / "index.html"] + sorted(ROOT.glob("*/index.html"))
    changed = []
    for page in pages:
        src = page.read_text()
        items = [(text(q), text(re.sub(r'<a [^>]*>[^<]*</a>\s*$', '', a.strip()))) for q, a in ITEM.findall(src)]
        if not items:
            continue
        entity = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]

        def repl(m):
            data = json.loads(m.group(2))
            nodes = faq_nodes(data)
            if not nodes:
                return m.group(0)
            for n in nodes:
                n["mainEntity"] = entity
            body = json.dumps(data, indent=2, ensure_ascii=False)
            return f"{m.group(1)}\n{body}\n  {m.group(3)}"

        new = LD.sub(repl, src)
        if new != src:
            changed.append(page.relative_to(ROOT))
            if not check:
                page.write_text(new)
    for p in changed:
        print(("would update " if check else "updated ") + str(p))
    if check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
