#!/usr/bin/env python3
"""Copy the shared partials from index.html into every other page.

The site is plain static HTML, so the <head> assets, header and footer are
duplicated in each page between marker comments:

    <!-- head:start -->   ... <!-- head:end -->
    <!-- header:start KEY --> ... <!-- header:end -->
    <!-- footer:start --> ... <!-- footer:end -->

index.html is the source of truth. KEY names the nav item to mark as the
current page (see ACTIVE below); the home page's active state is stripped
before copying. Pages without a marker pair are left alone.

Usage: python3 tools/sync_partials.py [--check]
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "index.html"
SKIP = {"admin"}  # private app, own chrome

ACTIVE = {
    "m2s": "/m2s/",
    "pricing": "/pricing/",
    "results": "/results/",
    "partners": "/partners/",
    "industries": "/#industries",
}

BLOCKS = {
    "head": re.compile(r"<!-- head:start -->.*?<!-- head:end -->", re.S),
    "header": re.compile(r"<!-- header:start (\S+) -->.*?<!-- header:end -->", re.S),
    "footer": re.compile(r"<!-- footer:start -->.*?<!-- footer:end -->", re.S),
}


def plain_header(block):
    """Header block with no nav item marked current."""
    block = re.sub(r"<!-- header:start \S+ -->", "<!-- header:start KEY -->", block)
    return block.replace(' class="is-active" aria-current="page"', "")


def header_for(template, key):
    out = template.replace("<!-- header:start KEY -->", f"<!-- header:start {key} -->")
    href = ACTIVE.get(key)
    if href:
        out = out.replace(
            f'<a href="{href}">', f'<a href="{href}" class="is-active" aria-current="page">', 1
        )
    return out


def main():
    check = "--check" in sys.argv
    src = SOURCE.read_text()
    head = BLOCKS["head"].search(src).group(0)
    header = plain_header(BLOCKS["header"].search(src).group(0))
    footer = BLOCKS["footer"].search(src).group(0)

    pages = [ROOT / "404.html"] + sorted(ROOT.glob("*/index.html"))
    changed = []
    for page in pages:
        if page.parent.name in SKIP or page == SOURCE:
            continue
        text = page.read_text()
        new = BLOCKS["head"].sub(lambda m: head, text, count=1)
        new = BLOCKS["header"].sub(lambda m: header_for(header, m.group(1)), new, count=1)
        new = BLOCKS["footer"].sub(lambda m: footer, new, count=1)
        if new != text:
            changed.append(page.relative_to(ROOT))
            if not check:
                page.write_text(new)

    # Home keeps its own key but gets the same normalised markup.
    home = BLOCKS["header"].sub(lambda m: header_for(header, m.group(1)), src, count=1)
    if home != src:
        changed.append(SOURCE.relative_to(ROOT))
        if not check:
            SOURCE.write_text(home)

    for p in changed:
        print(("would update " if check else "updated ") + str(p))
    if check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
