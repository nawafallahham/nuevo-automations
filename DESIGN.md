# Nuevo Automations: design system

The site is built on the **Taste** design kit (`~/.claude/skills/design-taste-frontend`), copied
into `/kit` (the runtime only: `system.css/js`, `ui/`, `motion/`, `layout/`, `backgrounds/`,
`icons/icon.css`, `moments/`, `diagrams/`). `/css/site.css` is the only site layer on top of it. Pages load one stylesheet,
`/css/bundle.css`, built by `python3 tools/build_css.py` from the kit's CSS and `site.css`, with the
two fonts (Funnel Display, Funnel Sans) self-hosted in `/assets/fonts` and preloaded. After editing
`site.css`: run `tools/build_css.py`, then `tools/sync_partials.py`.
`/css/style.css` is the old design; only `/admin/` still loads it.

Not published: `.assetsignore` excludes `*.md`.

## The deal (from the kit's dealers, never picked by taste)

| Part | Dealt | Why it fits |
|---|---|---|
| Kind | software (`data-type="software"`, `site-kind` software) | M2S is an AI sales assistant the company built and runs; the client allows no photographs, so the product's own UI carries the pages |
| Palette | `clay-pine`, accent and ink retuned to the logo's blue: ground `#efe9e0`, surface `#e2d9cb`, ink `#18213a`, muted `#575d6b`, accent/action `#0d518d` | warm stone, made for wellness buyers; the dealt pine green was swapped for the Nuevo logo's blue at the owner's request |
| Type | `funnel`: Funnel Display (headlines, 400) + Funnel Sans (text), self-hosted | the first pairing, `onest`, took four lines in the dealt hero's headline column |
| Radius | soft (8/12/20) | default |
| Hero (home) | `centred`: headline, lead, two buttons, then the M2S inbox in a lit frame | `triptych` was dealt first and failed `hero-lines` |
| Nav | `nav-centre`, the client's logo beside the name | |
| Close / footer | `close-word` / `footer-dark` | |
| Rhythm | `surface-pairs` (one `.ground-surface` band) | |
| Buttons | `solid` | |
| Moments | `counter-rolls` on the proof figures (home `#results`) | `marquee-row` was dealt too and dropped: its loop fails the layout check |

## Rules that hold on every page

- **Honesty (the client's hard rules).** No invented testimonials, ratings, client stats or
  results. The only figures: partners report 50–60% more revenue from the same traffic and 0
  extra headcount after full rollout; up to 30x ROAS on Khaleej Peptides, the founder's own store
  (always said so, never "a client"). Example chats keep a visible line saying they are examples
  with a made-up brand. Write it as "Example chats with a made-up brand." — the kit outlines in red
  any visible text matching `are examples`, `is illustrative`, `for illustration`, `(sample…)`,
  `placeholder`, `names and figures`.
- **Keep:** every URL, `<title>`, meta description, canonical, OG tags, JSON-LD, the
  facebook-domain-verification tag (home), Calendly embeds (`/book/`, `/consultation/`,
  `/wellness-brands/`), `js/consent.js` (Meta Pixel only after consent), `js/track.js`,
  `.js-lead` + `data-lead` on booking buttons, the worker.
- **Main action:** "Book a free audit" → `/book/`, worded the same everywhere, as
  `.btn.btn--primary`. The second action is WhatsApp (`https://wa.me/971508549171…`) as
  `.btn.btn--secondary` or a `.link`.
- **Copy:** the kit's copy rules (`references/copy.md`): headings name a thing, buttons are a verb and
  an object, no "Learn more", no virtue words (honest, quiet, simply…), no slogans.
- **No** check-icon lists, eyebrow labels on every section, scroll fade-ins, floating chat bubble,
  photographs.

## Shared partials

`index.html` is the source of the `head`, `header` and `footer` blocks; `python3
tools/sync_partials.py` copies them into every page and stamps `/css/` and `/js/` links with a
content hash. `/kit/` is not stamped (relative module imports); `_headers` gives it a short
revalidating cache. After editing an FAQ, `python3 tools/faq_ld.py <page>` rebuilds that page's
FAQPage JSON-LD from the visible questions.

## Inner pages

The home page follows the kit's one-section-per-screen layout and passes its gate. Inner pages are
long reading pages, so their sections take their content's height:

```html
<main id="top">
  <section class="page-head" aria-labelledby="page-h">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a> / Pricing</p>
      <h1 id="page-h">…</h1>
      <p class="t-lead">…</p>
      <div class="btn-row"><a class="btn btn--primary js-lead" data-lead="…" href="/book/">Book a free audit</a></div>
    </div>
  </section>
  <section class="band" aria-labelledby="…">            <!-- add ground-surface for the one contrasting band -->
    <div class="wrap grid"> … span-6 / span-5 start-8 … </div>   <!-- or <div class="wrap"> for one column -->
  </section>
</main>
```

| Old class (style.css) | New (kit + site.css) |
|---|---|
| `.page-hero`, `.eyebrow`, `.lede` | `section.page-head`, `.crumb`, `.t-lead` (no eyebrow) |
| `.section`, `.section--alt`, `.container` | `section.band`, `section.band.ground-surface`, `.wrap` |
| `.split` | `.wrap.grid` with `.span-6` + `.span-5.start-8` (or `.span-5` + `.span-6.start-7`) |
| `.ticks`, `.cost-list` | `ul.rows` (`li > span.rows__name` [+ `p`]); `.rows--plain` for one-line rows |
| `.card`, `.feature`, `.price-box` | `.card` (`h3`, `p`, `ul.rows`) in `.grid` with `.span-4`/`.span-6` |
| `details/summary` FAQ | `.faq` > `.faq__item` > `h3` + `p` (answers open) |
| answer box | `.answer > p` |
| related links | `ul.link-list > li > a.link` |
| `.cta-band` | delete: the footer's close asks for the audit on every page |
| `.btn-primary/-lg/-ghost/-wa` | `.btn.btn--primary`, `.btn.btn--secondary`, `.link` |
| `.stats`, `.stat` | `dl.stats > div > dt.t-small.muted + dd.t-stat` |

## Gate waivers (home page)

The home page passes the Taste gate (`node ~/.claude/skills/design-taste-frontend/scripts/gate.mjs index.html`) with these waived findings (`.taste-skill/waivers.json`, not committed):

- `phone-number` on `footer__col`: The client's real WhatsApp sales number, +971 50 854 9171, given in the brief as the site's second contact. Not invented; it reaches the client.
- `nav-covers` on `div.consent`: The cookie notice the client requires (js/consent.js: the Meta Pixel loads only after consent). It shows once, until the visitor answers, and pads the page so the last lines stay clear.
- `container-edges` on `div.consent`: The same required cookie notice: a fixed card outside the page's sections by design, removed for good once the visitor answers.
- `scroll-reveal` on `footer#contact`: No reveal is written for the close: the button's colour change is its hover, which fires when the cookie card steps aside over the footer and leaves the checker's pointer on the button.
