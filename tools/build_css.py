#!/usr/bin/env python3
"""Bundle the site's CSS into one file: /css/bundle.css.

Every page used to load about a dozen stylesheets from /kit plus Google Fonts, all render-
blocking. This concatenates them, in the kit's required order, behind the self-hosted
@font-face rules, so a page makes one CSS request. The kit's own files stay untouched in
/kit (they are vendored from the Taste skill); edit css/site.css for site rules, then run
this and tools/sync_partials.py (which stamps the bundle's ?v= hash). The output is\nminified with esbuild (needs Node; falls back to unminified).

Usage: python3 tools/build_css.py [--check]
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "css" / "bundle.css"

FONTS = """/* Funnel Display and Funnel Sans (SIL Open Font License), latin subset, self-hosted */
@font-face { font-family: "Funnel Display"; font-style: normal; font-weight: 400 700; font-display: swap;
  src: url(/assets/fonts/funnel-display-latin.woff2) format("woff2");
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
@font-face { font-family: "Funnel Sans"; font-style: normal; font-weight: 400 600; font-display: swap;
  src: url(/assets/fonts/funnel-sans-latin.woff2) format("woff2");
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
"""

# the kit's order (references/layout-v4.md): system, cards, motion, layout, icons; then the UI
# fragments and diagrams the home page draws, then the site layer last
PARTS = [
    "kit/system.css",
    "kit/ui/cards.css",
    "kit/motion/motion.css",
    "kit/layout/layout.css",
    "kit/icons/icon.css",
    "kit/ui/base.css",
    "kit/ui/chat/fragment.css",
    "kit/ui/window/fragment.css",
    "kit/ui/notify/fragment.css",
    "kit/ui/checklist/fragment.css",
    "kit/diagrams/diagram.css",
    "css/site.css",
]


def build():
    out = [FONTS]
    for part in PARTS:
        out.append(f"\n/* ==== {part} ==== */\n")
        out.append((ROOT / part).read_text())
    return "".join(out)


def minify(text):
    """Strip comments and collapse whitespace, nothing else.

    Rules, values and their order stay exactly as written (a full minifier
    such as esbuild merged rules and broke the kit's cascade). Strings and
    url() contents are copied through untouched."""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == "/" and text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if c in "\"'":
            j = i + 1
            while j < n and text[j] != c:
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1]); i = j + 1
            continue
        if c.isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            out.append(" "); i = j
            continue
        out.append(c); i += 1
    s = "".join(out)
    # Drop spaces next to punctuation where CSS ignores them. Not around
    # ':' (selectors like 'a :hover' differ) or '+', '-', '*', '/' (calc()).
    s = re.sub(r" ?([{};,>]) ?", r"\1", s)
    s = s.replace(";}", "}")
    return s.strip() + "\n"


def main():
    text = minify(build())
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text() == text else 1)
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(text) // 1024} KB)")


if __name__ == "__main__":
    main()
